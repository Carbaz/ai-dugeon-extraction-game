"""AI Mastered Dungeon Extraction Game scenes illustrator using subnp."""

from json import loads

import requests

from tools import fetch_image


SUBNP_API_URL = "https://t2i.mcpcore.xyz/generate"
# SUBNP_API_URL = "https://subnp.com/api/free/generate"  # Probably wrapping the other.

# Choose model to use, comment out the others:
MODEL = "magic"  # By: MagicStudio
# MODEL = "wan"  # By: Qwen.ai
# MODEL = "turbo"  # By: MitraAi
# MODEL = "flux"  # By: MitraAi
# MODEL = "flux-schnell"  # By: MitraAi

HEADERS = {"Content-Type": "application/json", "Cache-Control": "no-cache"}


def handle_stream(response):
    """Handle the streaming response from the API."""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            # Remove the 'data: ' prefix.
            line = line.replace("data: ", "", 1)
            message = loads(line)
            # Handle different statuses.
            if "imageUrl" in message:
                print("Image URL:", message["imageUrl"])
                return message["imageUrl"]
            elif message.get("status") == "processing":
                print(f"... {message.get('message')}")
            elif message.get("status") == "error":
                print(f"Error: {message.get('message')}")
                raise Exception(f"Error: {message.get('message')}")
            elif message.get("status") == "complete":
                print("Complete but no image")
                raise ValueError("No image URL found in the response.")
            else:
                print(f"Unknown line: {message}")
    raise ValueError("No image URL found in the response.")


# Function definition.
def draw(prompt, size=(1024, 1024), model=MODEL):
    """Generate an image based on the prompt."""
    response = requests.post(url=SUBNP_API_URL, stream=True, timeout=30,
                             json={"prompt": prompt, "model": model},
                             headers={"Content-Type": "application/json",
                                      "Cache-Control": "no-cache"})
    response.raise_for_status()
    # Extract the image URL from the response.
    image_url = handle_stream(response)
    # Fetch the image from the URL and return.
    return fetch_image(image_url)
