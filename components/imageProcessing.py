import numpy as np
import cv2


class ImageProcessing(object):
    def __init__(self, img):
        self.img_origin = img

    def _hsvMask(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        LOWER_RED = np.array([200, 100, 100])
        UPPER_RED = np.array([310, 255, 255])
        img_masked = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
        return img_masked

    def _filter(self, img):
        filter_3x3 = np.array([[0, -1,  0],
                               [0,  1,  0],
                               [0,  0,  0]], np.float32)
        img_filtered = cv2.filter2D(img, -1, filter_3x3)
        return img_filtered

    def _removeNoiseByLaveling(self, img):
        labelStats = cv2.connectedComponentsWithStats(img)
        masses = labelStats[2]
        for mass in masses:
            if mass[4] < 300:
                cv2.rectangle(img, (mass[0], mass[1]),
                              (mass[0]+mass[2], mass[1]+mass[3]), 0, -1)
        return img

    def getPreprocessedImage(self):
        hsv = self._hsvMask(self.img_origin)
        img_noiseremoved = self._removeNoiseByLaveling(hsv)
        return img_noiseremoved

    def getSurfaceHighlightedImage(self, stats_frame):
        img_highlighted = self.img_origin
        if stats_frame.isDetected():
            surface = stats_frame.D.surface
            for i in range(len(surface[0])):
                img_highlighted[surface[1][i], surface[0][i]] = (0, 255, 0)
        return img_highlighted

    def generateOutputImage(self, stats_frame, frame_num):
        img_output = self.img_origin
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_output, 'FRAME:{}'.format(frame_num),
                    (30, 100), font, 3, (0, 255, 0), 5, cv2.LINE_AA)
        if stats_frame.isDetected():
            B = stats_frame.B
            C = stats_frame.C
            D = stats_frame.D
            cv2.putText(img_output,
                        '5mm:{px}px(1px={mm})'.format(px=stats_frame.pixels_criterion, mm=stats_frame.mmppx),
                        (30, 200), font, 3, (255, 0, 255), 5, cv2.LINE_AA)
            cv2.line(img_output, B.bottom_line[0], B.bottom_line[1], (0, 255, 0), 10)
            cv2.putText(img_output, 'B:{}'.format(B.length),
                        (B.centroid[0], B.centroid[1]-30), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.line(img_output, C.bottom_line[0], C.bottom_line[1], (0, 255, 0), 10)
            cv2.putText(img_output, 'C:{}'.format(C.length),
                        (C.centroid[0], C.centroid[1]-30), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.line(img_output, B.coodinates_rear, (B.coodinates_rear[0], C.coodinates_front[1]), (255, 0, 255), 5)
            cv2.line(img_output, D.bottom_line[0], D.bottom_line[1], (255, 255, 0), 10)
            cv2.rectangle(img_output, (D.max_height[0]-20, D.max_height[1]), (D.max_height[0]+20, D.bottom_line[0][1]), (255, 255, 0), thickness=-1)
            cv2.putText(img_output, 'D_height:{px}({mm}mm)'.format(px=stats_frame.max_height, mm=stats_frame.length_measured),
                        (D.centroid[0]+200, D.centroid[1]-30), font, 3, (255, 255, 0), 3, cv2.LINE_AA)
        return img_output