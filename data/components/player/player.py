import queue

import pygame as pg

from data import hand_detection
from data.animation_manager import AnimationManager
from data.components.player.player_state_machine import PlayerStateMachine
from data.components.player.states.attack_left import AttackLeft
from data.components.player.states.attack_right import AttackRight
from data.components.player.states.move_left import MoveLeft
from data.components.player.states.move_right import MoveRight
from data.components.player.states.move_middle import MoveMiddle
from data.components.player.states.take_damage import TakeDamage
import threading


class Player(pg.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)


        self.current_gesture = None
        self.gesture_lock = threading.Lock()
        self.hand_detected = False  # Store detection result
        self.detecting = True  # Control detection thread
        self.detection_thread = threading.Thread(target=self.run_hand_detection, daemon=True)
        self.detection_thread.start()


        self.state_machine = PlayerStateMachine(self)
        self.initial_health = 3  # Set the initial health value
        self.health = self.initial_health  # Initialize player health

        self.player_positions = [500, 830, 1160]  # X-coordinates for left, middle, and right
        self.player_pos = 1
        self.last_move_time = 0
        self.surface = surface

        self.is_attacking = False
        self.is_hurt = False

        self.rect = pg.Rect(self.player_positions[self.player_pos], 800, 0, 0)

        self.animation_manager = AnimationManager()

    def update(self, now, keys, enemy):
        """Update player logic."""
        self.process_current_gesture()
        self.state_machine.update(self)

    def reset(self):
        """Reset the player to its initial state, including health."""
        self.health = self.initial_health
        self.is_hurt = False
        self.is_attacking = False
        self.player_pos = 1

    def take_damage(self, damage):
        """Handle player taking damage."""
        self.state_machine.change_state(TakeDamage(damage))

    def process_current_gesture(self):
        """Process the latest gesture detected by the hand detection thread."""
        if self.current_gesture:
            self.handle_movement(self.current_gesture)
            self.handle_attack(self.current_gesture)
            self.current_gesture = None

    def run_hand_detection(self):
        while self.detecting:
            detected_gesture = hand_detection.get_detected_gesture()
            if detected_gesture:
                with self.gesture_lock:
                    self.current_gesture = detected_gesture

    def handle_movement(self, gesture):
        """Move player directly in response to detected gesture."""
        if gesture == "move_left" and self.player_pos > 0:
            self.player_pos -= 1
            self.rect.x = self.player_positions[self.player_pos]
        elif gesture == "move_right" and self.player_pos < len(self.player_positions) - 1:
            self.player_pos += 1
            self.rect.x = self.player_positions[self.player_pos]
        elif gesture == "move_middle":
            self.player_pos = 1
            self.rect.x = self.player_positions[self.player_pos]

    def handle_attack(self, gesture):
        if gesture == "punch_left":
            self.state_machine.change_state(AttackLeft())
        elif gesture == "punch_right":
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
        overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
        overlay.fill((255, 0, 0, 100))
        surface.blit(overlay, (0, 0))


