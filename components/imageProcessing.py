import numpy as np
import cv2


class ImageProcessing(object):
    def __init__(self, frame):
        self.image = frame
    
    def preprocessing(self):
        hsv = self._hsvMask(self.image)
        noiseRemovedImage = self._removeNoiseByLaveling(hsv)
        return noiseRemovedImage

    def generateHighlightedSurfaceImage(self, frameWithStatus):
        hilightedImage = self.image
        if frameWithStatus.isDetected()==True:
            surface = frameWithStatus.surfaceOfD
            for i in range(len(surface[0])):
                hilightedImage[surface[1][i], surface[0][i]] = (0, 255, 0)
        return hilightedImage 

    def _hsvMask(self, img):
        #閾値が固定
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        LOWERRED = np.array([200, 0, 0])
        UPPERRED = np.array([310, 255, 255])
        maskedImage = cv2.inRange(hsv, LOWERRED, UPPERRED)
        return maskedImage
        
    def _filter(self, img):
        filter_3x3 = np.array([[ 0, -1,  0],
                               [ 0,  1,  0],
                               [ 0,  0,  0]], np.float32)
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

    