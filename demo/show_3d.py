from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

axix = 0.0
axiy = 0.0
z = 0.0


def drawFunc():
    # 清楚之前画面
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0, 0, 0, 0)  # (角度,x,y,z)
    glutWireTeapot(0.4)
    # gluLookAt(axix, axiy, z, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0)
    # 刷新显示
    glFlush()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    gluLookAt(axix, axiy, z, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0)
    glScalef(1.0, 2.0, 1.0)
    glutWireCube(1.0)
    glFlush()


def reshape_func(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / h, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)
    pass


def keyboardFunc(key, x, y):
    global axix, axiy, z
    if key == 'd':
        axix += 1.0
    if key == 'a':
        axix -= 1.0
    if key == 'w':
        z -= 1.0
    if key == 's':
        z += 1.0
    glutPostRedisplay()
    pass


# 使用glut初始化OpenGL
glutInit()
glShadeModel(GL_FLAT)
# 显示模式:GLUT_SINGLE无缓冲直接显示|GLUT_RGBA采用RGB(A非alpha)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
# 窗口位置及大小-生成
glutInitWindowPosition(0, 0)
glutInitWindowSize(400, 400)
glutCreateWindow(b"first")
# 调用函数绘制图像
glutDisplayFunc(display)
glutReshapeFunc(reshape_func)
glutKeyboardFunc(keyboardFunc)
# glutIdleFunc(display)
# 主循环
glutMainLoop()
