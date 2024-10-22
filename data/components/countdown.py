import pygame as pg
from .. import prepare

# Initialize the font here, so it's reusable.
FONT = pg.font.Font(prepare.FONTS["Fixedsys500c"], 150)


class Countdown:
    def __init__(self, duration=4000):
        """
        Initializes the countdown logic.
        :param duration: Total countdown time in milliseconds (default is 4000ms).
        """
        self.duration = duration
        self.start_time = 0
        self.current_count = None
        self.active = True

    def start(self):
        """Starts the countdown timer."""
        self.start_time = pg.time.get_ticks()
        self.active = True

    def update(self):
        """Updates the countdown logic based on elapsed time."""
        elapsed_time = pg.time.get_ticks() - self.start_time
        if elapsed_time >= self.duration:
            self.active = False
        else:
            # Determine which countdown number to show
            if elapsed_time < 1000:
                self.current_count = "3"
            elif elapsed_time < 2000:
                self.current_count = "2"
            elif elapsed_time < 3000:
                self.current_count = "1"
            else:
                self.current_count = "Fight!"

    def draw(self, surface):
        """Draws the countdown overlay on the screen."""
        if self.current_count:
            # Create a transparent black overlay
            overlay = pg.Surface(prepare.SCREEN_RECT.size)
            overlay.set_alpha(128)  # Set transparency (0 is fully transparent, 255 is fully opaque)
            overlay.fill((0, 0, 0))  # Fill the surface with black
            surface.blit(overlay, (0, 0))  # Draw the overlay onto the screen

            # Render the countdown text
            countdown_text = FONT.render(self.current_count, True, (255, 255, 255))  # Using Fixedsys500c font
            countdown_rect = countdown_text.get_rect(center=prepare.SCREEN_RECT.center)
            surface.blit(countdown_text, countdown_rect)
