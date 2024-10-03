import speech_recognition as sr
from googletrans import Translator
import time

def recognize_speech_from_mic():
    # Initialize recognizer and mic
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Please say something:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the audio input

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_text(text, dest_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

if __name__ == "__main__":
    # Initialize translator
    translator = Translator()

    print("Press Ctrl+C to stop the program.")
    
    while True:
        # Recognize speech
        recognized_text = recognize_speech_from_mic()

        if recognized_text:
            # Translate the recognized text to the desired language
            translated_text = translate_text(recognized_text, dest_language='es')  # Translate to Spanish
            print("Translated Text:", translated_text)

        # Optional: Add a small delay to prevent overwhelming the microphone
        time.sleep(1)  # Adjust as needed
