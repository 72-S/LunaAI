from flask import Flask, request, render_template, jsonify
from gpt4all import GPT4All
import edge_tts
import asyncio
import io
import base64
import nest_asyncio
import os
import tempfile
from deep_translator import GoogleTranslator
import random
import requests
import datetime

nest_asyncio.apply()

app = Flask(__name__)
model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
city = 'Waakirchen'
api = '19db1b8cf86382e5a6d546c5390a8613'

current_text = ''

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + ',de&units=metric&appid=' + api


def translate_text(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        print(translated_text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def get_weather_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def handle_special_commands(translated_text):
    time_commands = [
        "what time is it", "can you tell me the time", "what's the current time",
        "how late is it", "tell me the time", "time please", "how late do we have",
        "can you check the time", "i want to know the current time",
        "what time does your clock show", "how late is it right now", "can you tell me the exact time",
        "i lost my watch, what time is it", "i need the current time", "what time is it"
    ]

    time_responses = [
        "It's {time} now.", "The current time is {time}.",
        "Right now, it's {time}.", "On my clock, it's {time}.",
        "It's exactly {time}.", "My clock shows {time}.",
        "According to my internal clock, it's {time}.", "It's {time}, don't forget to be on time!",
        "Time flies, it's already {time}.", "Hold on, let me check... It's {time}."
    ]
    date_commands = [
        "what's the date today", "can you tell me the date", "what's today's date",
        "which day is it today", "tell me the date", "date please", "how late do we have",
        "can you check the date", "i want to know the current date",
        "what date does your calendar show", "how late is it right now", "can you tell me the exact date",
        "i need to know today's date", "which day of the month is it", "what date is today", "what is today",
        "show me the date"
    ]

    date_responses = [
        "Today is {date}.", "The current date is {date}.",
        "Right now, it's {date}.", "On my calendar, it's {date}.",
        "It's exactly {date}.", "My calendar shows {date}.",
        "According to my internal calendar, it's {date}.", "It's {date}, don't forget any appointments!",
        "Time flies, today is already {date}.", "Hold on, let me check... It's {date}."
    ]
    # Commands for general weather request
    weather_commands = [
        "what's the weather like", "can you tell me the weather",
        "how's the weather", "is it raining",
        "tell me the weather", "how's it outside", "forecast",
        "what's the weather forecast", "how's the sky looking",
        "should I take an umbrella", "is it sunny out",
        "weather update", "current weather", "is it cloudy",
        "is it windy", "weather status", "give me a weather report", "how is the weather", "how is the weather today"
    ]

    # Commands for temperature request
    temperature_commands = [
        "what's the temperature", "how hot is it", "how cold is it",
        "tell me the temperature", "current temperature", "how warm is it",
        "is it chilly outside", "temperature check", "how's the temperature",
        "is it freezing", "is it boiling", "temperature outside",
        "how's the temp", "what's the temp like", "is it hot or cold",
        "give me the temperature", "tell me how warm it is", "how many degrees do we have", "how many degrees"
    ]

    # Responses for general weather
    weather_responses = [
        "It's currently {description}.",
        "The weather is {description}.",
        "Expect {description} today.",
        "Today, it's {description}.",
        "Looks like it's {description} right now.",
        "The skies are {description}.",
        "The current weather condition is {description}.",
        "It seems like a {description} day.",
        "You might want to know it's {description} out there.",
        "It's a {description} day today."
    ]

    temp_responses = [
        "It's currently {temp}°C.",
        "The temperature is {temp}°C.",
        "It's currently at {temp}°C.",
        "Expect temperatures around {temp}°C today.",
        "Today's temperature: {temp}°C.",
        "Right now, it's {temp}°C.",
        "Feeling like {temp}°C at the moment.",
        "The mercury reads {temp}°C.",
        "If you're stepping out, it's {temp}°C.",
        "The current temperature reading is {temp}°C.",
        "It's a {temp}°C kind of day.",
        "You might find it to be {temp}°C outside."
    ]

    for command in time_commands:
        if command in translated_text.lower():
            current_time = datetime.datetime.now().strftime('%H:%M')  # Format: HH:MM
            return random.choice(time_responses).format(time=current_time)

    for command in date_commands:
        if command in translated_text.lower():
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
            return random.choice(date_responses).format(date=current_date)

    for command in weather_commands:
        if command in translated_text.lower():
            data = get_weather_data()  # Fetch data only if the command matches
            if not data:
                return "Sorry, I couldn't fetch the weather data right now."
            description = data['weather'][0]['description']
            return random.choice(weather_responses).format(description=description)

        # Checking for temperature commands
    for command in temperature_commands:
        if command in translated_text.lower():
            data = get_weather_data()  # Fetch data only if the command matches
            if not data:
                return "Sorry, I couldn't fetch the temperature data right now."
            temp = data['main']['temp']
            return random.choice(temp_responses).format(temp=temp)

    return None


def generate_text():
    global current_text
    translated_text = translate_text(current_text)
    response = handle_special_commands(translated_text)
    if response:
        return response
    generated_text = model.generate(translated_text, temp=0.6, max_tokens=1000)
    print(generated_text)
    return generated_text


def format_output(text):
    # Remove '*'
    text = text.replace('*', '-')

    # Remove "today?" from the beginning of the text
    if text.startswith('  today?'):
        text = text[len('today?'):].strip()

    lines = text.split('\n', 1)  # Split into two lines
    if len(lines) > 1:
        text = lines[1].strip()

    return text


async def generate_speech_async(text):
    voice = "en-GB-RyanNeural"
    communicate = edge_tts.Communicate(text, voice)

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name
    temp_file.close()

    # Save the audio to the temporary file
    await communicate.save(temp_file_path)

    # Read the audio from the temporary file into a BytesIO object
    audio_io = io.BytesIO()
    with open(temp_file_path, 'rb') as f:
        audio_io.write(f.read())
    audio_io.seek(0)

    # Delete the temporary file
    os.remove(temp_file_path)

    return audio_io


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global current_text
    if request.method == 'POST':
        text = request.json['text']
        current_text = text
        generated_text = generate_text()

        # Format the output
        formatted_text = format_output(generated_text)

        loop = asyncio.get_event_loop()
        audio_io = loop.run_until_complete(generate_speech_async(formatted_text))

        # Convert audio to base64
        audio_base64 = base64.b64encode(audio_io.getvalue()).decode('utf-8')

        # Return both text and audio in a JSON response
        return jsonify({
            'text': formatted_text,
            'audio': audio_base64
        })
    return render_template('index.html')


if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(host="", port=443, ssl_context=context)
