# common.py
import math
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
# import OpenGL.GLUT as glut
import numpy as ny
import cv2


# Python Imaging Library (PIL)
class Common:
    is_create = False
    vbo = object
    ebo = object
    vbo_length = 0
    ebo_length = 0


class Sphere(Common):
    """
    画一个球
    """
    def __init__(self, rigns, segments, radius):
        self.rigns = rigns
        self.segments = segments
        self.radius = radius

    def create_vao(self):
        v_data = []
        v_index = []
        for y in range(self.rigns):
            phi = (float(y) / (self.rigns - 1)) * math.pi
            for x in range(self.segments):
                theta = (float(x) / float(self.segments - 1)) * 2 * math.pi
                v_data.append(self.radius * math.sin(phi) * math.cos(theta))
                v_data.append(self.radius * math.cos(phi))
                v_data.append(self.radius * math.sin(phi) * math.sin(theta))
                v_data.append(math.sin(phi) * math.cos(theta))
                v_data.append(math.cos(phi))
                v_data.append(math.sin(phi) * math.sin(theta))
        for y in range(self.rigns - 1):
            for x in range(self.segments - 1):
                v_index.append((y + 0) * self.segments + x)
                v_index.append((y + 1) * self.segments + x)
                v_index.append((y + 1) * self.segments + x + 1)
                v_index.append((y + 1) * self.segments + x + 1)
                v_index.append((y + 0) * self.segments + x + 1)
                v_index.append((y + 0) * self.segments + x)
        self.vbo = vbo.VBO(ny.array(v_data, 'f'))
        self.ebo = vbo.VBO(ny.array(v_index, 'H'), target=GL_ELEMENT_ARRAY_BUFFER)
        self.vbo_length = self.segments * self.rigns
        self.ebo_length = len(v_index)
        self.is_create = True

    def draw_shader(self, vi, ni, ei):
        if not self.is_create:
            self.create_vao()
        self.vbo.bind()

    def draw(self):
        if not self.is_create:
            self.create_vao()
        self.vbo.bind()
        glInterleavedArrays(GL_N3F_V3F, 0, None)
        self.ebo.bind()
        glDrawElements(GL_TRIANGLES, self.ebo_length, GL_UNSIGNED_SHORT, None)


class Plane(Common):
    """
    画一个平面
    """
    def __init__(self, x_res, y_res, x_scale, y_scale):
        self.xr, self.yr, self.xc, self.yc = x_res - 1, y_res - 1, x_scale, y_scale

    def create_vbo(self):
        half_x = self.xr * self.xc * 0.5
        half_y = self.yr * self.yc * 0.5
        v_data = []
        v_index = []
        for y in range(self.yr):
            for x in range(self.xr):
                v_data.append(self.xc * float(x) - half_x)
                v_data.append(0.)
                v_data.append(self.yc * float(y) - half_y)
        for y in range(self.yr - 1):
            for x in range(self.xr - 1):
                v_index.append((y + 0) * self.xr + x)
                v_index.append((y + 1) * self.xr + x)
                v_index.append((y + 0) * self.xr + x + 1)
                v_index.append((y + 0) * self.xr + x + 1)
                v_index.append((y + 1) * self.xr + x)
                v_index.append((y + 1) * self.xr + x + 1)
        print(len(v_data), len(v_index))
        self.vbo = vbo.VBO(ny.array(v_data, 'f'))
        self.ebo = vbo.VBO(ny.array(v_index, 'H'), target=GL_ELEMENT_ARRAY_BUFFER)
        self.ebo_length = len(v_index)
        self.is_create = True

    def draw(self):
        if not self.is_create:
            self.create_vbo()
        self.vbo.bind()
        glInterleavedArrays(GL_V3F, 0, None)
        self.ebo.bind()
        glDrawElements(GL_TRIANGLES, self.ebo_length, GL_UNSIGNED_SHORT, None)


class Camera:

    def __init__(self):
        self.mouse_location = [0.0, 0.0]
        self.offset = 0.01
        self.origin = [0.0, 0.0, 0.0]
        self.length = 1.
        self.y_angle = 0.
        self.z_angle = 0.
        self.is_three = False
        self.z_angle = 0. if not self.is_three else math.pi

    def set_three(self, value):
        self.is_three = value
        self.z_angle = self.z_angle + math.pi
        self.y_angle = -self.y_angle

    def eye(self):
        return self.origin if not self.is_three else self.direction()

    def target(self):
        return self.origin if self.is_three else self.direction()

    def direction(self):
        length = 1. if not self.is_three else self.length if 0. else 1.
        xy = math.cos(self.y_angle) * length
        x = self.origin[0] + xy * math.sin(self.z_angle)
        y = self.origin[1] + length * math.sin(self.y_angle)
        z = self.origin[2] + xy * math.cos(self.z_angle)
        return [x, y, z]

    def move(self, x, y, z):
        sin_z, cos_z = math.sin(self.z_angle), math.cos(self.z_angle)
        x_step, z_step = x * cos_z + z * sin_z, z * cos_z - x * sin_z
        if self.is_three:
            x_step = -x_step
            z_step = -z_step
        self.origin = [self.origin[0] + x_step, self.origin[1] + y, self.origin[2] + z_step]

    def rotate(self, z, y):
        self.z_angle, self.y_angle = self.z_angle - z, self.y_angle + y if not self.is_three else -y

    def set_look_at(self):
        ve, vt = self.eye(), self.target()
        # print ve,vt
        glLoadIdentity()
        gluLookAt(ve[2], ve[1], ve[0], vt[2], vt[1], vt[0], 0.0, 1.0, 0.0)

    def time_func(self, value):
        import glo
        arr_position = glo.get_value('position')
        print(self.origin, arr_position)
        if arr_position is not None:
            self.origin[0] = 4 - arr_position[0] / 100
            self.origin[1] = arr_position[1] / 100
            # x = arr_position[0]
            # y = arr_position[1]
            # print(10*self.offset, 0.01 * x)
            # self.move(0.0001 * (500 - x), 0, 0.)
        glutPostRedisplay()
        glutTimerFunc(1, self.time_func, 1)

    def keypress(self, key, x, y):
        if key in (b'e', b'E'):
            self.move(0., 0., 1 * self.offset)
        if key in (b'f', b'F'):
            self.move(10 * self.offset, 0., 0.)
        if key in (b's', b'S'):
            self.move(-10 * self.offset, 0., 0.)
        if key in (b'd', b'D'):
            self.move(0., 0., -1 * self.offset)
        if key in (b'w', b'W'):
            self.move(0., 1 * self.offset, 0.)
        if key in (b'r', b'R'):
            self.move(0., -1 * self.offset, 0.)
        if key in (b'v', b'V'):
            self.set_three(not self.is_three)

    def mouse(self, x, y):
        rx = (x - self.mouse_location[0]) * self.offset * 0.1
        ry = (y - self.mouse_location[1]) * self.offset * -0.1
        self.rotate(rx, ry)
        print(x, y)
        self.mouse_location = [x, y]

