import speech_recognition as sr
from googletrans import Translator


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


def translate_text(text, target_language="nl"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"Translated Text ({target_language}): {translation.text}")
    return translation.text


def main():
    while True:
        text = capture_audio()
        if text:
            translated_text = translate_text(text, target_language="nl")
            print(f"Translation: {translated_text}")


if __name__ == "__main__":
    main()
