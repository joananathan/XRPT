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
        "-c:v", "copy",
        "-c:a", "aac",
        outputfile
    ]
    subprocess.run(cmd)
    
video_file = "suits.mp4"

i = 0
for start, end in [
    (271560, 313000),
    (313720, 351050),
]:
    temp_file = f"clip_{i}.mp4"
    segment(video_file, start, end, temp_file)
    i += 1