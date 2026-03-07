"""AI Mastered Dungeon Extraction Game scenes illustrator using Pixazo."""

import os
import time
from io import BytesIO
from logging import getLogger

import requests
from dotenv import load_dotenv


# Instantiate logger.
_logger = getLogger(__name__)

# Environment initialization.
load_dotenv(override=True)

PIXAZO_URL = "https://gateway.pixazo.ai"
PIXAZO_API_KEY = os.getenv('PIXAZO_API_KEY')

PIXAZO_MODEL = "tracks/v1/generate"
PIXAZO_TRACKS = "tracks/v1/status"
_logger.info(f'ILLUSTRATOR MODEL: {PIXAZO_MODEL}')

PIXAZO_API_URL = f"{PIXAZO_URL}/{PIXAZO_MODEL}"
PIXAZO_TRACKS_URL = f"{PIXAZO_URL}/{PIXAZO_TRACKS}"

HEADERS = {"Content-Type": "application/json",
           "Cache-Control": "no-cache",
           "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY}


def get_data(prompt, lyrics=""):
    """Return the data payload for a Pixazo music generation request."""
    return {"prompt": prompt, "lyrics": lyrics,
            "instrumental": not lyrics, "bpm": 140, "duration": 120,
            "infer_steps": 25, "guidance_scale": 7.5, "seed": 42}


def get_composition_url(task_id, max_retries=3):
    """Retrieve the composition URL, retrying until ready or limit reached."""
    data = {"task_id": task_id}
    for _ in range(max_retries):
        _logger.info(f'CHECKING STATUS FOR TASK ID: {task_id}')
        # print(f'CHECKING STATUS FOR TASK ID: {task_id}')
        response = requests.post(PIXAZO_TRACKS_URL, json=data, headers=HEADERS)
        response.raise_for_status()
        response_data = response.json()
        status = response_data.get("status")
        if status == "completed":
            audio_urls = response_data["result"].get("audio_urls")
            _logger.info(f"... Task is completed, audio at: {audio_urls}")
            # print(f"... Task is completed, audio at: {audio_urls}")
            if audio_urls:
                return audio_urls[0]  # Return the first URL from the list
            else:
                raise ValueError("No audio URLs found in the response.")
        elif status == "processing":
            _logger.info(f"... Task is still processing: {response_data.get('stage')}")
            # print(f"Task is still processing: {response_data.get('stage')}")
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            raise ValueError(f"Unexpected status: {status}")
    raise TimeoutError(f"Exceeded maximum retries ({max_retries}) for task: {task_id}")


def fetch_composition(url):
    """Fetch the composition from the URL and return it as an in-memory object."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    audio_content = response.content
    # Store the audio content in an in-memory BytesIO object
    audio_file = BytesIO(audio_content)
    audio_file.name = "composition.mp3"  # Set a name for the in-memory file
    _logger.info("Audio track fetched and stored in memory.")
    # print("Audio track fetched and stored in memory.")
    # Return the in-memory file object
    return audio_file


def compose(prompt):
    """Generate a music track based on the prompt."""
    data = get_data(prompt)
    response = requests.post(PIXAZO_API_URL, json=data, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response_data = response.json()
    _logger.info(f'COMPOSE TASK: {response_data}')
    # print(f'MESSAGE: {response_data}')
    task_id = response_data.get("task_id")
    # Retrieve the composition_url, waiting if necessary.
    composition_url = get_composition_url(task_id)
    # Fetch the composition from the URL and return.
    return fetch_composition(composition_url)


# ## ######################################################

def play_on_jupyter(composition):
    """Play the composition in a Jupyter notebook."""
    from IPython.display import Audio
    audio_file = compose(composition)
    return Audio(audio_file.read(), autoplay=True)


test_prompt = """
A cinematic Hans Zimmer style orchestral piece, building tension with heavy percussion
and brass, epic atmosphere"""
