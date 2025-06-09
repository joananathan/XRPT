import ffmpeg

input_file = "utput2.mp4"
subtitle_file = "test.srt"
output_file = "output_REALREALREAL.mp4"

style = (
    "FontName=Oswald,"
    f"FontSize=15,"
    "FontWeight=1000,"
    "Italic=1,"
    "BorderStyle=1,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,"
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
