import os
import wave
import pyaudio
import speech_recognition as sr
from transformers import pipeline

# Initialize translation pipeline for English to Dutch
translation_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-nl")  # English to Dutch

def record_audio(filename='audio.wav', duration=5):
    """Records audio for a specified duration and saves it to a WAV file."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []

    print("Recording...")
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

def transcribe_audio(filename='audio.wav'):
    """Transcribes audio from a file using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)  # Read the entire audio file

    try:
        # Recognize speech using Google Web Speech API
        recognized_text = recognizer.recognize_google(audio, language='en-US')
        return recognized_text
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_text(text):
    """Translates text from English to Dutch."""
    if text:
        print(f"Translating: {text}")  # Debug: Show what is being translated
        translation = translation_pipeline(text, max_length=40)
        translated_text = translation[0]['translation_text']
        print(f"Translated Output: {translated_text}")  # Debug: Show translated output
        return translated_text
    return "No text to translate."

def main():
    print("Starting the translator. Say 'stop' to exit.")
    
    while True:
        # Record audio
        record_audio(duration=5)  # Adjust duration as needed
        
        # Transcribe audio
        recognized_text = transcribe_audio()
        if recognized_text:
            print(f"Recognized Text: {recognized_text}")

            # Translate recognized text into Dutch
            translated_text = translate_text(recognized_text)
            print(f"Translated Text: {translated_text}")

            # Check if the user wants to stop
            if 'stop' in recognized_text.lower():
                print("Exiting the translator.")
                break

if __name__ == "__main__":
    main()
