"""
template for quick use
"""

from .. import state_machine

class State(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        pass

    def update(self, keys, now):
        pass

    def draw(self, surface, interpolate):
        pass

    def get_event(self, event):
        pass
