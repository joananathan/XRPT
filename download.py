from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess, os

def download_yt(url):
    save_folder = 'videos'
    
    yt = YouTube(url, on_progress_callback = on_progress)

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