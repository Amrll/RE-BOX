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
        self.timeout = 5
        self.alpha = 0
        self.alpha_speed = 2
        self.image = prepare.GFX['misc']['splash'].copy().convert()
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)

    def update(self, keys, now):
        self.now = now
        self.alpha = min(self.alpha+self.alpha_speed, 255)
        self.image.set_alpha(self.alpha)
        if self.now-self.start_time > 1000.0*self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        surface.fill(prepare.BACKGROUND_COLOR)
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == DEFAULT_CONTROLS["punch_left"] or event.key == DEFAULT_CONTROLS["punch_right"]:
                self.done = True
