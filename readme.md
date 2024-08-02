# Dilia The Elf

"Dilia The Elf" es un juego de decisiones desarrollado en Python utilizando la biblioteca Pygame. El juego presenta diálogos interactivos y opciones que afectan la historia, con una pantalla de inicio y música de fondo para una experiencia inmersiva.

## Estructura del Proyecto

El proyecto tiene la siguiente estructura de carpetas:
 
 Delia/
 ├── assets/  
 │ ├── file.png  
 │ ├── fuentes/  
 │ │ └── Baby_Stingrays.ttf 
 
 │ └── sounds/  
 
 │ └── Bosque_Encantado.mp3 
 
 ├── dialogues.json 
 
 └── main.py 
 

 - `assets/file.png`: Imagen de fondo utilizada en el juego.
- `assets/fuentes/Baby_Stingrays.ttf`: Fuente utilizada para el texto en el juego.
- `assets/sounds/Bosque_Encantado.mp3`: Música de fondo del juego.
- `dialogues.json`: Archivo JSON que contiene los diálogos y opciones del juego.
- `main.py`: Script principal del juego.
- ## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/dilia_the_elf.git
    ```

2. Navega a la carpeta del proyecto:
    ```bash
    cd dilia_the_elf
    ```

3. Asegúrate de tener Pygame instalado. Puedes instalarlo usando pip:
    ```bash
    pip install pygame
    ```

## Uso

Para ejecutar el juego, simplemente corre el script `main.py`:

```bash
python main.py
```
### Parte 3: Funcionamiento del Juego y Archivos JSON


## Funcionamiento del Juego

1. **Pantalla de Inicio**: El juego comienza con una pantalla de inicio que muestra el título "Dilia The Elf" y un botón "JUGAR". Haz clic en el botón para iniciar el juego.

2. **Diálogos**: Durante el juego, los diálogos se muestran en la pantalla. Los textos largos se ajustan automáticamente al ancho máximo definido.

3. **Opciones**: Si hay opciones disponibles en los diálogos, se muestran debajo del texto principal. Haz clic en una opción para tomar una decisión y avanzar en la historia.

4. **Imágenes y Audio**: Las imágenes y el audio se cargan y reproducen según el contenido del archivo `dialogues.json`.

## Archivos JSON

El archivo `dialogues.json` contiene la estructura de diálogos y opciones del juego. Aquí hay un ejemplo de formato:

```json
{
  "start": {
    "text": "Bienvenida a la aventura, Dilia.",
    "img": "assets/some_image.png",
    "audio": "assets/sounds/some_sound.mp3",
    "options": [
      {
        "text": "Ir al bosque",
        "next": "forest"
      },
      {
        "text": "Explorar la aldea",
        "next": "village"
      }
    ]
  },
  "forest": {
    "text": "Te adentras en el bosque...",
    "next": "end"
  },
  "village": {
    "text": "Exploras la aldea...",
    "next": "end"
  },
  "end": {
    "text": "Fin de la aventura."
  }
}
```
### Parte 4: Contribuciones y Licencia


## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Fork el repositorio.
2. Crea una rama para tu funcionalidad o corrección de errores.
3. Realiza tus cambios y haz commits.
4. Envía un pull request con una descripción clara de tus cambios.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

¡Gracias por jugar a "Dilia The Elf"! Esperamos que disfrutes la aventura.
