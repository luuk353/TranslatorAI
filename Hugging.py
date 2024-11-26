import speech_recognition as sr
import pyttsx3
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Define the model name for translation
model_name = "t5-base"

# Load the tokenizer and model for T5
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def generate_text(input_text):
    # Prepend the task instruction to the input text to indicate the translation task
    task_prefix = "Translate English to Dutch: "
    input_text = task_prefix + input_text

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    # Generate output using the model
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=4, early_stopping=True)

    # Decode the generated output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text


def recognize_speech():
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    print("Starting the translation service. Say 'stop' to exit.")

    while True:
        input_text = recognize_speech()

        if input_text is None:
            continue

        if "stop" in input_text.lower():
            print("Stopping the service.")
            break

        print(f"Translating: {input_text}")
        translated_text = generate_text(input_text)
        print(f"Translated Text: {translated_text}")

        # Speak the translated text
        speak_text(translated_text)


if __name__ == "__main__":
    main()
