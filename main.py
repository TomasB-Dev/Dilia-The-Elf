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

# Carga los diálogos desde el archivo JSON
def load_dialogues(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Renderiza el texto en la pantalla
def render_text(text, x, y, color=(0, 0, 0)):
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

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * line_height))

# Dibuja un fondo semitransparente detrás del texto
def draw_transparent_background(x, y, width, height, color=(255, 255, 255), alpha=150):
    overlay = pygame.Surface((width, height))  # Crear una superficie
    overlay.set_alpha(alpha)  # Establecer transparencia
    overlay.fill(color)  # Rellenar con el color
    screen.blit(overlay, (x, y))  # Dibujar sobre la pantalla

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
        #aca podria poner if y agregar la imagen correspondiente por encima asi queda debajo del texto
        if 'img' in node:
            image = pygame.image.load(node['img'])
            scaled_image = pygame.transform.scale(image, (400, 300))
            screen.blit(scaled_image, (0, 310))
        render_text(node['text'], 50, 195)

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
                draw_transparent_background(option_x - 10, option_y - 10, option_width + 20, line_height + 20)
                render_text(option_text, option_x, option_y)
                option_y += 60  # Espaciado entre opciones

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
                        option_y = 420
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
