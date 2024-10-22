import pygame as pg
from data.components.player.states.idle import Idle


class PlayerStateMachine:
    def __init__(self, player):
        self.player = player
        self.state = Idle()

    def update(self, player):
        """Update the current state."""
        self.state.update(player)

    def change_state(self, new_state):
        """Change the player state and handle enter/exit transitions."""
        # Call the exit method of the current state (if it exists)
        if hasattr(self.state, 'exit'):
            self.state.exit(self.player)

        # Change to the new state
        self.state = new_state

        # Call the enter method of the new state (if it exists)
        if hasattr(self.state, 'enter'):
            self.state.enter(self.player)
        