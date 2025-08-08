import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.is_running = True
        self.current_score = 0
        self.diamond_pos = [random.randint(-250, 230), 210]
        self.catcher_pos = [-90, -240]
        self.catcher_color = (1.0, 1.0, 1.0)
        self.diamond_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
        self.fall_rate = 0.006
        self.move_speed = 2
        self.game_time = time.time()
        self.prev_update = self.game_time

game_state = GameState()

def draw_pixel(x, y, pixel_size):
    glPointSize(pixel_size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def process_keys(key, mouse_x, mouse_y):
    if game_state.diamond_pos[1] < -220:
        return
    if not game_state.is_running:
        return
    move_distance = 20 * game_state.move_speed
    left_limit = -250
    right_limit = 90
    if key == GLUT_KEY_LEFT and game_state.catcher_pos[0] > left_limit:
        game_state.catcher_pos[0] = max(game_state.catcher_pos[0] - move_distance, left_limit)
    elif key == GLUT_KEY_RIGHT and game_state.catcher_pos[0] + 160 < 250:
        game_state.catcher_pos[0] = min(game_state.catcher_pos[0] + move_distance, right_limit)
    glutPostRedisplay()

def click_handler(button, state, x, y):
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
    restart_button = (0, 60)
    pause_button = (225, 275)
    exit_button_x = 440
    button_top = 70
    if x <= restart_button[1] and y <= button_top:
        print("Starting Over!")
        game_state.reset()
    elif pause_button[0] <= x <= pause_button[1] and y <= button_top:
        game_state.is_running = not game_state.is_running
    elif x >= exit_button_x and y <= button_top:
        print(f"Goodbye! Score: {game_state.current_score}")
        glutLeaveMainLoop()
    glutPostRedisplay()

def get_region(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    abs_dx, abs_dy = abs(dx), abs(dy)
    is_x_dominant = abs_dx >= abs_dy
    if dx >= 0 and dy >= 0:
        return 0 if is_x_dominant else 1
    elif dx < 0 <= dy:
        return 3 if is_x_dominant else 2
    elif dx >= 0 > dy:
        return 7 if is_x_dominant else 6
    else:
        return 4 if is_x_dominant else 5

def midpoint_line(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incr_e = 2 * dy
    incr_ne = 2 * (dy - dx)
    x, y = x1, y1
    while x <= x2:
        points.append([x, y])
        if d > 0:
            d += incr_ne
            y += 1
            x += 1
        else:
            d += incr_e
            x += 1
    return points

def convert_coordinates(region, x, y):
    if region in [1, 2, 5, 6]: x, y = y, x
    if region in [3, 4, 5, 6]: x = -x
    if region in [2, 4, 5, 7]: y = -y
    return x, y

def draw_line_segment(color, region, points):
    glColor3f(*color)
    if region in [1, 2, 5, 6]:
        for p in points: p[0], p[1] = p[1], p[0]
    if region in [2, 3, 4, 5]:
        for p in points: p[0] = -p[0]
    if region in [4, 5, 6, 7]:
        for p in points: p[1] = -p[1]
    for px, py in points:
        draw_pixel(px, py, 3)

def render_line(color, x1, y1, x2, y2):
    region = get_region(x1, y1, x2, y2)
    x1, y1 = convert_coordinates(region, x1, y1)
    x2, y2 = convert_coordinates(region, x2, y2)
    line_points = midpoint_line(x1, y1, x2, y2)
    draw_line_segment(color, region, line_points)

def draw_triangle_button(color, coords):
    render_line(color, *coords[0], *coords[1])
    render_line(color, *coords[1], *coords[2])
    render_line(color, *coords[2], *coords[0])

def draw_catcher():
    x, y = game_state.catcher_pos
    c = game_state.catcher_color
    render_line(c, x, y, x + 20, y - 15)
    render_line(c, x + 20, y - 15, x + 140, y - 15)
    render_line(c, x + 140, y - 15, x + 160, y)
    render_line(c, x + 160, y, x, y)

def draw_diamond():
    x, y = game_state.diamond_pos
    c = game_state.diamond_color
    render_line(c, x, y, x - 10, y - 10)
    render_line(c, x - 10, y - 10, x, y - 20)
    render_line(c, x, y - 20, x + 10, y - 10)
    render_line(c, x + 10, y - 10, x, y)

def draw_buttons():
    render_line((0.0, 1.0, 1.0), -240, 225, -220, 240)
    render_line((0.0, 1.0, 1.0), -240, 225, -200, 225)
    render_line((0.0, 1.0, 1.0), -240, 225, -220, 210)
    yellow = (1.0, 1.0, 0.0)
    if game_state.is_running:
        render_line(yellow, -10, 240, -10, 210)
        render_line(yellow, 10, 240, 10, 210)
    else:
        draw_triangle_button(yellow, [[-20, 240], [-20, 210], [20, 225]])
    red = (1.0, 0.0, 0.0)
    render_line(red, 200, 240, 240, 210)
    render_line(red, 200, 210, 240, 240)

def display_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 200.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    draw_buttons()
    draw_catcher()
    draw_diamond()
    glutSwapBuffers()

def check_catch_or_miss():
    if game_state.catcher_pos[0] - 20 < game_state.diamond_pos[0] < game_state.catcher_pos[0] + 160:
        game_state.current_score += 1
        game_state.diamond_pos = [random.randint(-250, 230), 210]
        game_state.diamond_color = (
            random.uniform(0.5, 1.0),
            random.uniform(0.5, 1.0),
            random.uniform(0.5, 1.0)
        )
        print(f"Score: {game_state.current_score}")
    else:
        game_state.catcher_color = (1.0, 0.0, 0.0)
        print(f"Game Over! Score: {game_state.current_score}")

def update_diamond_position(now):
    if now - game_state.prev_update >= game_state.fall_rate:
        game_state.diamond_pos[1] -= 1
        game_state.prev_update = now

def adjust_difficulty(now):
    if now - game_state.game_time >= 8:
        game_state.fall_rate /= 1.3
        game_state.move_speed = min(game_state.move_speed + 1, 12)
        game_state.game_time = now

def game_loop():
    if game_state.diamond_pos[1] == -220:
        check_catch_or_miss()
    if game_state.is_running:
        now = time.time()
        update_diamond_position(now)
        adjust_difficulty(now)
    glutPostRedisplay()

def setup():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(500, 800)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
game_window = glutCreateWindow(b"Catch the Diamonds!")
setup()
glutDisplayFunc(display_scene)
glutIdleFunc(game_loop)
glutSpecialFunc(process_keys)
glutMouseFunc(click_handler)
glutMainLoop()
