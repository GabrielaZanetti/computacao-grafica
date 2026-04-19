import pygame
import sys
from logic_gates import AndGate, OrGate, NotGate

# Inicializar Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tux Escape: A Revolta dos Circuitos")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Fonte
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

FPS = 60
CLOCK = pygame.time.Clock()

class Button:
    def __init__(self, x, y, width, height, text, value=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.value = value  # 0 ou 1

    def draw(self, screen):
        color = GREEN if self.value == 1 else RED
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(f"{self.text}: {self.value}", True, BLACK)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.value = 1 - self.value  # Alterna 0/1
            return True
        return False

class Lamp:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.on = False

    def draw(self, screen):
        color = GREEN if self.on else GRAY
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 2)

class GateUI:
    def __init__(self, x, y, width, height, gate):
        self.rect = pygame.Rect(x, y, width, height)
        self.gate = gate

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(self.gate.name, True, WHITE)
        screen.blit(text_surf, (self.rect.x + 20, self.rect.y + 15))


class ChoiceButton:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label

    def draw(self, screen, selected=False):
        fill = BLUE if selected else GRAY
        pygame.draw.rect(screen, fill, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(self.label, True, WHITE if selected else BLACK)
        screen.blit(text_surf, (self.rect.x + 12, self.rect.y + 10))

    def click(self, pos):
        return self.rect.collidepoint(pos)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 34)
        self.speed = 4

    def update(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(20, min(SCREEN_WIDTH - self.rect.width - 20, self.rect.x))
        self.rect.y = max(80, min(SCREEN_HEIGHT - self.rect.height - 20, self.rect.y))

    def draw(self, surface):
        # Corpo azul e barriga branca para lembrar um pinguim simplificado.
        pygame.draw.ellipse(surface, BLUE, self.rect)
        belly = self.rect.inflate(-14, -10)
        pygame.draw.ellipse(surface, WHITE, belly)
        eye_left = (self.rect.x + 10, self.rect.y + 10)
        eye_right = (self.rect.x + 24, self.rect.y + 10)
        pygame.draw.circle(surface, BLACK, eye_left, 2)
        pygame.draw.circle(surface, BLACK, eye_right, 2)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_hub_background():
    screen.fill((188, 230, 188))
    pygame.draw.rect(screen, (150, 205, 150), (0, 80, SCREEN_WIDTH, SCREEN_HEIGHT - 80))

    # Caminhos do mapa.
    pygame.draw.rect(screen, (196, 176, 138), (60, 260, 680, 70), border_radius=20)
    pygame.draw.rect(screen, (196, 176, 138), (360, 160, 70, 280), border_radius=20)

    draw_text("Tux Escape - Mapa de Fases", font, BLACK, 220, 24)
    draw_text("Ande com WASD/setas e aperte E perto do portal.", small_font, BLACK, 150, 56)


def run_selected_gate(gate_name, a_value, b_value):
    if gate_name == "AND":
        return AndGate().compute([a_value, b_value])
    if gate_name == "OR":
        return OrGate().compute([a_value, b_value])
    # NOT usa apenas A para manter a comparacao simples na Fase 3.
    return NotGate().compute([a_value])


def is_gate_correct_for_phase_3(gate_name):
    expected_gate = OrGate()
    combinations = [(False, False), (False, True), (True, False), (True, True)]

    for a_value, b_value in combinations:
        expected = expected_gate.compute([a_value, b_value])
        selected = run_selected_gate(gate_name, a_value, b_value)
        if expected != selected:
            return False
    return True


def draw_portal(rect, label, unlocked):
    fill = (88, 160, 255) if unlocked else (120, 120, 120)
    pygame.draw.rect(screen, fill, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
    draw_text(label, small_font, WHITE, rect.x + 12, rect.y + 18)


def phase_2_and():
    running = True
    button_a = Button(50, 250, 100, 50, "A")
    button_b = Button(50, 320, 100, 50, "B")
    gate_ui = GateUI(350, 250, 100, 100, AndGate())
    lamp = Lamp(600, 275, 30)

    while running:
        screen.fill(WHITE)
        draw_text("Fase 2: Primeira Porta Lógica - AND", font, BLACK, 200, 50)
        draw_text("Teste combinações: A e B", font, BLACK, 250, 100)
        draw_text("Lâmpada acende apenas quando A=1 E B=1", font, BLACK, 150, 150)

        button_a.draw(screen)
        button_b.draw(screen)
        gate_ui.draw(screen)
        lamp.draw(screen)

        # Computar saída da porta AND
        inputs = [bool(button_a.value), bool(button_b.value)]
        output = gate_ui.gate.compute(inputs)
        lamp.on = output

        if lamp.on:
            draw_text("Circuito correto! Aperte ENTER para voltar ao mapa.", font, GREEN, 95, 520)
        else:
            draw_text("Aperte ESC para sair da fase.", small_font, BLACK, 280, 560)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_a.click(event.pos)
                button_b.click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN and lamp.on:
                    return True

        pygame.display.flip()
        CLOCK.tick(FPS)

    return False


def phase_3_choose_gate():
    running = True
    button_a = Button(50, 250, 100, 50, "A")
    button_b = Button(50, 320, 100, 50, "B")
    lamp = Lamp(600, 275, 30)

    choice_buttons = [
        ChoiceButton(220, 430, 120, 50, "AND"),
        ChoiceButton(360, 430, 120, 50, "OR"),
        ChoiceButton(500, 430, 120, 50, "NOT"),
    ]
    selected_gate = None

    while running:
        screen.fill(WHITE)
        draw_text("Fase 3: Escolhendo a Porta", font, BLACK, 230, 40)
        draw_text("Objetivo: lampada acende quando uma das chaves estiver ligada.", font, BLACK, 70, 90)
        draw_text("Teste A e B e escolha entre AND, OR ou NOT.", font, BLACK, 150, 130)

        button_a.draw(screen)
        button_b.draw(screen)
        lamp.draw(screen)

        for choice in choice_buttons:
            choice.draw(screen, selected=(choice.label == selected_gate))

        if selected_gate is not None:
            output = run_selected_gate(selected_gate, bool(button_a.value), bool(button_b.value))
            lamp.on = output

            if is_gate_correct_for_phase_3(selected_gate):
                draw_text("Correto! A resposta e OR. Aperte ENTER para voltar ao mapa.", small_font, GREEN, 90, 520)
            else:
                draw_text("Ainda nao. Continue testando outra porta.", font, RED, 190, 520)
        else:
            lamp.on = False
            draw_text("Aperte ESC para sair da fase.", small_font, BLACK, 280, 560)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_a.click(event.pos)
                button_b.click(event.pos)

                for choice in choice_buttons:
                    if choice.click(event.pos):
                        selected_gate = choice.label
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN and selected_gate is not None and is_gate_correct_for_phase_3(selected_gate):
                    return True

        pygame.display.flip()
        CLOCK.tick(FPS)

    return False


def hub_world():
    player = Player(120, 290)

    portals = [
        {
            "name": "Fase 2 - AND",
            "rect": pygame.Rect(160, 200, 170, 60),
            "unlock": lambda progress: True,
            "phase_fn": phase_2_and,
            "progress_key": "phase_2_done",
        },
        {
            "name": "Fase 3 - Escolha",
            "rect": pygame.Rect(470, 200, 170, 60),
            "unlock": lambda progress: progress["phase_2_done"],
            "phase_fn": phase_3_choose_gate,
            "progress_key": "phase_3_done",
        },
    ]

    progress = {"phase_2_done": False, "phase_3_done": False}
    running = True

    while running:
        draw_hub_background()
        keys = pygame.key.get_pressed()
        player.update(keys)

        near_portal = None
        for portal in portals:
            unlocked = portal["unlock"](progress)
            draw_portal(portal["rect"], portal["name"], unlocked)

            if unlocked and player.rect.colliderect(portal["rect"].inflate(20, 20)):
                near_portal = portal

            if progress[portal["progress_key"]]:
                draw_text("OK", small_font, GREEN, portal["rect"].right + 8, portal["rect"].y + 18)

        if near_portal:
            draw_text("Aperte E para entrar na fase.", small_font, BLACK, 270, 520)
        else:
            draw_text("Explore o mapa e aproxime-se de um portal.", small_font, BLACK, 230, 520)

        if progress["phase_3_done"]:
            draw_text("Parabens! Tux escapou do antivirus!", font, GREEN, 180, 552)

        player.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and near_portal:
                completed = near_portal["phase_fn"]()
                if completed:
                    progress[near_portal["progress_key"]] = True

        pygame.display.flip()
        CLOCK.tick(FPS)


def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Tux Escape: A Revolta dos Circuitos", font, BLACK, 200, 200)
        draw_text("Clique para iniciar o mapa", font, BLUE, 255, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                hub_world()

        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()