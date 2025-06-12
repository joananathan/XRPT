from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess, os, ast, ffmpeg, shutil
from pytubefix import YouTube
import assemblyai as aai
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from datetime import timedelta
from moviepy import *
from content_aware_crop import load_yolov8_model, process_video, add_audio_to_video
from openai import OpenAI

class XRPT:
    def __init__(self):
        os.makedirs("videos", exist_ok=True)
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secretkey'
        self.app.config['UPLOAD_FOLDER'] = 'videos'
    
    def start(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def home():
            if request.method == 'POST':
                video_file = request.files.get('video_file')
                youtube_url = request.form.get('youtube_url')

                #INPUT VALIDATION
                if video_file and youtube_url:
                    flash("Please only provide one of link OR file", "error")
                    return redirect(url_for('home'))

                if not video_file and not youtube_url:
                    flash("Please provide a video file or a YouTube URL.", "error")
                    return redirect(url_for('home'))

                clip_length = request.form.get('clip_length')
                num_clips = request.form.get('num_clips')
                caption_style = int(request.form.get('caption_style'))
                filter_style = request.form.get('filter_adjustments')

                self.clear_video_folder()
                
                #More input validation based on video file or youtube link. Check video length.
                if video_file:
                    video_path = os.path.join(self.app.config['UPLOAD_FOLDER'], 'input_video.mp4')
                    video_file.save(video_path)
                    vid_length = self.get_video_length(video_path)
                    if vid_length > 2700 or vid_length < 300:
                        flash("Video length must be between 5 to 45 minutes.", "error")
                        return redirect(url_for('home'))
                else:
                    try:
                        yt = YouTube(youtube_url)
                        if yt.length > 2700 or yt.length < 300:
                            flash("Video length must be between 5 to 45 minutes.", "error")
                            return redirect(url_for('home'))
                        self.download_yt(yt)
                    except Exception as e:
                        print(e)
                        flash("Please enter a valid link", "error")
                        return redirect(url_for('home'))
                try:
                    transcript = self.transcribe_video()
                except RuntimeError:
                    flash("Video does not have enough speech to be analysed", "error")
                    return redirect(url_for('home'))
                
                #Call all the video processing functions
                chosen_sections = ast.literal_eval(self.choose_sections(clip_length, num_clips, transcript))
                self.cut_video(chosen_sections)
                self.crop_clips()
                self.add_filter(filter_style)
                self.caption_clip(caption_style)
                
                shutil.make_archive('static\\clips', 'zip', 'videos\\final')
                
                return render_template('results.html')
                
            return render_template('index.html')

        self.app.run(debug=True)
    
    def clear_video_folder(self):
        folder = self.app.config['UPLOAD_FOLDER']
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                
    def download_yt(self, yt):
        save_folder = self.app.config['UPLOAD_FOLDER']

        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

        video_path = os.path.join(save_folder, 'videostream.mp4')
        audio_path = os.path.join(save_folder, 'audiostream.mp4')
        file = os.path.join(save_folder, 'input_video.mp4')

        #I can only get the highest quality video by downloading video and audio separately (then combining them after)
        video_stream.download(output_path=save_folder, filename='videostream.mp4')
        audio_stream.download(output_path=save_folder, filename='audiostream.mp4')

        subprocess.run(fr"bin\\ffmpeg.exe -i {video_path} -i {audio_path} -c copy {file}")
    
    def get_video_length(self, video):
        result = subprocess.run(["bin\\ffprobe.exe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", video],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)
    
    def transcribe_video(self):
        aai.settings.api_key = os.environ["AAI_TOKEN"]
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(f"videos\\input_video.mp4")
        sentences = transcript.get_sentences()
        if len(sentences) < 30: #Ensure video has enough speech to analyse
            raise RuntimeError
        
        #format output
        output = []
        for sentence in sentences: 
            output.append(f'{sentence.text} {sentence.start}-{sentence.end}')
        return ('\n'.join(output))
    
    def choose_sections(self, clip_length, num_clips, transcript):
        endpoint = "https://models.github.ai/inference"
        model = "openai/gpt-4.1"
        token = os.environ["GITHUB_TOKEN"]

        with open('prompt.txt', 'r') as f:
            prompt = f.read()

        try:
            #Test if free Azure hosted API works (if below 8000 token limit)
            client = ChatCompletionsClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(token),
            )

            response = client.complete(
                messages=[
                    SystemMessage(prompt),
                    UserMessage(f"""{num_clips} clips of {clip_length} seconds
                                {transcript}"""),
                ],
                temperature=1,
                top_p=1,
                model=model
            )
            
        except:
            #Else use openai's own paid API
            client = OpenAI(api_key = os.environ.get("OPENAI_TOKEN"))

            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"""{num_clips} clips of {clip_length} seconds
                                                    {transcript}"""}]
            )

        return(response.choices[0].message.content)
    
    
    def cut_video(self, sections):
        def segment(inputfile, start_time, end_time, outputfile): 
            cmd = [
                "bin\\ffmpeg.exe",
                "-ss", str(timedelta(milliseconds=start_time)),
                "-to", str(timedelta(milliseconds=end_time)),
                "-i", inputfile,
                "-vf", "scale=-2:1920",
                "-c:v", "libx264",
                "-c:a", "aac",
                outputfile
            ]
            subprocess.run(cmd)
        

        os.makedirs("videos\\trimmed", exist_ok=True)
    
        video_file = "videos\\input_video.mp4"
        for i, (start, end) in enumerate(sections, start=1):
            temp_file = f"videos\\trimmed\\clip_{i}.mp4"
            segment(video_file, start, end, temp_file)
            
    def crop_clips(self):
        os.makedirs("videos\\cropped", exist_ok=True)
        folder = "videos\\trimmed"
        clips = sorted(os.listdir(folder))
        for i, clip in enumerate(clips, start=1):
            input_video_path = os.path.join(folder, clip)
            processed_video_path = f"videos\\cropped\\clip_{i}_noaudio.mp4"
            final_output_path = f"videos\\cropped\\clip_{i}.mp4"
            yolo_model_path = "static\\assets\\yolov8n.pt"
            
            model = load_yolov8_model(yolo_model_path)
            
            process_video(
                input_path=input_video_path,
                output_path=processed_video_path,
                model=model,
                target_aspect_ratio=9/16,
                smoothing_factor=0.95,
                min_confidence=0.6
            )
            
            add_audio_to_video(input_video_path, processed_video_path, final_output_path)
                
            os.remove(processed_video_path)
            
    def add_filter(self, adjustment):
        os.makedirs("videos\\filtered", exist_ok=True)
        folder = "videos\\cropped"
        
        #ignore the temp videos otherwise leads to numbering problems
        clips = sorted([f for f in os.listdir(folder) if not f.endswith('_noaudio.mp4')])
        
        for i, clip in enumerate(clips, start = 1):
            filepath = os.path.join(folder, clip)
            if adjustment in ["grain", "multiply", "flip"]:
                vid = VideoFileClip(filepath)
                if adjustment == "grain":
                    vid = vid.with_effects([vfx.Painting(1.5, 0.1)])
                elif adjustment == "multiply":
                    vid = vid.with_effects([vfx.LumContrast(lum=90, contrast=1.3, contrast_threshold=110)])
                elif adjustment == "flip":
                    vid = vid.with_effects([vfx.MirrorX()])
                
                vid.write_videofile(f"videos\\filtered\\clip_{i}.mp4", codec="libx264")
                vid.close()
            else:
                os.rename(filepath, f"videos\\filtered\\clip_{i}.mp4")
              
    def caption_clip(self, caption_style):
        #milliseconds to HH:MM:SS,mmm format
        def format_ms(milliseconds):
            milliseconds = int(milliseconds)
            seconds, ms = divmod(milliseconds, 1000)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)

            formatted = f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"
            return(formatted)
        
        def write_srt(srt_file, i, text, start, end):
            text_list = text.split()
            
            srt_file.write(f"{i}\n")
            srt_file.write(f"{format_ms(start)} --> {format_ms(end)}\n")
            
            if len(text) > 40:
                srt_file.write(' '.join(text_list[:int(len(text_list)/2)]))
                srt_file.write('\n')
                srt_file.write(' '.join(text_list[int(len(text_list)/2):]))
            else:
                srt_file.write(f"{text}")
            srt_file.write("\n\n")


        aai.settings.api_key = os.environ["AAI_TOKEN"]
        transcriber = aai.Transcriber()
        
        os.makedirs("videos\\final", exist_ok=True)
        folder = "videos\\filtered"
        clips = sorted(os.listdir(folder))
            
        #transcribe each clip again to subtitle them
        for i, clip in enumerate(clips, start=1):
            filepath = os.path.join(folder, clip)
            transcript = transcriber.transcribe(filepath)

            #Format output into srt format
            sentences = transcript.get_sentences()
            j = 1
            with open("output.srt", "w") as srt_file:
                for sentence in sentences:
                    sentence_list = sentence.text.split()
                    if len(sentence_list) > 12:
                        half_time = (sentence.start + sentence.end) / 2
                        
                        write_srt(srt_file, j, ' '.join(sentence_list[:int(len(sentence_list)/2)]), sentence.start, half_time)
                        j+=1
                        write_srt(srt_file, j, ' '.join(sentence_list[int(len(sentence_list)/2):]), half_time, sentence.end)
                    
                    else:
                        write_srt(srt_file, j, sentence.text, sentence.start, sentence.end)
                    
                    j += 1
            
            final_output_path = f"videos\\final\\clip_{i}.mp4"

            if caption_style == 1:
                style = (
                    "FontName=Oswald,"
                    f"FontSize=15,"
                    "FontWeight=1000,"
                    "Italic=0,"
                    "BorderStyle=1,"
                    "PrimaryColour=&H00FFFFFF,"
                    "OutlineColour=&H00000000,"
                    "Outline=0.3,"
                    "Shadow=0,"
                    "Alignment=2," 
                    f"MarginV=100"
                )
            elif caption_style == 2:
                style = (
                    "FontName=Oswald,"
                    f"FontSize=15,"
                    "FontWeight=1000,"
                    "Italic=1,"
                    "BorderStyle=1,"
                    "PrimaryColour=&H00FFFFFF,"
                    "OutlineColour=&H00000000,"
                    "Outline=0.3,"
                    "Shadow=0,"
                    "Alignment=2," 
                    f"MarginV=100"
                )
            elif caption_style == 3:
                style = (
                    "FontName=Oswald,"
                    f"FontSize=15,"
                    "FontWeight=1000,"
                    "Italic=0,"
                    "BorderStyle=3,"
                    "PrimaryColour=&H00FFFFFF,"
                    "OutlineColour=&H80000000,"
                    "Outline=0.3,"
                    "Shadow=0,"
                    "Alignment=2," 
                    f"MarginV=100"
                )
            else:
                style = (
                    "FontName=Oswald,"
                    f"FontSize=15,"
                    "FontWeight=1000,"
                    "Italic=1,"
                    "BorderStyle=3,"
                    "PrimaryColour=&H00FFFFFF,"
                    "OutlineColour=&H80000000,"
                    "Outline=0.3,"
                    "Shadow=0,"
                    "Alignment=2," 
                    f"MarginV=100"
                )

            print(style)
            
            ffmpeg.input(filepath).output(
                final_output_path,
                vf=f"subtitles='output.srt':fontsdir=./fonts:force_style='{style}'"
            ).run()
        

if __name__ == '__main__':
    xrpt_app = XRPT()
    xrpt_app.start()
