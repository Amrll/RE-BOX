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

class HandTrackingDynamic:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.__mode__ = mode
        self.__maxHands__ = maxHands
        self.__detectionCon__ = detectionCon
        self.__trackCon__ = trackCon
        self.handsMp = mp.solutions.hands
        self.hands = self.handsMp.Hands(max_num_hands=self.__maxHands__, min_detection_confidence=self.__detectionCon__, min_tracking_confidence=self.__trackCon__)
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
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.lmsList, bbox

    def isFist(self):
        """Returns True if the detected hand is making a fist."""
        fingers = []
        if len(self.lmsList) != 0:
            if self.lmsList[self.tipIds[0]][1] > self.lmsList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if self.lmsList[self.tipIds[id]][2] > self.lmsList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers.count(1) == 5

    def isPunch(self, lastPosition, currentPosition):
        """Detect if a punch is happening based on position change."""
        if lastPosition is not None:
            print('punch wow')
            return (currentPosition[1] - lastPosition[1] > 50) and (abs(currentPosition[1] - lastPosition[1]) > 20)
        return False

    def detectGesture(self, lastPositions, frame=None):
        """Detect specific gestures and return corresponding actions."""
        actions = []
        if self.results.multi_hand_landmarks:
            for i in range(len(self.results.multi_hand_landmarks)):
                lmsList, bbox = self.findPosition(frame, i)
                if self.isFist():
                    actions.append('punch_right' if bbox[0] < frame.shape[1] // 2 else 'punch_left')
                    currentPos = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
                    if self.isPunch(lastPositions[i], currentPos):
                        actions.append('punch_right' if bbox[0] < frame.shape[1] // 2 else 'punch_left')
                    lastPositions[i] = currentPos
        return actions
