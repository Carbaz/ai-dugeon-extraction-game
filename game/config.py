"""AI Mastered Dungeon Extraction Game Configuration module."""

import os
from logging import getLogger

from dotenv import load_dotenv

from . import prompts
from .composer import compose_pixazo
from .gameplay import Gameplay_Config
from .illustrator import draw_functions
from .interface import Interface_Config
from .storyteller import narrate, set_description_limit


# Environment initialization.
load_dotenv(override=True)

# Load configured draw function.
DRAW_ILLUSTRATOR = os.getenv('DRAW_FUNCTION', 'subnp')
DRAW_FUNCTION = draw_functions.get(DRAW_ILLUSTRATOR)

# Check env if Music generation is enabled.
if os.getenv('MUSIC_GENERATION', 'true').lower() in ['true', '1', 'yes']:
    COMPOSE_FUNCTION = compose_pixazo
else:
    COMPOSE_FUNCTION = None

# Set Storyteller description limit based on prompts configuration.
set_description_limit(prompts.STORYTELLER_LIMIT)

FOOTER_DISCLAIMER = """
<div style='text-align: center; font-size: small;'>
    This game uses generative AI for all its content, including text, images, music,
    and voice.
    Interactions and generated content may be used to train models from various
    providers, such as OpenAI.
</div>
"""

# Configure the game.
GAME_CONFIG = Gameplay_Config(
    draw_func=DRAW_FUNCTION,
    compose_func=COMPOSE_FUNCTION,
    narrate_func=narrate,
    scene_style=prompts.SCENE_STYLE,
    scene_prompt=prompts.SCENE_PROMPT,
    compose_style=prompts.COMPOSE_STYLE,
    compose_prompt=prompts.COMPOSE_PROMPT,
    storyteller_prompt=prompts.STORYTELLER_PROMPT,
    disable_img='images/disabled.jpg',
    error_img='images/machine.jpg',
    error_narrator='NEURAL SINAPSIS ERROR\n\n{ex}\n\nEND OF LINE\n\nRE-SUBMIT_',
    error_composer='NEURAL PERCEPTION ERROR\n\n{ex}\n\nEND OF LINE\n\nRE-SUBMIT_',
    error_illustrator='NEURAL PROJECTION ERROR\n\n{ex}\n\nEND OF LINE\n\nRE-SUBMIT_')

# Configure the interface.
UI_CONFIG = Interface_Config(
    start_img='images/chair.jpg',
    start_ambience='audios/intro_ambience.mp3',
    place_img='images/machine.jpg',
    description_label='Cognitive Projection',
    title_label='The Neural Nexus',
    input_button='Imprint your will',
    input_label='Cognitive Imprint',
    input_command='Awaiting neural imprint…',
    music_toggle_label=('Generate Music (Disable for faster generation)'
                        if COMPOSE_FUNCTION
                        else 'Music Generation disabled on server'),
    music_disabled=not bool(COMPOSE_FUNCTION),
    game_over_field='Game Over',
    game_over_label='Disengage Neural Links',
    footer_disclaimer=FOOTER_DISCLAIMER,
    start_scene=prompts.START_SCENE)


# Instantiate logger.
_logger = getLogger(__name__)

# Log illustrator configuration.
if DRAW_FUNCTION:
    _logger.info(f'ILLUSTRATOR USED: {DRAW_ILLUSTRATOR.capitalize()}')

# Log composer configuration.
_logger.info(f'MUSIC GENERATION {"ENABLED" if COMPOSE_FUNCTION else "DISABLED"}')

# Log scene prompt length calculation.
if (max_image_prompt := len(prompts.SCENE_PROMPT)
    + len(prompts.SCENE_STYLE) + prompts.STORYTELLER_LIMIT) > 1024:
    _logger.warning(f'ESTIMATED SCENE PROMPT MAX SIZE: {max_image_prompt}')
else:
    _logger.info(f'ESTIMATED SCENE PROMPT MAX SIZE: {max_image_prompt}')
