"""AI Mastered Dungeon Extraction Game gameplay module."""

import asyncio
from logging import getLogger
from typing import Callable, NamedTuple, Optional


# Define gameplay's configuration class.
class Gameplay_Config(NamedTuple):
    """Gradio interface configuration class."""
    draw_func: Callable
    weave_func: Callable
    narrate_func: Optional[Callable]
    compose_func: Optional[Callable]
    scene_style: str
    scene_prompt: str
    compose_style: str
    compose_prompt: str
    storyweaver_prompt: str
    disable_img: str
    error_img: str
    error_weaver: str
    error_composer: str
    error_illustrator: str


# Define Game's functions.

def get_gameplay_function(config: Gameplay_Config):
    """Return a pre-configured turn gameplay function."""
    async def gameplay_function(message, history, music_enabled,
                                narration_enabled, language):
        """Generate Game Master's response and draw the scene image."""
        # RETURNS: scene, ambience, narration, response, history, input
        # Request weaving.
        _logger.info(f'WEAVING SCENE...')
        try:
            response = config.weave_func(message, history, config.storyweaver_prompt)
        except Exception as ex:
            scene = config.error_img
            response = config.error_weaver.format(ex=ex)
            _logger.error(f'ERROR WEAVING SCENE: {ex}\n{message}\n{history}')
            return scene, None, None, response, history, message
        # Update history.
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response.model_dump_json()})

        # Prepare drawing task.
        async def draw_scene():
            if not config.draw_func:
                _logger.info(f'DRAWING DISABLED...')
                return config.disable_img

            _logger.info(f'DRAWING SCENE...')
            try:
                scene_data = {'scene_description': response.scene_description,
                              'scene_style': config.scene_style}
                scene_prompt = config.scene_prompt.format(**scene_data)
                _logger.info(f'DRAW PROMPT LENGTH IS: {len(scene_prompt)}')
                _logger.info(f'DRAW PROMPT BODY IS: \n\n{scene_prompt}\n')
                return await asyncio.to_thread(config.draw_func, scene_prompt)
            except Exception as ex:
                _logger.warning(f'ERROR DRAWING SCENE: {ex}')
                raise

        # Prepare composing task.
        async def compose_scene():
            if not config.compose_func or not music_enabled:
                _logger.info(f'COMPOSING DISABLED...')
                return None

            _logger.info(f'COMPOSING SCENE...')
            try:
                compose_data = {'scene_description': response.scene_description,
                                'compose_style': config.compose_style}
                compose_prompt = config.compose_prompt.format(**compose_data)
                _logger.info(f'COMPOSE PROMPT LENGTH IS: {len(compose_prompt)}')
                _logger.info(f'COMPOSE PROMPT BODY IS: \n\n{compose_prompt}\n')
                return await asyncio.to_thread(config.compose_func, compose_prompt)
            except Exception as ex:
                _logger.warning(f'ERROR COMPOSING SCENE: {ex}')
                return None

        # Prepare narration task.
        async def narrate_scene():
            if not config.narrate_func or not narration_enabled:
                _logger.info(f'NARRATION DISABLED...')
                return None

            _logger.info(f'NARRATING SCENE...')
            try:
                narrate_prompt = response.scene_description
                _logger.info(f'NARRATE LANGUAGE IS: {language}')
                _logger.info(f'NARRATE PROMPT LENGTH IS: {len(narrate_prompt)}')
                _logger.info(f'NARRATE PROMPT BODY IS: \n\n{narrate_prompt}\n')
                audio = await asyncio.to_thread(config.narrate_func, narrate_prompt,
                                                language=language)
                audio.seek(0)
                return audio.read()
            except Exception as ex:
                _logger.warning(f'ERROR NARRATING SCENE: {ex}')
                return None

        # Run all tasks concurrently
        try:
            scene, ambience, narration = await asyncio.gather(
                draw_scene(), compose_scene(), narrate_scene())
        except Exception as ex:
            scene = config.error_img
            response = config.error_illustrator.format(ex=ex)
            _logger.error(f'ERROR IN SCENE OPERATIONS: {ex}')
            return scene, None, None, response, history, ''
        _logger.info(f'ALL SCENE OPERATIONS COMPLETED.')
        return scene, ambience, narration, response, history, ''
    return gameplay_function


_logger = getLogger(__name__)
