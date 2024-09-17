"""
This module contains the possible keys for our game

for easy implementation of the opencv controls later in the project phase
"""

import pygame as pg


DEFAULT_CONTROLS = {
    'punch_left': pg.K_j,
    'punch_right': pg.K_k,
    'move_left': pg.K_a,
    'move_right': pg.K_d,
    'move_up': pg.K_w,
    'move_down': pg.K_s
}


class ControlManager:
    def __init__(self):
        self.controls = DEFAULT_CONTROLS
        self.action_map = {}

    def update_controls(self, key, action):
        """Update control mappings."""
        if key in self.controls:
            self.controls[key] = action

    def get_action(self, key):
        """Return the action associated with a key."""
        return self.controls.get(key, None)

    def handle_key_event(self, key_event):
        """Handle a key press event."""
        action = self.get_action(key_event.key)
        if action:
            self.execute_action(action)

    def execute_action(self, action):
        """Execute the action corresponding to the key pressed."""
        # Define what happens when an action is executed
        print(f"Action executed: {action}")
