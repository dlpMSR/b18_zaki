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
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (3840, 2160))
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    fig2d = plt.figure()
    fig3d = plt.figure()
    ax2d = fig2d.add_subplot(111)
    ax3d = fig3d.add_subplot(111, projection='3d')
    frame_num = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = ImageProcessing(frame)
            frameWithStats = StatusOfOneFrame(frame.preprocessing())
            output_frame = frame.generateOutputImage(frameWithStats, frame_num)
            out.write(output_frame)
            if frameWithStats.isDetected() == True:
                y, z = frameWithStats.getDSurface()
                x = np.full(z.size, frameWithStats.posInDepthDirection)
                ax2d.cla()
                ax2d.plot(y, z, color='r')
                xlim = ax2d.get_xlim()
                ax2d.set_ylim(0, xlim[1]-xlim[0])
                fig2d.savefig('./output/frame_{}.png'.format(frame_num))
                ax3d.plot(x, y, z, color='r', linewidth=1, alpha=0.1)
                ylim = ax3d.get_ylim()
                ax3d.set_zlim(0, ylim[1]-ylim[0])
                # plt.draw()
                # plt.pause(0.1)
            cv2.namedWindow('frame', cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            cv2.imshow('frame', output_frame)
            pbar.update(1)
            frame_num += 1
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
    weldInspection('./V_20190114_155120_vHDR_On_Trim.mp4')


if __name__ == '__main__':
    main()
