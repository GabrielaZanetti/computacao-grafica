"""
EI 03 - Visualização e Manipulação de Objetos 3D

Requisitos:
    pip install pygame PyOpenGL PyOpenGL_accelerate

Execução:
    python 03.py

Controles:
    W/S -> Rotação eixo X
    A/D -> Rotação eixo Y
    Q/E -> Rotação eixo Z

    SETAS ↑ ↓ ← → -> Translação
    Z/X -> Zoom

    + / - -> Escala
    O -> Carregar arquivo .OBJ
    ESC -> Sair

O programa implementa:
    - Renderização de objetos 3D
    - Projeção 3D para 2D (pipeline OpenGL)
    - Leitura de arquivos .OBJ
    - Transformações geométricas
    - Interação por teclado
"""

import math
import os
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# ==========================================================
# OBJ LOADER
# ==========================================================
class OBJ:
    def __init__(self, filename=None):
        self.vertices = []
        self.faces = []

        if filename:
            self.load(filename)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("v "):
                    values = line.strip().split()[1:]
                    vertex = tuple(map(float, values))
                    self.vertices.append(vertex)

                elif line.startswith("f "):
                    values = line.strip().split()[1:]
                    face = []

                    for value in values:
                        index = value.split("/")[0]
                        face.append(int(index) - 1)

                    self.faces.append(face)

    def draw(self):
        glBegin(GL_LINES)

        for face in self.faces:
            for i in range(len(face)):
                v1 = self.vertices[face[i]]
                v2 = self.vertices[face[(i + 1) % len(face)]]

                glVertex3fv(v1)
                glVertex3fv(v2)

        glEnd()


# ==========================================================
# CUBO PADRÃO
# ==========================================================
vertices_cubo = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

arestas_cubo = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)


def desenhar_cubo():
    glBegin(GL_LINES)

    for aresta in arestas_cubo:
        for vertice in aresta:
            glVertex3fv(vertices_cubo[vertice])

    glEnd()


# ==========================================================
# CONFIGURAÇÃO OPENGL
# ==========================================================
def inicializar():
    pygame.init()

    display = (1000, 700)

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("EI 03 - Objetos 3D")

    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

    glTranslatef(0.0, 0.0, -8)

    glEnable(GL_DEPTH_TEST)


# ==========================================================
# MAIN
# ==========================================================
def main():
    inicializar()

    obj_model = None

    rot_x = 0
    rot_y = 0
    rot_z = 0

    pos_x = 0
    pos_y = 0
    pos_z = -8

    escala = 1.0

    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # ROTAÇÃO
                if event.key == pygame.K_w:
                    rot_x += 5

                elif event.key == pygame.K_s:
                    rot_x -= 5

                elif event.key == pygame.K_a:
                    rot_y += 5

                elif event.key == pygame.K_d:
                    rot_y -= 5

                elif event.key == pygame.K_q:
                    rot_z += 5

                elif event.key == pygame.K_e:
                    rot_z -= 5

                # TRANSLAÇÃO
                elif event.key == pygame.K_LEFT:
                    pos_x -= 0.2

                elif event.key == pygame.K_RIGHT:
                    pos_x += 0.2

                elif event.key == pygame.K_UP:
                    pos_y += 0.2

                elif event.key == pygame.K_DOWN:
                    pos_y -= 0.2

                # ZOOM
                elif event.key == pygame.K_z:
                    pos_z += 0.5

                elif event.key == pygame.K_x:
                    pos_z -= 0.5

                # ESCALA
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    escala += 0.1

                elif event.key == pygame.K_MINUS:
                    escala = max(0.1, escala - 0.1)

                # CARREGAR OBJ
                elif event.key == pygame.K_o:
                    caminho = input(
                        "\nDigite o caminho do arquivo OBJ: "
                    ).strip()

                    if os.path.exists(caminho):
                        try:
                            obj_model = OBJ(caminho)
                            print("Modelo OBJ carregado com sucesso.")
                        except Exception as erro:
                            print("Erro ao carregar OBJ:", erro)
                    else:
                        print("Arquivo não encontrado.")

                elif event.key == pygame.K_ESCAPE:
                    running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        gluPerspective(45, (1000 / 700), 0.1, 100.0)

        glTranslatef(pos_x, pos_y, pos_z)

        glScalef(escala, escala, escala)

        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)
        glRotatef(rot_z, 0, 0, 1)

        glColor3f(1.0, 1.0, 1.0)

        if obj_model:
            obj_model.draw()
        else:
            desenhar_cubo()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
