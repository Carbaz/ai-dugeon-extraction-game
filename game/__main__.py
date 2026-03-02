"""AI Mastered Dungeon Extraction Game main entrypoint module."""

from logging import getLogger

from .config import GAME_CONFIG, UI_CONFIG
from .gameplay import get_gameplay_function
from .interface import get_interface


_logger = getLogger(__name__)


def main(*, local: bool = False):
    """Launch the game. Set local=True for browser auto-open."""
    _logger.info('STARTING GAME...')
    gameplay_function = get_gameplay_function(GAME_CONFIG)
    interface = get_interface(gameplay_function, UI_CONFIG)
    interface.launch(inbrowser=local, inline=False)


if __name__ == '__main__':
    main(local=True)
