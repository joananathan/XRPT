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

def cut_and_combine(video_path, sections, output_path):
    temp_files = [f"clip_{i}.mp4" for i in range(len(sections))]

    for temp_file, (start, end) in zip(temp_files, sections):
        segment(video_path, start, end, temp_file)

    # clips = [VideoFileClip(f) for f in temp_files]
    # final_video = concatenate_videoclips(clips)
    # final_video.write_videofile(output_path, codec='libx264', fps=30)

    # for clip in clips:
    #     clip.close()
    # for temp_file in temp_files:
    #     os.remove(temp_file)
    

video_file = "NDsO1LT_0lw.mp4"
# timestamps = [
#     [(320, 27944), (28032, 30216), (30288, 46372), (46516, 58660), (58700, 93504)],
#     [(93552, 103708), (106140, 129100), (129600, 147400)],
#     [(147480, 223392), (225224, 236992), (240320, 248324), (248392, 304808)],
#     [(305864, 364924), (395680, 407120)],
#     [(440720, 474612), (508472, 569416)],
#     [(626310, 693220), (693300, 702772)],
#     [(738424, 771710)]
# ]

# for i, timestamp in enumerate(timestamps):

#     output_file = str(i) + "outputtt_real.mp4"

#     cut_and_combine(video_file, timestamp, output_file)

i = 0
for start, end in [(320, 27944), (129600, 147400), (243216, 304808), (626310, 693300)]:
    temp_file = f"clip_{i}.mp4"
    segment(video_file, start, end, temp_file)
    i += 1