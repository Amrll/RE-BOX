import pygame as pg
from .. import state_machine, prepare
from ..animation_manager import AnimationManager
from ..components.enemy_health_drawer import draw_enemy_health
from ..components.player_health_drawer import draw_player_health
from ..controls import ControlManager
from ..components.enemy.enemy import Enemy
from ..components.player.player import Player
from ..components.countdown import Countdown


class Game(state_machine._State):
    def __init__(self):
        super(Game, self).__init__()
        self.animation_manager = AnimationManager()
        self.control_manager = ControlManager()
        self.ground = None
        self.hud = None
        self.next = None
        self.done = False

        self.player = Player(prepare.SCREEN)
        self.enemy = Enemy()

        self.countdown = Countdown(duration=4000)  # Initialize Countdown

    def reset_game_state(self):
        """Reset game state variables when restarting."""
        self.player.reset()  # Reset player to initial state
        self.enemy.reset()
        self.done = False
        self.countdown.start()  # Start countdown when resetting game state

    def startup(self, now, persistent):
        """Set up the game when it starts or restarts."""
        self.persist = persistent
        self.start_time = now
        self.reset_game_state()
        self.setup_arena()
        self.setup_hud()

    def setup_arena(self):
        """Set up the background arena."""
        background_image = prepare.GFX["misc"]["bg_ring"]
        self.ground = pg.transform.scale(background_image, prepare.SCREEN_RECT.size)

    def setup_hud(self):
        """Initialize the HUD for displaying health bars and info."""
        self.hud = pg.font.Font(None, 36)
    def get_event(self, event):
        """Handle player input for moving and attacking."""
        if not self.countdown.active:  # Don't accept inputs during countdown
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                action = self.control_manager.handle_key_event(event)
                self.player.handle_input(action, event.type == pg.KEYDOWN)

    def update(self, keys, now):
        """Update game state including player and enemy logic."""
        if self.countdown.active:
            self.countdown.update()  # Update the countdown
        else:
            # Update player and enemy only after countdown is over
            self.player.update(now, keys, self.enemy)

            # Pass the player's current position to the enemy
            self.enemy.update_player_position(self.player.player_pos)

            # Check if the enemy successfully attacks the player
            damage = self.enemy.attempt_attack()
            if damage > 0:
                self.player.take_damage(damage)

            # Check if the player attacked and handle damage to the enemy
            self.enemy.check_player_attack(self.player)

            # Trigger enemy attack logic
            self.enemy.update()

            # Check if game is over
            if self.player.health <= 0:
                self.game_over()
            elif self.enemy.health <= 0:
                self.victory()

    def draw(self, surface, interpolate):
        """Render the game visuals."""
        surface.blit(self.ground, (0, 0))  # Draw the background

        self.player.draw(surface)  # draw the player

        if self.enemy:  # Only draw enemy if alive
            self.enemy.draw(surface)

        draw_enemy_health(surface, self.enemy, self.hud, prepare.SCREEN_RECT)
        draw_player_health(surface, self.player.health, self.animation_manager)

        # Draw countdown overlay if active
        if self.countdown.active:
            self.countdown.draw(surface)

    def game_over(self):
        """Handle game over state."""
        self.next = "GAME_OVER"
        self.done = True

    def victory(self):
        """Handle victory state."""
        self.next = "VICTORY"
        self.done = True
