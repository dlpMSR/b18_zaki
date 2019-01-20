import numpy as np
import cv2


class ImageProcessing(object):
    def __init__(self, frame):
        self.image = frame

    def _hsvMask(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        LOWERRED = np.array([200, 100, 100])
        UPPERRED = np.array([310, 255, 255])
        maskedImage = cv2.inRange(hsv, LOWERRED, UPPERRED)
        return maskedImage

    def _filter(self, img):
        filter_3x3 = np.array([[0, -1,  0],
                               [0,  1,  0],
                               [0,  0,  0]], np.float32)
        filteredImage = cv2.filter2D(img, -1, filter_3x3)
        return filteredImage

    def _removeNoiseByLaveling(self, binarizedImage):
        labelStats = cv2.connectedComponentsWithStats(binarizedImage)
        masses = labelStats[2]
        for mass in masses:
            if mass[4] < 300:
                cv2.rectangle(binarizedImage, (mass[0], mass[1]),
                              (mass[0] + mass[2], mass[1] + mass[3]), 0, -1)
        return binarizedImage

    def preprocessing(self):
            hsv = self._hsvMask(self.image)
            noiseRemovedImage = self._removeNoiseByLaveling(hsv)
            return noiseRemovedImage

    def generateHighlightedSurfaceImage(self, frameWithStatus):
        hilightedImage = self.image
        if frameWithStatus.isDetected() == True:
            surface = frameWithStatus.D.surface
            for i in range(len(surface[0])):
                hilightedImage[surface[1][i], surface[0][i]] = (0, 255, 0)
        return hilightedImage

    def generateOutputImage(self, frameWithStatus):
        output_image = self.image
        font = cv2.FONT_HERSHEY_SIMPLEX
        if frameWithStatus.isDetected() == True:
            B = frameWithStatus.B
            C = frameWithStatus.C
            D = frameWithStatus.D
            cv2.line(output_image, B.getBottomLine()[0], B.getBottomLine()[1], (0, 255, 0), 10)
            cv2.putText(output_image, 'B:{}'.format(B.length),
                        (B.centroid[0], B.centroid[1]-30), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.line(output_image, C.getBottomLine()[0], C.getBottomLine()[1], (0, 255, 0), 10)
            cv2.putText(output_image, 'C:{}'.format(C.length),
                        (C.centroid[0], C.centroid[1]-30), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.line(output_image, B.rearEndCoordinates, (B.rearEndCoordinates[0], C.frontEndCoordinates[1]), (255, 0, 255), 5)
            cv2.line(output_image, D.getBottomLine()[0], D.getBottomLine()[1], (255, 255, 0), 10)
            cv2.rectangle(output_image, (D.maxOfHeight[0]-20, D.maxOfHeight[1]), (D.maxOfHeight[0]+20, D.getBottomLine()[0][1]), (255, 255, 0), thickness=-1)
            cv2.putText(output_image, 'D_height:{}'.format(D.getBottomLine()[0][1]-D.maxOfHeight[1]),
                        (D.centroid[0]+200, D.centroid[1]-30), font, 3, (255, 255, 0), 3, cv2.LINE_AA)
        return output_image