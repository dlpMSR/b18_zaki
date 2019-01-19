import numpy as np
import cv2
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time

from components.mass import Mass
from components.statusOfOneFrame import StatusOfOneFrame
from components.imageProcessing import ImageProcessing


def weldInspection():
    cap = cv2.VideoCapture('./V_20190114_155120_vHDR_On_Trim.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (3840, 2160))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = ImageProcessing(frame)
            frameWithStats = StatusOfOneFrame(frame.preprocessing())
            hilightedFrame = frame.generateHighlightedSurfaceImage(frameWithStats)
            out.write(hilightedFrame)
            if frameWithStats.isDetected() == True:
                z = frameWithStats.D.surface[1]
                y = frameWithStats.D.surface[0]
                x = np.full(z.size, frameWithStats.posInDepthDirection)
                ax.plot(x, y, z, color='green', linewidth=1)
            cv2.imshow('frame', hilightedFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    ax.set_zlim(800, 1600)
    plt.show()


def main():
    weldInspection()
    
if __name__ == '__main__':
    main()
