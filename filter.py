from moviepy import VideoFileClip
from moviepy import vfx, afx

myclip = VideoFileClip("nrbeast.mp4")

#myclip = myclip.with_effects([vfx.Painting(1.5, 0.1)])
myclip = myclip.with_effects([vfx.LumContrast(lum=100, contrast=1.6, contrast_threshold=150)])
#myclip = myclip.with_effects([vfx.MirrorX()])




myclip.write_videofile("nrbeastoutut.mp4", codec="libx264")