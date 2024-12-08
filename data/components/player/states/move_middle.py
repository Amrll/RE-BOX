import pygame as pg
from data.components.player.states.idle import Idle

class MoveMiddle:
    def __init__(self):
        pass

    def update(self, player):
        """Move player to the middle position if not already there."""
        if player.player_pos != 1:  # Check if not already in the middle
            player.player_pos = 1  # Set to middle position
            player.rect.x = player.player_positions[player.player_pos]
        player.state_machine.change_state(Idle())