import pygame
import json
import math 
import webbrowser
# Inicializa Pygame y el mezclador de audio
pygame.init()
pygame.mixer.init()

# Configuracion de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dilia The Elf")

# imagen de fondo
background_image = pygame.image.load("assets/file.png")
# icono de la ventana
icon_image = pygame.image.load("assets/icono.png")  
# escalo la imagen
scaled_icon = pygame.transform.scale(icon_image, (100, 100))  
pygame.display.set_icon(scaled_icon)


# Carga y redimensiona las imágenes del botón de mute/desmute manteniendo la proporción
def load_and_scale_image(image_path, scale_factor):
    """
    Carga una imagen desde una ruta y la escala por un factor dado.
    Args:
        image_path (str): Ruta de la imagen a cargar.
        scale_factor (float): Factor por el cual escalar la imagen.
    Returns:
        pygame.Surface: Imagen escalada.
    """
    image = pygame.image.load(image_path)
    width, height = image.get_size()
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return pygame.transform.scale(image, new_size)

#boton de discord
discord_button_image = load_and_scale_image("assets/img/discord.png", 0.3)
discord_button_rect = discord_button_image.get_rect(bottomleft=(20, 580))
discord_url = "https://discord.gg/PcChBEUmDT"

#btn mute
mute_button_image = load_and_scale_image("assets/img/mute.png", 0.1) 
unmute_button_image = load_and_scale_image("assets/img/unmute.png", 0.2)

# posicion del btn mute
mute_button_rect = mute_button_image.get_rect(topright=(780, 20))

# Configura la fuente
font_family = "assets/fuentes/Alone_On_Earth.otf"
font = pygame.font.Font(font_family, 36)
font_start = pygame.font.Font(font_family, 90)
line_height = 40
max_width = 700
box_padding = 20  # Espacio interno del cuadro de diálogo

