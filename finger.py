import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.modelComplex,
            self.detectionCon, self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        image, handLms, self.mpHands.HAND_CONNECTIONS
                    )
        return image

    def findFingerCount(self, image):
        fingerCount = 0
        fingerTips = [4, 8, 12, 16, 20]  # Landmark IDs for finger tips

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                landmarks = hand.landmark

                # Check if thumb is extended
                thumb = landmarks[fingerTips[0]]
                if landmarks[fingerTips[0]].x < landmarks[fingerTips[0] - 1].x:
                    fingerCount += 1

                # Check if fingers are extended
                for fingerTip in fingerTips[1:]:
                    if landmarks[fingerTip].y < landmarks[fingerTip - 2].y:
                        fingerCount += 1

        return fingerCount


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    while True:
        success, image = cap.read()
        image = tracker.findHands(image)
        fingerCount = tracker.findFingerCount(image)
        cv2.putText(image, str(fingerCount), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        cv2.imshow("Finger Count", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
