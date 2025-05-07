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
    
video_file = "downloaded.mp4"

i = 0
for start, end in [
    # Scene 1: Opening Courtroom Drama – Bail Hearing Narrative
    # This segment introduces the courtroom setting, the charges, initial exchanges about bail, and concludes with the judge denying bail—offers a mini-story with setup, tension, and resolution, around 45 seconds.
    (240, 83010),

    # Scene 2: Immunity Agreement Revelation and Fallout
    # This segment starts with the dramatic assertion of an immunity deal, builds with the judge questioning, the confirmation by the FBI, and culminates with the judge ordering a hearing and Reddington deciding to represent himself—clear narrative arc around the scope of the agreement.
    (113418, 278450)
]:
    temp_file = f"clip_{i}.mp4"
    segment(video_file, start, end, temp_file)
    i += 1