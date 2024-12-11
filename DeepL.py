import os
import speech_recognition as sr
import requests
import time

DEEPL_API_KEY = os.getenv("APIKEY")
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'


# Function to capture audio and convert it to text in real-time
def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

        print("Listening... (say something)")

        try:
            # Increase the timeout and phrase time limit to prevent premature timeouts
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None

# Function to translate text using DeepL
def translate_with_deepl(text, target_lang="NL"):
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_lang
    }

    response = requests.post(DEEPL_URL, data=params)
    if response.status_code == 200:
        return response.json()['translations'][0]['text']
    else:
        raise Exception(f"DeepL API Error: {response.status_code} - {response.text}")
