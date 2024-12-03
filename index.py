import flet as ft
from googletrans import Translator
from DeepL import translate_with_deepl, capture_audio  # Import the translate function from deepl.py
import threading
import speech_recognition as sr

# Initialize Google Translate
translator = Translator()


# Function to translate text using Google Translate
def translate_text_google(text, target_language="nl"):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to handle the entire translation process
def live_translation_process(page, detected_text_box, google_translation_box, deepl_translation_box, process_box, error_box):
    while True:
        detected_text = capture_audio()
        if detected_text:
            detected_text_box.value = detected_text
            process_box.value = f"Detected Text: {detected_text}"

            # Google Translate
            try:
                google_translation = translate_text_google(detected_text, target_language="nl")
                google_translation_box.value = google_translation
            except Exception as e:
                error_box.value = f"Google Translate Error: {str(e)}"

            # DeepL Translate
            try:
                deepl_translation = translate_with_deepl(detected_text, target_lang="NL")
                deepl_translation_box.value = deepl_translation
            except Exception as e:
                error_box.value = f"DeepL Translate Error: {str(e)}"

            process_box.value = "Translation Completed"
        else:
            error_box.value = "Could not understand the audio"
            process_box.value = ""

        page.update()

# Function to start and stop live translation
def start_translation_thread(page, detected_text_box, google_translation_box, deepl_translation_box, process_box, error_box):
    process_box.value = "Listening..."
    page.update()

    # Start live translation in a separate thread
    translation_thread = threading.Thread(target=live_translation_process, args=(page, detected_text_box, google_translation_box, deepl_translation_box, process_box, error_box))
    translation_thread.daemon = True
    translation_thread.start()

# Function to handle start/stop of the translation process in the UI
def main(page: ft.Page):
    page.title = "Live Translation (English to Dutch)"

    # UI Elements
    hello_world = ft.Text(value="Speech-to-Text Translator", color="green", size=15)
    detected_text_box = ft.TextField(height=75, width=600, label="Detected Text (English)", multiline=True)
    process_box = ft.TextField(height=75, width=600, label="Process Log", multiline=True)
    error_box = ft.TextField(height=75, width=600, label="Error Log", multiline=True, color="red")

    # Translation boxes for side-by-side layout
    google_translation_box = ft.TextField(
        height=100, width=300, label="Google Translate Output (Dutch)", multiline=True
    )
    deepl_translation_box = ft.TextField(
        height=100, width=300, label="DeepL Output (Dutch)", multiline=True
    )

    # Row to display translations side by side, aligned to the left
    translations_row = ft.Row(
        [
            google_translation_box,
            deepl_translation_box,
        ],
        alignment=ft.MainAxisAlignment.START,  # Align to the left
        spacing=10,
    )

    # Add elements to the page
    page.add(hello_world)
    page.add(detected_text_box)
    page.add(translations_row)
    page.add(process_box)
    page.add(error_box)

    # Button to start translation
    def on_button_click(e):
        start_translation_thread(page, detected_text_box, google_translation_box, deepl_translation_box, process_box, error_box)

    page.add(
        ft.ElevatedButton(
            content=ft.Text(value="Start Live Translation", size=15),
            on_click=on_button_click,
        )
    )

# Run the app
ft.app(main)
