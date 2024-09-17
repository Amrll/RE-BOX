import pygame
from .. import state_machine


class Game(state_machine._State):
    def __init__(self):
        super().__init__()
        self.player_pos = 1  # 0 = left, 1 = middle, 2 = right

    def update(self, screen, keys):
        if keys[pygame.K_LEFT]:
            self.player_pos = max(0, self.player_pos - 1)
        elif keys[pygame.K_RIGHT]:
            self.player_pos = min(2, self.player_pos + 1)

        screen.fill((100, 100, 100))  # Fill screen with another color
        # Display player based on self.player_pos
