"""Image tools for the AI Mastered Dungeon Extraction Game illustrators."""

import requests

from PIL import Image
from io import BytesIO


def fetch_image(url):
    """Fetch an image from the given URL and return it as a PIL Image object."""
    image_response = requests.get(url, stream=True, timeout=5)
    image_response.raise_for_status()
    return Image.open(BytesIO(image_response.content))
