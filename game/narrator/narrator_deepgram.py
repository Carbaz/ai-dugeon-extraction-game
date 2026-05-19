"""AI Mastered Dungeon Extraction Game scenes narrator using Deepgram."""

import os
from io import BytesIO
from logging import getLogger

from deepgram import DeepgramClient
from dotenv import load_dotenv


# Instantiate logger.
_logger = getLogger(__name__)

# Environment initialization.
load_dotenv(override=True)
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY', '')

# Define globals.
MODEL = "aura-2"
VOICE = "jupiter"
LANGUAGE = 'en'
_logger.info(f'NARRATOR MODEL: {MODEL}')
_logger.info(f'NARRATOR VOICE: {VOICE}')
_logger.info(f'NARRATOR LANGUAGE: {LANGUAGE}')

REQUEST_TEMPLATE = "{model}-{voice}-{language}"

# Client instantiation.
CLIENT = DeepgramClient(api_key=DEEPGRAM_API_KEY)


def save_wave_file(file, audio_data):
    """Save audio data to a file."""
    with open(file, "wb") as wf:
        wf.write(audio_data.read())
    audio_data.seek(0)


def create_wav_from_pcm(audio_data):
    """Create a properly formatted WAV file in memory from PCM audio data iterable."""
    audio_file = BytesIO()
    for chunk in audio_data:
        audio_file.write(chunk)
    audio_file.seek(0)
    audio_file.name = "narration.wav"
    return audio_file


def narrate(prompt, client=CLIENT, model=MODEL, voice=VOICE, language=LANGUAGE):
    """Generate audio content using Gemini's TTS capabilities."""
    print(f'Generating audio for prompt: "{prompt}"')
    audio_content = client.speak.v1.audio.generate(
        text=prompt, model=REQUEST_TEMPLATE.format(
            model=model, voice=voice, language=language))
    audio_file = create_wav_from_pcm(audio_content)
    return audio_file


# ## ######################################################

def play_on_jupyter(narration_audio):
    """Play the narration in a Jupyter notebook."""
    from IPython.display import Audio
    return Audio(narration_audio.read(), autoplay=True)


def narrate_on_jupyter(text):
    """Generate the narration in a Jupyter notebook."""
    print(f"Generating narration for:\n{text}")
    narration_audio = narrate(text)
    save_wave_file('out_deepgram.wav', narration_audio)
    return narration_audio


test_prompt = """
In a hole in the ground there lived a hobbit,
and this is the story of how he found himself in an adventure.
"""
