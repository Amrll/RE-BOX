import pygame as pg
from .idle import Idle

class AttackLeft:
    def __init__(self, start_time, duration):
        """Initialize the attack with a start time and duration."""
        self.start_time = start_time
        self.duration = duration
        self.damage = 1

    def update(self, enemy):
        """Handle the attack logic and transition back to Idle after the attack."""
        now = pg.time.get_ticks()

        # Check if the attack duration hasn't ended yet
        if now - self.start_time < self.duration:
            # Stay in the attack state if the player has not been hit yet
            pass
        else:
            # Once the attack is over, switch back to Idle state
            enemy.state_machine.change_state(Idle())

    def check_player_hit(self, player_pos):
        """Check if the player is in the attack zone (left position)."""
        if player_pos == 0:
            return self.damage
        return 0

    def handle_hit(self, enemy):
        """Handle player hit, immediately switch to Idle state."""
        enemy.state_machine.change_state(Idle())  # Transition to Idle right after hitting the player
