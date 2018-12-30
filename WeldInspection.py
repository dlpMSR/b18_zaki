import numpy as np
import cv2
import matplotlib.pyplot as plt
from statistics import mean, median,variance,stdev


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


def weldInspection():
    cap = cv2.VideoCapture('./test04.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (3840, 2160))
    frame_num = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = imageProcessing(frame)
            out.write(frame)
            #cv2.imshow('frame', frame)
            frame_num += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def imageProcessing(frame):
    #height, width = frame.shape[:2]
    #色マスク
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    lowerRed = np.array([200, 0, 0])
    upperRed = np.array([310, 255, 255])
    img_mask = cv2.inRange(hsv, lowerRed, upperRed)
    #ノイズキャンセル
    labelStats = cv2.connectedComponentsWithStats(img_mask)
    nLabels, labelImages, masses, center = labelStats
    for mass in masses:
        if mass[4] < 300:
            cv2.rectangle(img_mask, (mass[0], mass[1]),
                          (mass[0] + mass[2], mass[1] + mass[3]), 0, -1)
    #微分フィルタ
    img_filtered = img_mask
    #各部位を検出~連鎖
    tip = sakicho(img_filtered, 0)
    massA = Mass(img_filtered, tip)
    tip = sakicho(img_filtered, massA.rearEndCoordinates[0]+1)
    massB = Mass(img_filtered, tip)
    tip = sakicho(img_filtered, massB.rearEndCoordinates[0]+1)
    massC = Mass(img_filtered, tip)
    tip = sakicho(img_filtered, massC.rearEndCoordinates[0]+1)
    massD = Mass(img_filtered, tip)
    tip = sakicho(img_filtered, massD.rearEndCoordinates[0]+1)
    massE = Mass(img_filtered, tip)
    tip = sakicho(img_filtered, massE.rearEndCoordinates[0]+1)
    massF = Mass(img_filtered, tip)
    # 書きこみ
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.line(frame, massB.getBottomLine()[0], massB.getBottomLine()[1], (0, 255, 0), 2)
    cv2.putText(frame, str(massB.length), (massB.centroid[0], massB.centroid[1]-10), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.line(frame, massF.getBottomLine()[0], massF.getBottomLine()[1], (0, 255, 0), 2)
    cv2.putText(frame, str(massF.length), (massF.centroid[0], massF.centroid[1]-10), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.line(frame, massC.getBottomLine()[0], massC.getBottomLine()[1], (255, 0, 255), 2)
    cv2.putText(frame, str(massC.length), (massC.centroid[0], massC.centroid[1]-10), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.line(frame, massE.getBottomLine()[0], massE.getBottomLine()[1], (255, 0, 255), 2)
    cv2.putText(frame, str(massE.length), (massE.centroid[0], massE.centroid[1]-10), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.line(frame, massD.getBottomLine()[0], massD.getBottomLine()[1], (255, 255, 0), 2)
    cv2.putText(frame, str(massD.length), (massD.centroid[0], massD.centroid[1]+30), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.line(frame, massB.rearEndCoordinates, (massB.rearEndCoordinates[0], massC.frontEndCoordinates[1]), (0, 0, 255), 2)
    cv2.putText(frame, str(massC.frontEndCoordinates[1]-massB.rearEndCoordinates[1]),
                (massB.rearEndCoordinates[0]+10, massB.rearEndCoordinates[1]+40),
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.line(frame, (massD.maxOfHeight[0]-40, massD.maxOfHeight[1]),
                    (massD.maxOfHeight[0]+40, massD.maxOfHeight[1]), (255, 255, 0), 2)
    cv2.line(frame, (massD.maxOfHeight[0]+40, massD.maxOfHeight[1]),
                    (massD.maxOfHeight[0]+40, massD.getBottomLine()[1][1]), (255, 255, 0), 2)
    cv2.putText(frame, str(massD.getBottomLine()[0][1]-massD.maxOfHeight[1]), (massD.maxOfHeight[0]+60, massD.maxOfHeight[1]+30), font, 1, (255, 255, 0), 2, cv2.LINE_AA)

    return frame

def filter(img):
    filter_3x3 = np.array([[ 0,  -1,  0],
                           [ 0,  1,  0],
                           [ 0,  0,  0]], np.float32)
    img_filtered = cv2.filter2D(img, -1, filter_3x3)
    return img_filtered
    
def sakicho(img, offset):
    width = img.shape[1]
    for i in range(offset, width):
            line = img[:, i]
            test = np.where(line==255)
            if test[0].size != 0:
                tip = (i, test[0][0])
                break
    return tip

def imshow(img):
    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generateFrameImage():
    cap = cv2.VideoCapture('./test04.mp4')
    num = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        img_mask, output = imageProcessing(frame)
        #cv2.imshow('frame', frame)
        filename_frame = './frame/{}.jpg'.format(num)
        filename_mask = './mask/{}.jpg'.format(num)
        filename_output = './output/{}.jpg'.format(num)
        cv2.imwrite(filename_frame, frame)
        cv2.imwrite(filename_mask, img_mask)
        cv2.imwrite(filename_output, output)
        num += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    weldInspection()
    # imageProcessing()
    # generateFrameImage()


if __name__ == '__main__':
    main()
