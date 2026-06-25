import pygame
import os
import sys

# 1. Configuração dos caminhos (Compatível com PyCharm e PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    # Volta duas pastas para chegar na raiz do projeto (de systems/assets.py para raiz)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Definição dos diretórios de recursos
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_DIR = os.path.join(ASSETS_DIR, "images")
SOUND_DIR = os.path.join(ASSETS_DIR, "sounds")


# 3. Função que o seu arquivo 'enemy.py' está procurando:
def load_image_ratio(filename, max_size=None):
    """Carrega uma imagem e opcionalmente a redimensiona mantendo a proporção."""
    path = os.path.join(IMAGE_DIR, filename)
    image = pygame.image.load(path).convert_alpha()

    if max_size:
        width, height = image.get_size()
        scale = min(max_size[0] / width, max_size[1] / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        return pygame.transform.smoothscale(image, (new_width, new_height))

    return image


# 4. Mantemos essa aqui também caso o player.py use o nome antigo:
def load_image(filename, max_size=None):
    return load_image_ratio(filename, max_size)


# 5. Função para carregar Sons
def load_sound(filename):
    path = os.path.join(SOUND_DIR, filename)
    return pygame.mixer.Sound(path)