import speech_recognition as sr
from googletrans import Translator



# Function to capture audio from the microphone and convert it to text
def capture_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        # Adjust the recognizer sensitivity to ambient noise (for 1 second)
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Set a threshold for the microphone sensitivity (lower value for more sensitivity)
        recognizer.energy_threshold = 400  # Adjust this value to control sensitivity

        while True:
            try:
                # Continuously listen for audio, no timeout, listening indefinitely
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                print("Detected speech...")

                # Recognize the speech using Google
                text = recognizer.recognize_google(audio)
                print(f"Recognized Text: {text}")
                return text

            except sr.UnknownValueError:
                print("Could not understand the audio.")
                return None
            except sr.RequestError as e:
                print(f"Error with Google Speech Recognition: {e}")
                return None
            except sr.WaitTimeoutError:
                # In case no speech is detected for a period, continue listening
                continue


# Function to translate the captured text into the target language (default: Dutch)
def translate_text(text, target_language="nl"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"Translated Text ({target_language}): {translation.text}")
    return translation.text
