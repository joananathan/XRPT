from moviepy import VideoFileClip
from moviepy import vfx, afx

myclip = VideoFileClip("utput2.mp4")

#myclip = myclip.with_effects([vfx.Painting(1.5, 0.1)])
#myclip = myclip.with_effects([vfx.LumContrast(lum=90, contrast=1.3, contrast_threshold=110)])
myclip = myclip.with_effects([vfx.MirrorX()])




myclip.write_videofile("missionout.mp4", codec="libx264")