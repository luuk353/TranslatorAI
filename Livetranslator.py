import os

import requests
import speech_recognition as sr
import threading

# DeepL API key and endpoint
API_KEY = os.getenv("APIKEY")
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'


# Function to translate text using DeepL API
def translate_text(text, source_lang='EN', target_lang='NL'):
    params = {
        'auth_key': API_KEY,
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang,
    }
    response = requests.post(DEEPL_URL, data=params)
    if response.status_code == 200:
        translated_text = response.json()['translations'][0]['text']
        return translated_text
    else:
        print("Error with DeepL API:", response.status_code)
        return None


# Function to process speech as it is recognized
def recognize_speech_callback(recognizer, audio):
    try:
        # Recognize speech from the audio (in English)
        english_text = recognizer.recognize_google(audio, language='en-US')
        print(f"Recognized (English): {english_text}")

        # Translate English to Dutch instantly
        dutch_translation = translate_text(english_text)

        if dutch_translation:
            print(f"Translation (Dutch): {dutch_translation}")

    except sr.UnknownValueError:
        pass  # Ignore if unable to understand speech
    except sr.RequestError:
        print("Error with the speech recognition service.")


# Main function to handle live speech-to-text and translation
def live_translation():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()  # Initialize the microphone without the 'with' block

    # Start background listening (without ambient noise adjustment)
    print("Listening for speech...")
    while True:
        try:
            # Continuously listen for speech (immediate feedback)
            audio = recognizer.listen(microphone, timeout=5)  # Timeout set to 5 seconds to allow pause
            recognize_speech_callback(recognizer, audio)  # Process speech instantly as it is recognized
        except sr.WaitTimeoutError:
            continue  # Ignore timeout errors and keep listening


# Run live translation in a separate thread
if __name__ == "__main__":
    translation_thread = threading.Thread(target=live_translation)
    translation_thread.daemon = True  # Run in the background
    translation_thread.start()

    # Keep the program running indefinitely
    while True:
        pass
