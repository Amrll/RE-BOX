import pygame as pg
from data.components.player.states.idle import Idle

class MoveRight:
    def __init__(self):
        pass

    def update(self, player):
        """Move player to the right if possible."""
        if player.player_pos != 2:
            player.player_pos = 2
            player.rect.x = player.player_positions[player.player_pos]
        player.state_machine.change_state(Idle())
