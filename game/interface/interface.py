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
    start_narration: str
    place_img: str
    description_label: str
    title_label: str
    input_button: str
    input_label: str
    input_command: str
    music_toggle_label: str
    narration_toggle_label: str
    music_disabled: bool
    narration_disabled: bool
    game_over_field: str
    game_over_label: str
    start_scene: str
    footer_disclaimer: str


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
        with gr.Row():
            # Scene's ambience music.
            ambience_audio = gr.Audio(label="Ambience", show_label=True, sources=[],
                                      loop=True, interactive=False, autoplay=True,
                                      value=config.start_ambience, format="mp3",
                                      waveform_options={"waveform_progress_color":
                                                      "#3571C0"})
            # Scene's voice acting narration.
            narration_audio = gr.Audio(label="Narration", show_label=True, sources=[],
                                       loop=False, interactive=False, autoplay=True,
                                       value=config.start_narration, format="mp3",
                                       waveform_options={"waveform_progress_color":
                                                       "#35C06F"})
        # Scene's description.
        description_box = gr.Textbox(label=config.description_label, buttons=["copy"],
                                     value=config.start_scene, interactive=False)
        # Player's command.
        user_input = gr.Textbox(label=config.input_label,
                                placeholder=config.input_command)
        # Submit button.
        submit_btn = gr.Button(config.input_button)

        with gr.Row():
            # Music toggle.
            music_enabled = gr.Checkbox(
                label=config.music_toggle_label,
                value=not config.music_disabled,
                interactive=not config.music_disabled)
            # Narration toggle.
            narration_enabled = gr.Checkbox(
                label=config.narration_toggle_label,
                value=not config.narration_disabled,
                interactive=not config.narration_disabled)
            # Language selector.
            language = gr.Dropdown(label="Narration Language", show_label=True,
                                   interactive=True, choices=["en", "es", "de", "fr"],
                                   value="en")

        # Define Game Over control.
        def _reset_game():
            """Return initial values for game restart."""
            return (config.start_img, config.start_ambience, config.start_narration,
                    config.start_scene, [], '',
                    gr.update(interactive=True),
                    gr.update(value=config.input_button))

        def _game_over(scene, ambience, narration, response):
            """Return Game Over values, blocking input field."""
            return (scene, ambience, narration,
                    response, [], config.game_over_field,
                    gr.update(interactive=False),
                    gr.update(value=config.game_over_label))

        def game_over_wrap(message, history, button_label,
                           music_toggle, narration_toggle, language):
            """Check Game over status before and after Storyweaver call."""
            # Check game over before.
            if button_label == config.game_over_label:
                _logger.warning('GAME OVER STATUS. RESTARTING...')
                return _reset_game()
            # Call async Storyweaver function.
            scene, ambience, narration, response, history, input = asyncio.run(
                submit_function(message, history, music_toggle,
                                narration_toggle, language))
            # Preserve existing audio in the widget if no new ambience was generated.
            ambience = ambience or gr.update(autoplay=False)
            # Empty narration if none was generated.
            narration = narration or None
            # Check game over after (response may be a str if an error occurred).
            if hasattr(response, 'game_over') and response.game_over:
                _logger.info('GAME OVER AFTER MOVE. LOCKING.')
                return _game_over(scene, ambience, narration, response)
            # Return Storyweaver response
            _logger.info('MOVE COMPLETED. RETURNING SCENE.')
            return (scene, ambience, narration, response, history, input,
                    gr.update(), gr.update())

        # Assign function to button click event.
        submit_btn.click(fn=game_over_wrap, api_visibility="private",
                         inputs=[user_input, history_state, submit_btn,
                                 music_enabled, narration_enabled, language],
                         outputs=[scene_image, ambience_audio, narration_audio,
                                  description_box, history_state, user_input,
                                  user_input, submit_btn])
        # Assign function to input submit event. (Press enter)
        user_input.submit(fn=game_over_wrap, api_visibility="private",
                          inputs=[user_input, history_state, submit_btn,
                                  music_enabled, narration_enabled, language],
                          outputs=[scene_image, ambience_audio, narration_audio,
                                   description_box, history_state, user_input,
                                   user_input, submit_btn])
        # Footer with disclaimer.
        gr.Markdown(config.footer_disclaimer, elem_id="footer-disclaimer")
    return ui


# Instantiate logger.
_logger = getLogger(__name__)
