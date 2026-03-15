"""AI Mastered Dungeon Extraction Game Gradio interface module."""

import asyncio
from logging import getLogger
from typing import NamedTuple

import gradio as gr


# Define interface's configuration class.
class Interface_Config(NamedTuple):
    """Gradio interface configuration class."""
    start_img: str
    start_ambience: str
    place_img: str
    description_label: str
    title_label: str
    input_button: str
    input_label: str
    input_command: str
    game_over_field: str
    game_over_label: str
    start_scene: str


# Define game's interface.
def get_interface(submit_function, config: Interface_Config):
    """Create a game interface service."""
    with gr.Blocks(title=config.title_label) as ui:
        # Title.
        gr.Markdown(config.title_label)
        # Hidden state for history.
        history_state = gr.State([])
        # Scene's image.
        scene_image = gr.Image(value=config.start_img, placeholder=config.place_img,
                               label="Scene", type="pil", show_label=False)
        # Scene's ambience.
        # ambience_audio = None
        ambience_audio = gr.Audio(label="Ambience", show_label=False, sources=[],
                                  loop=True, interactive=False, autoplay=False,
                                  value=config.start_ambience, format="mp3",
                                  waveform_options={"waveform_progress_color":
                                                    "#3571C0"})
        # Scene's description.
        description_box = gr.Textbox(label=config.description_label, buttons=["copy"],
                                     value=config.start_scene, interactive=False)
        # Player's command.
        user_input = gr.Textbox(label=config.input_label,
                                placeholder=config.input_command)
        # Submit button.
        submit_btn = gr.Button(config.input_button)

        # Define Game Over control.
        def _reset_game():
            """Return Initial values for game restart."""
            return (config.start_img, config.start_scene, [], '',
                    gr.update(interactive=True),
                    gr.update(value=config.input_button))

        def _game_over(scene, response):
            """Return Game Over values, blocking input field."""
            return (scene, response, [], config.game_over_field,
                    gr.update(interactive=False),
                    gr.update(value=config.game_over_label))

        def game_over_wrap(message, history, button_label):
            """Check Game over status Before and After Storyteller call."""
            # Check game over before.
            if button_label == config.game_over_label:
                _logger.warning('GAME OVER STATUS. RESTARTING...')
                return _reset_game()

            # Call async Storyteller function
            scene, ambience, response, history, input = asyncio.run(
                submit_function(message, history))

            # Check game over after (response may be a str if an error occurred).
            if hasattr(response, 'game_over') and response.game_over:
                _logger.info('GAME OVER AFTER MOVE. LOCKING.')
                return _game_over(scene, response)
            # Return Storyteller response.
            return scene, ambience, response, history, input, gr.update(), gr.update()

        # Assign function to button click event.
        submit_btn.click(fn=game_over_wrap, api_visibility="private",
                         inputs=[user_input, history_state, submit_btn],
                         outputs=[scene_image, ambience_audio, description_box,
                                  history_state, user_input, user_input, submit_btn])
        # Assign function to input submit event. (Press enter)
        user_input.submit(fn=game_over_wrap, api_visibility="private",
                          inputs=[user_input, history_state, submit_btn],
                          outputs=[scene_image, ambience_audio, description_box,
                                   history_state, user_input, user_input, submit_btn])
    return ui


# Instantiate logger.
_logger = getLogger(__name__)
