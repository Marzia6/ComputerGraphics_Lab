from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

player_pos = [0, 0, 0]
player_rotation = 0
camera_pos = (0, 500, 500)
camera_mode = "third_person"
cheat_mode = False
auto_rotate = False
auto_follow = False
lives = 5
score = 0
missed_bullets = 0
bullets = []
enemies = []
particles = []
game_over = False
GRID_LENGTH = 600
fovY = 120
last_bullet_time = 0
feedback_messages = []
enemy_pulse = 0
camera_height = 500
camera_rotation = 0
gun_angle = 0

BULLET_SPEED = 15
BULLET_SIZE = 5
PLAYER_SPEED = 10
ROTATION_SPEED = 5
ENEMY_SPEED_MIN = 0.3
ENEMY_SPEED_MAX = 0.7
PARTICLE_LIFETIME = 30
GUN_BARREL_LENGTH = 25
GUN_HEIGHT = 15
GUN_OFFSET_FROM_CENTER = 5

def print_feedback(message):
    feedback_messages.append(message)
    if len(feedback_messages) > 5:
        feedback_messages.pop(0)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)
    glutSolidCube(60)
    glTranslatef(0, 0, 100)
    glColor3f(0, 1, 0)
    glutSolidCube(60)
    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)
    glTranslatef(100, 0, 100)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)
    glColor3f(0, 1, 1)
    glTranslatef(300, 0, 100)
    gluSphere(gluNewQuadric(), 80, 10, 10)
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_rotation, 0, 0, 1)
    
    if game_over:
        glRotatef(90, 1, 0, 0)

    glPushMatrix()
    glColor3f(0.2, 0.6, 0.9)
    glScalef(0.8, 0.4, 1.2)
    glutSolidCube(30)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 25)
    glColor3f(0.9, 0.7, 0.6)
    glutSolidSphere(8, 20, 20)
    glPopMatrix()

    for x_offset in [-20, 20]:
        glPushMatrix()
        glTranslatef(x_offset, 0, GUN_HEIGHT)
        glRotatef(90, 0, 1, 0)
        glColor3f(0.9, 0.7, 0.6)
        gluCylinder(gluNewQuadric(), 3, 3, 15, 10, 10)
        glPopMatrix()

    for x_offset, angle in [(-12, -10), (12, 10)]:
        glPushMatrix()
        glTranslatef(x_offset, 0, GUN_HEIGHT)
        glRotatef(angle, 0, 0, 1)
        glColor3f(0.9, 0.7, 0.6)
        glutSolidSphere(3, 10, 10)
        glPopMatrix()

    for x_offset in [-8, 8]:
        glPushMatrix()
        glTranslatef(x_offset, 0, -20)
        glScalef(0.4, 0.4, 1.2)
        glColor3f(0.1, 0.1, 0.5)
        glutSolidCube(15)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(GUN_OFFSET_FROM_CENTER, 0, GUN_HEIGHT)
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glScalef(1.2, 1.2, 10)
    glutSolidCube(2)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 10)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 1.5, 1.5, GUN_BARREL_LENGTH, 8, 8)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, -5)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 1.5, 2, 6, 8, 8)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def init_enemies():
    global enemies
    enemies = []
    for _ in range(5):
        x = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        y = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        enemies.append([x, y, 0, random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)])

def draw_enemies():
    global enemy_pulse
    
    pulse_size = 1 + 0.2 * math.sin(enemy_pulse)
    
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy[0], enemy[1], enemy[2])
        glColor3f(1.0, 0.0, 0.0)
        glScalef(pulse_size, pulse_size, pulse_size)
        glutSolidSphere(5, 20, 20)
        glPushMatrix()
        glTranslatef(0, 0, 5)
        glColor3f(0.0, 0.0, 0.0)
        glutSolidSphere(2.5, 20, 20)
        glPopMatrix()
        glPopMatrix()

