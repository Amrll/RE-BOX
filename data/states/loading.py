import pygame as pg
from .. import prepare, state_machine
from ..components.player.player import Player

LOADING_BAR_COLOR = (255, 0, 0)  # Red color for the loading bar
LOADING_BAR_BG_COLOR = (100, 100, 100)  # Gray background for the loading bar

class LoadingScreen(state_machine._State):
    """
    This state represents a loading screen that is shown between transitions.
    It can be used to simulate loading times or handle resource loading.
    """
    def __init__(self):
        state_machine._State.__init__(self)
        self.load_duration = 1000  # Time in milliseconds to display the loading screen
        self.next_state = None

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

    def startup(self, now, persistent):
        """Called when the state starts up, with optional persistent data."""
        self.persist = persistent
        self.start_time = now
        self.next_state = self.persist.get("next_state", "MAINMENU")  # Default to MAINMENU if not provided
        self.load_duration = self.persist.get("load_duration", 1000)  # Default load duration

    def cleanup(self):
        """Reset state done to False."""
        self.done = False
        return self.persist

    def update(self, keys, now):
        """Update the loading screen state."""
        elapsed_time = now - self.start_time
        self.bar_progress = min(elapsed_time / self.load_duration, 1)  # Progress goes from 0 to 1

        if elapsed_time > self.load_duration:
            self.done = True
            self.next = self.next_state  # Move to the next state

        # Update the player's idle animation
        self.player.update(now, keys, None)

    def draw(self, surface, interpolate):
        """Draw the loading screen."""
        surface.fill((0, 0, 0))  # Black background

        # Draw player idle animation in the center
        self.player_surface.fill((0, 0, 0, 0))  # Clear the player surface
        self.player.draw(self.player_surface)
        surface.blit(self.player_surface, (0, 0))  # Blit player to the main surface

        # Draw the loading bar background (gray)
        pg.draw.rect(surface, LOADING_BAR_BG_COLOR, (*self.bar_position, self.bar_width, self.bar_height))

        # Draw the loading bar progress (red)
        current_bar_width = self.bar_width * self.bar_progress  # Width based on progress
        pg.draw.rect(surface, LOADING_BAR_COLOR, (*self.bar_position, current_bar_width, self.bar_height))

    def get_event(self, event):
        """Handle events (e.g., key presses)."""
        pass  # No interaction during the loading screen
