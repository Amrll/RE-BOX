import pygame as pg

from data.components.enemy.states.idle import Idle


class Block:
    def __init__(self):
        self.start_time = pg.time.get_ticks()

    def update(self, enemy):
        """Handle the block state and exit if player hasn't attacked for 2000ms."""
        now = pg.time.get_ticks()

        # Exit the block state only if the player has not attacked for the set seconds
        if now - enemy.player_last_attacked_time > 5000:
            enemy.state_machine.change_state(Idle())

    def enter(self, enemy):
        enemy.is_blocking = True

    def exit(self, enemy):
        enemy.is_blocking = False
