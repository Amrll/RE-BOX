import random
import pygame as pg
from .block import Block
from .idle import Idle

class TakeDamage:
    def __init__(self, damage):
        self.duration = 1000  # Duration of the "taking damage" state in milliseconds
        self.start_time = pg.time.get_ticks()
        self.damage = damage  # Store the damage value

    def update(self, enemy):
        """Handle the take damage state and transition based on a higher probability for Block state."""
        now = pg.time.get_ticks()
        if now - self.start_time > self.duration:
            # 70% chance to go to Block state, 30% chance to go to Idle state
            if random.random() < 0.7:
                enemy.state_machine.change_state(Block())
            else:
                enemy.state_machine.change_state(Idle())

    def enter(self, enemy):
        """This function is called when entering the state (apply damage here)."""
        enemy.health -= self.damage  # Apply damage to the enemy's health

    def exit(self, enemy):
        """This function is called when exiting the state (optional cleanup)."""
        enemy.is_taking_damage = False  # Reset flag when exiting the state
