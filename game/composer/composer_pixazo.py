"""AI Mastered Dungeon Extraction Game ambience composer using Pixazo."""

import os
import time
from io import BytesIO
from logging import getLogger

import requests
from dotenv import load_dotenv
from pydub import AudioSegment


# Instantiate logger.
_logger = getLogger(__name__)

# Environment initialization.
load_dotenv(override=True)

PIXAZO_URL = "https://gateway.pixazo.ai"
PIXAZO_API_KEY = os.getenv('PIXAZO_API_KEY')

PIXAZO_MODEL = "tracks/v1/generate"
PIXAZO_TRACKS = "tracks/v1/status"
_logger.info(f'COMPOSER MODEL: {PIXAZO_MODEL}')

PIXAZO_API_URL = f"{PIXAZO_URL}/{PIXAZO_MODEL}"
PIXAZO_TRACKS_URL = f"{PIXAZO_URL}/{PIXAZO_TRACKS}"

HEADERS = {"Content-Type": "application/json",
           "Cache-Control": "no-cache",
           "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY}


def get_data(prompt, lyrics=""):
    """Return the data payload for a Pixazo music generation request."""
    return {"prompt": prompt, "lyrics": lyrics, "instrumental": not lyrics,
            # TODO: Instrumental can actually be without lyrics.
            "bpm": 140, "duration": 120, "infer_steps": 25,
            "guidance_scale": 7.5, "seed": 42}


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


def fetch_composition(url, volume=1):
    """Fetch composition, adjust volume and return as an in-memory object.

    Volume: 0.5 = 50% volume.
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    audio_content = response.content
    # Load audio from bytes
    audio = AudioSegment.from_mp3(BytesIO(audio_content))
    # Apply gain adjustment based on volume ratio
    adjusted_audio = audio.apply_gain(ratio_to_db(volume))
    # Export to bytes and store the audio content in an in-memory BytesIO object
    audio_file = BytesIO(adjusted_audio.export(format="mp3").read())
    audio_file.name = "composition.mp3"
    _logger.info(f"Track fetched, volume adjusted to {volume} and stored in memory.")
    return audio_file


def compose(prompt, lyrics=""):
    """Generate a music track based on the prompt."""
    data = get_data(prompt, lyrics)
    print(f'COMPOSE REQUEST: {data}')
    response = requests.post(PIXAZO_API_URL, json=data, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response_data = response.json()
    _logger.info(f'COMPOSE TASK: {response_data}')
    # print(f'MESSAGE: {response_data}')
    task_id = response_data.get("task_id")
    # Retrieve the composition_url, waiting if necessary.
    composition_url = get_composition_url(task_id)
    # Fetch the composition from the URL and return.
    return composition_url


# ## ######################################################

def play_on_jupyter(audio_file):
    """Play the audio file in a Jupyter notebook."""
    from IPython.display import Audio
    return Audio(audio_file.read(), autoplay=True)


def compose_on_jupyter(composition, lyrics="", volume=1):
    """Generate the composition in a Jupyter notebook."""
    print(f"Generating composition for:\n{composition}\nWith lyrics:\n{lyrics}")
    print(f"Generated at: {(composition_url := compose(composition, lyrics))}")
    audio_file = fetch_composition(composition_url, volume=volume)
    return audio_file


test_style = """
blend of epic orchestral elements, featuring dramatic percussion,
sweeping strings, and powerful brass, designed to evoke tension and grandeur"""

test_prompt = f"""
A cinematic {test_style} style atmosphere.
The composition should feature heavy percussion, powerful brass, and sweeping strings,
building tension and grandeur.
The piece must be perfectly loopable, with seamless transitions from the end back to
the beginning, ensuring no audible cuts or breaks. Under no circumstances should the
loop rely on muted or faded sections at the start or end; the transitions must be
entirely natural, with the melodic and rhythmic flow fully supporting the loop.
Additionally, there must not be an end crescendo, final note, or any element that
denotes the conclusion of the piece. The loop reproduction must feel continuous,
with no noticeable start or end moments.
"""

test_lyrics = (
    "The world was young, the mountains green, No stain yet on the Moon was seen, "
    "No words were laid on stream or stone, When Durin woke and walked alone.")
