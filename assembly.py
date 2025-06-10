import assemblyai as aai
import yt_dlp, os

token = os.environ["AAI_TOKEN"]

def transcribe_youtube_video(video_url: str, api_key: str) -> str:
    # """
    # Transcribe a YouTube video given its URL.
    
    # Args:
    #     video_url: The YouTube video URL to transcribe
    #     api_key: AssemblyAI API key
    
    # Returns:
    #     The transcript text
    # """
    # # Configure yt-dlp options for audio extraction
    # ydl_opts = {
    #     'outtmpl': 'video.mp4',
    #     'ffmpeg_location': 'bin',
    #     'postprocessors': [{
    #         'key': 'FFmpegVideoConvertor',
    #         'preferedformat': 'mp4',
    #     }]
    # }

    # # Download and extract audio
    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([video_url])
    #     # Get video ID from info dict
    #     info = ydl.extract_info(video_url, download=False)
    #     video_id = info['id']
    
    # Configure AssemblyAI
    aai.settings.api_key = api_key

    # Transcribe the downloaded audio file
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(f"output_real.mp4")
    sentences = transcript.get_sentences()
    output = []
    for i, sentence in enumerate(sentences): 
        output.append(f'{sentence.text} {sentence.start}-{sentence.end}')
    return ('\n'.join(output))

transcript_text = transcribe_youtube_video("https://youtu.be/rJMT8c_rr-s", token)
print(transcript_text)
with open("transcript.txt", "w", encoding="utf-8") as file:
    file.write(transcript_text)
