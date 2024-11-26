import speech_recognition as sr
from googletrans import Translator


def capture_audio():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak.")
        try:
            audio = recognizer.listen(source)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Error: Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Error: Request to Google Speech Recognition failed; {e}")
            return None


def translate_text(text, target_language="nl"):

    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        print(f"Translated Text ({target_language}): {translation.text}")
        return translation.text
    except exceptions.TranslatorError as e:
        print(f"Error: Translation failed; {e}")
        return "Translation Error"


def main():

    print("Speech-to-Text Translator (Type 'exit' to quit)\n")
    target_language = "nl"  # Default target language is Dutch
    while True:
        print("\nSay something...")
        text = capture_audio()
        if text:
            if text.lower() == "exit":
                print("Exiting the program. Goodbye!")
                break
            translated_text = translate_text(text, target_language=target_language)
            print(f"Final Translation: {translated_text}")
        else:
            print("No valid input captured. Please try again.")


if __name__ == "__main__":
    main()
