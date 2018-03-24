# -*- coding: utf-8 -*-
import threading

import cv2
import sys
# from PIL import Image
import glo


class Position(threading.Thread):
    def __init__(self, unit_test=False):
        threading.Thread.__init__(self)
        self.position = []                  # 当前位置信息
        self.camera_idx = 0                 # 摄像头ID
        self.unit_test = unit_test          # 是否单元测试

        if self.unit_test:
            self.window_name = "face area"

    def run(self):
        cv2.namedWindow('capture position window')
        cap = cv2.VideoCapture(self.camera_idx)
        classifier_face = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_rects = classifier_face.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
            if len(face_rects) > 0:
                print(round_position(face_rects[0]))
                # self.position = round_position((face_rects[0]))
                glo.set_value('position', round_position(face_rects[0]))
                if self.unit_test:
                    x, y, w, h = face_rects[0]
                    # 识别出人脸后要画的边框的颜色，RGB格式
                    color = (0, 0, 255)
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
            if self.unit_test:
                # 显示图像
                cv2.imshow(self.window_name, frame)
                c = cv2.waitKey(10)
                if c & 0xFF == ord('q'):
                    break
        # 释放摄像头并销毁所有窗口
        cap.release()
        cv2.destroyAllWindows()
        pass


def round_position(position):
    # print(position)
    for i in range(len(position)):
        position[i] /= 100
        position[i] *= 100
    return position


if __name__ == '__main__':
    thread1 = Position(True)
    thread1.run()
