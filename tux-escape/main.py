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

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


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
            draw_text("Circuito correto! Clique fora dos botoes para ir para Fase 3.", font, GREEN, 80, 520)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_a = button_a.click(event.pos)
                clicked_b = button_b.click(event.pos)

                if lamp.on and not clicked_a and not clicked_b:
                    return True

        pygame.display.flip()

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
                draw_text("Correto! A resposta e OR. Fase 3 concluida.", font, GREEN, 170, 520)
            else:
                draw_text("Ainda nao. Continue testando outra porta.", font, RED, 190, 520)
        else:
            lamp.on = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_a.click(event.pos)
                button_b.click(event.pos)

                for choice in choice_buttons:
                    if choice.click(event.pos):
                        selected_gate = choice.label

        pygame.display.flip()

    return False

def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Tux Escape: A Revolta dos Circuitos", font, BLACK, 200, 200)
        draw_text("Clique para Iniciar", font, BLUE, 300, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                completed_phase_2 = phase_2_and()
                if completed_phase_2:
                    phase_3_choose_gate()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()