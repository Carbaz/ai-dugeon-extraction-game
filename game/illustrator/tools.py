"""Image tools for the AI Mastered Dungeon Extraction Game illustrators."""

from io import BytesIO
from logging import getLogger

import requests
from PIL import Image


def fetch_image(url):
    """Fetch an image from the given URL and return it as a PIL Image object."""
    _logger.info(f'FETCHING IMAGE FROM URL: {url}')
    image_response = requests.get(url, stream=True, timeout=5)
    image_response.raise_for_status()
    _logger.info(f'IMAGE FETCHED SUCCESSFULLY')
    return Image.open(BytesIO(image_response.content))


_logger = getLogger(__name__)
