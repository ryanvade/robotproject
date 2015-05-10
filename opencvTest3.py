#!/usr/bin/env python

# this code was used to make:
# "OpenCV motion tracking with python code"
#  https://www.youtube.com/watch?v=EADWZatXnAU&feature=plcp

import os
import cv2 as cv
import time
import sys
import math
import re
from ConfigParser import *


class Source:
    def __init__(self, id, flip=True):
        self.capture = cv.CaptureFromCAM(0)

    def grab_frame(self):
        self.frame = cv.QueryFrame(self.capture)
        if not self.frame:
            print
            "can't grab frame"
            sys.exit(2)
        cv.Flip(self.frame, None, 1)
        return self.frame


class Setup:
    def __init__(self):
        self.LoadIniData()
        self.source = Source(self.cameraid)
        self.count = -1
        self.storage = cv.CreateMemStorage(0)
        self.last = 0
        self.old_center = (0, 0)
        self.orig = self.source.grab_frame()

        self.width = self.orig.width
        self.height = self.orig.height
        self.size = (self.width, self.height)
        self.smallheight = self.working_height
        self.smallwidth = int(self.width * self.smallheight / self.height * 1.0)
        self.smallsize = (self.smallwidth, self.smallheight)

        # alloc mem for images used at various stages
        self.small = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_8U, 3)
        self.motion = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_8U, 3)
        self.eye = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_8U, 3)
        self.mhi = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_32F, 1)
        self.orient = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_32F, 1)
        self.segmask = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_32F, 1)
        self.mask = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_8U, 1)
        self.temp = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_8U, 3)
        self.buf = range(10)
        for i in range(self.n_frames):
            self.buf[i] = cv.CreateImage(self.smallsize, cv.IPL_DEPTH_8U, 1)
            cv.SetZero(self.buf[i])

        self.combined = cv.CreateImage((self.smallwidth * self.xwindows, self.smallheight), cv.IPL_DEPTH_8U, 3)

        if self.store:
            self.writer = cv.CreateVideoWriter(self.output, 0, 15, cv.GetSize(self.combined), 1)

        # make window
        cv.NamedWindow("Motion Detection")

        cv.CreateTrackbar('Height', 'Motion Detection', self.height_value, 100, self.change_height)

        cv.CreateTrackbar('Jitter', 'Motion Detection', self.jitter_value, 100, self.change_jitter)

    def LoadIniData(self):
        FileName = re.sub(r'\.py$', "", os.path.abspath(__file__)) + '.ini'
        self.cp = ConfigParser()
        try:
            self.cp.readfp(open(FileName, 'r'))
        # f.close()
        except IOError:
            raise Exception, 'NoFileError'

        self.store = self.cp.getboolean('Variables', 'store')
        self.cameraid = self.cp.getint('Variables', 'cameraid')
        self.output = self.cp.get('Variables', 'output')
        self.FPS = self.cp.getint('Variables', 'fps')
        self.xwindows = self.cp.getint('Variables', 'xwindows')
        self.working_height = self.cp.getint('Variables', 'working_height')
        self.clocks_per_sec = self.cp.getfloat('Variables', 'clocks_per_sec')
        self.mhi_duration = self.cp.getfloat('Variables', 'mhi_duration')
        self.max_time_delta = self.cp.getfloat('Variables', 'max_time_delta')
        self.min_time_delta = self.cp.getfloat('Variables', 'min_time_delta')
        self.n_frames = self.cp.getint('Variables', 'n_frames')
        self.height_value = self.cp.getint('Variables', 'height_value')
        self.jitter_value = self.cp.getint('Variables', 'jitter_value')

        return

    def process_motion(self, img):
        center = (-1, -1)
        # a lot of stuff from this section was taken from the code motempl.py,
        #  openCV's python sample code
        timestamp = time.clock() / self.clocks_per_sec  # get current time in seconds
        idx1 = self.last
        cv.CvtColor(img, self.buf[self.last], cv.CV_BGR2GRAY)  # convert frame to grayscale
        idx2 = (self.last + 1) % self.n_frames
        self.last = idx2
        silh = self.buf[idx2]
        cv.AbsDiff(self.buf[idx1], self.buf[idx2], silh)  # get difference between frames
        cv.Threshold(silh, silh, 30, 1, cv.CV_THRESH_BINARY)  # and threshold it
        cv.UpdateMotionHistory(silh, self.mhi, timestamp, self.mhi_duration)  # update MHI
        cv.ConvertScale(self.mhi, self.mask, 255. / self.mhi_duration,
                        (self.mhi_duration - timestamp) * 255. / self.mhi_duration)
        cv.SetZero(img)
        cv.Merge(self.mask, None, None, None, img)
        cv.CalcMotionGradient(self.mhi, self.mask, self.orient, self.max_time_delta, self.min_time_delta, 3)
        seq = cv.SegmentMotion(self.mhi, self.segmask, self.storage, timestamp, self.max_time_delta)
        inc = 0
        a_max = 0
        max_rect = -1

        # there are lots of things moving around
        #  in this case just find find the biggest change on the image
        for (area, value, comp_rect) in seq:
            if comp_rect[2] + comp_rect[3] > 60:  # reject small changes
                if area > a_max:
                    a_max = area
                    max_rect = inc
            inc += 1

        # found it, now just do some processing on the area.
        if max_rect != -1:
            (area, value, comp_rect) = seq[max_rect]
            color = cv.CV_RGB(255, 0, 0)
            silh_roi = cv.GetSubRect(silh, comp_rect)
            # calculate number of points within silhouette ROI
            count = cv.Norm(silh_roi, None, cv.CV_L1, None)

            # this rectangle contains the overall motion ROI
            cv.Rectangle(self.motion, (comp_rect[0], comp_rect[1]),
                         (comp_rect[0] + comp_rect[2],
                          comp_rect[1] + comp_rect[3]), (0, 0, 255), 1)

            # the goal is to report back a center of movement contained in a rectangle
            # adjust the height based on the number generated by the slider bar
            h = int(comp_rect[1] + (comp_rect[3] * (float(self.height_value) / 100)))
            # then calculate the center
            center = ((comp_rect[0] + comp_rect[2] / 2), h)

        return center


    def pipeline(self):
        presentation = []
        self.orig = self.source.grab_frame()
        cv.Resize(self.orig, self.small)

        size = self.smallsize

        # store the raw image
        presentation.append((self.small, 'raw'))

        self.motion = cv.CloneImage(self.small)

        # location of the thingy moving on the screen is defined by center
        center = self.process_motion(self.motion)

        # if an object is found draw the circle on the same location.
        if center != (-1, -1):
            cv.Circle(self.motion, center, cv.Round(30), cv.CV_RGB(0, 225, 0), 3, cv.CV_AA, 0)
        # store the picture
        presentation.append((self.motion, 'motion'))

        ####
        # processing of final image
        self.eye = cv.CloneImage(self.small)  # get a copy

        # if the center was not found, just draw the center on the old location.
        if center == (-1, -1):
            cv.Circle(self.eye, self.old_center, cv.Round(30 * .7), cv.CV_RGB(0, 225, 0), 3, cv.CV_AA, 0)
            self.old_center = self.old_center
        else:
            # anti-jittering section
            x1 = self.old_center[0]
            y1 = self.old_center[1]
            x2 = center[0]
            y2 = center[1]
            dx = x2 - x1
            dy = y2 - y1
            d = math.sqrt((dx) ** 2 + (dy) ** 2)  # calculate a distance from old location to new.
            angle = math.atan2(dy, dx)  # get an angle while we're doing the math

            if d > self.jitter_value:  # if the distance is really far....
                self.old_center = (x2, y2)
                # calculate a near point that exists on the line between the old and new point
                self.old_center = (cv.Round(x1 + self.jitter_value * math.cos(angle)),
                                   cv.Round(y1 + self.jitter_value * math.sin(angle)))
                # and draw it
                cv.Circle(self.eye, self.old_center, 30, cv.CV_RGB(255, 0, 0), 3, cv.CV_AA, 0)
            else:  # the distance is not far so just draw it
                self.old_center = (x2, y2)
                cv.Circle(self.eye, self.old_center, 30, cv.CV_RGB(0, 225, 0), 3, cv.CV_AA, 0)

        presentation.append((self.eye, 'final'))

        # combine and show the results
        combined = self.combine_images(presentation)
        cv.ShowImage('Motion detection', combined)

        if self.store:
            cv.WriteFrame(self.writer, self.combined)

    def change_jitter(self, position):
        self.jitter_value = position

    def change_height(self, position):
        self.height_value = position

    def combine_images(self, images):

        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1.4, 1.4, 0, 2, 8)

        for i, (image, name) in enumerate(images):
            if image.nChannels == 1:
                cv.Merge(image, image, image, None, self.temp)
            else:
                cv.Copy(image, self.temp)
            xoffset = (i % self.xwindows) * self.smallsize[0]
            yoffset = (i / self.xwindows) * self.smallsize[1]
            cv.SetImageROI(self.combined, (xoffset, yoffset, self.smallsize[0],
                                           self.smallsize[1]))
            cv.Copy(self.temp, self.combined)
            cv.PutText(self.combined, name, (5, 40), font, (30, 200, 200))
            cv.ResetImageROI(self.combined)
        return self.combined

    def run(self):
        while True:
            t = time.time()
            self.pipeline()
            # not sure what this is about.
            wait = max(2, (1000 / self.FPS) - int((time.time() - t) * 1000))
            cv.WaitKey(wait)


if __name__ == '__main__':
    s = Setup()
    s.run()