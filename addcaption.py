import ffmpeg

input_file = "clips\output.mp4"
subtitle_file = "output.srt"
output_file = "output_REALREALREAL.mp4"

style = (
    "FontName=Oswald,"
    f"FontSize=15,"
    "FontWeight=1000,"
    "Italic=1,"
    "BorderStyle=3,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H80000000,"
    "Outline=0.3,"
    "Shadow=0,"
    "Alignment=2," 
    f"MarginV=100"
)

# Apply subtitles with styling
ffmpeg.input(input_file).output(
    output_file,
    vf=f"subtitles={subtitle_file}:fontsdir=./fonts:force_style='{style}'"
).run()
