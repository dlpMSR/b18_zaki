import numpy as np
from components.mass import Mass


class StatusOfOneFrame(object):
    def __init__(self, preprocessedFrame):
        self.frame = preprocessedFrame
        self.B, self.C, self.D = self._scanOneFrame()
        self.posInDepthDirection = self._calculatePosInDepthDirection()

    def _getSakicho(self, offset):
        width = self.frame.shape[1]
        for i in range(offset, width):
            line = self.frame[:, i]
            test = np.where(line == 255)
            if test[0].size != 0:
                sakicho = (i, test[0][0])
                break
        return sakicho

    def _scanOneFrame(self):
        tip = self._getSakicho(0)
        A = Mass(self.frame, tip)
        tip = self._getSakicho(A.rearEndCoordinates[0]+1)
        B = Mass(self.frame, tip)
        tip = self._getSakicho(B.rearEndCoordinates[0]+1)
        C = Mass(self.frame, tip)
        tip = self._getSakicho(C.rearEndCoordinates[0]+1)
        D = Mass(self.frame, tip)
        return B, C, D

    def _calculatePosInDepthDirection(self):
        MinOfB = 5
        MaxOfC = 10
        LengthOfRuler = 190
        minRateOfB = MinOfB / (MinOfB+MaxOfC)
        gradientRateOfB = (1-minRateOfB) / LengthOfRuler
        rateOfB = self.B.length / (self.B.length+self.C.length)
        posInDepthDirection = (rateOfB-minRateOfB) / gradientRateOfB
        return posInDepthDirection

    def isDetected(self):
        l = self.D.length
        if 530 < l < 570:
            return True
        else:
            return False

    def getDSurface(self):
        height = self.frame.shape[0]
        y = height - self.D.surface[1]
        y = y - y.min()
        return np.vstack((self.D.surface[0], y))