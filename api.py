import os, ast
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI

num_clips = 1
clip_length = "60"
with open("transcript.txt", "r") as f:
    transcript = f.read()

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

with open('prompt.txt', 'r') as f:
    prompt = f.read()


try:
    #Test if free Azure hosted API works (if below 8000 token limit)
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    response = client.complete(
        messages=[
            SystemMessage(prompt),
            UserMessage(f"""{num_clips} clips of {clip_length} seconds
                        {transcript}"""),
        ],
        temperature=1,
        top_p=1,
        model=model
    )

    print(response.choices[0].message.content)
    response = response.choices[0].message.content
    print("Free")
    
except:
    #Else use openai's own paid api
    client = OpenAI(api_key = os.environ.get("OPENAI_TOKEN"))

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"""{num_clips} clips of {clip_length} seconds
                                            {transcript}"""}]
    )

    print(response.choices[0].message.content)
    print("Not Free")
    
chosen_sections = ast.literal_eval(response)
print(chosen_sections)