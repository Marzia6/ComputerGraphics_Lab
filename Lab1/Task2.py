# TASK2
import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *

paused, blinking = False, False
stored_speed, stored_blink = None, None
frame_interval = 50
blink_start_time = 0
objects = []

directions = {
    0: (-0.01, 0.01),
    1: (0.01, -0.01),
    2: (0.01, 0.01),
    3: (-0.01, -0.01)
}
direction_toggle = {0: 1, 1: 0, 2: 3, 3: 2}

def initialize():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_object(x, y, r, g, b):
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(r, g, b)
    glVertex2f(x, y)
    glEnd()


def update_scene(value):
    if paused:
        glutTimerFunc(frame_interval, update_scene, None)
        return

    for obj in objects:
        dx, dy = directions[obj[5]]
        new_x, new_y = obj[0] + dx, obj[1] + dy

        if not (-1 <= new_x <= 1):
            obj[5] = direction_toggle[obj[5]]
            dx, dy = directions[obj[5]]

        if not (-1 <= new_y <= 1):
            obj[5] = direction_toggle[obj[5]]
            dx, dy = directions[obj[5]]

        obj[0] += dx
        obj[1] += dy

    glutPostRedisplay()
    glutTimerFunc(frame_interval, update_scene, None)


def special_key_handler(key, x, y):
    global frame_interval
    frame_interval += -10 if key == GLUT_KEY_UP else 10 if key == GLUT_KEY_DOWN else 0
    frame_interval = max(1, frame_interval)


def key_handler(key, x, y):
    global paused, frame_interval, blinking, stored_speed, stored_blink

    if key == b' ':
        paused = not paused
        stored_speed, stored_blink, frame_interval, blinking = (
            (frame_interval, blinking, -1, False) if paused 
            else (stored_speed, stored_blink, stored_speed, stored_blink)
        )

        if not paused:
            glutTimerFunc(frame_interval, update_scene, None)

    glutPostRedisplay()


def mouse_handler(button, state, x, y):
    global blinking, blink_start_time, paused
    if not paused:
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            width_half = glutGet(GLUT_WINDOW_WIDTH) / 2
            height_half = glutGet(GLUT_WINDOW_HEIGHT) / 2
            pos_x = (x - width_half) / width_half
            pos_y = -((y - height_half) / height_half)
            objects.append([
                pos_x, pos_y,
                random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1),
                random.randint(0, 3)
            ])
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            blinking = not blinking
            blink_start_time = time.time()
    glutPostRedisplay()

def show_screen():
    global blink_start_time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if not blinking or (time.time() - blink_start_time) % 1 <= 0.5:
        for obj in objects:
            draw_object(*obj[:5])

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"TASK2")
glutDisplayFunc(show_screen)
glutMouseFunc(mouse_handler)
glutTimerFunc(frame_interval, update_scene, None)
glutKeyboardFunc(key_handler)
glutSpecialFunc(special_key_handler)
glutMainLoop()
