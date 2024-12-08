import pygame as pg
from data.animation_manager import AnimationManager


class Player(pg.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)

        # Only the necessary attributes for animation display
        self.surface = surface
        self.rect = pg.Rect(400, 300, 0, 0)  # Place player sprite at the center or preferred position

        self.animation_manager = AnimationManager()

    def update(self, now, keys, enemy):
        """Update player logic. This will be just for animation on the loading screen."""
        pass  # No need to handle gestures or movement

    def draw(self, surface):
        """Draw the player animation."""
        # Play idle animation for the player
        self.animation_manager.play_animation("Idle_player", surface, (self.rect.x, self.rect.y))

