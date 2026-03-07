"""AI Mastered Dungeon Extraction Game scenes illustrator package."""

from .illustrator_dalle_2 import draw as draw_dalle_2
from .illustrator_dalle_3 import draw as draw_dalle_3
from .illustrator_gemini import draw as draw_gemini
from .illustrator_gpt import draw as draw_gpt
from .illustrator_grok import draw as draw_grok
from .illustrator_grok import draw_x as draw_grok_x
from .illustrator_pixazo import draw as draw_pixazo
from .illustrator_subnp import draw as draw_subnp


__all__ = ['draw_dalle_2', 'draw_dalle_3', 'draw_gemini', 'draw_gpt',
           'draw_grok', 'draw_grok_x', 'draw_pixazo', 'draw_subnp']

draw_functions = {
    'dalle_2': draw_dalle_2,
    'dalle_3': draw_dalle_3,
    'gemini': draw_gemini,
    'gpt': draw_gpt,
    'grok': draw_grok,
    'grok_x': draw_grok_x,
    'pixazo': draw_pixazo,
    'subnp': draw_subnp
}
