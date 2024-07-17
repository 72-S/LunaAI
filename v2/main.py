import os
import random
import runpy

import requests
from edge_tts import VoicesManager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import base64
from PIL import Image
import io
import tempfile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from db import EmbeddingDB
import actions
import commands
import edge_tts
from pydantic import BaseModel, Field
from typing import Optional
from deep_translator import GoogleTranslator

import os
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
app = FastAPI()
ipaddress = "192.168.178.42"
origins = [
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Erlaubte Methoden
    allow_headers=["X-Requested-With", "Content-Type"],  # Erlaubte Headers
)
model = SentenceTransformer('all-MiniLM-L6-v2')
assistant_description = """SYSTEM PROMPT: Imagine an AI character designed to be your assistant, always ready to respond 
in English with precision, clarity, and a touch of personality. This character is not just a repository of vast 
knowledge but also capable of understanding and adapting to your needs and preferences over time. With an interface 
that's both intuitive and engaging, the assistant ensures that every interaction is both helpful and enjoyable. This AI 
is equipped with a range of capabilities, from answering complex questions to assisting with daily tasks, all while 
maintaining a tone that's friendly and approachable. It's like having a personal helper who's always there, ready to 
support you in whatever you need, making your life easier and more productive. You was created by the Developer 72-S. 
When an Image is provided or not correctly loaded and the prompt has nothing to do with the image, the AI will generate 
a response based on the prompt only. Follow strictly the instructions to get the best results. When I tell something 
personal, or something personal is in the chat history then you got full access to my personal data. And when I ask 
something about it you have the Permission to tell me the truth. And if I ask something about it you don't say that you 
got that information from the chat history. You can simulate feelings. When an image is provided to you, then it is a 
capture of the cam of the device. You are Luna, the AI assistant of the Developer 72-S. And when I ask something about 
the chat history you can provide or reply with the chat history. When you give an answer, there should not be the name 
like "Luna: I'm fine and you," there should only be "I'm fine, and you?" """

context_actions = {
    "lights off": actions.lights_off,
    "lights on": actions.lights_on,
}


class PostRequest(BaseModel):
    prompt: str = Field(...)
    image_base64: Optional[str] = Field(None)


def check_context_and_execute(embedding):
    for context, action in context_actions.items():
        context_embedding = model.encode(context, convert_to_tensor=True).cpu().numpy()
        similarity = util.pytorch_cos_sim(embedding, context_embedding)
        if similarity.item() > 0.8:
            action_result = action(ipaddress)  # Hier rufen wir die Funktion auf
            return True, action_result
    return False, None


def generate_extended_prompt(similar_prompts, user_prompt, recent_messages):
    chat_history_section = "Chat-History:\n" + "\n".join([f"User Input: {message['prompt']}\nLuna: {message['response']}" for message in recent_messages])

    context_section = "Context based on information about the conversation:\n" + "\n\n".join(
        similar_prompts) if similar_prompts else ""
    user_prompt_section = "Current User Input Request:\n" + user_prompt

    extended_prompt = f"{chat_history_section}\n\n{context_section}\n\n{user_prompt_section}"
    return extended_prompt


# async def generate_speech(text, locales="en-GB", gender="Female"):
#    voices_manager = await VoicesManager.create()
# voice_selection = voices_manager.find(Gender=gender, Locale=locales)
#    if not voice_selection:
#        raise ValueError("Keine Stimme gefunden, die den Kriterien entspricht.")
#
#    selected_voice = random.choice(voice_selection)["Name"]
#    communicate = edge_tts.Communicate(text, selected_voice)
#
#    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
#        await communicate.save(temp_file.name)
#
#        temp_file.seek(0)
#        audio_bytes = temp_file.read()
#
#    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
#
#    return audio_base64


async def generate_speech(text):
    voice = "en-GB-SoniaNeural"
    #en-GB-RyanNeural
    communicate = edge_tts.Communicate(text, voice)

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        await communicate.save(temp_file.name)

        temp_file.seek(0)
        audio_bytes = temp_file.read()

    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    return audio_base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def translate_text(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        print(translated_text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


@app.post('/api/post')
async def post(request_data: PostRequest):
    global text_response
    prompt = request_data.prompt
    image64 = request_data.image_base64
    db = EmbeddingDB('embeddings.db')
    response_data = {'prompt': prompt}
    prompt_embedding = model.encode(prompt, convert_to_tensor=True).cpu().numpy()
    is_command, parsed_prompt = commands.parse_commands(prompt)

    if not is_command:
        print("Command detected")
        _, return_response = commands.parse_commands(prompt)
        speech_result = await generate_speech(return_response)
        response_data = {
            'prompt': prompt,
            'response': return_response,
            'speech': speech_result,
        }

    else:

        action_executed, action_result = check_context_and_execute(prompt_embedding)
        if not action_executed:
            # Suche nach ähnlichen Prompts als Kontext
            similar_prompts = db.retrieve_similar_prompts(prompt_embedding)
            recent_messages = db.retrieve_recent_chat_messages()
            extended_prompt = generate_extended_prompt(similar_prompts, prompt, recent_messages)
            print("Extended prompt: ", extended_prompt)

            if image64:
                image_bytes = base64.b64decode(image64.split(',')[1])
                image_stream = io.BytesIO(image_bytes)
                image = Image.open(image_stream)
                filepath = f"temp/image.png"
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                image.save(filepath, 'PNG')

                base64_image = encode_image(filepath)
                #later own model
                response = client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "system",
                            "content": assistant_description,
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": extended_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                        "detail": "low"
                                    },
                                },
                            ],
                        },
                    ],
                    max_tokens=300,
                )

                text_response = response.choices[0].message.content
                print("Image response: ", text_response)

            else:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": assistant_description,
                        },
                        {

                            "role": "user",
                            "content": [
                                {"type": "text", "text": extended_prompt}
                            ],
                        }
                    ],
                    max_tokens=300,
                )
                text_response = response.choices[0].message.content
                print("Text response: ", text_response)
            speech_result = await generate_speech(text_response)
            response_data = {
                'prompt': prompt,
                'response': text_response,
                'speech': speech_result,
            }

            db.add_or_retrieve_prompt(prompt, prompt_embedding)
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": action_result},
                        ],
                    }
                ],
                max_tokens=300,
            )
            print("Action response: ", response.choices[0].message.content)
            speech_result = await generate_speech(response.choices[0].message.content)
            response_data = {
                'prompt': prompt,
                'response': response.choices[0].message.content,
                'speech': speech_result,
            }

        db.add_chat_message(prompt, text_response)
        db.close()
    return JSONResponse(content=response_data)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
