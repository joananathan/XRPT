from pydub import AudioSegment
sound = AudioSegment.from_file("videos\\input_video.mp4")
sound.export("videos\\transcribe.mp3", format="mp3", bitrate="64k")