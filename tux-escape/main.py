import pygame
import sys
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PlayerAnimator:
    """Gerencia a animação do personagem baseado na direção e movimentação."""
    def __init__(self, images_path=None, scale=0.55):
        self.images_path = images_path or os.path.join(BASE_DIR, "images")
        self.scale = scale
        self.animations = {}
        self.current_direction = "front"
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 8  # Frames para trocar de sprite (60/8 = 7.5 FPS)
        self.last_dx = 0
        self.last_dy = 0
        self.load_animations()
    
    def load_animations(self):
        """Carrega todas as imagens de animação."""
        fallback_path = os.path.join(BASE_DIR, "tux.png")
        fallback_img = None
        if os.path.exists(fallback_path):
            fallback_img = pygame.image.load(fallback_path).convert_alpha()

        direction_files = {
            "front": "front",
            "back": "back",
            "left": "left",
            "right": "right",
        }
        for direction, file_prefix in direction_files.items():
            self.animations[direction] = []
            for i in range(1, 4):  # 3 frames por direção
                path = os.path.join(self.images_path, f"{file_prefix}{i}.png")
                if os.path.exists(path):
                    img = pygame.image.load(path).convert_alpha()
                elif fallback_img:
                    img = fallback_img.copy()
                else:
                    img = pygame.Surface((40, 52), pygame.SRCALPHA)
                    pygame.draw.ellipse(img, (255, 255, 255), (6, 4, 28, 44))
                    pygame.draw.ellipse(img, (0, 0, 0), (10, 8, 20, 36))
                if self.scale != 1:
                    width = max(1, int(img.get_width() * self.scale))
                    height = max(1, int(img.get_height() * self.scale))
                    img = pygame.transform.smoothscale(img, (width, height))
                self.animations[direction].append(img)
    
    def update(self, dx, dy):
        """Atualiza a animação baseado no movimento."""
        # Só anima se houver movimento
        if dx != 0 or dy != 0:
            # Detecta a direção do movimento
            if abs(dx) > abs(dy):
                self.current_direction = "right" if dx > 0 else "left"
            else:
                self.current_direction = "front" if dy > 0 else "back"
            
            # Incrementa contador de frames apenas durante movimento
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                frames = self.animations.get(self.current_direction, [])
                if frames:
                    self.current_frame = (self.current_frame + 1) % len(frames)
                else:
                    self.current_frame = 0
        else:
            # Reseta a animação quando parar de se mover
            self.frame_counter = 0
            self.current_frame = 0
    
    def get_current_image(self):
        """Retorna a imagem atual da animação."""
        frames = self.animations.get(self.current_direction, [])
        if not frames:
            for fallback_frames in self.animations.values():
                if fallback_frames:
                    frames = fallback_frames
                    break
        if frames:
            self.current_frame %= len(frames)
            return frames[self.current_frame]
        return None
    
    def get_rect(self, pos):
        """Retorna o rect da imagem atual centralizado na posição."""
        img = self.get_current_image()
        if img:
            return img.get_rect(center=pos)
        return pygame.Rect(pos[0], pos[1], int(40 * self.scale), int(52 * self.scale))

def load_intro_surface():
    path_png = os.path.join(BASE_DIR, "intro.png")
    try:
        if os.path.exists(path_png):
            img = pygame.image.load(path_png)
            return img.convert_alpha()
    except Exception:
        pass

    return None


