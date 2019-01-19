import numpy as np
import cv2
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

from components.mass import Mass
from components.statusOfOneFrame import StatusOfOneFrame
from components.imageProcessing import ImageProcessing


def weldInspection(video_path):
    cap = cv2.VideoCapture(video_path)
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    pbar = tqdm(total=int(length))
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
                y, z = frameWithStats.getDSurfaceForGraph()
                x = np.full(z.size, frameWithStats.posInDepthDirection)
                ax.plot(x, y, z, color='k', linewidth=1, alpha=0.1)
                ylim = ax.get_ylim()
                ax.set_zlim(0, ylim[1]-ylim[0])
                plt.draw()
                plt.pause(0.01)
            cv2.namedWindow('frame', cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            cv2.imshow('frame', hilightedFrame)
            pbar.update(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    pbar.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    plt.show()


def main():
    weldInspection('./V_20190114_154827_vHDR_On_Trim.mp4')


if __name__ == '__main__':
    main()
