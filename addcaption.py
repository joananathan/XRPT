import ffmpeg

input_file = "nrbeastoutut.mp4"
subtitle_file = "test.srt"
output_file = "output_REALREAL.mp4"

# Shorts-style caption styling
probe = ffmpeg.probe(input_file)
height = int([s for s in probe['streams'] if s['codec_type'] == 'video'][0]['height'])

font_size_percent = 0.015
font_size = int(height * font_size_percent)

margin_percent = 0.08
margin_pixels = int(height * margin_percent)
print(f"eiorjwripwejriopwejripweorjeioj margin pixels {margin_pixels}  uioewhrieuwrh font size {font_size}")

style = (
    "FontName=Oswald,"
    f"FontSize={font_size},"
    "FontWeight=1000,"
    "Italic=0,"
    "BorderStyle=3,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H80000000,"
    "Outline=0.2,"
    "Shadow=0,"
    "Alignment=2," 
    f"MarginV={margin_pixels}"
)

# Apply subtitles with styling
ffmpeg.input(input_file).output(
    output_file,
    vf=f"subtitles={subtitle_file}:fontsdir=./fonts:force_style='{style}'"
).run()
