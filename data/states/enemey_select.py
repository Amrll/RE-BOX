import pygame as pg
from .. import state_machine, prepare
from ..components.enemy.enemy import Enemy


class EnemySelect(state_machine._State):
    def __init__(self):
        super(EnemySelect, self).__init__()
        self.enemies = [
            {"name": "emoji", "health": 5, "warning_duration": 1000, "image": prepare.GFX["enemies"]["emoji"]["portrait"]},
            {"name": "speedy", "health": 7, "warning_duration": 1000, "image": prepare.GFX["backgrounds"]["ring1"]},
            {"name": "tank", "health": 15, "warning_duration": 2000, "image": prepare.GFX["backgrounds"]["ring1"]},
            {"name": "balanced", "health": 10, "warning_duration": 1500, "image": prepare.GFX["backgrounds"]["ring1"]},
        ]
        self.selected_index = 0
        self.font = pg.font.Font(None, 36)
        self.grid_cell_size = 80
        self.grid_cols = 5


    def render_current_enemy(self, surface):
        """Render the portrait and details of the currently selected enemy."""
        enemy = self.enemies[self.selected_index]

        # Get the screen width and height for centering
        screen_width, screen_height = surface.get_size()

        # Calculate centered position of the portrait
        portrait_width, portrait_height = 200, 200
        portrait_x = (screen_width - portrait_width) // 2 - 200
        portrait_y = 250

        # Draw enemy portrait
        portrait_rect = pg.Rect(portrait_x, portrait_y, portrait_width, portrait_height)
        pg.draw.rect(surface, (50, 50, 50), portrait_rect)
        portrait_image = enemy["image"]  # Use preloaded image
        portrait_image = pg.transform.scale(portrait_image, (portrait_width, portrait_height))
        surface.blit(portrait_image, (portrait_rect.x, portrait_rect.y))

        # Use the Fixedsys500c font for text
        font = pg.font.Font(prepare.FONTS["Fixedsys500c"], 36)

        text_x = portrait_x + portrait_width + 100

        name_text = font.render(enemy["name"], True, (255, 255, 255))
        speed_text = font.render(f"Speed: {enemy['warning_duration'] // 100}", True, (255, 255, 255))
        strength_text = font.render(f"Strength: {enemy['health']}", True, (255, 255, 255))

        name_y = portrait_y + 25
        speed_y = name_y + 50  # Spacing between lines
        strength_y = speed_y + 50

        # Draw the text
        surface.blit(name_text, (text_x, name_y))
        surface.blit(speed_text, (text_x, speed_y))
        surface.blit(strength_text, (text_x, strength_y))

    def render_enemy_grid(self, surface):
        """Render enemy options in a grid layout."""
        # Set the grid size: 10 columns and 3 rows
        grid_cols = 10
        grid_rows = 3

        # Calculate the total grid width and height
        total_width = grid_cols * self.grid_cell_size
        total_height = grid_rows * self.grid_cell_size

        # Center the grid horizontally and vertically
        center_x = (prepare.SCREEN_RECT.width - total_width) // 2
        center_y = (prepare.SCREEN_RECT.height - total_height) // 2 + 200

        # Iterate over each grid cell (up to 30 total cells: 10 columns * 3 rows)
        for row in range(grid_rows):
            for col in range(grid_cols):
                # Calculate position of the current cell
                x = center_x + col * self.grid_cell_size
                y = center_y + row * self.grid_cell_size

                # Calculate index for this cell (max of 30 possible cells)
                index = row * grid_cols + col

                # Draw the cell background first (empty or with enemy)
                if index < len(self.enemies):
                    enemy = self.enemies[index]
                    color = (255, 255, 255) if index == self.selected_index else (
                    100, 100, 100)  # Highlight selected enemy
                    # Draw the background cell
                    rect = pg.Rect(x, y, self.grid_cell_size - 10, self.grid_cell_size - 10)
                    pg.draw.rect(surface, color, rect)

                    # Crop and fit the enemy's portrait inside the cell
                    portrait = pg.transform.scale(enemy["image"], (
                    self.grid_cell_size - 20, self.grid_cell_size - 20))  # Scale the portrait to fit

                    # Ensure the portrait fits inside the box, and it is not drawn outside
                    portrait_rect = pg.Rect(x + 5, y + 5, self.grid_cell_size - 10, self.grid_cell_size - 10)
                    surface.blit(portrait, portrait_rect)
                else:
                    # Empty cell, make it darker
                    color = (50, 50, 50)  # Darker color for empty cells
                    rect = pg.Rect(x, y, self.grid_cell_size - 10, self.grid_cell_size - 10)
                    pg.draw.rect(surface, color, rect)

    def handle_input(self, keys):
        """Handle keyboard input for enemy selection."""
        if keys[pg.K_UP]:
            self.selected_index = max(0, self.selected_index - self.grid_cols)
        elif keys[pg.K_DOWN]:
            self.selected_index = min(len(self.enemies) - 1, self.selected_index + self.grid_cols)
        elif keys[pg.K_LEFT]:
            self.selected_index = (self.selected_index - 1) % len(self.enemies)
        elif keys[pg.K_RIGHT]:
            self.selected_index = (self.selected_index + 1) % len(self.enemies)
        elif keys[pg.K_RETURN]:
            self.next = "GAME"
            self.done = True

    def update(self, keys, now):
        """Update enemy selection logic."""
        self.handle_input(keys)

    def draw(self, surface, interpolate):
        """Render the enemy selection screen."""
        surface.fill((0, 0, 0))  # Clear screen with black
        self.render_current_enemy(surface)
        self.render_enemy_grid(surface)

    def cleanup(self):
        """Store selected enemy data in the persistent dictionary."""
        self.persist["selected_enemy"] = self.enemies[self.selected_index]
        return self.persist


def render_font(font, size, msg, color=(255, 255, 255)):
    selected_font = pg.font.Font(prepare.FONTS[font], size)
    return selected_font.render(msg, 1, color)
