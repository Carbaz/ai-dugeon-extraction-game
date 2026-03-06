"""Entrypoint wrapper for Hugging Face Spaces. Delegates to game/__main__.py."""

from game.__main__ import main


# HBD: We assign the 'app' to 'demo' to allow watch autoreload:
# 'demo' is required to be defined at the global scope for reload to work in Gradio.
# Initial warnings may appear at launch with 'gradio app.py' because 'demo' will not
# exists until the app service ends inside main, but it will do when reload requires it,
# once the service has been stopped.
demo = main()
