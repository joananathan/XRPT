import os
from moviepy import *
import subprocess
from datetime import timedelta


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
    
video_file = "videos\input_video.mp4"

i = 0
for start, end in [(58750, 91713),(103990, 134340)]:
    temp_file = f"clip_{i}.mp4"
    segment(video_file, start, end, temp_file)
    i += 1