import base64
import tempfile
import edge_tts


async def generate_speech(text):
    voice = "en-GB-SoniaNeural"
    communicate = edge_tts.Communicate(text, voice)
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        await communicate.save(temp_file.name)
        temp_file.seek(0)
        audio_bytes = temp_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64