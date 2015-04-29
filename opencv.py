__author__ = 'ryanvade'
import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def nothing(x):
    pass


lower_white = np.array([0, 0, 0], dtype=np.uint8)
upper_white = np.array([179, 255, 255], dtype=np.uint8)
cv2.namedWindow("Control", cv2.WINDOW_AUTOSIZE)
# Create trackbars in "Control" window
cv2.createTrackbar("LowH", "Control", lower_white[0], 179, nothing)
cv2.createTrackbar("HighH", "Control", upper_white[0], 179, nothing)

cv2.createTrackbar("LowS", "Control", lower_white[1], 255, nothing)
cv2.createTrackbar("HighS", "Control", upper_white[1], 255, nothing)

cv2.createTrackbar("LowV", "Control", lower_white[2], 255, nothing)
cv2.createTrackbar("HighV", "Control", upper_white[2], 255, nothing)

lastX = -1
lastY = -1

while (1):

    _, frame = cap.read()
    imgLines = frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white[0] = cv2.getTrackbarPos("LowH", "Control")
    lower_white[1] = cv2.getTrackbarPos("LowS", "Control")
    lower_white[2] = cv2.getTrackbarPos("LowV", "Control")
    upper_white[0] = cv2.getTrackbarPos("HighH", "Control")
    upper_white[1] = cv2.getTrackbarPos("HighS", "Control")
    upper_white[2] = cv2.getTrackbarPos("HighV", "Control")
    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame, frame, mask = mask)
    size = np.array([5, 5])
    cv2.erode(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cv2.dilate(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cv2.dilate(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cv2.erode(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    oMoments = cv2.moments(mask, 0)

    dM01 = int(oMoments['m01'])
    dM10 = int(oMoments['m10'])
    dArea = int(oMoments['m00'])

    if dArea >= 1000:
        posX = int(dM10 / dArea)
        posY = int(dM01 / dArea)
        if lastX >= 0 and lastY >= 0 and posX >= 0 and posY >= 0:
            cv2.line(imgLines, (posX, posY), (lastX, lastY), (0, 0, 255), 2)

        lastX = posX
        lastY = posY
    #frame = frame + imgLines
    cv2.imshow('frame', frame)
    cv2.imshow('path', imgLines)
    cv2.imshow('mask', mask)
    # cv2.imshow('res', res)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

