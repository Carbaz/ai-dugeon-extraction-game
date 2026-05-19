"""AI Mastered Dungeon Extraction Game narrator package."""

from .narrator_deepgram import narrate as narrate_deepgram
from .narrator_gemini import narrate as narrate_gemini


__all__ = ['narrate_deepgram', 'narrate_gemini']
