import math
import random
import time

import pygame


# Inicializacao
pygame.init()
WIDTH = 740 + random.randint(-20, 24)
HEIGHT = 720 + random.randint(-18, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aula 05 - Relogio Analogico")
clock = pygame.time.Clock()


# Painel no canto superior esquerdo
PANEL_X = 18
PANEL_Y = 16
PANEL_W = 280
PANEL_H = 238


# Geometria base
SAFE_LEFT = PANEL_X + PANEL_W + 28
CENTER = (
	(SAFE_LEFT + (WIDTH - 24)) // 2 + random.randint(-6, 6),
	HEIGHT // 2 + random.randint(8, 22),
)

max_radius = min(
	CENTER[0] - SAFE_LEFT,
	WIDTH - CENTER[0] - 24,
	CENTER[1] - 26,
	HEIGHT - CENTER[1] - 24,
)
RADIUS = max(170, min(max_radius - 6, random.randint(196, 222)))

MAIN_HOUR_LEN = int(RADIUS * random.uniform(0.48, 0.54))
MAIN_MIN_LEN = int(RADIUS * random.uniform(0.70, 0.78))
MAIN_SEC_LEN = int(RADIUS * random.uniform(0.82, 0.90))

MAIN_HOUR_W = random.randint(7, 9)
MAIN_MIN_W = random.randint(5, 7)
MAIN_SEC_W = random.randint(2, 3)


# Cores (tema preto/roxo/azul)
BG = (10, 8, 17)
RING = (184, 171, 255)
RING_SOFT = (105, 92, 156)
NUMBERS = (219, 225, 255)
TICK = (108, 101, 160)
HOUR_COLOR = (144, 98, 232)
MINUTE_COLOR = (86, 130, 245)
SECOND_COLOR = (126, 205, 255)
ALARM_COLOR = (191, 157, 255)
CENTER_DOT = (232, 236, 255)
PANEL_BG = (22, 18, 35)
PANEL_EDGE = (80, 69, 126)
TEXT_COLOR = (228, 230, 255)


# Fonte
font_numbers = pygame.font.SysFont(None, 38)
font_help = pygame.font.SysFont(None, 24)
font_alarm = pygame.font.SysFont(None, 30)


# Alarme
alarm_hour = random.randint(0, 23)
alarm_minute = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])


