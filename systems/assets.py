import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")


def load_image(filename):
    return pygame.image.load(
        os.path.join(IMAGE_DIR, filename)
    ).convert_alpha()


def load_image_ratio(filename, max_size):
    image = pygame.image.load(
        os.path.join(IMAGE_DIR, filename)
    ).convert_alpha()

    width, height = image.get_size()

    scale = min(
        max_size[0] / width,
        max_size[1] / height
    )

    new_width = int(width * scale)
    new_height = int(height * scale)

    return pygame.transform.smoothscale(
        image,
        (new_width, new_height)
    )


def load_sound(filename):
    return pygame.mixer.Sound(
        os.path.join(SOUND_DIR, filename)
    )
