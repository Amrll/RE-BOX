import pygame as pg
from data.components.player.states.idle import Idle


class MoveLeft:
    def __init__(self):
        pass

    def update(self, player):
        """Move player to the left if possible."""
        if player.player_pos != 0:
            player.player_pos = 0
            player.rect.x = player.player_positions[player.player_pos]
        player.state_machine.change_state(Idle())  # After moving, switch to Idle state
