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
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'ffmpeg_location': "bin",
        'postprocessors': [{
            'key': 'FFmpegVideoRemuxer',
        }]
    }

    # Download and extract audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        # Get video ID from info dict
        info = ydl.extract_info(video_url, download=False)
        video_id = info['id']
    
#     # Configure AssemblyAI
#     aai.settings.api_key = ''
    
#     # Transcribe the downloaded audio file
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(f"{video_id}.m4a")
#     sentences = transcript.get_sentences()
#     output = []
#     for sentence in sentences:
#         output.append(f'{sentence.text} {sentence.start}-{sentence.end}')
#         print('\n'.join(output))
#     return transcript.text

transcript_text = transcribe_youtube_video("https://youtu.be/NDsO1LT_0lw", "")
# #print(transcript_text)
