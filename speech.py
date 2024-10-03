import pyaudio
import torch

# Load the Silero speech recognition model
model = torch.hub.load("snakers4/silero-models", "silero_stt", language='en', device='cpu')

# Constants for audio recording
CHUNK = 1024  # Number of frames in each buffer
FORMAT = pyaudio.paInt16  # Sample size in bits
CHANNELS = 1  # Number of audio channels (1 for mono)
RATE = 48000  # Sampling rate (Hz)

def mock_translate(text, target_language="es"):
    # Replace with actual translation logic or API call
    return f"[Translated to {target_language}] {text}"

def stream_audio():
    audio = pyaudio.PyAudio()

    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        return

    print("Listening...")

    while True:
        try:
            audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
        except Exception as e:
            print(f"Error reading audio stream: {e}")
            continue

        # Convert audio chunk to tensor
        audio_chunk = torch.frombuffer(audio_chunk, dtype=torch.int16).float().unsqueeze(0)

        # Normalize the audio tensor to the range [-1, 1]
        audio_chunk = audio_chunk / 32768.0
        
        # Use Silero to recognize speech
        with torch.no_grad():  # Disable gradient calculation for inference
            # Call the model with audio input
            transcription_output = model(audio_chunk)


        # Check if the transcription is a tuple and extract the relevant part
        if isinstance(transcription_output, tuple):
            # Extract the transcription from the first element (this may vary)
            transcription_text = transcription_output  # Adjust if necessary
        else:
            transcription_text = transcription_output

        # Handle output format: If it's a tensor, convert to string
        if isinstance(transcription_text, torch.Tensor):
            transcription_text = transcription_text.squeeze(0).cpu().numpy()
            # You may need to adjust this part based on the actual output type
            transcription_text = "".join(map(chr, transcription_text))  # Convert numerical output to string

        # Print and translate the recognized text
        if transcription_text:
            print(f"Original Text: {transcription_text}")
            translated_text = mock_translate(transcription_text)
            print(f"Translated Text: {translated_text}")

if __name__ == "__main__":
    stream_audio()