def main_menu():
    pygame.init()
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tux Escape - Menu")

    DARK_BG = (18, 18, 26)
    WHITE = (255, 255, 255)
    SOFT_WHITE = (240, 240, 240)
    RED = (220, 30, 30)
    GREEN = (30, 180, 60)
    BLACK = (0, 0, 0)

    font_large = pygame.font.Font(None, 64)
    font = pygame.font.Font(None, 36)
    small = pygame.font.Font(None, 24)

    intro_surface = load_intro_surface()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(DARK_BG)

        mouse_pos = pygame.mouse.get_pos()

        # Top margin and available sizes
        top_margin = 40
        max_img_w = int(SCREEN_WIDTH * 0.75)
        max_img_h = 300
        current_y = top_margin

        # Intro image / placeholder
        if intro_surface:
            iw, ih = intro_surface.get_size()
            scale = min(max_img_w / iw, max_img_h / ih, 1)
            new_w = int(iw * scale)
            new_h = int(ih * scale)
            img = pygame.transform.smoothscale(intro_surface, (new_w, new_h))
            img_rect = img.get_rect(center=(SCREEN_WIDTH // 2, current_y + new_h // 2))
            screen.blit(img, img_rect)
            current_y += new_h + 20
        else:
            ph_w = max_img_w
            ph_h = 200
            ph_rect = pygame.Rect((SCREEN_WIDTH - ph_w) // 2, current_y, ph_w, ph_h)
            pygame.draw.rect(screen, (60, 60, 70), ph_rect, border_radius=8)
            txt_ph = small.render("(intro.png não encontrado)", True, SOFT_WHITE)
            screen.blit(txt_ph, txt_ph.get_rect(center=ph_rect.center))
            current_y += ph_h + 20

        # Texto vermelho centralizado
        red_text = font_large.render("INICIAR O JOGO", True, RED)
        red_rect = red_text.get_rect(center=(SCREEN_WIDTH // 2, current_y + 24))
        screen.blit(red_text, red_rect)
        current_y += 80

        # Botão verde estilo 'tec'
        btn_w = 260
        btn_h = 72
        btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, current_y, btn_w, btn_h)
        hover = btn_rect.collidepoint(mouse_pos)
        base = GREEN
        color = tuple(min(255, c + 30) for c in base) if hover else base
        pygame.draw.rect(screen, color, btn_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, btn_rect, 3, border_radius=12)
        label = font.render("Iniciar", True, BLACK)
        screen.blit(label, label.get_rect(center=btn_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    show_portal_map(screen, clock)
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def show_portal_map(screen, clock):
    """Mapa com 3 portas (AND, OR, NOR) que o jogador pode explorar"""
    font_big = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 32)
    font_tiny = pygame.font.Font(None, 20)
    
    pure_black = (0, 0, 0)
    pure_white = (255, 255, 255)
    blue = (0, 100, 200)
    yellow = (255, 255, 0)
    green = (0, 200, 0)
    
    # Inicializa o animador do personagem
    player_animator = PlayerAnimator()
    player_pos = [500, 600]
    player_speed = 4
    
    # 3 Portas
    gates_info = [
        {"name": "AND", "color": blue, "rect": pygame.Rect(150, 150, 150, 200), "done": False},
        {"name": "OR", "color": yellow, "rect": pygame.Rect(425, 150, 150, 200), "done": False},
        {"name": "NOR", "color": green, "rect": pygame.Rect(700, 150, 150, 200), "done": False},
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += player_speed
        
        # Atualiza animação
        player_animator.update(dx, dy)
        
        # Move o personagem
        next_pos = [player_pos[0] + dx, player_pos[1] + dy]
        next_pos[0] = max(50, min(screen.get_width() - 50, next_pos[0]))
        next_pos[1] = max(50, min(screen.get_height() - 100, next_pos[1]))
        player_pos = next_pos
        
        player_rect = player_animator.get_rect(player_pos)
        
        # Verifica colisão com as portas
        for i, gate in enumerate(gates_info):
            if player_rect.colliderect(gate["rect"]):
                # Só entra se a porta ainda não estiver concluída
                if not gate.get("done"):
                    show_gate_explanation(screen, clock, gate["name"], gate["color"])
                    gates_info[i]["done"] = True
                # Reposiciona abaixo da porta para evitar reentrada imediata
                player_pos = [gate["rect"].centerx, gate["rect"].bottom + 100]
                break
        
        screen.fill(pure_black)
        
        # Título do mapa
        title = font_big.render("ESCOLHA UMA PORTA", True, pure_white)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 20))
        
        # Desenha as 3 portas
        for gate in gates_info:
            pygame.draw.rect(screen, gate["color"], gate["rect"], border_radius=12)
            pygame.draw.rect(screen, pure_white, gate["rect"], 3, border_radius=12)
            
            # Nome da porta
            name_text = font_small.render(gate["name"], True, pure_black)
            screen.blit(name_text, name_text.get_rect(center=(gate["rect"].centerx, gate["rect"].centery - 30)))
            
            # Marca concluída (OK) se 'done' estiver True
            if gate.get("done"):
                pad = 5
                ok_text = font_small.render("OK", True, (0, 200, 0))
                ok_w, ok_h = ok_text.get_width(), ok_text.get_height()
                ok_bg_w, ok_bg_h = ok_w + pad * 2, ok_h + pad * 2
                ok_bg_x = gate["rect"].right - ok_bg_w - 8
                ok_bg_y = gate["rect"].top + 8
                ok_bg = pygame.Rect(ok_bg_x, ok_bg_y, ok_bg_w, ok_bg_h)
                pygame.draw.rect(screen, pure_white, ok_bg, border_radius=6)
                screen.blit(ok_text, (ok_bg.x + pad, ok_bg.y + pad))
        
        # Desenha o personagem
        player_img = player_animator.get_current_image()
        if player_img:
            screen.blit(player_img, player_rect)
        
        # Instrução
        hint = font_tiny.render("Encoste em uma porta para entrar | ESC para voltar", True, pure_white)
        screen.blit(hint, (50, screen.get_height() - 30))
        
        pygame.display.flip()
        clock.tick(60)


def show_gate_explanation(screen, clock, gate_name, gate_color):
    """Tela de explicação detalhada de cada porta lógica com teste interativo"""
    font_big = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 44)
    font_small = pygame.font.Font(None, 32)
    font_tiny = pygame.font.Font(None, 24)

    pure_black = (0, 0, 0)
    pure_white = (255, 255, 255)
    green_on = (0, 255, 0)
    red_off = (128, 0, 0)
    dark_gray = (40, 40, 40)

    descriptions = {
        "AND": ("Porta E (AND)", "Saída = 1 apenas se AMBAS as entradas são 1"),
        "OR": ("Porta OU (OR)", "Saída = 1 se PELO MENOS UMA entrada é 1"),
        "NOR": ("Porta NOR", "Saída = 1 apenas se NENHUMA entrada é 1")
    }

    input1 = 0
    input2 = 0

    # Botões de entrada (empilhados)
    btn_input1 = pygame.Rect(200, 300, 120, 80)
    btn_input2 = pygame.Rect(200, 420, 120, 80)

    # Lâmpada
    lamp_rect = pygame.Rect(750, 300, 120, 150)

    gate_title, gate_desc = descriptions[gate_name]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_input1.collidepoint(event.pos):
                    input1 = 1 - input1
                if btn_input2.collidepoint(event.pos):
                    input2 = 1 - input2

        if gate_name == "AND":
            output = input1 and input2
        elif gate_name == "OR":
            output = input1 or input2
        else:
            output = not (input1 or input2)

        screen.fill(pure_black)

        # Título e descrição
        title = font_big.render(gate_title, True, gate_color)
        screen.blit(title, (100, 30))
        desc_text = font_small.render(gate_desc, True, gate_color)
        screen.blit(desc_text, (100, 120))


        # Entradas
        def draw_input_button(rect, value, label):
            label_text = font_small.render(label, True, pure_white)
            screen.blit(label_text, (rect.x + 10, rect.y - 40))

            shadow_rect = rect.move(5, 5)
            pygame.draw.rect(screen, (35, 35, 35), shadow_rect, border_radius=10)
            base_rect = rect.move(0, 4)
            pygame.draw.rect(screen, (90, 25, 25), base_rect, border_radius=10)

            press_offset = 4 if value else 0
            button_rect = rect.move(press_offset, press_offset)
            button_color = green_on if value else red_off
            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(screen, pure_white, button_rect, 2, border_radius=10)

            highlight_y = button_rect.y + 6 if not value else button_rect.y + 3
            pygame.draw.line(screen, (255, 255, 255),
                             (button_rect.x + 12, highlight_y),
                             (button_rect.right - 12, highlight_y), 2)

            value_text = font_medium.render(str(value), True, pure_black)
            screen.blit(value_text, value_text.get_rect(center=button_rect.center))

        draw_input_button(btn_input1, input1, "Entrada 1")
        draw_input_button(btn_input2, input2, "Entrada 2")

        # Fios (vindo de baixo dos botões até a lâmpada)
        wire1_color = green_on if input1 else red_off
        pygame.draw.line(screen, wire1_color, (btn_input1.centerx, btn_input1.bottom + 10),
                         (lamp_rect.centerx - 30, lamp_rect.centery), 4)
        wire2_color = green_on if input2 else red_off
        pygame.draw.line(screen, wire2_color, (btn_input2.centerx, btn_input2.bottom + 10),
                         (lamp_rect.centerx + 30, lamp_rect.centery), 4)

        # Desenha uma lâmpada estilizada
        bulb_center = (lamp_rect.centerx, lamp_rect.centery - 20)
        bulb_radius = min(lamp_rect.width, lamp_rect.height) // 4
        # Glow quando ligada
        if output:
            glow_s = pygame.Surface((bulb_radius * 6, bulb_radius * 6), pygame.SRCALPHA)
            glow_color = (255, 220, 80, 80)
            pygame.draw.circle(glow_s, glow_color, (glow_s.get_width() // 2, glow_s.get_height() // 2), bulb_radius * 2)
            screen.blit(glow_s, (bulb_center[0] - glow_s.get_width() // 2, bulb_center[1] - glow_s.get_height() // 2))

        # Corpo do bulbo
        bulb_color = (255, 220, 80) if output else (80, 80, 80)
        pygame.draw.circle(screen, bulb_color, bulb_center, bulb_radius)
        pygame.draw.circle(screen, pure_white, bulb_center, bulb_radius, 2)

        # Filamento
        fil_color = (200, 100, 0) if output else (50, 30, 30)
        fx, fy = bulb_center
        pygame.draw.line(screen, fil_color, (fx - bulb_radius // 2, fy), (fx + bulb_radius // 2, fy), 3)
        pygame.draw.line(screen, fil_color, (fx - bulb_radius // 2 + 6, fy + 6), (fx - bulb_radius // 2, fy), 2)
        pygame.draw.line(screen, fil_color, (fx + bulb_radius // 2 - 6, fy + 6), (fx + bulb_radius // 2, fy), 2)

        # Base da lâmpada
        base_w = bulb_radius
        base_h = bulb_radius // 2
        base_rect = pygame.Rect(fx - base_w // 2, fy + bulb_radius - 4, base_w, base_h)
        pygame.draw.rect(screen, (100, 100, 100), base_rect)
        pygame.draw.rect(screen, pure_white, base_rect, 2)

        lamp_label = font_small.render("Saída", True, pure_white)
        screen.blit(lamp_label, (lamp_rect.x + 20, lamp_rect.bottom + 10))

        # Operação e instrução
        if gate_name == "AND":
            operation = f"{input1} AND {input2} = {int(output)}"
        elif gate_name == "OR":
            operation = f"{input1} OR {input2} = {int(output)}"
        else:
            operation = f"{input1} NOR {input2} = {int(output)}"
        op_text = font_small.render(operation, True, gate_color)
        screen.blit(op_text, (100, 480))
        hint = font_tiny.render("Pressione ENTER ou ESC para voltar", True, pure_white)
        screen.blit(hint, (100, 620))

        pygame.display.flip()
        clock.tick(60)


def run_game(screen, clock):
    # Cena minimalista: apenas preto e branco piscando + dialogos.
    pure_black = (0, 0, 0)
    pure_white = (255, 255, 255)
    soft_white = (241, 242, 243)  # #f1f2f3
    soft_black = (33, 33, 33)     # #212121

    bubble_color = pure_white
    bubble_border = pure_black
    text_color = pure_black
    small_font = pygame.font.Font(None, 28)

    # Inicializa o animador do personagem
    player_animator = PlayerAnimator()
    player_pos = [120, 460]
    player_speed = 4
    phase_1_door = pygame.Rect(60, screen.get_height() - 180, 120, 150)

    dialog_duration_ms = 3000
    first_start = 0
    first_end = first_start + dialog_duration_ms
    second_start = first_end
    second_end = second_start + dialog_duration_ms

    # Pisca de forma suave entre #f1f2f3 e #212121.
    blink_period_ms = 2200
    start_ticks = pygame.time.get_ticks()

    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                in_game = False

        elapsed = pygame.time.get_ticks() - start_ticks
        dialog_phase = elapsed < second_end
        instruction_visible = elapsed >= second_end

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # Enquanto os dialogos aparecem, personagem nao anda.
        if not dialog_phase:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy -= player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy += player_speed

        # Balao de instrucoes no canto superior direito.
        instruction_rect = pygame.Rect(screen.get_width() - 360, 20, 340, 90)

        # Move em dois eixos para tratar colisao com o balao.
        next_pos = [player_pos[0] + dx, player_pos[1] + dy]
        
        # Cria rect temporário para verificar colisões
        player_animator.update(dx, dy)
        player_rect = player_animator.get_rect(next_pos)
        
        if instruction_visible and player_rect.colliderect(instruction_rect):
            next_pos[0] = player_pos[0]
            player_rect = player_animator.get_rect(next_pos)
        
        if instruction_visible and player_rect.colliderect(instruction_rect):
            next_pos[1] = player_pos[1]
            player_rect = player_animator.get_rect(next_pos)

        # Limita os limites da tela
        next_pos[0] = max(20, min(screen.get_width() - 40, next_pos[0]))
        next_pos[1] = max(20, min(screen.get_height() - 52, next_pos[1]))
        player_pos = next_pos

        if dialog_phase:
            phase = (elapsed % blink_period_ms) / blink_period_ms
            wave = (math.sin(phase * 2 * math.pi) + 1.0) / 2.0
            bg = (
                int(soft_black[0] + (soft_white[0] - soft_black[0]) * wave),
                int(soft_black[1] + (soft_white[1] - soft_black[1]) * wave),
                int(soft_black[2] + (soft_white[2] - soft_black[2]) * wave),
            )
            fg = pure_black if wave > 0.5 else pure_white
        else:
            # Ao finalizar os dialogos, fundo fica preto total.
            bg = pure_black
            fg = pure_white

        screen.fill(bg)

        # Desenha o personagem animado
        player_img = player_animator.get_current_image()
        if player_img:
            player_rect = player_animator.get_rect(player_pos)
            screen.blit(player_img, player_rect)

        if first_start <= elapsed < first_end:
            bubble_1 = pygame.Rect(screen.get_width() - 560, 20, 540, 90)
            pygame.draw.rect(screen, bubble_color, bubble_1, border_radius=14)
            pygame.draw.rect(screen, bubble_border, bubble_1, 2, border_radius=14)
            txt_1 = small_font.render("O virus atacou o sistema e desligou as lizes", True, text_color)
            screen.blit(txt_1, txt_1.get_rect(center=bubble_1.center))

        elif second_start <= elapsed < second_end:
            bubble_2 = pygame.Rect(screen.get_width() - 560, 20, 540, 90)
            pygame.draw.rect(screen, bubble_color, bubble_2, border_radius=14)
            pygame.draw.rect(screen, bubble_border, bubble_2, 2, border_radius=14)
            txt_2 = small_font.render("Ajuste as missoes para fugir", True, text_color)
            screen.blit(txt_2, txt_2.get_rect(center=bubble_2.center))

        if instruction_visible:
            pygame.draw.rect(screen, bubble_color, instruction_rect, border_radius=14)
            pygame.draw.rect(screen, bubble_border, instruction_rect, 2, border_radius=14)
            line_1 = small_font.render("Movimento:", True, text_color)
            line_2 = small_font.render("WASD / Setas", True, text_color)
            line_3 = small_font.render("ESC para voltar", True, text_color)
            screen.blit(line_1, (instruction_rect.x + 18, instruction_rect.y + 14))
            screen.blit(line_2, (instruction_rect.x + 18, instruction_rect.y + 40))
            screen.blit(line_3, (instruction_rect.x + 18, instruction_rect.y + 64))

            # Porta da Fase 1
            pygame.draw.rect(screen, pure_white, phase_1_door, border_radius=8)
            pygame.draw.rect(screen, pure_black, phase_1_door, 3, border_radius=8)
            door_label = small_font.render("PORTA", True, pure_black)
            phase_label = small_font.render("FASE 1", True, pure_black)
            screen.blit(door_label, door_label.get_rect(center=(phase_1_door.centerx, phase_1_door.y + 45)))
            screen.blit(phase_label, phase_label.get_rect(center=(phase_1_door.centerx, phase_1_door.y + 80)))

            # Ao chegar na porta, vai para o mapa com 3 portas
            if player_rect.colliderect(phase_1_door):
                show_portal_map(screen, clock)
                return

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
