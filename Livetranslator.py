import speech_recognition as sr
from googletrans import Translator
import threading
import time
import sys

# Global variable to hold recognized text
recognized_text = ""
translation = ""
running = True  # To control the running status

def capture_audio_in_background(recognizer, microphone):
    global recognized_text

    def callback(recognizer, audio):
        global recognized_text
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            recognized_text = text  # Update the recognized text
        except sr.UnknownValueError:
            # If speech is unintelligible, continue listening
            pass
        except sr.RequestError as e:
            print(f"Error with the recognition service; {e}")

    # Start listening in the background
    recognizer.listen_in_background(microphone, callback, phrase_time_limit=5)

def translate_text():
    global recognized_text, translation
    translator = Translator()

    while running:  # Continue running while the 'running' flag is True
        if recognized_text:  # If there is new text recognized
            # Translate the text in real-time
            translation = translator.translate(recognized_text, dest="nl")  # Change 'nl' to any target language
            print(f"Translation: {translation.text}")
        time.sleep(0.5)  # Short delay to allow for continuous updates

def main():
    global running
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Start the background audio capture in a separate thread
    audio_thread = threading.Thread(target=capture_audio_in_background, args=(recognizer, microphone))
    audio_thread.start()

    # Start translating in a separate thread
    translation_thread = threading.Thread(target=translate_text)
    translation_thread.start()

    # Main thread listens for the keyboard interrupt (Ctrl+C) and stops gracefully
    try:
        while running:
            if translation:
                print(f"Live Translation: {translation.text}")
            time.sleep(1)  # Short delay to prevent the loop from overloading the system
    except KeyboardInterrupt:
        print("\nShutting down...")
        running = False  # Set the flag to False to stop the other threads
        audio_thread.join()  # Wait for the audio thread to finish
        translation_thread.join()  # Wait for the translation thread to finish
        print("Program exited gracefully.")

if __name__ == "__main__":
    main()
