from deep_translator import GoogleTranslator


def translate_text(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        print(translated_text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text