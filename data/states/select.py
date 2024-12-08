"""
This screen allows users to select between:
    * Story Mode
    * Arcade Mode
    * Settings
    * Exit (Quit Game)
"""
import sys
import threading
import time

import pygame as pg
from .. import prepare, state_machine, menu_helpers, tools, hand_detection
from ..controls import ControlManager

FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 34)
OPTIONS = ["STORY MODE", "QUICK PLAY", "SETTINGS", "EXIT"]

OPTION_COLORS = {
    "STORY MODE": pg.Color(96, 96, 96),
    "GAME": pg.Color("white"),
    "SETTINGS": pg.Color("white"),
    "EXIT": pg.Color("white"),
}
HIGHLIGHT_COLOR = (108, 148, 136)

# Placement and spacing constants.
OPT_X = 300
OPT_SPACER = 80


class MainMenu(state_machine._State):
    """
    This State is updated while the game shows the main menu screen.
    """
    def __init__(self):
        super().__init__()

        self.last_gesture_time = None
        self.current_gesture = None
        self.gesture_lock = threading.Lock()
        self.detecting = True
        self.gesture_debounce_time = .5
        self.detection_thread = threading.Thread(target=self.run_hand_detection, daemon=True)
        self.detection_thread.start()
        
        
        state_machine._State.__init__(self)
        self.ground = prepare.GFX["misc"]["title_screen"]
        self.image = prepare.GFX["backgrounds"]["ring1"]
        self.index = 0
        self.next = None
        self.options = self.make_options(FONT, OPTIONS, OPT_SPACER)
        self.control_manager = ControlManager()

    def make_options(self, font, options, spacer):
        rendered = []
        # Calculate the total width of the options with spacing
        option_sizes = [font.size(option)[0] for option in options]
        total_width = sum(option_sizes) + spacer * (len(options) - 1)
        x_start = (prepare.SCREEN_RECT.width - total_width) // 2  # Center horizontally

        # Fixed Y position for the row of options
        y_position = prepare.SCREEN_RECT.height - 400

        # Render each option
        current_x = x_start
        for option, width in zip(options, option_sizes):
            color = OPTION_COLORS.get(option, pg.Color("white"))
            msg = font.render(option, True, color)
            rect = msg.get_rect(midtop=(current_x + width // 2, y_position))
            rendered.append((msg, rect))
            current_x += width + spacer  # Move to the next option position
        return rendered

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)
        self.index = 1  # Reset the menu index to the first option
        self.done = False  # Ensure 'done' is reset
        self.next = None

    def cleanup(self):
        """Reset State.done to False."""
        self.next = None
        self.done = False
        return self.persist

    def update(self, keys, now):
        pass

    def draw(self, surface, interpolate):
        """Draw the menu options."""
        surface.blit(self.ground, (0, 0))

        arena_image = pg.transform.scale(self.image, prepare.SCREEN_RECT.size)
        surface.blit(arena_image, (0, 0))

        # Create a semi-transparent gray overlay
        overlay = pg.Surface(prepare.SCREEN_RECT.size)
        overlay.fill((0, 0, 0))  # Gray color (you can adjust this color)
        overlay.set_alpha(60)
        surface.blit(overlay, (0, 0))

        # Load and align the title image
        title_image = prepare.GFX["misc"]["titlewords"]
        scaled_title_image = pg.transform.scale(title_image, title_image.get_size())  # Keep the original size
        title_rect = scaled_title_image.get_rect(midbottom=(prepare.SCREEN_RECT.centerx, 0))  # Start above screen
        title_rect.centery = prepare.SCREEN_RECT.centery  # Center the image vertically

        # Draw the title image
        surface.blit(scaled_title_image, title_rect)

        for i, (msg, rect) in enumerate(self.options):
            # Highlight the selected option
            if i == self.index:
                highlight_rect = rect.inflate(20, 20)
                pg.draw.rect(surface, HIGHLIGHT_COLOR, highlight_rect, border_radius=10)

            surface.blit(msg, rect)
            
    def run_hand_detection(self):
        while self.detecting:
            detected_gesture = hand_detection.get_detected_gesture()

            # Only update current_gesture if enough time has passed since the last update
            if detected_gesture:
                current_time = time.time()
                if self.last_gesture_time is None or current_time - self.last_gesture_time >= self.gesture_debounce_time:
                    with self.gesture_lock:
                        self.current_gesture = detected_gesture
                        self.last_gesture_time = current_time

                        if detected_gesture == "move_right":
                            self.index = (self.index + 1) % len(OPTIONS)
                            if self.index == 0:
                                self.index = (self.index + 1) % len(OPTIONS)
                        elif detected_gesture == "move_left":
                            self.index = (self.index - 1) % len(OPTIONS)
                            # Skip "STORY MODE" (index 0) when navigating
                            if self.index == 0:
                                self.index = (self.index - 1) % len(OPTIONS)
                        elif detected_gesture in ("punch_left", "punch_right"):
                            self.pressed_enter()

    def get_event(self, event):
        """Handle key events using ControlManager."""
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            action = self.control_manager.handle_key_event(event)

            if event.type == pg.KEYDOWN:
                if action == "move_right":
                    self.index = (self.index + 1) % len(OPTIONS)
                    if self.index == 0:
                        self.index = (self.index + 1) % len(OPTIONS)
                elif action == "move_left":
                    self.index = (self.index - 1) % len(OPTIONS)
                    # Skip "STORY MODE" (index 0) when navigating
                    if self.index == 0:
                        self.index = (self.index - 1) % len(OPTIONS)
                elif action == "punch_left" or action == "punch_right":
                    self.pressed_enter()

    def pressed_enter(self):
        """Set the next state based on the selected option."""
        selected_option = OPTIONS[self.index]
        if selected_option == "QUICK PLAY":
            self.next = "ENEMYSELECT"
            self.done = True
        elif selected_option == "EXIT":
            pg.quit()
            sys.exit()
        elif selected_option == "STORY MODE":
            pass  # Do nothing for STORY MODE
        else:
            self.next = selected_option
            self.done = True