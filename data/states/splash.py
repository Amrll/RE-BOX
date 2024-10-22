"""
The splash screen of the game. The first thing the user sees.
"""

import pygame as pg
from .. import prepare, state_machine
from ..controls import DEFAULT_CONTROLS

class Splash(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "TITLE"
        self.timeout = 5  # Time in seconds before moving to the next state

        # Load the splash image with transparency (using convert_alpha)
        self.original_image = prepare.GFX['misc']['splash'].copy().convert_alpha()  # Original image for scaling
        self.rect = self.original_image.get_rect(center=prepare.SCREEN_RECT.center)

        # Scale settings for POV zoom-in effect
        self.scale_factor = 0.05  # Start small, like it's far away
        self.max_scale = 1.3
        self.zoom_speed = 9  # Speed at which the image zooms in

        # Current size of the splash image (starting small)
        self.image = pg.transform.scale(self.original_image,
                                        (int(self.rect.width * self.scale_factor),
                                         int(self.rect.height * self.scale_factor)))

        # Rect for positioning the image
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)

    def update(self, keys, now):
        self.now = now

        # Zoom-in effect: increase scale factor over time
        if self.scale_factor < self.max_scale:
            self.scale_factor += self.zoom_speed * 0.01  # Increment scale factor
            new_width = int(self.original_image.get_width() * self.scale_factor)
            new_height = int(self.original_image.get_height() * self.scale_factor)

            # Scale the image based on the new factor
            self.image = pg.transform.scale(self.original_image, (new_width, new_height))

            # Re-center the image on the screen
            self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)

        # Automatically move to the next screen after the timeout
        if self.now - self.start_time > 1000.0 * self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        # Fill the background with black before drawing the image
        surface.fill((0, 0, 0))  # Black background

        # Blit the zooming image onto the screen
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == DEFAULT_CONTROLS["punch_left"] or event.key == DEFAULT_CONTROLS["punch_right"]:
                self.done = True
