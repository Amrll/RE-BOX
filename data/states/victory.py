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
VICTORY_FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 100)
OPTIONS = ["CONTINUE", "REPLAY", "MAIN MENU"]
HIGHLIGHT_COLOR = (108, 148, 136)
BACKGROUND_COLOR = (0, 0, 0)
OPTION_SPACER = 80

class Victory(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.control_manager = ControlManager()
        self.index = 0
        self.options = self.make_options(FONT, OPTIONS, OPTION_SPACER)
        self.victory_text = self.make_victory_text(VICTORY_FONT)

    def make_victory_text(self, font):
        """Create the 'Victory' text and center it at the top of the screen."""
        victory_msg = font.render("VICTORY", True, pg.Color("green"))
        rect = victory_msg.get_rect(center=(prepare.SCREEN_RECT.width // 2, 370))  # Position near the top
        return victory_msg, rect

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

    def cleanup(self):
        """Reset State.done to False."""
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
                    self.index = (self.index + 1) % len(OPTIONS)
                elif action == "move_up":
                    self.index = (self.index - 1) % len(OPTIONS)
                elif action == "punch_left" or action == "punch_right":
                    self.handle_selection()

    def handle_selection(self):
        """Handle the selected option."""
        selected_option = OPTIONS[self.index]
        if selected_option == "CONTINUE":
            self.next = "GAME"  # Continue the game (or go to the next level)
        elif selected_option == "REPLAY":
            self.next = "GAME"  # Replay the game (restart the current level)
        elif selected_option == "MAIN MENU":
            self.next = "LOADING"
            self.persist["next_state"] = "SELECT"  # Go back to the main menu after loading
            self.persist["load_duration"] = 1500  # Display loading screen for 2 seconds
        self.done = True
