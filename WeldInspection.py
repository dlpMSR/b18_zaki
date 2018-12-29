import numpy as np
import cv2


def generateFrameImage():
    cap = cv2.VideoCapture('./test01.mp4')
    num = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        filename = './frame/{}.jpg'.format(num)
        cv2.imwrite(filename, frame)
        num += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def imageProcessing():
    frame = cv2.imread('./frame/113.jpg')
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (round(width / 4), round(height / 4)))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    lowerRed = np.array([200, 60, 0])
    upperRed = np.array([275, 255, 255])
    img_mask = cv2.inRange(hsv, lowerRed, upperRed)
    img_color = cv2.bitwise_and(frame, frame, mask=img_mask)
    cv2.imwrite('./red.jpg', img_color)
    imshow(img_color)


def imshow(img):
    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    imageProcessing()
    # generateFrameImage()


if __name__ == '__main__':
    main()
