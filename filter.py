from moviepy import VideoFileClip
from moviepy import vfx, afx

myclip = VideoFileClip("clip_0.mp4")

myclip = myclip.with_effects([vfx.MultiplyColor(0.5)])

myclip.write_videofile("output.mp4", codec="libx264")