import pygame
import json

# Inicializa Pygame y el mezclador de audio
pygame.init()
pygame.mixer.init()

# Configura la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dilia The Elf")

# Carga la imagen de fondo
background_image = pygame.image.load("assets/file.png")

# Configura la fuente
font_family = "assets/fuentes/Baby_Stingrays.ttf"
font = pygame.font.Font(font_family, 36)
font_start = pygame.font.Font(font_family, 90)
line_height = 40
max_width = 700
box_padding = 20  # Espacio interno del cuadro de diálogo

# Carga los diálogos desde el archivo JSON
def load_dialogues(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Renderiza el texto con sombra
def render_text_with_shadow(text, x, y, text_color=(255, 255, 255), shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
    # Renderiza la sombra
    shadow_surf = font.render(text, True, shadow_color)
    shadow_rect = shadow_surf.get_rect(topleft=(x + shadow_offset[0], y + shadow_offset[1]))
    screen.blit(shadow_surf, shadow_rect)

    # Renderiza el texto principal
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(topleft=(x, y))
    screen.blit(text_surf, text_rect)

# Ajusta el texto dentro del cuadro de diálogo con salto de línea automático
def render_text_with_wrapping(text, x, y, max_width, color=(255, 255, 255)):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    return lines

# Dibuja un fondo semitransparente detrás del texto
def draw_dialogue_box(x, y, width, height, color=(0, 0, 0), alpha=200):
    box_surf = pygame.Surface((width, height))
    box_surf.set_alpha(alpha)
    box_surf.fill(color)
    screen.blit(box_surf, (x, y))

# Reproduce el audio correspondiente
def play_audio(audio_file):
    pygame.mixer.Sound(audio_file).play()

# Reproduce la música de fondo
def play_background_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Reproduce en bucle
    pygame.mixer.music.set_volume(0.07)

# Renderiza texto centrado
def render_centered_text(text, font, screen_width, y_offset):
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen_width / 2, y_offset))
    return text_surface, text_rect

# Pantalla de inicio
def show_start_screen():
    screen.blit(background_image, (0, 0))  # Usa la imagen de fondo

    screen_width, screen_height = screen.get_size()

    # Renderiza y centra el título
    title_text, title_rect = render_centered_text("Dilia The Elf", font_start, screen_width, screen_height / 2 - 50)
    screen.blit(title_text, title_rect)

    # Renderiza y centra el botón "JUGAR"
    play_button_text, play_button_rect = render_centered_text("JUGAR", font_start, screen_width, screen_height / 2 + 50)
    screen.blit(play_button_text, play_button_rect)
    
    pygame.display.flip()

    # Espera a que el usuario haga clic en el botón de jugar
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(x, y):  # Verifica si se hizo clic en el botón "JUGAR"
                    waiting_for_input = False

# Función principal del juego
def main():
    dialogues = load_dialogues('dialogues.json')
    play_background_music('assets/sounds/Bosque_Encantado.mp3')  # Música de fondo
    show_start_screen()
    
    current_node = 'start'

    while True:
        if current_node not in dialogues:
            show_start_screen()
            current_node = 'start'
            continue

        screen.blit(background_image, (0, 0))  # Usa la imagen de fondo
        node = dialogues[current_node]

        # Muestra la imagen correspondiente si existe
        if 'img' in node:
            image = pygame.image.load(node['img'])
            scaled_image = pygame.transform.scale(image, (400, 300))
            screen.blit(scaled_image, (0, 310))
        
        # Dibuja el cuadro de diálogo y renderiza el texto
        dialog_box_x, dialog_box_y = 50, 50
        dialog_box_width = max_width
        dialog_box_height = 300
        draw_dialogue_box(dialog_box_x, dialog_box_y, dialog_box_width, dialog_box_height)

        if 'text' in node:
            lines = render_text_with_wrapping(node['text'], dialog_box_x + box_padding, dialog_box_y + box_padding, dialog_box_width - 2 * box_padding)
            for i, line in enumerate(lines):
                render_text_with_shadow(line, dialog_box_x + box_padding, dialog_box_y + box_padding + i * line_height)

        # Reproduce la pista de audio correspondiente
        if 'audio' in node:
            play_audio(node['audio'])
                
        # Dibuja opciones si existen
        if 'options' in node:
            option_y = 450
            for option in node['options']:
                option_text = option['text']
                option_width = font.size(option_text)[0]
                option_x = (800 - option_width) // 2
                # Dibuja el fondo semitransparente antes de renderizar el texto
                draw_dialogue_box(option_x - 10, option_y - 10, option_width + 20, line_height + 20, color=(0, 0, 0), alpha=150)
                render_text_with_shadow(option_text, option_x, option_y)  # Texto con sombra
                option_y += 90  # Espaciado entre opciones

        pygame.display.flip()

        # Espera a que el usuario haga clic
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_input = False
                    if 'options' in node:
                        # Manejo de opciones si existen
                        x, y = pygame.mouse.get_pos()
                        option_y = 450
                        for option in node['options']:
                            option_width = font.size(option['text'])[0]
                            option_x = (800 - option_width) // 2
                            if option_x - 10 < x < option_x + option_width + 10 and option_y - 10 < y < option_y + line_height + 10:
                                current_node = option['next']
                                break
                            option_y += 60  # Espaciado entre opciones
                    else:
                        if 'next' in node:
                            current_node = node['next']
                        else:
                            show_start_screen()
                            current_node = 'start'

if __name__ == "__main__":
    main()
