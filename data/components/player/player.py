import pygame as pg

from data.animation_manager import AnimationManager
from data.components.player.player_state_machine import PlayerStateMachine
from data.components.player.states.attack_left import AttackLeft
from data.components.player.states.attack_right import AttackRight
from data.components.player.states.move_left import MoveLeft
from data.components.player.states.move_right import MoveRight
from data.components.player.states.take_damage import TakeDamage


class Player(pg.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)
        self.state_machine = PlayerStateMachine(self)
        self.initial_health = 3  # Set the initial health value
        self.health = self.initial_health  # Initialize player health
        self.player_positions = [600, 830, 1060]  # X-coordinates for left, middle, and right
        self.player_pos = 1  # 0 = left, 1 = middle, 2 = right
        self.move_back_time = 1000  # Time to move back to middle (milliseconds)
        self.last_move_time = 0
        self.surface = surface

        self.is_attacking = False
        self.is_hurt = False

        self.rect = pg.Rect(self.player_positions[self.player_pos], 800, 0, 0)

        self.animation_manager = AnimationManager()

    def update(self, now, keys, enemy):
        """Update player logic."""
        self.state_machine.update(self)

    def reset(self):
        """Reset the player to its initial state, including health."""
        self.health = self.initial_health

    def move_to_position(self, pos):
        """Move player to a specified position."""
        self.player_pos = pos
        # Update the player's rect position based on the new position
        self.rect.x = self.player_positions[self.player_pos]

    def take_damage(self, damage):
        """Handle player taking damage."""
        self.state_machine.change_state(TakeDamage(damage))

    def handle_input(self, action, is_keydown):
        """Handle player input actions for movement and attack."""
        if is_keydown:
            if action == "move_left":
                self.state_machine.change_state(MoveLeft())
            elif action == "move_right":
                self.state_machine.change_state(MoveRight())
            elif action == "punch_left":
                self.state_machine.change_state(AttackLeft())
            elif action == "punch_right":
                self.state_machine.change_state(AttackRight())

    def attack(self):
        """Handle player attack logic."""
        self.is_attacking = True

    def reset_attack(self):
        """Reset the player's attack flag after attack is processed."""
        self.is_attacking = False

    def draw(self, surface):
        self.animation_manager.play_animation("Idle_player", surface, (self.rect.x, self.rect.y))

        if self.is_hurt:
            self.draw_hurt_overlay(self.surface)

    def draw_hurt_overlay(self, surface):
        """Draw a red overlay to indicate damage."""
        overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)  # Create a transparent surface
        overlay.fill((255, 0, 0, 100))  # Red with transparency (100 is the alpha)
        surface.blit(overlay, (0, 0))
