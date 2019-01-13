from statistics import mean


class Mass(object):
    def __init__(self, img, tip):
        self.x, self.y = self.uneUne(img, tip)

        self.length = abs(self.x[-1]-self.x[0])
        self.frontEndCoordinates = (self.x[0], self.y[0])
        self.rearEndCoordinates = (self.x[-1], self.y[-1])
        self.centroid = (int((self.x[0]+self.x[-1])/2), int((self.y[0]+self.y[-1])/2))
        self.maxOfHeight = self.getMaxofHeight()
    
    def uneUne(self, img, tip):
        x = [tip[0]]
        y = [tip[1]]
        while True:
            pos_x = x[-1]
            pos_y = y[-1]
            scan_line = img[pos_y-20:pos_y+20, pos_x+1]
            for i in range(len(scan_line)):
                if scan_line[i] != 0:
                    x.append(pos_x+1)
                    y.append(pos_y-20+i)
                    break
            else:
                break
        return x, y
    
    def getBottomLine(self):
        leftend_x = self.x[0]
        rightend_y = self.x[-1]
        sample_left_y = self.y[0:20:2]
        sample_right_y = self.y[-1:-21:-2]
        bottom_y = mean(sample_left_y+sample_right_y)
        return (leftend_x, bottom_y), (rightend_y, bottom_y)
    
    def getMaxofHeight(self):
        i = self.y.index(min(self.y))
        return self.x[i], self.y[i]  
