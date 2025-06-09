import assemblyai as aai
import os

def transcribe_video():
    aai.settings.api_key = os.environ["AAI_TOKEN"]
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(f"videos\\audiostream.mp4")
    sentences = transcript.get_sentences()
    output = []
    for sentence in sentences: 
        output.append(f'{sentence.text} {sentence.start}-{sentence.end}')
    return ('\n'.join(output))
transcript_text = transcribe_video()
with open("transcript.txt", "w", encoding="utf-8") as file:
    file.write(transcript_text)