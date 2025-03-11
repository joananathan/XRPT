import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy import *

def cut_and_combine(video_path, sections, output_path):
    """Cuts sections from a video using ffmpeg_extract_subclip and combines them."""
    temp_files = [f"clip_{i}.mp4" for i in range(len(sections))]

    # Extract clips
    for temp_file, (start, end) in zip(temp_files, sections):
        ffmpeg_extract_subclip(video_path, start / 1000, end / 1000, temp_file)

    # Load and concatenate clips
    clips = [VideoFileClip(f) for f in temp_files]
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_path, codec='libx264', fps=30)

    # Cleanup
    for clip in clips:
        clip.close()
    for temp_file in temp_files:
        os.remove(temp_file)

# Example usage:
video_file = "NDsO1LT_0lw.webm"
timestamps = [(320, 11216), (39240, 59274), (100000, 200000)]  # Sections in milliseconds
output_file = "output_real.mp4"

cut_and_combine(video_file, timestamps, output_file)