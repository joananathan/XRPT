import assemblyai as aai
import yt_dlp

def transcribe_youtube_video(video_url: str, api_key: str) -> str:
    """
    Transcribe a YouTube video given its URL.
    
    Args:
        video_url: The YouTube video URL to transcribe
        api_key: AssemblyAI API key
    
    Returns:
        The transcript text
    """
    # Configure yt-dlp options for audio extraction
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'ffmpeg_location': r"C:\Users\jz7jo\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    # Download and extract audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        # Get video ID from info dict
        info = ydl.extract_info(video_url, download=False)
        video_id = info['id']
    
    # Configure AssemblyAI
    aai.settings.api_key = ''
    
    # Transcribe the downloaded audio file
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(f"{video_id}.m4a")
    sentences = transcript.get_sentences()
    for sentence in sentences:
        print(f'"{sentence.text}" {sentence.start}-{sentence.end}')
    return transcript.text

transcript_text = transcribe_youtube_video("https://youtu.be/NDsO1LT_0lw", "b400692d86c34501a858a7779e0691a0")
#print(transcript_text)
