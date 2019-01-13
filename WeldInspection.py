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
                print(frameWithStats.maxHeightOfD)
                
            cv2.imshow('frame', hilightedFrame)
            frame_num += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
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
