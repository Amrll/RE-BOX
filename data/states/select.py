"""
This screen allows users to select between:
    * Story Mode
    * Arcade Mode
    * Settings
    * Exit (Quit Game)
"""
import sys

import pygame as pg
from .. import prepare, state_machine, menu_helpers, tools
from ..controls import ControlManager

FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 60)
OPTIONS = ["STORY MODE", "GAME", "SETTINGS", "EXIT"]
HIGHLIGHT_COLOR = (108, 148, 136)

# Placement and spacing constants.
OPT_Y = 300
OPT_SPACER = 80

class MainMenu(state_machine._State):
    """
    This State is updated while the game shows the main menu screen.
    """
    def __init__(self):
        state_machine._State.__init__(self)
        self.index = 0
        self.next = None
        self.options = self.make_options(FONT, OPTIONS, OPT_SPACER)
        self.control_manager = ControlManager()
        self.title_image = TitleImage()

    def make_options(self, font, options, spacer):
        """Create the menu options and position them on the right side of the screen."""
        rendered = []
        # Calculate total height of all options
        total_height = len(options) * spacer
        y_start = (prepare.SCREEN_RECT.height - total_height) // 2

        for i, option in enumerate(options):
            msg = font.render(option, True, pg.Color("white"))
            # Adjust the x-coordinate to place the options on the right side
            x_position = prepare.SCREEN_RECT.width * 3 // 4  # About three-quarters across the screen
            rect = msg.get_rect(center=(x_position, y_start + i * spacer))
            rendered.append((msg, rect))
        return rendered

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)
        self.index = 0  # Reset the menu index to the first option
        self.done = False  # Ensure 'done' is reset
        self.next = None

    def cleanup(self):
        """Reset State.done to False."""

        self.next = None
        self.done = False
        return self.persist

    def update(self, keys, now):
        # Title image
        self.title_image.update(now)

    def draw(self, surface, interpolate):
        """Draw the menu options."""
        surface.fill(prepare.BACKGROUND_COLOR)

        # Draw the title image
        #surface.blit(self.title_image.image, self.title_image.rect)

        for i, (msg, rect) in enumerate(self.options):
            if i == self.index:
                pg.draw.rect(surface, HIGHLIGHT_COLOR, rect.inflate(20, 20))
            surface.blit(msg, rect)

    def get_event(self, event):
        """Handle key events using ControlManager."""
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            action = self.control_manager.handle_key_event(event)  # Get the action based on the key event

            if event.type == pg.KEYDOWN:
                if action == "move_down":
                    self.index = (self.index + 1) % len(OPTIONS)
                elif action == "move_up":
                    self.index = (self.index - 1) % len(OPTIONS)
                elif action == "punch_left" or action == "punch_right":
                    self.pressed_enter()

    def pressed_enter(self):
        """Set the next state based on the selected option."""
        selected_option = OPTIONS[self.index]
        if selected_option == "EXIT":
            pg.quit()
            sys.exit()
        else:
            self.next = selected_option
            self.done = True


class TitleImage(tools._BaseSprite):
    def __init__(self, *groups):
        # Load the title image
        original_image = prepare.GFX["misc"]["titlewords"]

        # Resize the image to be smaller
        new_size = (original_image.get_width() // 2, original_image.get_height() // 2)  # Example resize
        self.image = pg.transform.scale(original_image, new_size)

        # Initialize the sprite
        tools._BaseSprite.__init__(self, (0, 0), self.image.get_size(), *groups)

        # Position the title image on the top left of the screen
        self.rect = self.image.get_rect(topleft=(120, 60))  # Adjust as needed
        self.exact_position = list(self.rect.topleft)

    def update(self, now):
        # Update the sprite position
        self.rect.topleft = self.exact_position

