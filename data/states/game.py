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
        self.enemy = Enemy()
        self.animation_manager = AnimationManager()
        self.control_manager = ControlManager()
        self.ground = None
        self.hud = None
        self.next = None
        self.done = False

        self.player = Player(prepare.SCREEN)

        self.countdown = Countdown(duration=4000)  # Initialize Countdown

        # Variables for blinking effect
        self.warning_visible = True
        self.warning_blink_timer = 0  # Timer for blinking
        self.warning_blink_interval = 200

    def reset_game_state(self):
        """Reset game state variables when restarting."""
        self.player.reset()  # Reset player to initial state
        self.enemy.reset()
        self.done = False
        self.countdown.start()

    def startup(self, now, persistent):
        """Set up the game when it starts or restarts."""
        self.persist = persistent
        self.start_time = now
        self.reset_game_state()
        self.setup_arena()
        self.setup_hud()

        selected_enemy = self.persist.get("selected_enemy", {"name": "Default", "health": 10, "warning_duration": 1500})

        # Set the properties of the enemy using the selected values
        self.enemy.enemy_name = selected_enemy["name"]
        self.enemy.initial_health = selected_enemy["health"]
        self.enemy.health = selected_enemy["health"]
        self.enemy.warning_duration = selected_enemy["warning_duration"]


    def setup_arena(self):
        """Set up the background arena."""
        background_image = prepare.GFX["misc"]["bg_ring"]
        self.ground = pg.transform.scale(background_image, prepare.SCREEN_RECT.size)

    def setup_hud(self):
        """Initialize the HUD for displaying health bars and info."""
        self.hud = pg.font.Font(None, 36)

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

        # Draw warning overlay for attack column if active
        self.draw_warning(surface)

        # Draw countdown overlay if active
        if self.countdown.active:
            self.countdown.draw(surface)

    def draw_warning(self, surface):
        """Draw the warning for the attack column with a blinking effect."""
        if self.enemy.is_warning_active():
            # Update blinking state
            current_time = pg.time.get_ticks()
            if current_time - self.warning_blink_timer >= self.warning_blink_interval:
                self.warning_visible = not self.warning_visible
                self.warning_blink_timer = current_time

            if self.warning_visible:
                attack_position = self.enemy.get_warning_position()

                # Ensure valid attack_position
                if attack_position not in (0, 1, 2):
                    return  # Ignore invalid positions

                # Define column dimensions
                screen_width, screen_height = surface.get_size()
                column_width = screen_width / 3  # Use floating-point division for precision

                # Calculate the rectangle for the warning column
                rect_x = round(attack_position * column_width)
                warning_rect = pg.Rect(rect_x, 0, round(column_width), screen_height)

                # Draw a translucent orange overlay
                overlay = pg.Surface(warning_rect.size)
                overlay.set_alpha(128)  # Transparency level
                overlay.fill((255, 165, 0))  # Orange color for the warning
                surface.blit(overlay, warning_rect.topleft)

    def game_over(self):
        """Handle game over state."""
        self.next = "GAME_OVER"
        self.done = True

    def victory(self):
        """Handle victory state."""
        self.next = "VICTORY"
        self.done = True
