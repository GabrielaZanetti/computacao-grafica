# Aula 05 - Criando um Relógio Analógico com PyGame ou PyOpenGL
# MARCOS RONALDO MELO CAVALHEIRO
# •
# 11 de mar. (editado: 13 de mar.)
# 1 ponto
# Data de entrega: 25 de mar., 19:20
# Data de entrega: Individual

# Objetivo: Desenvolver um relógio analógico sincronizado com o relógio do sistema, utilizando PyGame ou PyOpenGL.

# Requisitos da Atividade:
# O relógio deve ser desenhado em 2D, com os ponteiros ajustando-se em tempo real.
# Os ponteiros devem ter cores diferentes:
#                     * Vermelho para os segundos
#                     * Azul para os minutos
#                     * Verde para as horas
# O relógio deve ter um anel externo indicando a estrutura de um relógio real.
# Deve ser centralizado na tela.
# O acadêmico pode escolher entre PyGame ou PyOpenGL para sua implementação.

# Desafio Extra (Opcional)
# Adicionar os números de 1 a 12 ao redor do relógio.
# Criar um ponteiro de alarme ajustável via teclado.
# O que entregar?
# O código-fonte da implementação.
# Um print da execução do relógio.
# Um pequeno relatório explicando as escolhas feitas na implementação.
# Como Começar?
# Escolha entre PyGame ou PyOpenGL e utilize um dos exemplos disponíveis como referência.
# Opção 1: PyGame
# Usa renderização 2D com superfícies e linhas.
# Opção 2: PyOpenGL
# Usa gráficos vetoriais para desenhar as formas.
# Recursos e Dicas
# Para PyGame:  pip install pygame-ce
# Para PyOpenGL:  pip install PyOpenGL PyOpenGL_accelerate
# Sugestão: Utilize time.localtime() para obter a hora do sistema.
# Cálculo dos ponteiros: Utilize funções trigonométricas (math.sin(), math.cos()) para calcular os ângulos corretamente.
# Dúvidas? Poste nos comentários ou entre em contato com o professor.

# OBS.: 4 academicos escolhidos aletóriamente iram explicar o código


import pygame
import math
import time

# Inicialização
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Relógio Analógico")

clock = pygame.time.Clock()

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250

# Função para desenhar números
def draw_numbers():
    font = pygame.font.SysFont(None, 36)
    for i in range(1, 13):
        angle = math.radians(i * 30 - 90)
        x = CENTER[0] + int(math.cos(angle) * (RADIUS - 40))
        y = CENTER[1] + int(math.sin(angle) * (RADIUS - 40))
        text = font.render(str(i), True, (255, 255, 255))
        rect = text.get_rect(center=(x, y))
        screen.blit(text, rect)

# Função para desenhar ponteiros
def draw_hand(angle, length, color, width):
    x = CENTER[0] + int(math.cos(angle) * length)
    y = CENTER[1] + int(math.sin(angle) * length)
    pygame.draw.line(screen, color, CENTER, (x, y), width)

# Loop principal
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hora atual
    now = time.localtime()
    sec = now.tm_sec
    minute = now.tm_min
    hour = now.tm_hour % 12

    # Ângulos (em radianos)
    sec_angle = math.radians(sec * 6 - 90)
    min_angle = math.radians(minute * 6 + sec * 0.1 - 90)
    hour_angle = math.radians(hour * 30 + minute * 0.5 - 90)

    # Desenhar círculo externo
    pygame.draw.circle(screen, (255, 255, 255), CENTER, RADIUS, 4)

    # Desenhar números
    draw_numbers()

    # Desenhar ponteiros
    draw_hand(hour_angle, 120, (0, 255, 0), 8)   # Verde - horas
    draw_hand(min_angle, 180, (0, 0, 255), 6)    # Azul - minutos
    draw_hand(sec_angle, 220, (255, 0, 0), 2)    # Vermelho - segundos

    pygame.display.flip()
    clock.tick(60)

pygame.quit()