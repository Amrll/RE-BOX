import os
import threading
import time

import pygame as pg
from .. import state_machine, prepare, hand_detection
from ..components.enemy.enemy import Enemy
from ..controls import DEFAULT_CONTROLS


class EnemySelect(state_machine._State):
    def __init__(self):
        super(EnemySelect, self).__init__()
        self.last_gesture_time = None
        self.current_gesture = None
        self.gesture_lock = threading.Lock()
        self.detecting = True
        self.gesture_debounce_time = .5
        self.detection_thread = threading.Thread(target=self.run_hand_detection, daemon=True)
        self.detection_thread.start()


        self.enemies = [
            {"name": "emoji", "health": 5, "warning_duration": 1000, "image": prepare.GFX["enemies"]["emoji"]["portrait"]},
            {"name": "skully", "health": 10, "warning_duration": 800, "image": prepare.GFX["enemies"]["skull"]["portrait"]},
            {"name": "tank", "health": 15, "warning_duration": 2000, "image": prepare.GFX["backgrounds"]["ring1"]},
            {"name": "balanced", "health": 10, "warning_duration": 1500, "image": prepare.GFX["backgrounds"]["ring1"]},
        ]
        self.selected_index = 0
        self.font = pg.font.Font(None, 36)
        self.grid_cell_size = 80
        self.grid_cols = 5
        self.reset_game_state()

        self.music_playing = False
        self.music_file = prepare.MUSIC["select_enemy"]

        self.choose_sound = pg.mixer.Sound(prepare.SFX["choosing"])
        self.punch_sound = pg.mixer.Sound(prepare.SFX["hit"])
        self.play_sound = False


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

    def run_hand_detection(self):
        while self.detecting:
            detected_gesture = hand_detection.get_detected_gesture()

            # Only update current_gesture if enough time has passed since the last update
            if detected_gesture:
                current_time = time.time()
                if self.last_gesture_time is None or current_time - self.last_gesture_time >= self.gesture_debounce_time:
                    with self.gesture_lock:
                        self.current_gesture = detected_gesture
                        self.last_gesture_time = current_time

                        if detected_gesture == "move_right":
                            if self.play_sound:
                                self.choose_sound.play()
                            self.selected_index = (self.selected_index + 1) % len(self.enemies)
                        elif detected_gesture == "move_left":
                            if self.play_sound:
                                self.choose_sound.play()
                            self.selected_index = (self.selected_index - 1) % len(self.enemies)
                        elif detected_gesture in ("punch_left", "punch_right"):
                            if self.play_sound:
                                self.punch_sound.play()
                            pg.mixer.music.stop()
                            self.next = "GAME"
                            self.done = True

    def get_event(self, event):
        """Handle keyboard input for enemy selection."""
        if event.type == pg.KEYDOWN:
            if event.key == DEFAULT_CONTROLS["move_left"]:
                if self.play_sound:
                    self.choose_sound.play()
                self.selected_index = (self.selected_index - 1) % len(self.enemies)
            elif event.key == DEFAULT_CONTROLS["move_right"]:
                if self.play_sound:
                    self.choose_sound.play()
                self.selected_index = (self.selected_index + 1) % len(self.enemies)
            elif event.key == DEFAULT_CONTROLS["move_up"]:
                if self.play_sound:
                    self.choose_sound.play()
                self.selected_index = max(0, self.selected_index - self.grid_cols)
            elif event.key == DEFAULT_CONTROLS["move_down"]:
                if self.play_sound:
                    self.choose_sound.play()
                self.selected_index = min(len(self.enemies) - 1, self.selected_index + self.grid_cols)
            elif event.key == DEFAULT_CONTROLS["punch_left"] or event.key == DEFAULT_CONTROLS["punch_right"]:
                if self.play_sound:
                    self.punch_sound.play()
                pg.mixer.music.stop()
                self.next = "GAME"
                self.done = True



    def startup(self, now, persistent):
        """Called when transitioning to this state."""
        self.persist = persistent
        self.reset_game_state()

        # Start background music
        if not self.music_playing:
            pg.mixer.music.load(self.music_file)
            pg.mixer.music.play(-1)  # Loop indefinitely
            self.music_playing = True

        self.play_sound = True

    def reset_game_state(self):
        """Reset game state variables when restarting."""
        self.selected_index = 0
        self.done = False
        if "selected_enemy" in self.persist:
            del self.persist["selected_enemy"]

    def update(self, keys, now):
        pass

    def draw(self, surface, interpolate):
        """Render the enemy selection screen."""
        surface.fill((0, 0, 0))  # Clear screen with black
        self.render_current_enemy(surface)
        self.render_enemy_grid(surface)

    def cleanup(self):
        """Store selected enemy data in the persistent dictionary."""
        self.detecting = False
        self.play_sound = False
        self.persist["selected_enemy"] = self.enemies[self.selected_index]
        return self.persist


def render_font(font, size, msg, color=(255, 255, 255)):
    selected_font = pg.font.Font(prepare.FONTS[font], size)
    return selected_font.render(msg, 1, color)
