"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its state_machine dictionary.
"""

import pygame as pg
from . import prepare, tools
from .states import splash, title, game, select, game_over, victory, loading, enemey_select


def main():
    pg.init()

    app = tools.Control(prepare.ORIGINAL_CAPTION)
    pg.display.set_icon(prepare.ICON_IMAGE)
    # Set up the state dictionary
    state_dict = {
        "SPLASH": splash.Splash(),
        "TITLE": title.Title(),
        "SELECT": select.MainMenu(),
        "GAME": game.Game(),
        "GAME_OVER": game_over.GameOver(),
        "VICTORY": victory.Victory(),
        "LOADING": loading.LoadingScreen(),
        "ENEMYSELECT": enemey_select.EnemySelect(),
    }

    # Set up the states in the state machine and start with "SPLASH"
    app.state_machine.setup_states(state_dict, "SPLASH")

    # Start the main loop
    app.main()

    # Quit Pygame when done
    pg.quit()
