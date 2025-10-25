import requests
import os

def bentoml_ttx_get_audio(text: str, lang: str, api_url: str, headers=None) -> bytes:
    """
    Sends a JSON payload with 'text' and 'lang' to a BentoML TTS endpoint
    and returns the binary audio data.

    Parameters:
    - text: The input text to synthesize.
    - lang: Language code (e.g., 'en').
    - api_url: The BentoML endpoint URL.
    - headers: Optional headers (e.g., for authorization or content-type).

    Returns:
    - Binary audio data (bytes) if successful.
    - Raises an exception if the request fails.
    """
    payload = {
        "text": text,
        "lang": lang
    }

    if headers is None:
        headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.content

def save_audio_to_folder(audio_bytes: bytes, folder: str, filename: str):
    """
    Saves binary audio data to a specified folder with the given filename.

    Parameters:
    - audio_bytes: The binary audio data.
    - folder: Destination folder path.
    - filename: Name of the audio file (e.g., 'output.wav').
    """
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    print(f"✅ Audio saved to {path}")