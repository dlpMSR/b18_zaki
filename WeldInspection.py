import numpy as np
import cv2
import csv
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
    f = open('./output.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['frame_num', 'pix_5mm', 'mm/px', 'B_length', 'C_length', 'max_height', 'max_height(mm)'])
    result_list = []
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
            frame_status = StatusOfOneFrame(frame.preprocessing(), frame_num)
            output_frame = frame.generateOutputImage(frame_status, frame_num)
            out.write(output_frame)
            result_list.append(frame_status.getFrameStatus())
            if frame_status.isDetected() == True:
                frame_status.generate2DGraph(ax2d)
                frame_status.update3DGraph(ax3d)
                fig2d.savefig('./output/frame_{}.png'.format(frame_num))
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
    for item in result_list:
        writer.writerow(item)
    f.close()
    pbar.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    plt.show()


def main():
    weldInspection('./V_20190114_155120_vHDR_On_Trim.mp4')


if __name__ == '__main__':
    main()
