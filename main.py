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
import json
import datetime

nest_asyncio.apply()

app = Flask(__name__)
model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")

current_text = ''

API_KEY = "19db1b8cf86382e5a6d546c5390a8613"
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q=Waakirchen,de&units=metric&appid=' + API_KEY


def translate_text(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        print(translated_text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def set_led_color(color):
    url = "http://home.local/json/state"
    data = {
        "seg": [
            {
                "col": [color]
            }
        ]
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print(f"LED set to {color}")
    else:
        print(f"Failed to set the LED to {color}", response.status_code, response.text)


def get_weather_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def handle_special_commands(translated_text):
    light_off_commands = [
        "light off", "lights off", "turn the lights off", "switch off the lights",
        "shut off the lights", "kill the lights", "dim the lights", "lights out",
        "turn off the light", "shut down the lights", "turn off the leds", "leds off",
        "shut off the leds", "kill the leds", "led off"
    ]
    light_off_responses = [
        "The light has been turned off.", "Lights are now off.",
        "I've turned off the lights for you.", "Sure, the lights are off now.",
        "Done, the lights are off.", "Okay, I've shut off the lights for you.",
        "The LEDs are now off.", "LEDs have been turned off.",
        "Alright, turning off the lights.", "Your wish is my command, lights are off."
    ]

    light_on_commands = [
        "light on", "lights on", "turn the lights on", "switch on the lights",
        "turn on the lights", "illuminate the room", "lights up", "brighten the room",
        "turn on the light", "power on the lights", "turn on the leds", "leds on",
        "power on the leds", "illuminate with leds", "led on", "switch on the light"
    ]
    light_on_responses = [
        "The light has been turned on.", "Lights are now on.",
        "I've turned on the lights for you.", "Sure, the lights are on now.",
        "Done, the lights are on.", "Okay, I've powered on the lights for you.",
        "The LEDs are now on.", "LEDs have been turned on.",
        "Alright, turning on the lights.", "Your wish is my command, lights are on."
    ]
    white_commands = [
        "white light", "change to white", "set light to white", "turn the lights white",
        "switch to white light", "make the light white", "lights white please", "want white illumination",
        "white illumination", "give me white light", "i want white color", "set leds to white",
        "white leds", "change leds to white", "make the leds white", "LEDs white"
    ]
    purple_commands = [
        "purple light", "change to purple", "set light to purple", "turn the lights purple",
        "switch to purple light", "make the light purple", "lights purple please", "want purple illumination",
        "purple illumination", "give me purple light", "i want purple color", "set leds to purple",
        "purple leds", "change leds to purple", "make the leds purple", "LEDs purple"
    ]
    blue_commands = [
        "blue light", "change to blue", "set light to blue", "turn the lights blue",
        "switch to blue light", "make the light blue", "lights blue please", "want blue illumination",
        "blue illumination", "give me blue light", "i want blue color", "set leds to blue",
        "blue leds", "change leds to blue", "make the leds blue", "LEDs blue"
    ]
    red_commands = [
        "red light", "change to red", "set light to red", "turn the lights red",
        "switch to red light", "make the light red", "lights red please", "want red illumination",
        "red illumination", "give me red light", "i want red color", "set leds to red",
        "red leds", "change leds to red", "make the leds red", "LEDs red"
    ]
    green_commands = [
        "green light", "change to green", "set light to green", "turn the lights green",
        "switch to green light", "make the light green", "lights green please", "want green illumination",
        "green illumination", "give me green light", "i want green color", "set leds to green",
        "green leds", "change leds to green", "make the leds green", "LEDs green"
    ]
    white_responses = [
        "The light has been set to white.", "Lights are now white.",
        "I've changed the lights to white for you.", "Sure, the lights are white now.",
        "Done, the lights are white.", "Okay, I've set the lights to white for you.",
        "The LEDs are now white.", "LEDs have been set to white.",
        "Alright, turning the lights white.", "Your wish is my command, lights are white."
    ]

    purple_responses = [
        "The light has been set to purple.", "Lights are now purple.",
        "I've changed the lights to purple for you.", "Sure, the lights are purple now.",
        "Done, the lights are purple.", "Okay, I've set the lights to purple for you.",
        "The LEDs are now purple.", "LEDs have been set to purple.",
        "Alright, turning the lights purple.", "Your wish is my command, lights are purple."
    ]

    blue_responses = [
        "The light has been set to blue.", "Lights are now blue.",
        "I've changed the lights to blue for you.", "Sure, the lights are blue now.",
        "Done, the lights are blue.", "Okay, I've set the lights to blue for you.",
        "The LEDs are now blue.", "LEDs have been set to blue.",
        "Alright, turning the lights blue.", "Your wish is my command, lights are blue."
    ]

    red_responses = [
        "The light has been set to red.", "Lights are now red.",
        "I've changed the lights to red for you.", "Sure, the lights are red now.",
        "Done, the lights are red.", "Okay, I've set the lights to red for you.",
        "The LEDs are now red.", "LEDs have been set to red.",
        "Alright, turning the lights red.", "Your wish is my command, lights are red."
    ]

    green_responses = [
        "The light has been set to green.", "Lights are now green.",
        "I've changed the lights to green for you.", "Sure, the lights are green now.",
        "Done, the lights are green.", "Okay, I've set the lights to green for you.",
        "The LEDs are now green.", "LEDs have been set to green.",
        "Alright, turning the lights green.", "Your wish is my command, lights are green."
    ]
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
        "is it windy", "weather status", "give me a weather report", "how is the weather", "how is the weather today",
        "what is the weather in waakirchen"
    ]

    # Commands for temperature request
    temperature_commands = [
        "what's the temperature", "how hot is it", "how cold is it",
        "tell me the temperature", "current temperature", "how warm is it",
        "is it chilly outside", "temperature check", "how's the temperature",
        "is it freezing", "is it boiling", "temperature outside",
        "how's the temp", "what's the temp like", "is it hot or cold",
        "give me the temperature", "tell me how warm it is", "how many degrees do we have"
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

    for command in light_off_commands:
        if command in translated_text.lower():
            url = "http://home.local/win&T=0"
            response = requests.get(url)
            if response.status_code != 200:
                print("Failed to turn off LED")
            return random.choice(light_off_responses)

    for command in light_on_commands:
        if command in translated_text.lower():
            url = "http://home.local/win&T=1"
            response = requests.get(url)
            if response.status_code != 200:
                print("Failed to turn on LED")
            return random.choice(light_on_responses)

    for command in white_commands:
        if command in translated_text.lower():
            set_led_color([255, 255, 255, 0])
            return random.choice(white_responses)

    for command in purple_commands:
        if command in translated_text.lower():
            set_led_color([255, 0, 255, 0])
            return random.choice(purple_responses)

    for command in blue_commands:
        if command in translated_text.lower():
            set_led_color([0, 0, 255, 0])
            return random.choice(blue_responses)

    for command in red_commands:
        if command in translated_text.lower():
            set_led_color([255, 0, 0, 0])
            return random.choice(red_responses)

    for command in green_commands:
        if command in translated_text.lower():
            set_led_color([0, 255, 0, 0])
            return random.choice(green_responses)

    for command in time_commands:
        if command in translated_text.lower():
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Format: HH:MM:SS
            return random.choice(time_responses).format(time=current_time)

    for command in date_commands:
        if command in translated_text.lower():
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
            return random.choice(date_responses).format(date=current_date)

    for command in weather_commands:
        data = get_weather_data()
        if not data:
            return "Sorry, I couldn't fetch the weather data right now."
        description = data['weather'][0]['description']
        if command in translated_text.lower():
            return random.choice(weather_responses).format(description=description)

    for command in temperature_commands:
        data = get_weather_data()
        if not data:
            return "Sorry, I couldn't fetch the temperature data right now."
        temp = data['main']['temp']
        if command in translated_text.lower():
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
    # Entfernen von '*'
    text = text.replace('*', '-')

    # Entfernen von 'today?' am Anfang des Textes
    if text.startswith('  today?'):
        text = text[len('today?'):].strip()

    lines = text.split('\n', 1)  # Teilt den Text in zwei Teile: den ersten Absatz und den Rest
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

        # Formatieren Sie den generierten Text
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
    app.run(host='192.168.178.31', port=443, ssl_context=context)
