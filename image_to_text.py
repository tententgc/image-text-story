import os
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv
    
load_dotenv()
    
client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
image_path= "/Users/tententgc/Documents/GitHub/image-text-story/image_test.jpg"

base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                         "url": f"data:image/jpeg;base64,{base64_image}",
                    }
                },
            ],
        }
    ],
    max_tokens=300,
)

message_content = response.choices[0].message.content
print(message_content)


voice_response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input= message_content,
)

voice_response.stream_to_file("output.mp3")