import requests
import speech_recognition as sr
import pyttsx3

# DeepL API key and endpoint
API_KEY = 'a7ad26a8-8d22-4d81-a943-b78f19f8ed98:fx'
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'

# Initialize text-to-speech engine
engine = pyttsx3.init()


# Function to get speech input and convert to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise
        audio = recognizer.listen(source)
        print("Recognizing speech...")
        try:
            text = recognizer.recognize_google(audio, language='nl-NL')  # Recognize Dutch
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
        return None


# Function to translate text using DeepL API
def translate_text(text, source_lang='NL', target_lang='EN'):
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


# Function to speak the translated text
def speak_translation(translation):
    engine.say(translation)
    engine.runAndWait()


# Main function to keep translating continuously
def main():
    while True:
        # Step 1: Recognize Dutch speech
        dutch_text = recognize_speech()

        if dutch_text:
            # Step 2: Translate Dutch to English
            english_translation = translate_text(dutch_text)

            if english_translation:
                print("Translation:", english_translation)
                # Step 3: Speak the translated English text
                speak_translation(english_translation)


# Run the program
if __name__ == "__main__":
    main()
