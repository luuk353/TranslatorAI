import flet as ft
from Googletranslate import capture_audio, translate_text  # Import the functions from translator.py


def main(page: ft.Page):
    page.title = "Flet Speech-to-Text Translator Example"

    # Create the UI elements with smaller size
    hello_world = ft.Text(value="Google translate translater", color="green", size=15)
    translation_box = ft.TextField(height=100, width=300, label="Translated Text",
                                   multiline=True)  # Smaller box for translation
    process_box = ft.TextField(height=75, width=300, label="Process Log", multiline=True)  # Smaller process box
    detected_text_box = ft.TextField(height=75, width=300, label="Detected Text",
                                     multiline=True)  # Smaller detected text box
    error_box = ft.TextField(height=75, width=300, label="Error Log", multiline=True, color="red")  # Smaller error box
    img = ft.Image(
        src="/tedx-logo.png",
        width=75,
        height=75,
        fit=ft.ImageFit.CONTAIN,
    )

    # Add the UI elements to the page
    page.add(hello_world)
    page.add(detected_text_box)  # Add the detected text box
    page.add(translation_box)
    page.add(process_box)
    page.add(error_box)  # Add the error box
    page.add(img)

    # Flag to control continuous listening
    listening = False

    # Function to handle the button click event and trigger the speech recognition and translation
    def on_button_click(e):
        nonlocal listening
        if listening:
            process_box.value = "Stopped Listening"
            listening = False
        else:
            process_box.value = "Listening..."  # Show that we're now listening
            translation_box.value = ""  # Clear previous translation
            detected_text_box.value = ""  # Clear previous detected text
            error_box.value = ""  # Clear previous error messages
            listening = True
            page.update()

            # Continuous listening and translating
            def listen_and_translate():
                while listening:
                    process_box.value = "Listening..."  # Update process box to show listening
                    page.update()

                    text = capture_audio()  # Capture audio from the user
                    if text:
                        # Update process box to show the detected text
                        process_box.value = f"Detected Text: {text}"  # Show the recognized text
                        detected_text_box.value = text  # Display detected text in the detected text box
                        error_box.value = ""  # Clear error box if recognition is successful
                        page.update()

                        try:
                            # Translate the captured text
                            translated_text = translate_text(text, target_language="nl")  # Translate the text
                            translation_box.value = translated_text  # Update the translated text in the translation box
                            process_box.value = f"Recognized Text: {text}"  # Show the detected text in process box
                        except Exception as e:
                            process_box.value = f"Error during translation: {str(e)}"  # Error in translation
                        page.update()  # Refresh the page to reflect the updated values
                    else:
                        # If recognition fails, show error message in the error box
                        error_box.value = "Google Speech Recognition could not understand the audio"  # Error if no text was recognized
                        process_box.value = ""  # Clear process box to avoid confusion
                        page.update()

            # Start a new thread for continuous listening and translating
            listen_and_translate()  # Call the function to start listening and translating

    # Add a button to trigger the speech-to-text translation process
    page.add(
        ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="Klik hier om te beginnen!", size=15),  # Smaller text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(8),
                bgcolor=ft.colors.RED_400,
            ),
            on_click=on_button_click,  # Trigger on button click
        ),
    )


# Run the Flet app
ft.app(main)
