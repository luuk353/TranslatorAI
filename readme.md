# Live Speech Translator

A real-time speech translation application that converts English speech to Dutch text, providing translations from both Google Translate and DeepL APIs side by side.

- [Live Speech Translator](#live-speech-translator)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Dependencies](#dependencies)
  - [Technical Details](#technical-details)
  - [Troubleshooting](#troubleshooting)
  - [About the Project](#about-the-project)


## Features

- Real-time speech recognition using Google's Speech Recognition
- Dual translation services:
  - Google Translate
  - DeepL API (Free tier)
- Modern GUI built with Flet framework
- Side-by-side translation comparison
- Process and error logging

## Prerequisites

- Python 3.7+
- DeepL API key (free tier)
- Working microphone
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd TranslatorAI
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Configure your DeepL API key:
   - Sign up for a free API key at [DeepL API](https://www.deepl.com/pro-api)
   - Open `DeepL.py` and replace the `DEEPL_API_KEY` value

## Usage

1. Start the application:
```bash
python index.py
```

2. Click the "Start Live Translation" button
3. Speak in English (the app will listen for 5-10 seconds per phrase)
4. View the results:
   - Top: Original detected English text
   - Left: Google Translate Dutch translation
   - Right: DeepL Dutch translation
   - Bottom: Process and error logs

## Project Structure

- `index.py`: Main application with GUI and translation thread management
- `DeepL.py`: Speech recognition and DeepL API integration
- `requirements.txt`: Project dependencies

## Dependencies

- flet: Modern GUI framework
- googletrans==3.1.0a0: Google Translate API
- SpeechRecognition: Speech-to-text conversion
- requests: HTTP requests for DeepL API
- PyAudio: Audio processing

## Technical Details

- Speech Recognition:
  - Adjusts for ambient noise
  - 5-second timeout
  - 10-second phrase time limit
- Translations:
  - Target language: Dutch (NL)
  - Runs in a separate daemon thread
  - Real-time updates to the UI

## Troubleshooting

1. Speech Recognition Issues:
   - Ensure your microphone is working and set as default
   - Speak clearly and wait for the "Listening..." message
   - Check if you see "Could not understand the audio" frequently

2. Translation Issues:
   - Verify your internet connection
   - Check the error log for specific API errors
   - Ensure your DeepL API key is valid and properly set

3. PyAudio Installation Issues (Windows):
   - If pip install fails, download the appropriate `.whl` file from [PyAudio Wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
   - Install using: `pip install [downloaded-wheel-file].whl`

## About the Project

We have developed a project called the "Live Translator." This is a brief introduction describing its features and how everything is structured. In this introduction, we provide a short overview of the project, explaining why we created it and how the program works.

The application uses speech recognition to convert audio into text. This is achieved using the speech_recognition library. The recognized text is then translated into Dutch, first with Google Translate and then with DeepL, with the results displayed side by side.

The process is executed in real-time. As soon as the application starts listening, the detected text is displayed along with the translations from Google Translate and DeepL.

We use the Flet library for the front-end of the project. The goal of this project is to provide a tool for live translations that is both fast and accurate, with a direct comparison between two popular translation tools.

How does it work? In this project, we utilize DeepL, but what exactly is DeepL? DeepL is not a traditional Large Language Model (LLM), like OpenAI's ChatGPT, but a neural machine translation system that leverages advanced AI and deep learning techniques to translate text.

In our project, we use DeepL to translate the detected English text. We access their translation model through the DeepL API. DeepL processes the text, considers the context of sentences, and generates the translated text.

We also integrate the Google Translate API in our project. This works similarly to the Google Translate tool we all know. In our system, it listens to spoken text and translates it into the desired language. One common issue with Google Translate is that it often makes errors in sentence structure. Additionally, it sometimes mistranslates words in the context of the rest of the sentence. With DeepL, we encounter this issue much less frequently because it is a much larger LLM. By displaying both DeepL and Google Translate API translations, we can clearly compare the results of a simple translation tool and those of a more advanced LLM.

