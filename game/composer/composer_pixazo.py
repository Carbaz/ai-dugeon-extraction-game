"""AI Mastered Dungeon Extraction Game ambience composer using Pixazo."""

import os
import time
from io import BytesIO
from logging import getLogger

import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.utils import ratio_to_db


# Instantiate logger.
_logger = getLogger(__name__)

# Environment initialization.
load_dotenv(override=True)

PIXAZO_URL = "https://gateway.pixazo.ai"
PIXAZO_API_KEY = os.getenv('PIXAZO_API_KEY')

PIXAZO_MODEL = "tracks/v1/generate"
_logger.info(f'COMPOSER MODEL: {PIXAZO_MODEL}')

PIXAZO_API_URL = f"{PIXAZO_URL}/{PIXAZO_MODEL}"

HEADERS = {"Content-Type": "application/json",
           "Cache-Control": "no-cache",
           "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY}


def get_data(prompt, lyrics=""):
    """Return the data payload for a Pixazo music generation request."""
    return {"prompt": prompt, "lyrics": lyrics, "instrumental": not lyrics,
            # TODO: Instrumental can actually be without lyrics.
            "bpm": 140, "duration": 120, "infer_steps": 25,
            "guidance_scale": 7.5, "seed": 42}


def get_composition_url(response_data, max_retries=6, retry_delay=10):
    """Retrieve the composition URL, retrying until ready or limit reached."""
    request_id = response_data.get("request_id")
    polling_url = response_data.get("polling_url")
    for turn in range(max_retries):
        _logger.info(f'CHECKING STATUS FOR REQUEST ID: {request_id}'
                     f' ({turn + 1}/{max_retries})')
        # print(f'CHECKING STATUS FOR REQUEST ID: {request_id}'
        #       f' ({turn + 1}/{max_retries})')
        response = requests.get(polling_url, headers=HEADERS)
        response.raise_for_status()
        response_data = response.json()
        _logger.info(f'POLLING RESPONSE: {response_data}')
        # print(f'POLLING RESPONSE: {response_data}')
        status = response_data.get("status")
        if status.upper() == "COMPLETED":
            audio_urls = response_data["output"].get("media_url")
            _logger.info(f"... TASK IS COMPLETED, AUDIO AT: {audio_urls}")
            # print(f"... Task is completed, audio at: {audio_urls}")
            if audio_urls:
                return audio_urls[0]  # Return the first URL from the list
            else:
                raise ValueError("No audio URLs found in the response.")
        elif status.upper() == "FAILED" or status.upper() == "ERROR":
            _logger.info(f"... TASK HAS FAILED: {response_data.get('error')}")
            # print(f"... Task has failed: {response_data.get('error')}")
            raise ValueError(f"Task has failed. {response_data.get('error')}")
        elif status.upper() == "QUEUED":
            _logger.info("... TASK IS STILL QUEUED")
            # print("... Task is still queued")
            time.sleep(retry_delay)  # Wait for retry_delay seconds before retrying
        elif status.upper() == "PROCESSING":
            _logger.info("... TASK IS STILL PROCESSING")
            # print("... Task is still processing")
            time.sleep(retry_delay)  # Wait for retry_delay seconds before retrying
        else:
            raise ValueError(f"Unexpected status: {status}")
    raise TimeoutError(f"Exceeded maxi retries ({max_retries}) for task: {request_id}")


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


def compose(prompt, lyrics="[instrumental]"):
    """Generate a music track based on the prompt."""
    data = get_data(prompt, lyrics)
    # print(f'COMPOSE REQUEST: {data}')
    response = requests.post(PIXAZO_API_URL, json=data, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response_data = response.json()
    _logger.info(f'COMPOSE TASK: {response_data}')
    # print(f'COMPOSE TASK: {response_data}')
    # Retrieve the composition_url, waiting if necessary.
    composition_url = get_composition_url(response_data)
    # Fetch the composition from the URL and return.
    return composition_url


# ## ######################################################

def play_on_jupyter(audio_file):
    """Play the audio file in a Jupyter notebook."""
    from IPython.display import Audio
    return Audio(audio_file.read(), autoplay=True)


def compose_on_jupyter(composition, lyrics="[instrumental]", volume=1):
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
building tension and grandeur throughout the piece.
Create a dramatic and emotional musical journey that supports the narrative of the
lyrics, with distinct sections for verses, chorus, and bridges that showcase the dynamic
range of the orchestral arrangement.
Voices should be grave ones, mix a male grave chorus voices and a female main vocal for
the chorus parts with a sense of awakening and creation, as if the music is emerging
from darkness.
"""

# Original lyrics written by GitHub Copilot (Claude Haiku 4.5)
# Theme: Awakening, creation, light emerging from darkness, building worlds
test_lyrics = """
[Intro - orchestral]

[Verse 1]
From silence deep, the first light breaks
The ancient stone begins to wake
The void retreats, the void recedes
A world is born of primal seeds

[Verse 2]
The mountains rise from sleeping earth
Creation stirs, the moment of rebirth
Across the lands, the rivers flow
A symphony of all below

[Pre-Chorus]
Can you feel it?
The awakening call

[Chorus]
Rise, rise, the world unfolds
Stories waiting to be told
From the darkness, light takes hold
A new beginning, brave and bold

[Verse 3]
The winds are singing ancient songs
The earth belongs, the world belongs
Each breath of life, each beating heart
This is the moment, the brand new start

[Bridge]
We are the watchers of the dawn
We are the dreamers carrying on
With every step, with every sound
We build the world we've found

[Chorus]
Rise, rise, the world unfolds
Stories waiting to be told
From the darkness, light takes hold
A new beginning, brave and bold

[Outro - fading]
"""
