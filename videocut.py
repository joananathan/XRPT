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
    
video_file = "nGIa-VL4P_4.mp4"

i = 0
for start, end in [
    (320, 60126),  # Scene 1: Reaction video introduction, medical scenes, and sponsorship mention
    (14400, 42998),  # Scene 2: Vasectomy discussion, privacy concerns, and humorous reactions
    (498494, 527026)  # Scene 3: Health discussion, weight challenges, and team-building diet
]:
    temp_file = f"clip_{i}.mp4"
    segment(video_file, start, end, temp_file)
    i += 1