import pygame as pg

def draw_rounded_rect(surface, color, rect, radius):
    """Helper function to draw a rectangle with rounded corners."""
    pg.draw.rect(surface, color, rect, border_radius=radius)

def draw_enemy_health(surface, enemy, hud, screen_rect):
    """Draw the enemy health bar with rounded corners."""
    health_bar_width = 800
    health_bar_height = 30
    health_ratio = enemy.health / enemy.initial_health  # Use enemy's actual health
    current_health_bar_width = health_bar_width * health_ratio

    # Draw enemy health bar with rounded corners
    health_bar_x = screen_rect.centerx - health_bar_width // 2
    health_bar_y = 160
    border_radius = 10  # Radius for rounded corners

    # Background (gray) health bar
    background_rect = pg.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
    draw_rounded_rect(surface, (128, 128, 128), background_rect, border_radius)

    # Current health (red) bar with rounded corners
    current_health_rect = pg.Rect(health_bar_x, health_bar_y, current_health_bar_width, health_bar_height)
    draw_rounded_rect(surface, (255, 0, 0), current_health_rect, border_radius)

    # Draw enemy name above health bar
    enemy_name_text = hud.render(enemy.enemy_name, True, (255, 255, 255))
    surface.blit(enemy_name_text, (screen_rect.centerx - enemy_name_text.get_width() // 2, 130))
