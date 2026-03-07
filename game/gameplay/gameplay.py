"""AI Mastered Dungeon Extraction Game gameplay module."""

import asyncio
from logging import getLogger
from typing import Callable, NamedTuple


# Define gameplay's configuration class.
class Gameplay_Config(NamedTuple):
    """Gradio interface configuration class."""
    draw_func: Callable
    compose_func: Callable
    narrate_func: Callable
    scene_style: str
    scene_prompt: str
    compose_style: str
    compose_prompt: str
    storyteller_prompt: str
    disable_img: str
    error_img: str
    error_narrator: str
    error_composer: str
    error_illustrator: str


# Define Game's functions.

def get_gameplay_function(config: Gameplay_Config):
    """Return a pre-configured turn gameplay function."""
    async def gameplay_function(message, history):
        """Generate Game Master's response and draw the scene image."""
        # Request narration.
        _logger.info(f'NARRATING SCENE...')
        try:
            response = config.narrate_func(message, history, config.storyteller_prompt)
        except Exception as ex:
            scene = config.error_img
            response = config.error_narrator.format(ex=ex)
            _logger.error(f'ERROR NARRATING SCENE: {ex}\n{message}\n{history}')
            return scene, None, response, history, message
        # Update history.
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response.model_dump_json()})

        # Prepare drawing task
        async def draw_scene():
            if not config.draw_func:
                _logger.info(f'DRAWING DISABLED...')
                return config.disable_img

            _logger.info(f'DRAWING SCENE...')
            try:
                scene_data = {'scene_description': response.scene_description,
                              'scene_style': config.scene_style}
                scene_prompt = config.scene_prompt.format(**scene_data)
                _logger.info(f'PROMPT BODY IS: \n\n{scene_prompt}\n')
                _logger.info(f'PROMPT LENGTH IS: {len(scene_prompt)}')
                return await asyncio.to_thread(config.draw_func, scene_prompt)
            except Exception as ex:
                _logger.warning(f'ERROR DRAWING SCENE: {ex}')
                raise

        # Prepare composing task
        async def compose_scene():
            if not config.compose_func:
                _logger.info(f'COMPOSING DISABLED...')
                return None

            _logger.info(f'COMPOSING SCENE...')
            try:
                compose_data = {'scene_description': response.scene_description,
                                'compose_style': config.compose_style}
                compose_prompt = config.compose_prompt.format(**compose_data)
                _logger.info(f'COMPOSE PROMPT BODY IS: \n\n{compose_prompt}\n')
                _logger.info(f'COMPOSE PROMPT LENGTH IS: {len(compose_prompt)}')
                return await asyncio.to_thread(config.compose_func, compose_prompt)
            except Exception as ex:
                _logger.warning(f'ERROR COMPOSING SCENE: {ex}')
                return None

        # Run both tasks concurrently
        try:
            scene, ambience = await asyncio.gather(draw_scene(), compose_scene())
        except Exception as ex:
            scene = config.error_img
            response = config.error_illustrator.format(ex=ex)
            _logger.error(f'ERROR IN SCENE OPERATIONS: {ex}')
            return scene, None, response, history, ''

        return scene, ambience, response, history, ''
    return gameplay_function


_logger = getLogger(__name__)
