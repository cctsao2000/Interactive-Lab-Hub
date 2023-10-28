import cv2
import mediapipe as mp

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self,image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
                if id == 8:
                    cv2.circle(image,(cx,cy), 15 , (255,255,255), cv2.FILLED)
        return lmlist

def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()
    in_range = 0
    while True:
        success,image = cap.read()
        image = cv2.flip(image,1)
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        cv2.putText(image, 'Capture', (80, 280), cv2.FONT_HERSHEY_PLAIN,2,(1, 1, 1),2)
        cv2.rectangle(image,(100,300),(200,400),(1,1,1),5)
        if len(lmList) != 0:
            index_finger_pos = lmList[8]
            print(index_finger_pos)
            if index_finger_pos[1] in range(100,200):
                if index_finger_pos[2] in range(300,400):
                    in_range += 1   
            if in_range > 30:
                print('success')
                cv2.imwrite('photo.png', image)
                in_range = 0
        cv2.imshow("Video",image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()