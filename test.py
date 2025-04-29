import yt_dlp

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
    'outtmpl': '%(id)s.%(ext)s',
    'ffmpeg_location': 'bin',  # Only needed if ffmpeg isn't globally installed
    'merge_output_format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }]
}

video_url="https://www.youtube.com/watch?v=nGIa-VL4P_4"
# Download and extract audio
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
    # Get video ID from info dict
    info = ydl.extract_info(video_url, download=False)
    video_id = info['id']