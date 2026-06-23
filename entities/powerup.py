import pygame
import random

from config import WIDTH, HEIGHT


class PowerUp(pygame.sprite.Sprite):

    TYPES = ["life", "double", "shield"]

    def __init__(self):

        super().__init__()

        self.type = random.choice(self.TYPES)

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        # cores por tipo
        if self.type == "life":
            color = (0, 255, 0)
        elif self.type == "double":
            color = (0, 150, 255)
        else:
            color = (255, 215, 0)

        pygame.draw.circle(self.image, color, (15, 15), 12)

        self.rect = self.image.get_rect()

        # spawn seguro (melhorado)
        self.rect.x = WIDTH + random.randint(10, 80)
        self.rect.y = random.randint(50, HEIGHT - 50)

        self.speed = 4

    def update(self):

        self.rect.x -= self.speed

        if self.rect.right < -10:
            self.kill()