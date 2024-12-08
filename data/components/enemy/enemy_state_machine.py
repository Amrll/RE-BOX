import random
import pygame as pg

from data.components.enemy.states.idle import Idle
from data.components.enemy.states.attack_middle import AttackMiddle
from data.components.enemy.states.attack_left import AttackLeft
from data.components.enemy.states.attack_right import AttackRight
from .states.warning import WarningAttack
from data.components.enemy.states.take_damage import TakeDamage


class EnemyStateMachine:
    def __init__(self, enemy):
        self.enemy = enemy
        self.state = Idle()

        # Attack timers and durations
        self.last_attack_time = 0
        self.attack_time_interval = 4000  # Time interval for next attack (milliseconds)
        self.attack_duration = 1000  # Duration of each attack (milliseconds)

    def update(self, enemy):
        """Update the enemy state and check for attack conditions."""
        now = pg.time.get_ticks()

        # Trigger a new attack if enough time has passed
        if now - self.last_attack_time > self.attack_time_interval:
            self.start_random_attack(now)

        # Update the current state (Idle or Attack state)
        self.state.update(enemy)

    def change_state(self, new_state):
        """Switch to a new state."""
        # Call exit on the current state if it has an exit method
        if hasattr(self.state, 'exit'):
            self.state.exit(self.enemy)  # Pass the enemy instance to exit method
        self.state = new_state  # Switch to the new state
        if hasattr(self.state, 'enter'):
            self.state.enter(self.enemy)

    def start_random_attack(self, now):
        """Randomly start an attack in one of three positions."""
        attack_position = random.choice([0, 1, 2])  # Choose a random attack position

        self.change_state(WarningAttack(attack_position, duration=self.enemy.warning_duration))

        self.last_attack_time = now  # Record the time of the attack

    def start_attack(self, attack_position):
        """Start the actual attack after the warning phase."""
        if attack_position == 0:
            self.change_state(AttackLeft(pg.time.get_ticks(), self.attack_duration))
        elif attack_position == 1:
            self.change_state(AttackMiddle(pg.time.get_ticks(), self.attack_duration))
        elif attack_position == 2:
            self.change_state(AttackRight(pg.time.get_ticks(), self.attack_duration))
