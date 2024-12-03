import requests

# DeepL API Configuration
DEEPL_API_KEY = 'a7ad26a8-8d22-4d81-a943-b78f19f8ed98:fx'
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'


def translate_with_deepl(text, source_lang="NL", target_lang="EN"):
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang,
    }
    response = requests.post(DEEPL_URL, data=params)
    if response.status_code == 200:
        return response.json()['translations'][0]['text']
    else:
        raise Exception(f"DeepL API Error: {response.status_code} - {response.text}")
