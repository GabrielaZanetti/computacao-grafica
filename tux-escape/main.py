import pygame
import sys
import os
import math

def load_intro_surface(path_pdf="tux-escape/intro.pdf", path_png="tux-escape/intro.png"):
    # Tenta renderizar PDF com PyMuPDF (fitz). Se não disponível, tenta PNG.
    try:
        import fitz
        if os.path.exists(path_pdf):
            doc = fitz.open(path_pdf)
            page = doc.load_page(0)
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            mode = "RGBA" if pix.alpha else "RGB"
            surf = pygame.image.frombuffer(pix.samples, (pix.width, pix.height), mode)
            return surf
    except Exception:
        pass

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
            txt_ph = small.render("(intro.pdf não encontrado)", True, SOFT_WHITE)
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
                    run_game(screen, clock)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def show_phase_1_screen(screen, clock):
    font_big = pygame.font.Font(None, 96)
    font_small = pygame.font.Font(None, 32)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False

        screen.fill((0, 0, 0))
        title = font_big.render("FASE 1", True, (255, 255, 255))
        hint = font_small.render("Pressione ENTER ou ESC para voltar", True, (241, 242, 243))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30)))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40)))
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

    player_rect = pygame.Rect(120, 460, 40, 52)
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
        next_rect = player_rect.copy()
        next_rect.x += dx
        if instruction_visible and next_rect.colliderect(instruction_rect):
            next_rect.x = player_rect.x

        next_rect.y += dy
        if instruction_visible and next_rect.colliderect(instruction_rect):
            next_rect.y = player_rect.y

        next_rect.x = max(20, min(screen.get_width() - next_rect.width - 20, next_rect.x))
        next_rect.y = max(20, min(screen.get_height() - next_rect.height - 20, next_rect.y))
        player_rect = next_rect

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

        # Personagem em preto/branco.
        pygame.draw.ellipse(screen, fg, player_rect)
        belly = player_rect.inflate(-16, -14)
        pygame.draw.ellipse(screen, bg, belly)

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

            # Ao chegar na porta, vai para a tela da fase 1.
            if player_rect.colliderect(phase_1_door):
                show_phase_1_screen(screen, clock)
                return

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
