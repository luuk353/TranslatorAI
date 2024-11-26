import speech_recognition as sr
from googletrans import Translator

# Function to capture audio from the microphone and convert it to text
def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Processing audio...")
        text = recognizer.recognize_google(audio)
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Error with Google Speech Recognition; {e}")
        return None

# Function to translate the captured text into the target language (default: Dutch)
def translate_text(text, target_language="nl"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"Translated Text ({target_language}): {translation.text}")
    return translation.text
