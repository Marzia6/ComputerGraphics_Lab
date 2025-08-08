# TASK1
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

rain_shift = 0
bg_brightness = 1

drops = []
for _ in range(200):
    x_pos = random.uniform(-1, 1)
    y_pos = random.uniform(0, 1)
    drops.append([x_pos, y_pos])

def initialize():
    if bg_brightness == 1:
        glClearColor(1, 1, 1, 0)
    elif bg_brightness > 0.5:
        glClearColor(0.6, 0.6, 0.6, 0)
    else:
        glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)

def render_Roof():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(0.4, 0.0, 0.8)

    glVertex2f(-0.6, 0.1)
    glVertex2f(0.0, 0.6)
    glVertex2f(0.0, 0.6)
    glVertex2f(0.6, 0.1)
    glVertex2f(-0.6, 0.1)
    glVertex2f(0.6, 0.1)

    glEnd()

def render_Structure():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(0.4, 0.0, 0.8)
    glVertex2f(-0.55, 0.1)
    glVertex2f(-0.55, -0.8)
    glVertex2f(-0.55, -0.8)
    glVertex2f(0.55, -0.8)
    glVertex2f(0.55, -0.8)
    glVertex2f(0.55, 0.1)
    glEnd()

def render_Entry():
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0.53, 0.81, 0.98)
    glVertex2f(-0.2, -0.8)
    glVertex2f(-0.2, -0.2)
    glVertex2f(-0.2, -0.2)
    glVertex2f(0.2, -0.2)
    glVertex2f(0.2, -0.2)
    glVertex2f(0.2, -0.8)
    glEnd()

def render_Windows():
    glBegin(GL_LINES)
    glColor3f(0.53, 0.81, 0.98)
    
    glVertex2f(-0.45, -0.1)
    glVertex2f(-0.25, -0.1)
    glVertex2f(-0.25, -0.1)
    glVertex2f(-0.25, -0.3)
    glVertex2f(-0.25, -0.3)
    glVertex2f(-0.45, -0.3)
    glVertex2f(-0.45, -0.3)
    glVertex2f(-0.45, -0.1)
    
    glVertex2f(-0.35, -0.1)
    glVertex2f(-0.35, -0.3)
    glVertex2f(-0.45, -0.2)
    glVertex2f(-0.25, -0.2)
    
    glVertex2f(0.25, -0.1)
    glVertex2f(0.45, -0.1)
    glVertex2f(0.45, -0.1)
    glVertex2f(0.45, -0.3)
    glVertex2f(0.45, -0.3)
    glVertex2f(0.25, -0.3)
    glVertex2f(0.25, -0.3)
    glVertex2f(0.25, -0.1)
    
    glVertex2f(0.35, -0.1)
    glVertex2f(0.35, -0.3)
    glVertex2f(0.25, -0.2)
    glVertex2f(0.45, -0.2)
    
    glEnd()

def RainDrops():
    glColor3f(0.0, 0.0, 0.8)
    glBegin(GL_LINES)
    for drop in drops:
        x1, y1 = drop
        x2, y2 = x1 + rain_shift, y1 - 0.05
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
    glEnd()

def Updated_Rain(value):
    global drops
    drops = [
        [random.uniform(-1, 1), random.uniform(0, 1)] if (y - (0.01 + abs(rain_shift)) < -1)
        else [x + rain_shift, y - (0.01 + abs(rain_shift))]
        for x, y in drops
    ]
    glutPostRedisplay()
    glutTimerFunc(30, Updated_Rain, None)

def key_Controls(key, x, y):
    global rain_shift, bg_brightness

    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        rain_shift += 0.002 if key == GLUT_KEY_RIGHT else -0.002
    elif key in (GLUT_KEY_UP, GLUT_KEY_DOWN):
        bg_brightness = max(0, min(1, bg_brightness + (0.1 if key == GLUT_KEY_UP else -0.1)))

    initialize()

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    render_Roof()
    render_Entry()
    RainDrops()
    render_Structure()
    render_Windows()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"TASK1")

glutDisplayFunc(show_screen)
glutTimerFunc(30, Updated_Rain, None)
glutSpecialFunc(key_Controls)
glutMainLoop()

  
  