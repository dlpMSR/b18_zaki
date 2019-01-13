from .mass import Mass

class StatsOfOneFrame(object):
    def __init__(self, preprocessedFrame):
        self.frame = preprocessedFrame
        self.posInDepthDirection
        self.lengthOfB
        self.lengthOfC
        self.surfaceOfD
        self.isDetected = false

    def sakicho(img, offset):
        width = img.shape[1]
        for i in range(offset, width):
                line = img[:, i]
                test = np.where(line==255)
                if test[0].size != 0:
                    tip = (i, test[0][0])
                    break
        return tip
     

