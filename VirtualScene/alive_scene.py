import threading

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from VirtualScene import common
import sys

from Detect import face

window = 0
sph = common.Sphere(8, 16, 1)
camera = common.Camera()
plane = common.Plane(12, 12, 1., 1.)


def init_gl(width, height):
    glClearColor(0.1, 0.1, 0.5, 0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    camera.move(0.0, 3.0, -5)


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    camera.set_look_at()
    plane.draw()
    glTranslatef(-1.5, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glEnd()
    glTranslatef(3.0, 0.0, 0.0)
    sph.draw()
    glutSwapBuffers()


def mouse_button(button, mode, x, y):
    if button == GLUT_RIGHT_BUTTON:
        camera.mouse_location = [x, y]


def resize_scene(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


class AliveScene(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.window = 0

    def run(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 400)
        glutInitWindowPosition(800, 400)
        self.window = glutCreateWindow("open_gl")
        glutDisplayFunc(draw_scene)
        glutIdleFunc(draw_scene)
        glutReshapeFunc(resize_scene)
        glutMouseFunc(mouse_button)
        glutMotionFunc(camera.mouse)
        glutKeyboardFunc(camera.keypress)
        glutSpecialFunc(camera.keypress)
        glutTimerFunc(1, camera.time_func, 1)
        init_gl(640, 480)

        # 在glutglinit前开线程在glutmainloop 后开线程都会有问题
        thread1 = face.Position()
        thread1.start()

        glutMainLoop()


