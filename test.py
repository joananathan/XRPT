from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess
 
url = "https://youtu.be/rJMT8c_rr-s"
 
yt = YouTube(url, on_progress_callback = on_progress)

video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

video_stream.download(filename='video.mp4')
audio_stream.download(filename='audiostream.mp4')

output_file = "downloaded.mp4"

subprocess.run([
    "bin\\ffmpeg.exe",
    "-i", 'video.mp4',
    "-i", 'audio.mp4',
    "-c:v", "libx264",
    "-c:a", "aac",
    output_file
])