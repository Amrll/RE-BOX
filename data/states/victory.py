"""
This State is updated when the game is won. It shows a 'Victory' message and
provides a menu to select options such as continuing the game, replaying the game, or going back to the main menu.
"""

import sys
import pygame as pg
from .. import prepare, state_machine, tools
from ..controls import ControlManager

# Constants
FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 60)
SMALLER_FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 30)
VICTORY_FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 100)
OPTIONS = ["REPLAY", "MAIN MENU"]
HIGHLIGHT_COLOR = (108, 148, 136)
BACKGROUND_COLOR = (0, 0, 0)
OPTION_SPACER = 80

class Victory(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.selected_enemy = None
        self.control_manager = ControlManager()
        self.index = 0
        self.options = self.make_options(FONT, OPTIONS, OPTION_SPACER)
        self.victory_text = self.make_victory_text(VICTORY_FONT)
        self.stats_text = None

        self.enemies = self.persist.get("enemies", [])

        self.music_playing = False
        self.music_file = prepare.MUSIC["victory"]

        self.choose_sound = pg.mixer.Sound(prepare.SFX["choosing"])
        self.punch_sound = pg.mixer.Sound(prepare.SFX["hit"])
        self.play_sound = False

    def make_victory_text(self, font):
        """Create the 'Victory' text and center it at the top of the screen."""
        victory_msg = font.render("VICTORY", True, pg.Color("green"))
        rect = victory_msg.get_rect(center=(prepare.SCREEN_RECT.width // 2, 370))  # Position near the top
        return victory_msg, rect

    def make_stats_text(self, font, health, fight_time):
        """Create the stats text showing remaining health and fight duration."""
        stats_msg = f"Remaining Health: {health} | Time: {fight_time:.2f}s"
        stats_surface = font.render(stats_msg, True, pg.Color("white"))
        rect = stats_surface.get_rect(center=(prepare.SCREEN_RECT.width // 2, 280))  # Positioned above Victory text
        return stats_surface, rect

    def make_options(self, font, options, spacer):
        """Create the menu options and position them in the center of the screen."""
        rendered = []
        total_height = len(options) * spacer
        y_start = (prepare.SCREEN_RECT.height - total_height) // 2 + 100  # Positioned below the Victory text

        for i, option in enumerate(options):
            msg = font.render(option, True, pg.Color("white"))
            rect = msg.get_rect(center=(prepare.SCREEN_RECT.width // 2, y_start + i * spacer))
            rendered.append((msg, rect))
        return rendered

    def startup(self, now, persistent):
        self.persist = persistent
        self.start_time = now

        self.play_sound = True

        # Retrieve health and fight_time from persistent state
        health = self.persist.get("health", 3)  # Default to 3 if not provided
        fight_time = self.persist.get("fight_time", 0.00)  # Default to 3.00 if not provided
        self.stats_text = self.make_stats_text(SMALLER_FONT, health, fight_time)

        self.selected_enemy = self.persist.get(
            "selected_enemy", {"name": "Default", "health": 10, "warning_duration": 1500}
        )

        # Start background music
        if not self.music_playing:
            pg.mixer.music.load(self.music_file)
            pg.mixer.music.play(0)  # Loop indefinitely
            self.music_playing = True

    def cleanup(self):
        """Reset State.done to False."""
        self.play_sound = False
        self.done = False
        return self.persist

    def update(self, keys, now):
        """Handle menu navigation and option selection."""
        if keys[pg.K_RETURN]:
            self.done = True
            self.handle_selection()

    def draw(self, surface, interpolate):
        """Draw the Victory screen with 'Victory' text and menu options."""
        surface.fill(BACKGROUND_COLOR)  # Fill the screen with black

        # Draw the "Victory" text
        surface.blit(*self.victory_text)

        surface.blit(*self.stats_text)

        # Draw the menu options
        for i, (msg, rect) in enumerate(self.options):
            if i == self.index:
                pg.draw.rect(surface, HIGHLIGHT_COLOR, rect.inflate(20, 20))  # Highlight the selected option
            surface.blit(msg, rect)

    def get_event(self, event):
        """Handle key events for menu navigation."""
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            action = self.control_manager.handle_key_event(event)  # Get the action based on the key event

            if event.type == pg.KEYDOWN:
                if action == "move_down":
                    if self.play_sound:
                        self.choose_sound.play()
                    self.index = (self.index + 1) % len(OPTIONS)
                elif action == "move_up":
                    if self.play_sound:
                        self.choose_sound.play()
                    self.index = (self.index - 1) % len(OPTIONS)
                elif action == "punch_left" or action == "punch_right":
                    if self.play_sound:
                        self.punch_sound.play()
                    pg.mixer.music.stop()
                    self.music_playing = False
                    self.handle_selection()

    def handle_selection(self):
        """Handle the selected option."""
        selected_option = OPTIONS[self.index]
        if selected_option == "REPLAY":
            self.next = "GAME"
            self.done = True
            # Ensure the selected enemy is carried over to the next game session
            self.persist["selected_enemy"] = self.selected_enemy
            return self.persist
        elif selected_option == "MAIN MENU":
            self.next = "LOADING"
            self.persist["next_state"] = "SELECT"  # Go back to the main menu after loading
            self.persist["load_duration"] = 1500  # Display loading screen for 2 seconds
        self.done = True