def draw_bullets():
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['x'], bullet['y'], bullet['z'])
        glColor3f(0.8,0,0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glutSolidSphere(BULLET_SIZE, 10, 10)
        glDisable(GL_BLEND)
        glPopMatrix()

def draw_particles():
    glPointSize(3)
    glBegin(GL_POINTS)
    for particle in particles:
        glColor3f(particle['color'][0], particle['color'][1], particle['color'][2])
        glVertex3f(particle['x'], particle['y'], particle['z'])
    glEnd()

def draw_grid():
    grid_size = 50
    glPushMatrix()
    for x in range(-GRID_LENGTH, GRID_LENGTH, grid_size):
        for y in range(-GRID_LENGTH, GRID_LENGTH, grid_size):
            glBegin(GL_QUADS)
            if (x // grid_size + y // grid_size) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glVertex3f(x, y, 0)
            glVertex3f(x + grid_size, y, 0)
            glVertex3f(x + grid_size, y + grid_size, 0)
            glVertex3f(x, y + grid_size, 0)
            glEnd()

    height = 50
    wall_thickness = 5

    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(0, GRID_LENGTH, height / 2)
    glScalef(GRID_LENGTH * 2, wall_thickness, height)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(0, -GRID_LENGTH, height / 2)
    glScalef(GRID_LENGTH * 2, wall_thickness, height)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.5, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(GRID_LENGTH, 0, height / 2)
    glScalef(wall_thickness, GRID_LENGTH * 2, height)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(-GRID_LENGTH, 0, height / 2)
    glScalef(wall_thickness, GRID_LENGTH * 2, height)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def draw_feedback_panel():
    for i, message in enumerate(feedback_messages[-5:]):
        draw_text(20, 130 - i*25, message, GLUT_BITMAP_9_BY_15)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == "first_person":
        if auto_follow and cheat_mode:
            look_x = player_pos[0] + math.cos(math.radians(player_rotation)) * 100
            look_y = player_pos[1] + math.sin(math.radians(player_rotation)) * 100
        else:
            look_x = player_pos[0] + math.cos(math.radians(player_rotation)) * 100
            look_y = player_pos[1] + math.sin(math.radians(player_rotation)) * 100
        
        gluLookAt(player_pos[0], player_pos[1], 100,
                  look_x, look_y, 50,
                  0, 0, 1)
    else:
        camera_distance = 500
        angle_rad = math.radians(camera_rotation)
        camera_x = -camera_distance * math.cos(angle_rad)
        camera_y = -camera_distance * math.sin(angle_rad)
        camera_z = camera_height
        
        gluLookAt(camera_x, camera_y, camera_z,
                  0, 0, 0,
                  0, 0, 1)

def fire_bullet():
    global last_bullet_time
    
    current_time = glutGet(GLUT_ELAPSED_TIME)
    if current_time - last_bullet_time > 200:
        angle_rad = math.radians(player_rotation)
        
        gun_x = player_pos[0] + math.cos(angle_rad) * GUN_OFFSET_FROM_CENTER - math.sin(angle_rad) * 0
        gun_y = player_pos[1] + math.sin(angle_rad) * GUN_OFFSET_FROM_CENTER + math.cos(angle_rad) * 0
        
        bullet_start_x = gun_x + math.cos(angle_rad) * GUN_BARREL_LENGTH
        bullet_start_y = gun_y + math.sin(angle_rad) * GUN_BARREL_LENGTH
        
        bullets.append({
            'x': bullet_start_x,
            'y': bullet_start_y,
            'z': GUN_HEIGHT,
            'dx': math.cos(angle_rad) * BULLET_SPEED,
            'dy': math.sin(angle_rad) * BULLET_SPEED,
            'dz': 0,
            'life': 100
        })
        last_bullet_time = current_time
        print_feedback("Player Bullet Fired!")
        print("Player Bullet Fired!")

def keyboardListener(key, x, y):
    global cheat_mode, auto_rotate, auto_follow, game_over, lives, score
    global missed_bullets, player_pos, player_rotation, camera_mode, camera_height, camera_rotation
    
    if game_over and key == b'r':
        player_pos = [0, 0, 0]
        player_rotation = 0
        lives = 5
        score = 0
        missed_bullets = 0
        bullets.clear()
        particles.clear()
        game_over = False
        cheat_mode = False
        auto_rotate = False
        auto_follow = False
        camera_mode = "third_person"
        camera_height = 500
        camera_rotation = 0
        init_enemies()
        feedback_messages.clear()
        print_feedback("Game restarted!")
        return
    
    if game_over:
        return
    
    if key == b'w':
        new_x = player_pos[0] + math.cos(math.radians(player_rotation)) * PLAYER_SPEED
        new_y = player_pos[1] + math.sin(math.radians(player_rotation)) * PLAYER_SPEED
        if -GRID_LENGTH + 50 < new_x < GRID_LENGTH - 50 and -GRID_LENGTH + 50 < new_y < GRID_LENGTH - 50:
            player_pos[0] = new_x
            player_pos[1] = new_y
        else:
            print_feedback("Cannot move beyond board boundaries!")
    elif key == b's':
        new_x = player_pos[0] - math.cos(math.radians(player_rotation)) * PLAYER_SPEED
        new_y = player_pos[1] - math.sin(math.radians(player_rotation)) * PLAYER_SPEED
        if -GRID_LENGTH + 50 < new_x < GRID_LENGTH - 50 and -GRID_LENGTH + 50 < new_y < GRID_LENGTH - 50:
            player_pos[0] = new_x
            player_pos[1] = new_y
        else:
            print_feedback("Cannot move beyond board boundaries!")
    elif key == b'd':
        player_rotation -= ROTATION_SPEED
    elif key == b'a':
        player_rotation += ROTATION_SPEED
    elif key == b'c':
        cheat_mode = not cheat_mode
        auto_rotate = cheat_mode
    elif key == b'v' and cheat_mode:
        if camera_mode == "first_person":
            auto_follow = not auto_follow
    elif key == b' ':
        fire_bullet()

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global camera_height, camera_rotation
    
    if key == GLUT_KEY_UP:
        camera_height += 20
        if camera_height > 1000:
            camera_height = 1000
    elif key == GLUT_KEY_DOWN:
        camera_height -= 20
        if camera_height < 100:
            camera_height = 100
    elif key == GLUT_KEY_LEFT:
        camera_rotation -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_rotation += 5

def mouseListener(button, state, x, y):
    global camera_mode, auto_follow
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if camera_mode == "first_person":
            camera_mode = "third_person"
            auto_follow = False
        else:
            camera_mode = "first_person"
    
    glutPostRedisplay()

def add_particles(x, y, z, count=10):
    for _ in range(count):
        particles.append({
            'x': x + random.uniform(-5, 5),
            'y': y + random.uniform(-5, 5),
            'z': z + random.uniform(-5, 5),
            'dx': random.uniform(-0.5, 0.5),
            'dy': random.uniform(-0.5, 0.5),
            'dz': random.uniform(-0.5, 0.5),
            'color': (random.random(), random.random(), random.random()),
            'life': PARTICLE_LIFETIME
        })

def check_collisions():
    global lives, score, enemies, bullets, missed_bullets, particles
    
    for enemy in enemies[:]:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < 50:
            lives -= 1
            enemy[0] = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
            enemy[1] = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
            print_feedback(f"Remaining Player Life: {lives}")
            print(f"Remaining Player Life: {lives}")
    
    for bullet in bullets[:]:
        bullet_hit = False
        for i, enemy in enumerate(enemies[:]):
            dx = bullet['x'] - enemy[0]
            dy = bullet['y'] - enemy[1]
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < 25:
                score += 10
                bullets.remove(bullet)
                enemies[i][0] = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
                enemies[i][1] = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
                bullet_hit = True
                add_particles(enemy[0], enemy[1], enemy[2])
                break
        
        if not bullet_hit and (abs(bullet['x']) > GRID_LENGTH or abs(bullet['y']) > GRID_LENGTH):
            bullets.remove(bullet)
            if not cheat_mode:
                missed_bullets += 1
                print_feedback(f"Bullet missed: {missed_bullets}")
                print(f"Bullet missed: {missed_bullets}")

def idle():
    global lives, missed_bullets, game_over, bullets, enemy_pulse, last_bullet_time, player_rotation, particles, gun_angle
    
    if game_over:
        return
        
    enemy_pulse += 0.03
    
    for particle in particles[:]:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['z'] += particle['dz']
        particle['life'] -= 1
        if particle['life'] <= 0:
            particles.remove(particle)
    
    for enemy in enemies:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            enemy[0] += dx / distance * enemy[3]
            enemy[1] += dy / distance * enemy[3]
    
    for bullet in bullets[:]:
        bullet['x'] += bullet['dx']
        bullet['y'] += bullet['dy']
        bullet['z'] += bullet['dz']
        bullet['life'] -= 1
        
        if bullet['life'] <= 0:
            bullets.remove(bullet)
    
    if cheat_mode:
        player_rotation += 2
        
        if auto_follow and enemies:
            closest = min(enemies, key=lambda e: math.hypot(e[0]-player_pos[0], e[1]-player_pos[1]))
            dx = closest[0] - player_pos[0]
            dy = closest[1] - player_pos[1]
            target_angle = math.degrees(math.atan2(dy, dx))
            player_rotation = target_angle
        
        current_time = glutGet(GLUT_ELAPSED_TIME)
        if current_time - last_bullet_time > 100:
            if enemies:
                closest = min(enemies, key=lambda e: math.hypot(e[0]-player_pos[0], e[1]-player_pos[1]))
                
                angle_rad = math.radians(player_rotation)
                gun_x = player_pos[0] + math.cos(angle_rad) * GUN_OFFSET_FROM_CENTER - math.sin(angle_rad) * 0
                gun_y = player_pos[1] + math.sin(angle_rad) * GUN_OFFSET_FROM_CENTER + math.cos(angle_rad) * 0
                bullet_start_x = gun_x + math.cos(angle_rad) * GUN_BARREL_LENGTH
                bullet_start_y = gun_y + math.sin(angle_rad) * GUN_BARREL_LENGTH
                
                dx = closest[0] - bullet_start_x
                dy = closest[1] - bullet_start_y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    dx /= dist
                    dy /= dist
                
                bullets.append({
                    'x': bullet_start_x,
                    'y': bullet_start_y,
                    'z': GUN_HEIGHT,
                    'dx': dx * BULLET_SPEED * 2,
                    'dy': dy * BULLET_SPEED * 2,
                    'dz': 0,
                    'life': 100
                })
                last_bullet_time = current_time
                print("Player Bullet Fired!")
                print_feedback("Bullet fired!")
    check_collisions()
    
    if lives <= 0 or missed_bullets >= 10:
        game_over = True
        print_feedback("Game Over! Press R to restart.")
    
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    draw_grid()
    
    if not game_over:
        draw_player()
        draw_enemies()
        draw_bullets()
        draw_particles()
        
        glDisable(GL_DEPTH_TEST)
        draw_text(10, 770, f"Player Life Remaining: {lives}")
        draw_text(10, 740, f"Game Score: {score}")
        draw_text(10, 710, f"Player Bullet Missed: {missed_bullets}")
        draw_feedback_panel()
        glEnable(GL_DEPTH_TEST)
    else:
        draw_player()
        
        glDisable(GL_DEPTH_TEST)
        glColor4f(0, 0, 0, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(0, 700)
        glVertex2f(400, 700)
        glVertex2f(400, 800)
        glVertex2f(0, 800)
        glEnd()
        
        draw_text(50, 770, f"Game is Over. Your Score is {score}.", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(50, 740, 'Press "R" to RESTART the Game.', GLUT_BITMAP_TIMES_ROMAN_24)
        glEnable(GL_DEPTH_TEST)
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Assignment3:Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    init_enemies()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()