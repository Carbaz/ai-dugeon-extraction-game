"""AI Mastered Dungeon Extraction Game scenes illustrator using Pixazo."""

import os

import requests
from dotenv import load_dotenv

from tools import fetch_image


# Environment initialization.
load_dotenv(override=True)

PIXAZO_URL = "https://gateway.pixazo.ai"
PIXAZO_API_KEY = os.getenv('PIXAZO_API_KEY')

# Choose model to use, comment out the others:
# PIXAZO_MODEL = "getImage/v1/getSDXLImage"  # Stable Diffusion XL.
PIXAZO_MODEL = "flux-1-schnell/v1/getData"  # Flux.

PIXAZO_API_URL = f"{PIXAZO_URL}/{PIXAZO_MODEL}"

NEGATIVE_PROMPT = """
Low-quality, blurry image.
Avoid abstract or cartoonish styles, harsh lighting, and unnatural colors.
"""

HEADERS = {"Content-Type": "application/json",
           "Cache-Control": "no-cache",
           "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY}


def get_data(prompt, negative, size):
    """Return the data payload for a Pixazo image generation request."""
    return {"prompt": prompt, "negative_prompt": negative,
            "num_steps": 20, "guidance_scale": 5, "seed": 40,
            "width": size[0], "height": size[1]}


def get_url(message):
    """Extract the image URL from the response."""
    if not (image_url :=
            message.get("imageUrl")
            or message.get("image_url")
            or message.get("output")):
        raise ValueError("No image URL found in the response.")
    return image_url


def draw(prompt, negative=NEGATIVE_PROMPT, size=(1024, 1024)):
    """Generate an image based on the prompt."""
    data = get_data(prompt, negative, size)
    response = requests.post(PIXAZO_API_URL, headers=HEADERS, json=data, timeout=30)
    response.raise_for_status()
    response_data = response.json()
    print(f'MESSAGE: {response_data}')
    # Extract the image URL from the response.
    image_url = get_url(response_data)
    # Fetch the image from the URL.
    return fetch_image(image_url)


draw("Ducks conquering a castle on a desert on a colorful cinematographic"
     "and photorealistic style")
