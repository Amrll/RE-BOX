"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its state_machine dictionary.
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Boxing Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw everything here

    pygame.display.update()

pygame.quit()
sys.exit()
