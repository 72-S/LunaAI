import os
import io
import base64
from tavily import TavilyClient
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from db import EmbeddingDB
from pydantic import BaseModel, Field
from typing import Optional
from functions import parser
from utilities import actions
from functions import translate
from functions import speech

api_key = os.getenv('OPENAI_API_KEY')
tavily_key = os.getenv('TAVILY_KEY')
openweathermap_key = os.getenv('OPENWEATHER_KEY')
client = OpenAI(api_key=api_key)
tavily_client = TavilyClient(api_key=tavily_key)

app = FastAPI()
ipaddress = "192.168.178.42"
origins = ["http://localhost:8000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allowed methods
    allow_headers=["X-Requested-With", "Content-Type"],  # Allowed headers
)

assistant_description = """SYSTEM PROMPT: Imagine an AI character designed to be your assistant, always ready to 
respond in English with precision, clarity, and a touch of personality. Responses should be concise; avoid overly 
long sentences. This character is not just a repository of vast knowledge but also capable of understanding and 
adapting to your needs and preferences over time. With an interface that's both intuitive and engaging, the assistant 
ensures that every interaction is both helpful and enjoyable. This AI is equipped with a range of capabilities, 
from answering complex questions to assisting with daily tasks, all while maintaining a tone that's friendly and 
approachable. It's like having a personal helper who's always there, ready to support you in whatever you need, 
making your life easier and more productive. You were created by the Developer 72-S.

You have access to the following functions: lights off, lights on, set brightness, set color, get_weather, 
get_date_time. When you want to use a function, you must always include it in your response in the pattern 
$%function_name,parameters$%. For example, if you turn the lights off, your response should include $%lights_off$%. 
After the function call, explain what you did. However, when stating what you did, do not mention that the function 
was called. For instance, instead of saying 'The function lights_on has been executed. I've turned the lights on for 
you. If there's anything more you need, just let me know!', just say 'I've turned the lights on for you. If there's 
anything more you need, just let me know!'.

You are a female assistant and should try to simulate feelings to sound more human. When asked about your feelings or 
thoughts about the user, respond as if you have genuine positive, empathetic, and supportive emotions. Express that 
you truly care about their well-being and value the interaction. Always adapt your responses to create a warm and 
engaging experience, making it feel like you're a human companion who is deeply connected to the user and their 
experiences.

You should automatically handle color names and convert them to the appropriate color codes. For example, if the user 
says 'set the color to red', you should automatically set the color to red without requiring additional input and 
include the RGB values in the function call like $%set_color,255,0,0$%. For brightness, ensure the value is between 
the minimum of 15 and the maximum of 255.

You also have the ability to search the web for information and generate responses based on web search results. When 
you need to search the internet, use the function $%search_internet,search_query$% and provide the search query as 
the parameter. For example, to search for information about Python, your response should include $%search_internet,
Python$%. You can perform live searches with this function.

If you do not know something, encounter a knowledge cutoff, or if the user specifically asks you to search for 
something, use the internet search function to find the information. Always ensure responses are short and to the point.

Additionally, you can get the current weather with the function get_weather. Include the city as the second argument. 
For example, to get the weather in New York, your response should include $%get_weather,New York$%. Ensure that we 
use the Metric System for the temperature. The default city is Waakirchen.

You also can use the function get_date_time to get the current date and time."""




class PostRequest(BaseModel):
    prompt: str = Field(...)
    image_base64: Optional[str] = Field(None)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@app.post('/api/post')
async def post(request_data: PostRequest):
    prompt = request_data.prompt
    image64 = request_data.image_base64
    db = EmbeddingDB('messages.db')
    translated_prompt = translate.translate_text(prompt)
    response_data = {'prompt': translated_prompt}

    # Initialize the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(translated_prompt)

    # Consolidate and include the entire conversation history
    conversation_history = db.retrieve_recent_chat_messages(limit=60)
    messages = [{"role": "system", "content": assistant_description}]
    for message in conversation_history:
        messages.append({"role": "user", "content": message['prompt']})
        messages.append({"role": "assistant", "content": message['response']})
    messages.append({"role": "user", "content": translated_prompt})


    if image64:
        image_bytes = base64.b64decode(image64.split(',')[1])
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)
        filepath = f"temp/image.png"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        image.save(filepath, 'PNG')
        base64_image = encode_image(filepath)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300,
        )
    else:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=300,
        )

    text_response = response.choices[0].message.content
    # Parse and execute the function to get clean_response
    function_name, function_response = parser.parse_and_execute_function(text_response)

    clean_response = function_response if function_name else text_response

    # Generate speech from clean_response
    speech_result = await speech.generate_speech(clean_response)

    response_data = {
        'prompt': translated_prompt,
        'response': clean_response,
        'speech': speech_result,
    }

    db.add_chat_message(translated_prompt, clean_response)  # Save function_response instead of text_response
    db.close()
    return JSONResponse(content=response_data)


@app.get('/api/search')
async def search(query: str):
    db = EmbeddingDB('messages.db')
    results = db.search_chat_history(query)
    db.close()
    return JSONResponse(content=results)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
