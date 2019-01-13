import numpy as np
import cv2
import matplotlib.pyplot as plt

from components.mass import Mass
from components.statusOfOneFrame import StatusOfOneFrame
from components.imageProcessing import ImageProcessing


def weldInspection():
    cap = cv2.VideoCapture('./test04.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (3840, 2160))
    frame_num = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = ImageProcessing(frame)
            frameWithStats = StatusOfOneFrame(frame.preprocessing())
            hilightedFrame = frame.generateHighlightedSurfaceImage(frameWithStats)
            out.write(hilightedFrame)
            if frameWithStats.isDetected() == True:
                # To do : 上手く検出されたときの処理を記述
                print(frameWithStats.maxHeightOfD)
                print(frameWithStats.posInDepthDirection)
            cv2.imshow('frame', hilightedFrame)
            frame_num += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    weldInspection()
    
if __name__ == '__main__':
    main()
