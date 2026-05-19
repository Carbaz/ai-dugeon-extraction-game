"""AI Mastered Dungeon Extraction Game scenes narrator using Google's Gemini."""

import wave
from io import BytesIO
from logging import getLogger

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Instantiate logger.
_logger = getLogger(__name__)

# Environment initialization.
load_dotenv(override=True)

# Define globals.
MODEL = "gemini-2.5-flash-preview-tts"
VOICE = "Charon"
_logger.info(f'NARRATOR MODEL: {MODEL}')
_logger.info(f'NARRATOR VOICE: {VOICE}')

# Client instantiation.
CLIENT = genai.Client()


def save_wave_file(file, audio_data):
    """Save audio data to a file."""
    with open(file, "wb") as wf:
        wf.write(audio_data.read())
    audio_data.seek(0)


def save_wave_file_from_PCM(file, pcm, channels=1, sample_width=2, rate=24000):
    """Save raw PCM audio data as a WAV file or BytesIO."""
    with wave.open(file, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    # If the file is a BytesIO object, reset its position to the beginning after writing.
    if isinstance(file, BytesIO):
        file.seek(0)


def create_wav_from_pcm(audio_content, channels=1, sample_width=2, rate=24000):
    """Create a properly formatted WAV file in memory from PCM audio data."""
    audio_file = BytesIO()
    save_wave_file_from_PCM(audio_file, audio_content, channels, sample_width, rate)
    audio_file.name = "narration.wav"
    return audio_file


def narrate(prompt, client=CLIENT, model=MODEL, voice=VOICE):
    """Generate audio content using Gemini's TTS capabilities."""
    print(f'Generating audio for prompt: "{prompt}"')
    response = client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(temperature=1, response_modalities=["audio"],
            speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)))))
    audio_content = response.candidates[0].content.parts[0].inline_data.data
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
    save_wave_file('out_gemini.wav', narration_audio)
    return narration_audio


test_prompt = """
In a hole in the ground there lived a hobbit,
and this is the story of how he found himself in an adventure.
"""
