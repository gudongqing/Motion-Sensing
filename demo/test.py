import cv2

def test_cv2():
    cascade = cv2.CascadeClassifier(
        "D:\\opencv249\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt_tree.xml")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=9, minSize=(50, 50),
                                        flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        for x, y, z, w in rect:
            cv2.rectangle(frame, (x, y), (x + z, y + w), (0, 0, 255), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def CatchUsbVideo():
    cv2.namedWindow("catch face")

    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    camera_idx = 0
    cap = cv2.VideoCapture(camera_idx)

    # 告诉OpenCV使用人脸识别分类器
    classfier_face = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
    # classfier_face = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_righteye_2splits.xml")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 0, 255)

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

        # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier_face.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                print(x, y, w, h)
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

        # 显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

    # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()

