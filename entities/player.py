import pygame
import pygame

from config import *

from entities.bullet import Bullet

from systems.assets import (
    load_image_ratio
)

class Player(pygame.sprite.Sprite):

    def __init__(
        self,
        bullet_group,
        all_sprites,
        shoot_sound
    ):
        super().__init__()

        self.image = load_image_ratio(
            "player.png",
            PLAYER_SIZE
        )

        self.rect = self.image.get_rect(
            center=(120, HEIGHT // 2)
        )

        self.bullets = bullet_group
        self.all_sprites = all_sprites
        self.shoot_sound = shoot_sound

        self.lives = MAX_LIVES

        self.last_hit = 0
        self.invincible_time = 1500

    def shoot(self):

        bullet = Bullet(
            self.rect.right,
            self.rect.centery
        )

        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

        self.shoot_sound.play()

    def take_damage(self):

        now = pygame.time.get_ticks()

        if now - self.last_hit > self.invincible_time:

            self.lives -= 1
            self.last_hit = now

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED

        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        self.rect.clamp_ip(
            pygame.Rect(
                0,
                0,
                WIDTH,
                HEIGHT
            )
        )