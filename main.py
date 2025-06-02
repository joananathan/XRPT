from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess, os
from pytubefix import YouTube

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
                    flash("Please provide only one input: either upload a file or provide a YouTube URL.", "error")
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
                    if vid_length > 10800 or vid_length < 30:
                        flash("Video length must be between 30 seconds to three hours.", "error")
                        return redirect(url_for('home'))
                else:
                    try:
                        yt = YouTube(youtube_url)
                        if yt.length > 10800 or yt.length < 30:
                            flash("Video length must be between 30 seconds to three hours.", "error")
                            return redirect(url_for('home'))
                        self.download_yt(yt)
                    except Exception as e:
                        flash("Invalid YouTube link or download error.", "error")
                        return redirect(url_for('home'))
                    
                flash("Video processing started.", "success")
                return redirect(url_for('home'))

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

        video_stream.download(output_path=save_folder, filename='videostream.mp4')
        audio_stream.download(output_path=save_folder, filename='audiostream.mp4')

        subprocess.run([
            "bin\\ffmpeg.exe",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            file
        ])
    
    def get_video_length(self, video):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", video],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)

if __name__ == '__main__':
    xrpt_app = XRPT()
    xrpt_app.start()
