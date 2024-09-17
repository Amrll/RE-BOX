"""
For hands, fists, and punch detection.
 should be able to:
        *detect if the player is gonna attack
        *idk if we should also put the tracking of location of the user here.
        *implement ni josh
"""


import cv2
import mediapipe as mp
import time
import math as math


class HandTrackingDynamic:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.__mode__ = mode
        self.__maxHands__ = maxHands
        self.__detectionCon__ = detectionCon
        self.__trackCon__ = trackCon
        self.handsMp = mp.solutions.hands
        self.hands = self.handsMp.Hands(max_num_hands=self.__maxHands__, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findFingers(self, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.handsMp.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmsList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmsList.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmsList, bbox

    def isFist(self):
        """Returns True if the detected hand is making a fist."""
        fingers = []
        if len(self.lmsList) != 0:
            # Thumb: Check if it's bent (tip is to the left of the lower joint for right hand)
            if self.lmsList[self.tipIds[0]][1] > self.lmsList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers: Check if the tips are below the second joint
            for id in range(1, 5):
                if self.lmsList[self.tipIds[id]][2] > self.lmsList[self.tipIds[id] - 2][2]:
                    fingers.append(1)  # Finger is bent
                else:
                    fingers.append(0)  # Finger is not bent

        # If all fingers are bent, it is a fist
        return fingers.count(1) == 5

    def findDistance(self, p1, p2, frame, draw=True, r=15, t=3):
        x1, y1 = self.lmsList[p1][1:]
        x2, y2 = self.lmsList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 0.255), cv2.FILLED)
        len = math.hypot(x2 - x1, y2 - y1)

        return len, frame, [x1, y1, x2, y2, cx, cy]


def main():
    ctime = 0
    ptime = 0
    cap = cv2.VideoCapture(0)
    detector = HandTrackingDynamic()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    lastPositions = [None, None]  # Track positions of fists in previous frames

    while True:
        ret, frame = cap.read()

        frame = detector.findFingers(frame)
        if detector.results.multi_hand_landmarks:
            for i in range(len(detector.results.multi_hand_landmarks)):
                lmsList, bbox = detector.findPosition(frame, i)
                if detector.isFist():
                    cv2.putText(frame, f"Fist Detected {i+1}", (10, 100 * (i + 1)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

                    # Check if a punch is happening (by detecting forward movement)
                    currentPos = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
                    if lastPositions[i] is not None:
                        # Compare y-coordinate to detect forward motion (simplified)
                        if currentPos[1] - lastPositions[i][1] > 50 and abs(currentPos[1] - lastPositions[i][1]) > 20:
                            cv2.putText(frame, "Punch Detected!", (400, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    lastPositions[i] = currentPos

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
