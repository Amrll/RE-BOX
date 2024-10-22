import pygame as pg
from data.states.enemy_state_machine import EnemyStateMachine

class Enemy(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state_machine = EnemyStateMachine()
        # Initialize other enemy properties (position, image, etc.)

    def update(self):
        self.state_machine.update(self)

    def draw(self, surface):
        # Draw the enemy on the surface
        pass
