import numpy as np
from components.mass import Mass


class StatusOfOneFrame(object):
    def __init__(self, preprocessedFrame):
        self.frame = preprocessedFrame
        self.targets = self.scanOneFrame()
        self.lengthOfB = self.targets[0].length
        self.lengthOfC = self.targets[1].length
        self.surfaceOfD = self.targets[2].surface
        self.maxHeightOfD = self.targets[2].maxOfHeight
        self.posInDepthDirection = 0

    def getSakicho(self, offset):
        width = self.frame.shape[1]
        for i in range(offset, width):
                line = self.frame[:, i]
                test = np.where(line==255)
                if test[0].size != 0:
                    sakicho = (i, test[0][0])
                    break
        return sakicho
    
    def scanOneFrame(self):
        tip = self.getSakicho(0)
        A = Mass(self.frame, tip)
        tip = self.getSakicho(A.rearEndCoordinates[0]+1)
        B = Mass(self.frame, tip)
        tip = self.getSakicho(B.rearEndCoordinates[0]+1)
        C = Mass(self.frame, tip)
        tip = self.getSakicho(C.rearEndCoordinates[0]+1)
        D = Mass(self.frame, tip)
        return B, C, D

    def calcuratePosInDepthDirection(self):
        # 奥行方向の位置を計算する
        pass

    def isDetected(self):
        # !!閾値が固定値!!
        l = self.targets[2].length
        if 530 < l  <570:
            return True
        else:
            return False      

