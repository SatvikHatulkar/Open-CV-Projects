import cv2
import numpy as np
import time
import HandTrackingModule as htm
import os

######################################
brushThickness = 15
erasorThickness = 30
######################################

folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList= []

for imPath in myList:
    images = cv2.imread(f"{folderPath}/{imPath}")
    overlayList.append(images)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 720)
# cap.set(720, 1920, 3)

detector = htm.handDetector(detectionCon=0.85)
xp, yp  = 0, 0

imgCanvas = np.zeros((720, 1920, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)


    # 2. Find Hand Landmark
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        # Tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]


        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)


        # 4. If Selection Mode - Two finger are up
        if fingers[1] and fingers[2] and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
            xp, yp  = 0, 0
            # print("Selection mode")
            # Checking for the click
            if y1 < 40:
                if 120 < x1 < 226:
                    header = overlayList[0]
                    drawColor = (0, 0, 255)
                elif 226 < x1 < 326:
                    header = overlayList[1]
                    drawColor = (0, 255, 0)
                elif 326 < x1 < 426:
                    header = overlayList[2]
                    drawColor = (255, 0, 0)
                elif 426 < x1 < 526:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

    # 5. If Drawing Mode - Index finger is up
        elif fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("Drawing mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, erasorThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, erasorThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

        else:
            print("Please any select mode")
    # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    # imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    # img = cv2.bitwise_and(img, imgInv)
    # img = cv2.bitwise_or(img, imgCanvas)



    img[0:40, 0:1920]  = header
    cv2.imshow("Image", img )
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)