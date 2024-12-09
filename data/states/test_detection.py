"""
template for quick use
"""
import threading

from .. import state_machine, hand_detection


class TestDetection(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.detecting = True
        self.gesture_lock = threading.Lock()
        self.detection_thread = threading.Thread(target=self.run_hand_detection, daemon=True)
        self.detection_thread.start()

    def run_hand_detection(self):
        while self.detecting:
            detected_gesture = hand_detection.get_detected_gesture()

    def update(self, keys, now):
        pass

    def draw(self, surface, interpolate):
        pass

    def get_event(self, event):
        pass
