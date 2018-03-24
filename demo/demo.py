#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from Detect import face
import glo
from VirtualScene import alive_scene

arr_position = [0, 0, 0, 0]


class DetectMove(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # print(arr_position)
        print('starting detect move.')
        while True:
            arr_position[0] += 1


class AliveScene(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('starting alive scene.')
        while True:
            print(arr_position)


def main():
    glo.init()
    thread1 = face.Position()
    thread2 = alive_scene.AliveScene()
    thread1.start()
    thread2.start()
    threads = [thread1, thread2]
    # 添加线程到线程列表

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")


if __name__ == '__main__':
    main()

