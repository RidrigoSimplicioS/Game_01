import pygame

from config import (
    BULLET_SPEED,
    WIDTH,
    BULLET_SIZE
)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface(
            BULLET_SIZE,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            self.image,
            (255, 255, 0),
            self.image.get_rect()
        )

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):

        self.rect.x += BULLET_SPEED

        if self.rect.left > WIDTH:
            self.kill()