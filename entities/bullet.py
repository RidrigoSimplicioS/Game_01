import pygame
from config import *


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.Surface(BULLET_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 0), self.image.get_rect())

        self.rect = self.image.get_rect(center=(x, y))

        self.speed = BULLET_SPEED

    def update(self):

        self.rect.x += self.speed

        if self.rect.left > WIDTH:
            self.kill()