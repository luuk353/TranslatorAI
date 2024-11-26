import os
import wave
import pyaudio
import speech_recognition as sr
from transformers import pipeline
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Initialize translation pipeline for English to Dutch (nl)
translation_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-nl")


def record_audio(filename='audio.wav', duration=5):
    """Records audio for a specified duration and saves it to a WAV file."""
    audio = pyaudio.PyAudio()
    try:
        # Open the audio stream
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        frames = []

        print("Recording...")
        for _ in range(0, int(16000 / 1024 * duration)):
            try:
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Error during recording frame: {e}")
                break

        print("Finished recording.")
        stream.stop_stream()
        stream.close()

        # Save the audio to a file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
    except Exception as e:
        print(f"Error during recording: {e}")
    finally:
        audio.terminate()


def transcribe_audio(filename='audio.wav'):
    """Transcribes audio from a file using SpeechRecognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)  # Read the entire audio file

        # Recognize speech using Google Web Speech API
        recognized_text = recognizer.recognize_google(audio, language='en-US')
        return recognized_text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


def translate_text(text):
    """Translates text from English to Dutch."""
    if text:
        print(f"Translating: {text}")
        try:
            translation = translation_pipeline(text, max_length=40)
            translated_text = translation[0]['translation_text']
            print(f"Translated Output(NL): {translated_text}")
            return translated_text
        except Exception as e:
            print(f"Error during translation: {e}")
            return "Translation failed."
    return "No text to translate."


def main():
    print("Starting the translator. Say 'stop' to exit.")

    try:
        while True:
            # Record audio for 5 seconds (can be adjusted)
            record_audio(duration=5)

            # Transcribe the recorded audio to text
            recognized_text = transcribe_audio()
            if recognized_text:
                print(f"Recognized Text: {recognized_text}")

                # Translate the recognized text into Dutch
                translated_text = translate_text(recognized_text)
                print(f"Translated Text: {translated_text}")

                # Exit if the user says "stop"
                if 'stop' in recognized_text.lower():
                    print("Exiting the translator.")
                    break
            else:
                print("No text recognized. Trying again...")

    except KeyboardInterrupt:
        print("\nTranslation app interrupted. Exiting gracefully.")


if __name__ == "__main__":
    main()
