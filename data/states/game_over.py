"""
This State is updated when the game is over. It shows a 'Game Over' message and
provides a menu to select options such as retrying the game, going back to the main menu, or exiting.
"""

import sys
import pygame as pg
from .. import prepare, state_machine, tools
from ..controls import ControlManager

# Constants
FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 60)
GAME_OVER_FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 100)
OPTIONS = ["RETRY", "MAIN MENU", "EXIT"]
HIGHLIGHT_COLOR = (108, 148, 136)
BACKGROUND_COLOR = (0, 0, 0)
OPTION_SPACER = 80

class GameOver(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.control_manager = ControlManager()
        self.index = 0
        self.options = self.make_options(FONT, OPTIONS, OPTION_SPACER)
        self.game_over_text = self.make_game_over_text(GAME_OVER_FONT)
        self.music_playing = False
        self.music_file = prepare.MUSIC["lose"]

    def make_game_over_text(self, font):
        """Create the 'Game Over' text and center it at the top of the screen."""
        game_over_msg = font.render("GAME OVER", True, pg.Color("red"))  # "Game Over" in red
        rect = game_over_msg.get_rect(center=(prepare.SCREEN_RECT.width // 2, 370))
        return game_over_msg, rect

    def make_options(self, font, options, spacer):
        """Create the menu options"""
        rendered = []
        total_height = len(options) * spacer
        y_start = (prepare.SCREEN_RECT.height - total_height) // 2 + 100  # Positioned below the Game Over text

        for i, option in enumerate(options):
            msg = font.render(option, True, pg.Color("white"))
            rect = msg.get_rect(center=(prepare.SCREEN_RECT.width // 2, y_start + i * spacer))
            rendered.append((msg, rect))
        return rendered

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now

        # Start background music
        if not self.music_playing:
            pg.mixer.music.load(self.music_file)
            pg.mixer.music.play(0)  # Loop indefinitely
            self.music_playing = True

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
        """Draw the GameOver screen with 'Game Over' text and menu options."""
        surface.fill(BACKGROUND_COLOR)

        # Draw the "Game Over" text
        surface.blit(*self.game_over_text)

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
                    pg.mixer.music.stop()
                    self.handle_selection()

    def handle_selection(self):
        """Handle the selected option."""
        selected_option = OPTIONS[self.index]
        if selected_option == "RETRY":
            self.next = "GAME"  # Restart the game
        elif selected_option == "MAIN MENU":
            self.next = "LOADING"
            self.persist["next_state"] = "SELECT"  # Go back to the main menu after loading
            self.persist["load_duration"] = 1500  # Go back to the main menu
        elif selected_option == "EXIT":
            pg.quit()
            sys.exit()
        self.done = True