# Carga el JSON
def load_dialogues(filename):
    """
    Carga los diálogos el archivo JSON.
    Args:
        filename (str): Ruta del archivo JSON.
    Returns:
        dict: Contenido del archivo JSON cargado.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Renderiza el texto con sombra
def render_text_with_shadow(text, x, y, text_color=(255, 255, 255), shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
    """
    Renderiza texto con una sombra.
    Args:
        text (str): Texto a renderizar.
        x (int): Coordenada x de la posición del texto.
        y (int): Coordenada y de la posición del texto.
        text_color (tuple): Color del texto en formato RGB.
        shadow_color (tuple): Color de la sombra en formato RGB.
        shadow_offset (tuple): Desplazamiento de la sombra en píxeles.
    """
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
    """
    Ajusta el texto dentro de un cuadro de diálogo con salto de línea automático.
    Args:
        text (str): Texto a renderizar.
        x (int): Coordenada x de la posición del texto.
        y (int): Coordenada y de la posición del texto.
        max_width (int): Ancho máximo del texto.
        color (tuple): Color del texto en formato RGB.
    """
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

# Dibuja un fondo atras del texto
def draw_dialogue_box(x, y, width, height, color=(0, 0, 0), alpha=200):
    """
    Dibuja un cuadro de diálogo con bordes redondeados y un fondo texturizado.
    Args:
        x (int): Coordenada x de la posición del cuadro.
        y (int): Coordenada y de la posición del cuadro.
        width (int): Ancho del cuadro.
        height (int): Alto del cuadro.
        color (tuple): Color del cuadro en formato RGB.
        alpha (int): Nivel de transparencia del cuadro (0-255).
    """
    box_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    box_surf.set_alpha(alpha)
    
    # Dibuja un rectángulo redondeado
    rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(box_surf, color, rect, border_radius=20)
    
    # Añadir una textura sutil (opcional)
    texture = pygame.image.load('assets/texture.jpg')
    texture = pygame.transform.scale(texture, (width, height))
    texture.set_alpha(70)  # Ajusta la transparencia de la textura
    box_surf.blit(texture, (0, 0))
    
    screen.blit(box_surf, (x, y))

# Reproduce el dialogo 
def play_audio(audio_file):
    """
    Reproduce un archivo de audio.
    Args:
        audio_file (str): Ruta del archivo de audio a reproducir.
    """
    pygame.mixer.Sound(audio_file).play()

# Reproduce la música de fondo
def play_background_music(music_file):
    """
    Reproduce música de fondo en bucle.
    Args:
        music_file (str): Ruta del archivo de música a reproducir.
    """
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Reproduce en bucle
    pygame.mixer.music.set_volume(0.07)

# Renderiza texto centrado
def render_centered_text(text, font, screen_width, y_offset):
    """
    Renderiza texto centrado en la pantalla.
    Args:
        text (str): Texto a renderizar.
        font (pygame.font.Font): Fuente del texto.
        screen_width (int): Ancho de la pantalla.
        y_offset (int): Desplazamiento vertical del texto.
    Returns:
        tuple: Superficie y rectángulo del texto renderizado.
    """
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen_width / 2, y_offset))
    return text_surface, text_rect

# Pantalla de inicio
def show_start_screen():
    """
    Muestra la pantalla de inicio con animación del botón "JUGAR".
    """
    clock = pygame.time.Clock()
    animation_start_time = pygame.time.get_ticks()
    
    while True:
        screen.blit(background_image, (0, 0))  # Usa la imagen de fondo

        screen_width, screen_height = screen.get_size()

        # Renderiza y centra el título
        title_text, title_rect = render_centered_text("Dilia The Elf", font_start, screen_width, screen_height / 2 - 50)
        screen.blit(title_text, title_rect)

        # Animación del botón "JUGAR"
        # Calcula el tiempo transcurrido en segundos desde que comenzó la animación
        elapsed_time = (pygame.time.get_ticks() - animation_start_time) / 1000.0
        # Calcula un factor de escala basado en una función seno para crear una animación de "latido" (pulso) en el texto
        # `math.sin(elapsed_time * 2 * math.pi)` produce un valor oscilante entre -1 y 1, creando un ciclo completo (onda seno)
        # Multiplicar por 2 * math.pi ajusta la velocidad de la oscilación
        # Multiplicar por 0.05 ajusta la amplitud de la oscilación
        # `1 +` asegura que el factor de escala oscile entre 0.95 y 1.05
        scale_factor = 1 + 0.05 * math.sin(elapsed_time * 2 * math.pi)  # Ajusta la velocidad y amplitud de la animación
        # Crea una fuente animada, ajustando su tamaño en función del factor de escala calculado
        # El tamaño de la fuente varía alrededor de 90 píxeles, creciendo y encogiéndose de acuerdo con `scale_factor`
        animated_font = pygame.font.Font(font_family, int(90 * scale_factor))
        play_button_text, play_button_rect = render_centered_text("JUGAR", animated_font, screen_width, screen_height / 2 + 50)
        screen.blit(play_button_text, play_button_rect)
        screen.blit(discord_button_image, discord_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(x, y):  # Verifica si se hizo clic en el botón "JUGAR"
                    return
                elif discord_button_rect.collidepoint(x, y):  # Verifica si se hizo clic en el botón de Discord
                    webbrowser.open(discord_url)  # Abre el enlace de Discord

        
        clock.tick(60)

# Muestra los créditos y vuelve a la pantalla inicial
def show_credits():
    print("Creditos funciona")
    screen.fill((255, 255, 255)) 

    credits_text = [
        "Créditos",
        "",
        "Desarrollado por Tomas Dev",
        "Gracias por jugar!",
        "",
        "Agradecimientos especiales a:",
        "- Docallisme por la Fuente",
        "- Monster por el insomnio",
        "- Dark Por Las recomendaciones",
        "- Filo por el 'testing'",
        "Fin."
    ]

    y_offset = 100
    for line in credits_text:
        text_surface, text_rect = render_centered_text(line, font, screen.get_width(), y_offset)
        screen.blit(text_surface, text_rect)
        y_offset += 40

    pygame.display.flip()

    # Espera unos segundos antes de volver a la pantalla inicial
    pygame.time.wait(10000)
    show_start_screen()


# Función principal del juego
def main():
    dialogues = load_dialogues('dialogues.json')
    play_background_music('assets/sounds/Bosque_Encantado.mp3')  # Música de fondo
    show_start_screen()
    
    current_node = 'start'
    is_muted = False  # Variable para manejar el estado del mute

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
        dialog_box_x, dialog_box_y = 50, 75
        dialog_box_width = max_width
        dialog_box_height = 240
        draw_dialogue_box(dialog_box_x, dialog_box_y, dialog_box_width, dialog_box_height)

        if 'text' in node:
            lines = render_text_with_wrapping(node['text'], dialog_box_x + box_padding, dialog_box_y + box_padding, dialog_box_width - 2 * box_padding)
            for i, line in enumerate(lines):
                render_text_with_shadow(line, dialog_box_x + box_padding, dialog_box_y + box_padding + i * line_height)

        # Reproduce la pista de audio correspondiente si no está en mute
        if 'audio' in node and not is_muted:
            play_audio(node['audio'])
                
        # Dibuja opciones si existen
        if 'options' in node:
            option_y = 450
            for option in node['options']:
                option_text = option['text']
                option_width = font.size(option_text)[0]
                option_x = (800 - option_width) // 2
                # Dibuja el fondo antes de renderizar el texto
                draw_dialogue_box(option_x - 10, option_y - 10, option_width + 20, line_height + 20, color=(0, 0, 0), alpha=150)
                render_text_with_shadow(option_text, option_x, option_y)  # Texto con sombra
                option_y += 90  # Espaciado entre opciones

        # Dibuja el botón de mute/desmute
        if is_muted:
            screen.blit(mute_button_image, mute_button_rect)
        else:
            screen.blit(unmute_button_image, mute_button_rect)

        pygame.display.flip()

        # Espera a que el usuario haga clic
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Verifica si se hizo clic en el botón de mute/desmute
                    if mute_button_rect.collidepoint(x, y):
                        is_muted = not is_muted
                        if is_muted:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    else:
                        waiting_for_input = False
                        if 'options' in node:
                            # Manejo de opciones si existen
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
                                if current_node == 'end' :  # Verifica si es el nodo de finalización
                                    show_credits()  # Muestra los créditos y vuelve a la pantalla inicial
                                    current_node = 'start'
                            else: 
                                show_start_screen()
                                current_node = 'start'

if __name__ == "__main__":
    main()
