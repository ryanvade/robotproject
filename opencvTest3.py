import os
import time
import sys
import math
import re
import cv2 as cv
import numpy as np

class Source:
    def __init__(self, id, flip=True):
        self.capture = cv.VideoCapture(0)

    def grab_frame(self):
        self.frame = self.capture.read()
        if not self.frame:
            print ("Can't grab from Frame")
            sys.exit(1)
        cv.flip(self.frame, 1, None)
        return self.frame

class Setup:
    def __init__(self):
        self.source = Source(0)
        self.count = -1
        self.last = 0
        self.old_center = (0, 0)
        self.orig = self.source.grab_frame()

        self.width = self.orig.width
        self.height = self.orig.height
        self.size = (self.width, self.height)
        self.smallHeight = 260
        self.smallWidth = int(self.width * self.smallHeight / self.height * 1.0)
        self.smallSize = (self.smallWidth, self.smallHeight)

        self.small = np.array(self.smallSize)
        self.motion = np.array(self.smallSize)
        self.mhi = np.array(self.smallSize)
        self.orient = np.array(self.smallSize)
        self.segmask = np.array(self.smallSize)
        self.mask = np.array(self.smallSize)
        self.temp = np.array(self.smallSize)
        self.buf = range(10)

        for i in range (5):
            self.buf[i] = np.zeros(self.smallSize)

        self.combined = np.array([self.smallWidth * 3, self.smallHeight])

        cv.namedWindow("Motion Detection")
        cv.createTrackbar("Height", "Motion Detection", 30, 100, self.change_height)
        cv.createTrackbar("Jitter", "Motion Detection", 20, 100, self.change_jitter)

    def process_motion(self, img):
        center = (-1, 1)
        timestamp = time.clock() / 1.0
        cv.cvtColor(img, self.buf[self.last], cv.COLOR_BGR2GRAY)
        idx2 = (self.last + 1) % 5
        idx = self.last
        self.last = idx2
        silh = self.buf[idx2]
        cv.absdiff(self.buf[idx], self.buf[idx2], silh)
        cv.threshold(silh, silh, 30, 1, cv.THRESH_BINARY)

        cv.updateMotionHistory(silh, self.mhi, timestamp, 0.2)