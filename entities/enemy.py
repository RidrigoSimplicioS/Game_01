import pygame
import random

from systems.assets import (
    load_image_ratio
)

from config import *

class Enemy(pygame.sprite.Sprite):

    SPRITES = [
        ("enemy_blue.png", ENEMY_BLUE_SIZE),
        ("enemy_green.png", ENEMY_GREEN_SIZE),
        ("enemy_red.png", ENEMY_RED_SIZE)
    ]

    def __init__(self):
        super().__init__()

        sprite_file, sprite_size = random.choice(
            self.SPRITES
        )

        self.image = load_image_ratio(
            sprite_file,
            sprite_size
        )

        self.rect = self.image.get_rect()

        self.rect.x = WIDTH + 50

        self.rect.y = random.randint(
            50,
            HEIGHT - self.rect.height - 50
        )

    def update(self):

        self.rect.x -= ENEMY_SPEED

        if self.rect.right < 0:
            self.kill()