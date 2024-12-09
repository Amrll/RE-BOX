"""
for if the player wants to use their keyboard instead
"""


import pygame as pg

DEFAULT_CONTROLS = {
    'move_left': pg.K_a,
    'move_right': pg.K_d,
    'move_up': pg.K_w,
    'move_down': pg.K_s,
    'punch_left': pg.K_j,
    'punch_right': pg.K_k,
    'select': pg.K_RETURN 
}


class ControlManager:
    def __init__(self):
        self.controls = DEFAULT_CONTROLS

    def update_controls(self, action, key):
        """Update the control mappings."""
        if action in self.controls:
            self.controls[action] = key

    def get_action(self, key):
        """Return the action associated with a key press."""
        for action, mapped_key in self.controls.items():
            if mapped_key == key:
                return action
        return None

    def handle_key_event(self, key_event):
        """Handle a key press event and return the action."""
        action = self.get_action(key_event.key)
        return action

    def execute_action(self, action):
        """Execute the action corresponding to the key pressed."""
        print(f"Action executed: {action}")
