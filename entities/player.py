import pygame
from config import *
from entities.bullet import Bullet
from systems.assets import load_image


class Player(pygame.sprite.Sprite):

    def __init__(self, bullet_group, all_sprites, shoot_sound):
        super().__init__()

        self.image = load_image("player.png")
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))

        self.bullets = bullet_group
        self.all_sprites = all_sprites
        self.shoot_sound = shoot_sound

        self.lives = MAX_LIVES

        self.double_shot = False
        self.shield = False

        self.double_timer = 0
        self.shield_timer = 0

        self.last_hit = 0
        self.invincible_time = 1500

    def shoot(self):
        if self.double_shot:
            b1 = Bullet(self.rect.right, self.rect.centery - 10)
            b2 = Bullet(self.rect.right, self.rect.centery + 10)
            self.bullets.add(b1, b2)
            self.all_sprites.add(b1, b2)
        else:
            b = Bullet(self.rect.right, self.rect.centery)
            self.bullets.add(b)
            self.all_sprites.add(b)

        self.shoot_sound.play()

    def take_damage(self):
        if self.shield:
            return

        now = pygame.time.get_ticks()

        if now - self.last_hit > self.invincible_time:
            self.lives -= 1
            self.last_hit = now

    def apply_powerup(self, power_type):
        now = pygame.time.get_ticks()

        if power_type == "life":
            self.lives = min(MAX_LIVES, self.lives + 1)
        elif power_type == "double":
            self.double_shot = True
            self.double_timer = now
        elif power_type == "shield":
            self.shield = True
            self.shield_timer = now

    def update(self):
        keys = pygame.key.get_pressed()

        # Movimentação padrão pelas Setas do Teclado
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        now = pygame.time.get_ticks()

        if self.double_shot and now - self.double_timer > 7000:
            self.double_shot = False

        if self.shield and now - self.shield_timer > 7000:
            self.shield = False