import speech_recognition as sr
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Initialize the T5 model and tokenizer
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

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
    input_text = f"translate English to {target_language}: {text}"
    
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    
    # Generate translation
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=4, early_stopping=True)
    
    # Decode the translated text
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Translated Text ({target_language}): {translated_text}")
    return translated_text

def main():
    while True:
        text = capture_audio()
        if text:
            translated_text = translate_text(text, target_language="nl")
            print(f"Translation: {translated_text}")

if __name__ == "__main__":
    main()
