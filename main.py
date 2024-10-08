import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

target=20
timer = 0
stateResult = False
startGame = False
total = 0
score=[0,0]

while True:
    imgBG = cv2.imread("resources/bg.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime + 1
            cv2.putText(
                imgBG,
                str(int(timer)),
                (600, 375),
                cv2.FONT_HERSHEY_COMPLEX,
                3,
                (255, 0, 255),
                4,
            )

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 1, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 1, 0]:
                        playerMove = 3
                    if fingers == [0, 1, 1, 1, 1]:
                        playerMove = 4
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 5

                    num = random.randint(1, 5)
                    imgAI = cv2.imread(f"resources/{num}.png", cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 330))

                    if playerMove != num:
                        total += playerMove
                    if playerMove==num:
                      if total<target:
                        score[1]+=1
                      else:
                        score[0]+=1
                    

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 330))

    cv2.putText(
        imgBG, str(total), (605, 535), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 4
    )
    cv2.putText(imgBG, str(score[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(score[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord("s"):
        startGame = True
        initialTime = time.time()
        stateResult = False
