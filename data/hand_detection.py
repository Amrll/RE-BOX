import mediapipe as mp
import cv2
from scipy.stats import linregress
import numpy as np
import time
import threading
# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Variables for smoothing hand positions
left_hand_positions = [np.array([0, 0]), np.array([0, 0])]
right_hand_positions = [np.array([0, 0]), np.array([0, 0])]
damping_factor = 0.15
cap = cv2.VideoCapture(0)

# Track areas for detecting punches
hands_area = [[], []]

# Cooldown tracking
cooldown_time = 1 # Cooldown duration in seconds
last_punch_time = {"left": 0, "right": 0}

previous_column = {"Left": "middle", "Right": "middle"}

gesture_lock = threading.Lock()
current_gesture = None

def detect_punch():
    """
    Detect punches based on hand movement slopes.
    Returns 'punch_left', 'punch_right', or None.
    """
    global left_hand_positions, right_hand_positions, hands_area, previous_column, current_gesture

    success, frame = cap.read()
    if not success:
        return None

    target_width = 640
    target_height = 480
    frame_resized = cv2.resize(frame, (target_width, target_height))

    # Convert frame to RGB
    img_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = frame.shape
    column_width = w // 3

    if results.multi_hand_landmarks:
        for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
            x_list, y_list = [], []
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)

            x_min, x_max = min(x_list), max(x_list)
            y_min, y_max = min(y_list), max(y_list)

            top_left = np.array([x_min, y_min])
            bottom_right = np.array([x_max, y_max])

            handedness = results.multi_handedness[hand_id].classification[0].label
            hand_positions = left_hand_positions if handedness == "Left" else right_hand_positions
            hand_index = 0 if handedness == "Left" else 1

            # Smooth position updates
            current_top_left = hand_positions[0] + (top_left - hand_positions[0]) * damping_factor
            current_bottom_right = hand_positions[1] + (bottom_right - hand_positions[1]) * damping_factor

            # Update hand positions
            hand_positions[0] = current_top_left
            hand_positions[1] = current_bottom_right

            # Calculate hand area
            hand_width = current_bottom_right[0] - current_top_left[0]
            hand_height = current_bottom_right[1] - current_top_left[1]
            hands_area[hand_index].append(hand_width * hand_height)


            # Detect column based on hand position (cx)
            hand_center_x = int((current_top_left[0] + current_bottom_right[0]) / 2)
            if hand_center_x < column_width:
                current_column = "right"
            elif hand_center_x < 2 * column_width:
                current_column = "middle"
            else:
                current_column = "left"

            # Trigger movement if column changes
            if current_column != previous_column[handedness]:
                previous_column[handedness] = current_column
                with gesture_lock:
                    current_gesture = f"move_{current_column}"
                    return

    current_time = int(time.time())
    # Check punch movement using slope
    if len(hands_area[0]) >= 5 and len(hands_area[1]) >= 5:
        left_slopes = linregress(range(5), hands_area[0][-5:]).slope
        right_slopes = linregress(range(5), hands_area[1][-5:]).slope

        hands_area[0] = hands_area[0][-5:]
        hands_area[1] = hands_area[1][-5:]

        if left_slopes > 600 and current_time - last_punch_time["left"] > cooldown_time:
            last_punch_time["left"] = current_time
            with gesture_lock:
                current_gesture = "punch_right"
                return

        # Right hand punch
        elif right_slopes > 600 and current_time - last_punch_time["right"] > cooldown_time:
            last_punch_time["right"] = current_time
            with gesture_lock:
                current_gesture = "punch_left"
                return

    current_gesture = None


def start_hand_detection():
    while True:
        detect_punch()


def get_detected_gesture():
    global current_gesture
    time.sleep(0.01)
    with gesture_lock:
        return current_gesture


# Run hand detection in a separate thread
hand_detection_thread = threading.Thread(target=start_hand_detection, daemon=True)
hand_detection_thread.start()
