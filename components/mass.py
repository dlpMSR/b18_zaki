import numpy as np
from statistics import mean


class Mass(object):
    def __init__(self, img, tip):
        self.x, self.y = self.uneUne(img, tip)
        self.surface = np.array([self.x, self.y])
        self.length = abs(self.x[-1]-self.x[0])
        self.coodinates_front = (self.x[0], self.y[0])
        self.coodinates_rear = (self.x[-1], self.y[-1])
        self.centroid = (int((self.x[0]+self.x[-1])/2),
                         int((self.y[0]+self.y[-1])/2))
        self.max_height = self.getMaxofHeight()
        self.bottom_line = self.getBottomLine()

    def uneUne(self, img, tip):
        x = [tip[0]]
        y = [tip[1]]
        while True:
            pos_x = x[-1]
            pos_y = y[-1]
            scan_line = img[pos_y-20:pos_y+20, pos_x+1]
            scan_line = np.where(scan_line != 0)
            if scan_line[0].size == 0:
                break
            else:
                i_min = np.min(scan_line)
                x.append(pos_x+1)
                y.append(pos_y-20+i_min)
        return x, y

    def getBottomLine(self):
        leftend_x = self.x[0]
        rightend_x = self.x[-1]
        if self.length > 20:
            sample_left_y = self.y[20:40:2]
            sample_right_y = self.y[-21:-41:-2]
            bottom_y = mean(sample_left_y+sample_right_y)
        else:
            bottom_y = self.y[0]
        return (leftend_x, bottom_y), (rightend_x, bottom_y)

    def getMaxofHeight(self):
        i = self.y.index(min(self.y))
        return self.x[i], self.y[i]