MINI_CENTER = (PANEL_X + PANEL_W // 2, PANEL_Y + 165)
MINI_RADIUS = 62


def angle_from_clock(hours=0, minutes=0, seconds=0):
	total_hours = (hours % 12) + (minutes / 60.0) + (seconds / 3600.0)
	return math.radians(total_hours * 30 - 90)


def draw_hand(center, angle, length, color, width):
	x = center[0] + int(math.cos(angle) * length)
	y = center[1] + int(math.sin(angle) * length)
	pygame.draw.line(screen, color, center, (x, y), width)


def draw_ticks(center, radius):
	for i in range(60):
		angle = math.radians(i * 6 - 90)
		outer_x = center[0] + int(math.cos(angle) * (radius - 6))
		outer_y = center[1] + int(math.sin(angle) * (radius - 6))

		if i % 5 == 0:
			inner_len = radius - 30
			width = 3
		else:
			inner_len = radius - 16
			width = 1

		inner_x = center[0] + int(math.cos(angle) * inner_len)
		inner_y = center[1] + int(math.sin(angle) * inner_len)
		pygame.draw.line(screen, TICK, (inner_x, inner_y), (outer_x, outer_y), width)


def draw_numbers(center, radius):
	for i in range(1, 13):
		angle = math.radians(i * 30 - 90)
		x = center[0] + int(math.cos(angle) * (radius - 52))
		y = center[1] + int(math.sin(angle) * (radius - 52))
		text = font_numbers.render(str(i), True, NUMBERS)
		rect = text.get_rect(center=(x, y))
		screen.blit(text, rect)


def draw_alarm_panel():
	# Caixa de fundo do painel
	pygame.draw.rect(screen, PANEL_BG, (PANEL_X, PANEL_Y, PANEL_W, PANEL_H), border_radius=12)
	pygame.draw.rect(screen, PANEL_EDGE, (PANEL_X, PANEL_Y, PANEL_W, PANEL_H), 2, border_radius=12)

	# Instrucoes acima do alarme
	instr1 = font_help.render("Controles do alarme:", True, TEXT_COLOR)
	instr2 = font_help.render("Cima/Baixo = hora", True, TEXT_COLOR)
	instr3 = font_help.render("Esquerda/Direita = minuto", True, TEXT_COLOR)
	screen.blit(instr1, (PANEL_X + 12, PANEL_Y + 10))
	screen.blit(instr2, (PANEL_X + 12, PANEL_Y + 30))
	screen.blit(instr3, (PANEL_X + 12, PANEL_Y + 50))

	# Texto do alarme no canto superior esquerdo
	alarm_text = font_alarm.render(f"Alarme: {alarm_hour:02d}:{alarm_minute:02d}", True, ALARM_COLOR)
	screen.blit(alarm_text, (PANEL_X + 12, PANEL_Y + 78))

	# Mini relogio analogico abaixo do alarme
	pygame.draw.circle(screen, RING_SOFT, MINI_CENTER, MINI_RADIUS, 2)
	pygame.draw.circle(screen, RING_SOFT, MINI_CENTER, MINI_RADIUS - 1, 1)

	for i in range(12):
		ang = math.radians(i * 30 - 90)
		o_x = MINI_CENTER[0] + int(math.cos(ang) * (MINI_RADIUS - 4))
		o_y = MINI_CENTER[1] + int(math.sin(ang) * (MINI_RADIUS - 4))
		i_x = MINI_CENTER[0] + int(math.cos(ang) * (MINI_RADIUS - 14))
		i_y = MINI_CENTER[1] + int(math.sin(ang) * (MINI_RADIUS - 14))
		pygame.draw.line(screen, TICK, (i_x, i_y), (o_x, o_y), 2)

	alarm_hour_angle = angle_from_clock(alarm_hour % 12, alarm_minute, 0)
	alarm_min_angle = math.radians(alarm_minute * 6 - 90)
	draw_hand(MINI_CENTER, alarm_hour_angle, int(MINI_RADIUS * 0.55), HOUR_COLOR, 4)
	draw_hand(MINI_CENTER, alarm_min_angle, int(MINI_RADIUS * 0.78), MINUTE_COLOR, 3)
	pygame.draw.circle(screen, CENTER_DOT, MINI_CENTER, 4)


running = True
while running:
	screen.fill(BG)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				alarm_hour = (alarm_hour + 1) % 24
			elif event.key == pygame.K_DOWN:
				alarm_hour = (alarm_hour - 1) % 24
			elif event.key == pygame.K_RIGHT:
				alarm_minute = (alarm_minute + 1) % 60
			elif event.key == pygame.K_LEFT:
				alarm_minute = (alarm_minute - 1) % 60

	# Hora atual do sistema
	now = time.localtime()
	sec = now.tm_sec
	minute = now.tm_min
	hour = now.tm_hour % 12

	# Angulos dos ponteiros principais
	sec_angle = math.radians(sec * 6 - 90)
	min_angle = math.radians(minute * 6 + sec * 0.1 - 90)
	hour_angle = angle_from_clock(hour, minute, sec)

	# Mostrador principal
	pygame.draw.circle(screen, RING, CENTER, RADIUS, 4)
	pygame.draw.circle(screen, RING_SOFT, CENTER, RADIUS - 2, 1)
	draw_ticks(CENTER, RADIUS)
	draw_numbers(CENTER, RADIUS)

	# Ponteiros principais
	draw_hand(CENTER, hour_angle, MAIN_HOUR_LEN, HOUR_COLOR, MAIN_HOUR_W)
	draw_hand(CENTER, min_angle, MAIN_MIN_LEN, MINUTE_COLOR, MAIN_MIN_W)
	draw_hand(CENTER, sec_angle, MAIN_SEC_LEN, SECOND_COLOR, MAIN_SEC_W)

	# Ponteiro de alarme no relogio principal
	alarm_angle = math.radians((alarm_hour % 12) * 30 + alarm_minute * 0.5 - 90)
	draw_hand(CENTER, alarm_angle, int(RADIUS * 0.73), ALARM_COLOR, 3)

	pygame.draw.circle(screen, CENTER_DOT, CENTER, 7)
	draw_alarm_panel()

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
