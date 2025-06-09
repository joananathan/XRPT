from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess, os, ast
from pytubefix import YouTube
import assemblyai as aai
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from pydub import AudioSegment

class XRPT:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secretkey'
        self.app.config['UPLOAD_FOLDER'] = 'videos'
    
    def start(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def home():
            if request.method == 'POST':
                video_file = request.files.get('video_file')
                youtube_url = request.form.get('youtube_url')

                if video_file and youtube_url:
                    flash("Please only provide one of link OR file", "error")
                    return redirect(url_for('home'))

                if not video_file and not youtube_url:
                    flash("Please provide a video file or a YouTube URL.", "error")
                    return redirect(url_for('home'))

                clip_length = int(request.form.get('clip_length', 60))
                caption_style = request.form.get('caption_style', 'default')
                num_clips = int(request.form.get('num_clips', 1))

                self.clear_video_folder()

                if video_file:
                    video_path = os.path.join(self.app.config['UPLOAD_FOLDER'], 'input_video.mp4')
                    video_file.save(video_path)
                    vid_length = self.get_video_length(video_path)
                    if vid_length > 2700 or vid_length < 180:
                        flash("Video length must be between three minutes to three hours.", "error")
                        return redirect(url_for('home'))
                else:
                    try:
                        yt = YouTube(youtube_url)
                        if yt.length > 2800 or yt.length < 180:
                            flash("Video length must be between three minutes to three hours.", "error")
                            return redirect(url_for('home'))
                        self.download_yt(yt)
                    except Exception as e:
                        flash("Please enter a valid link", "error")
                        return redirect(url_for('home'))
                transcript = self.transcribe_video()
                with open("transcript.txt", "w", encoding="utf-8") as file:
                    file.write(transcript)
                chosen_sections = ast.literal_eval(self.choose_sections(clip_length, num_clips, transcript))
                print(chosen_sections)
                
            return render_template('index.html')

        self.app.run(debug=True)
    
    def clear_video_folder(self):
        folder = self.app.config['UPLOAD_FOLDER']
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
    def download_yt(self, yt):
        save_folder = 'videos'

        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

        video_path = os.path.join(save_folder, 'videostream.mp4')
        audio_path = os.path.join(save_folder, 'audiostream.mp4')
        file = os.path.join(save_folder, 'input_video.mp4')

        #I can only get the highest quality video by downloading video and audio separately (then combining them after)
        video_stream.download(output_path=save_folder, filename='videostream.mp4')
        audio_stream.download(output_path=save_folder, filename='audiostream.mp4')

        subprocess.run(f"ffmpeg -i {video_path} -i {audio_path} -c copy {file}")
    
    def get_video_length(self, video):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", video],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)
    
    def transcribe_video(self):
        #Get compressed audio file only for shorter file processing
        sound = AudioSegment.from_file("videos\\input_video.mp4")
        sound.export("videos\\transcribe.mp3", format="mp3", bitrate="64k")
        
        aai.settings.api_key = os.environ["AAI_TOKEN"]
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(f"videos\\transcribe.mp3")
        sentences = transcript.get_sentences()
        
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

        return(response.choices[0].message.content)

if __name__ == '__main__':
    xrpt_app = XRPT()
    xrpt_app.start()
