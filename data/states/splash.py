import threading
import time
import pygame as pg
from .. import prepare, state_machine, hand_detection
from ..components.player.player_template import Player

LOADING_BAR_COLOR = (255, 0, 0)  # Red color for the loading bar
LOADING_BAR_BG_COLOR = (100, 100, 100)

class Splash(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "TITLE"

        self.load_duration = 1000  # Time for loading process (in milliseconds)

        # Loading bar dimensions and positions
        self.bar_width = 1000
        self.bar_height = 30
        self.bar_position = (prepare.SCREEN_RECT.centerx - self.bar_width // 2, prepare.SCREEN_RECT.centery + 350)  # Position it below the animation
        self.bar_progress = 0  # To track progress

        # Initialize the player sprite to display idle animation
        self.player_surface = pg.Surface(prepare.SCREEN_RECT.size, pg.SRCALPHA)  # Create a transparent surface
        self.player = Player(self.player_surface)
        self.player.rect.x = prepare.SCREEN_RECT.centerx - 140  # Position player idle in the center
        self.player.rect.y = prepare.SCREEN_RECT.centery - 50

        # Hand gesture detection
        self.current_gesture = None
        self.gesture_lock = threading.Lock()
        self.detecting = True
        self.detection_thread = threading.Thread(target=self.run_hand_detection, daemon=True)
        self.detection_thread.start()
        self.gesture_detected = False
        self.start_time = None  # Start time for the loading process (None initially)
        self.last_gesture_time = time.time()
        self.gesture_debounce_time = 1  # 300 ms debounce time

    def run_hand_detection(self):
        while self.detecting:
            detected_gesture = hand_detection.get_detected_gesture()

            # Only update current_gesture if enough time has passed since the last update
            if detected_gesture:
                current_time = time.time()
                with self.gesture_lock:
                    self.current_gesture = detected_gesture
                    self.last_gesture_time = current_time

    def update(self, keys, now):
        """Update the loading screen state."""

        # Start the loading time once gesture is detected
        with self.gesture_lock:
            if self.current_gesture is not None:
                # Detect the gesture once, and only if the gesture hasn't been processed yet
                if not self.gesture_detected:
                    self.gesture_detected = True
                    # Initialize the start time once the gesture is detected
                    self.start_time = pg.time.get_ticks()

        # Track elapsed time only if the gesture is detected
        if self.gesture_detected and self.start_time is not None:
            elapsed_time = now - self.start_time
            self.bar_progress = min(elapsed_time / self.load_duration, 1)  # Progress goes from 0 to 1

            if elapsed_time > self.load_duration:
                self.done = True
                self.detecting = False

        # Update the player's idle animation
        self.player.update(now, keys, None)

    def draw(self, surface, interpolate):
        """Draw the loading screen."""
        surface.fill((0, 0, 0))  # Black background

        # Draw player idle animation in the center
        self.player_surface.fill((0, 0, 0, 0))
        self.player.draw(self.player_surface)
        surface.blit(self.player_surface, (0, 0))

        # Draw the loading bar background (gray)
        pg.draw.rect(surface, LOADING_BAR_BG_COLOR, (*self.bar_position, self.bar_width, self.bar_height))

        # Draw the loading bar progress (red)
        current_bar_width = self.bar_width * self.bar_progress  # Width based on progress
        pg.draw.rect(surface, LOADING_BAR_COLOR, (*self.bar_position, current_bar_width, self.bar_height))

        self.note = render_font("Fixedsys500c", 30, "Initializing Assets...", (255, 255, 255))

        # Calculate the position of the note below the player
        center_x = prepare.SCREEN_RECT.centerx
        center_y = self.player.rect.bottom + 350  # 20px below the player's bottom

        self.rect = self.note.get_rect(center=(center_x, center_y))

        # Draw the note on the screen
        surface.blit(self.note, self.rect)

    def get_event(self, event):
        pass


def render_font(font, size, msg, color=(255, 255, 255)):
    selected_font = pg.font.Font(prepare.FONTS[font], size)
    return selected_font.render(msg, 1, color)
