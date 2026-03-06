"""AI Mastered Dungeon Extraction Game scenes illustrator using Pixazo."""

import os
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image


# Environment initialization.
load_dotenv(override=True)

PIXAZO_URL = "https://gateway.pixazo.ai"
PIXAZO_API_KEY = os.getenv('PIXAZO_API_KEY')

# Choose model to use, comment out the others:

# Stable Diffusion XL model, more consistent and faster.
PIXAZO_MODEL = "getImage/v1/getSDXLImage"

# Stable Diffusion 3.5 model, more detailed but slower.
# PIXAZO_MODEL = "sd3-5/v1/r-sd-3-5-large"

# Flux model, more artistic and faster but less consistent.
# PIXAZO_MODEL = "flux-1-schnell/v1/getData"

NEGATIVE_PROMPT = """
Low-quality, blurry image.
Avoid abstract or cartoonish styles, harsh lighting, and unnatural colors.
"""

HEADERS = {"Content-Type": "application/json", "Cache-Control": "no-cache",
           "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY}


def SD_data(prompt, size):
    """Return the data payload for a Pixazo SDXL image generation request."""
    return {
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,
        "width": size[0],
        "height": size[1],
        "num_steps": 20,
        "guidance_scale": 5,
        "seed": 40}


# Function definition.
def draw(prompt, size=(1024, 1024)):
    """Generate an image based on the prompt."""
    data = SD_data(prompt, size)
    response = requests.post(f"{PIXAZO_URL}/{PIXAZO_MODEL}", headers=HEADERS,
                             json=data, timeout=30)
    response_data = response.json()
    print(response_data)

    # Extract the image URL from the response.
    if not (image_url :=
            response_data.get("imageUrl")
            or response_data.get("image_url")
            or response_data.get("output")):
        raise ValueError("No image URL found in the response.")

    # Fetch the image from the URL.
    image_response = requests.get(image_url, stream=True)
    image_response.raise_for_status()

    # Load the image into a PIL Image object.
    image = Image.open(BytesIO(image_response.content))
    return image
