import pygame as pg

def draw_player_health(surface, player_health, animation_manager):
    """Draw the player's health using the animated heart images."""
    # Define the position for the first heart
    heart_x = 250
    heart_y = 140
    heart_spacing = 60  # Space between hearts

    # Draw a heart for each unit of player health
    for i in range(player_health):
        heart_position = (heart_x + i * heart_spacing, heart_y)
        # Play the heart animation for each health point
        animation_manager.play_animation("Heart", surface, heart_position)
