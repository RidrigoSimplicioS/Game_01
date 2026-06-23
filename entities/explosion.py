import pygame

class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.frames = []
        self.current_frame = 0
        self.animation_speed = 2
        self.counter = 0

        # cria "spritesheet fake" (círculos crescendo)
        for i in range(1, 7):
            surf = pygame.Surface((60, 60), pygame.SRCALPHA)

            pygame.draw.circle(
                surf,
                (255, 200, 0),
                (30, 30),
                i * 5
            )

            pygame.draw.circle(
                surf,
                (255, 80, 0),
                (30, 30),
                i * 3
            )

            self.frames.append(surf)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):

        self.counter += 1

        if self.counter >= self.animation_speed:
            self.counter = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.kill()
                return

            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)