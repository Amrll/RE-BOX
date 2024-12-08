import pygame as pg
from .enemy_state_machine import EnemyStateMachine
from .states.attack_left import AttackLeft
from .states.attack_middle import AttackMiddle
from .states.attack_right import AttackRight
from .states.take_damage import TakeDamage
from .states.warning import WarningAttack
from .states.block import Block
from ...animation_manager import AnimationManager

STATE_COLORS = {
    'Idle': (0, 255, 0),          # Green for Idle state
    'Block': (0, 0, 255),         # Blue for Block state
    'AttackLeft': (255, 0, 0),
    'AttackMiddle': (255, 0, 0),
    'AttackRight': (255, 0, 0),    # Red for attack states
    'TakeDamage': (255, 0, 255),   # Magenta for Take Damage state
}


class Enemy(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state_machine = EnemyStateMachine(self)
        self.enemy_name = "Test Enemy"
        self.initial_health = 10
        self.health = self.initial_health
        self.rect = pg.Rect(920, 500, 100, 100)
        self.player_pos = 1
        self.is_blocking = False
        self.player_last_attacked_time = pg.time.get_ticks()
        self.is_taking_damage = False
        self.damage = 0

        self.warning_duration = 1500

        self.animation_manager = AnimationManager()


    def update(self):
        """Update the enemy state machine."""
        self.state_machine.update(self)

    def reset(self):
        """Reset the enemy to its initial state, including health."""
        self.health = self.initial_health

    def update_player_position(self, player_pos):
        """Update the player's position for attack checks."""
        self.player_pos = player_pos

    def attempt_attack(self):
        """Attempt an attack. Returns damage only if within the attack window."""
        now = pg.time.get_ticks()
        if isinstance(self.state_machine.state, (AttackLeft, AttackMiddle, AttackRight)):
            if now - self.state_machine.state.start_time < self.state_machine.state.duration:
                if self.state_machine.state.check_player_hit(self.player_pos):
                    damage = self.state_machine.state.damage
                    self.state_machine.state.handle_hit(self)
                    return damage
        return 0

    def is_warning_active(self):
        """Check if the enemy is in the WarningAttack state."""
        return isinstance(self.state_machine.state, WarningAttack)

    def get_warning_position(self):
        """Get the position of the current warning if active."""
        if self.is_warning_active():
            return self.state_machine.state.attack_position
        return None

    def check_player_attack(self, player):
        """Check if the player is attacking and process damage if not blocking."""
        if player.is_attacking:
            self.player_last_attacked_time = pg.time.get_ticks()  # Update the time when the player attacks
            if not self.is_blocking and not self.is_taking_damage:
                self.take_damage(1)
            player.reset_attack()

    def take_damage(self, damage):
        """Reduce enemy's health when taking damage."""
        self.is_taking_damage = True  # Set flag to indicate damage is being taken
        self.state_machine.change_state(TakeDamage(damage))

    def draw(self, surface):
        # Use self.enemy_name to select different animations based on the enemy's name
        if isinstance(self.state_machine.state, AttackLeft):
            self.animation_manager.play_animation(f"{self.enemy_name}_attack", surface, (self.rect.x, self.rect.y))
        elif isinstance(self.state_machine.state, AttackMiddle):
            self.animation_manager.play_animation(f"{self.enemy_name}_attack", surface, (self.rect.x, self.rect.y))
        elif isinstance(self.state_machine.state, AttackRight):
            self.animation_manager.play_animation(f"{self.enemy_name}_attack", surface, (self.rect.x, self.rect.y))
        elif isinstance(self.state_machine.state, TakeDamage):
            self.animation_manager.play_animation(f"{self.enemy_name}_hurt", surface, (self.rect.x, self.rect.y))
        elif isinstance(self.state_machine.state, Block):
            self.animation_manager.play_animation(f"{self.enemy_name}_block", surface, (self.rect.x, self.rect.y))
        elif isinstance(self.state_machine.state, WarningAttack):
            self.animation_manager.play_animation(f"{self.enemy_name}_warning", surface, (self.rect.x, self.rect.y))
        else:
            self.animation_manager.play_animation(f"{self.enemy_name}_idle", surface, (self.rect.x, self.rect.y))

