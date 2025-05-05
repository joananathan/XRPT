from moviepy import VideoFileClip
from moviepy import vfx, afx

myclip = VideoFileClip("clip_1 - Trim.mp4")

# myclip = myclip.with_effects([vfx.Painting(1.9, 2)])
# myclip = myclip.with_effects([vfx.LumContrast(lum=160, contrast=2.5, contrast_threshold=120)])
myclip = myclip.with_effects([vfx.MirrorX()])




myclip.write_videofile("output.mp4", codec="libx264")