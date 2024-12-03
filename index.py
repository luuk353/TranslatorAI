import flet as ft
from Googletranslate import capture_audio, translate_text as google_translate  # Google Translate logic
from DeepL import translate_with_deepl  # Import DeepL logic


def main(page: ft.Page):
    page.title = "Speech-to-Text Translator Comparison (EN to NL)"

    # UI Elements
    hello_world = ft.Text(value="Speech-to-Text Translator Comparison (English to Dutch)", color="green", size=15)
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
    page.add(translations_row)  # Add the row containing translation outputs
    page.add(process_box)
    page.add(error_box)

    listening = False

    def on_button_click(e):
        nonlocal listening
        if listening:
            process_box.value = "Stopped Listening"
            listening = False
        else:
            process_box.value = "Listening..."
            detected_text_box.value = ""
            google_translation_box.value = ""
            deepl_translation_box.value = ""
            error_box.value = ""
            listening = True
            page.update()

            def listen_and_translate():
                while listening:
                    process_box.value = "Listening..."
                    page.update()

                    # Capture audio
                    text = capture_audio()
                    if text:
                        detected_text_box.value = text
                        process_box.value = f"Detected Text: {text}"
                        error_box.value = ""
                        page.update()

                        try:
                            # Google Translate
                            google_translation = google_translate(text, target_language="NL")
                            google_translation_box.value = google_translation

                            # DeepL Translate
                            deepl_translation = translate_with_deepl(text, source_lang="EN", target_lang="NL")
                            deepl_translation_box.value = deepl_translation

                            process_box.value = "Translation Completed"
                        except Exception as ex:
                            error_box.value = f"Error: {str(ex)}"
                            process_box.value = ""
                        page.update()
                    else:
                        error_box.value = "Could not understand the audio"
                        process_box.value = ""
                        page.update()

            listen_and_translate()

    # Add button
    page.add(
        ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [ft.Text(value="Click to Start/Stop", size=15)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(8),
                bgcolor=ft.colors.BLUE_400,
            ),
            on_click=on_button_click,
        )
    )


# Run the app
ft.app(main)
