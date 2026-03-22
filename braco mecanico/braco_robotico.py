import pygame
import math
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 930, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braço Robótico 2D")

clock = pygame.time.Clock()

# Cores
INK = (13, 9, 19)
GRID = (34, 28, 51)
LILAC = (154, 92, 207)
VIOLET = (111, 75, 182)
AZURE = (63, 126, 214)
NEON_BLUE = (96, 170, 245)
JOINT = (212, 225, 255)

# Estado do braço
base_x = WIDTH // 2 + random.randint(-55, 45)
base_y = HEIGHT // 2 + random.randint(-18, 18)

angle1 = random.randint(-35, 70)  # braço 1
angle2 = random.randint(-120, 35)  # braço 2

length1 = random.randint(110, 150)
length2 = random.randint(90, 130)

BASE_SPEED = 4
ROT_SPEED_1 = 2.3
ROT_SPEED_2 = 2.0

base_radius = random.randint(9, 12)
joint_radius = random.randint(6, 8)
arm_width_1 = random.randint(7, 10)
arm_width_2 = random.randint(5, 8)

def draw_axes():
    pygame.draw.line(screen, GRID, (0, base_y), (WIDTH, base_y), 1)
    pygame.draw.line(screen, GRID, (base_x, 0), (base_x, HEIGHT), 1)

def draw_arm():
    global base_x, base_y, angle1, angle2

    # Base
    base_pos = (base_x, base_y)

    # Braço 1
    x1 = base_x + length1 * math.cos(math.radians(angle1))
    y1 = base_y - length1 * math.sin(math.radians(angle1))

    # Braço 2
    x2 = x1 + length2 * math.cos(math.radians(angle1 + angle2))
    y2 = y1 - length2 * math.sin(math.radians(angle1 + angle2))

    # Desenho
    pygame.draw.circle(screen, LILAC, base_pos, base_radius)
    pygame.draw.line(screen, VIOLET, base_pos, (x1, y1), arm_width_1)
    pygame.draw.circle(screen, JOINT, (int(x1), int(y1)), joint_radius)
    pygame.draw.line(screen, AZURE, (x1, y1), (x2, y2), arm_width_2)
    pygame.draw.circle(screen, NEON_BLUE, (int(x2), int(y2)), joint_radius)

running = True
while running:
    screen.fill(INK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movimento da base
    if keys[pygame.K_LEFT]:
        base_x -= BASE_SPEED
    if keys[pygame.K_RIGHT]:
        base_x += BASE_SPEED
    if keys[pygame.K_UP]:
        base_y -= BASE_SPEED
    if keys[pygame.K_DOWN]:
        base_y += BASE_SPEED

    # Rotação braço 1
    if keys[pygame.K_a]:
        angle1 += ROT_SPEED_1
    if keys[pygame.K_d]:
        angle1 -= ROT_SPEED_1

    # Rotação braço 2
    if keys[pygame.K_w]:
        angle2 += ROT_SPEED_2
    if keys[pygame.K_s]:
        angle2 -= ROT_SPEED_2

    draw_axes()
    draw_arm()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()