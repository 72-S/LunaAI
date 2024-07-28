import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import os
import time
import requests
import base64
from pydub import AudioSegment
from pydub.playback import play
import io
import threading
import numpy as np

# API endpoint
API_URL = "http://127.0.0.1:5000/api/post"

# Vosk model path - update this to your Vosk model path
VOSK_MODEL_PATH = "/v3/models/vosk-model-small-de-0.15"

# Wake word
WAKE_WORD = "luna"

# Audio recording parameters
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen_for_wake_word():
    try:
        model = Model(VOSK_MODEL_PATH)
    except Exception as e:
        print(f"Error loading Vosk model: {e}")
        print("Please make sure you have downloaded the Vosk model and updated the VOSK_MODEL_PATH.")
        sys.exit(1)

    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, dtype='int16',
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, SAMPLE_RATE)
        print("Listening for wake word...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print(f"Recognized text: {result.get('text', '')}")  # Debugging statement
                if WAKE_WORD in result.get("text", "").lower():
                    print("Wake word detected!")
                    return True

def get_audio_input():
    print("Listening for your command...")
    audio_data = b""
    silence_threshold = 300  # Lowered threshold
    silence_duration = 0
    silence_limit = 1.0  # Maximum silence duration in seconds

    with sd.InputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, dtype='int16', channels=1, callback=callback):
        while True:
            if q.empty():
                time.sleep(0.1)
                continue

            data = q.get()
            audio_data += data

            # Convert bytes to numpy array for easier processing
            numpy_data = np.frombuffer(data, dtype=np.int16)
            max_amplitude = np.max(np.abs(numpy_data))

            print(f"Max amplitude: {max_amplitude}")  # Debugging output

            if max_amplitude < silence_threshold:
                silence_duration += len(data) / SAMPLE_RATE
                print(f"Silence duration: {silence_duration}")  # Debugging output
                if silence_duration > silence_limit:  # Stop after 1 second of silence
                    print("Silence detected, stopping recording.")
                    break
            else:
                silence_duration = 0

    print(f"Total audio data length: {len(audio_data)}")  # Debugging output
    return audio_data

def transcribe_audio(audio_data):
    try:
        model = Model(VOSK_MODEL_PATH)
    except Exception as e:
        print(f"Error loading Vosk model: {e}")
        print("Please make sure you have downloaded the Vosk model and updated the VOSK_MODEL_PATH.")
        sys.exit(1)

    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.AcceptWaveform(audio_data)
    result = json.loads(rec.Result())
    transcription = result.get("text", "")
    print(f"Transcription: {transcription}")
    return transcription

def send_to_api(transcription):
    payload = {
        "prompt": transcription
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an HTTPError if the response was an unsuccessful status code
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to API: {e}")
        return {"response": "Error connecting to API.", "speech": ""}

def play_audio(audio_base64):
    if audio_base64:
        audio_bytes = base64.b64decode(audio_base64)
        audio = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
        play(audio)

def main():
    while True:
        if listen_for_wake_word():
            print("Wake word detected, waiting for command...")
            # Clear the queue
            while not q.empty():
                q.get()
            # Small pause to allow user to start speaking
            time.sleep(0.5)

            audio_input = get_audio_input()
            print(f"Audio input length: {len(audio_input)}")

            if len(audio_input) > 0:
                transcription = transcribe_audio(audio_input)
                if transcription:
                    print(f"Transcription: {transcription}")
                    api_response = send_to_api(transcription)
                    print(f"API Response: {api_response['response']}")

                    # Play audio response in a separate thread
                    audio_thread = threading.Thread(target=play_audio, args=(api_response['speech'],))
                    audio_thread.start()
                else:
                    print("No transcription available.")
            else:
                print("No audio input captured.")
        else:
            print("No wake word detected, continuing to listen...")

if __name__ == "__main__":
    main()
