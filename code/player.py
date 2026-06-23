import pygame
import random
import os

from config import *

from entities.player import Player
from entities.enemy import Enemy

from systems.assets import (
    load_image,
    load_sound,
    SOUND_DIR
)

from systems.phase_manager import PhaseManager

class Game:

    def __init__(self, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.running = True
        self.menu = True

        self.score = 0

        self.phase_manager = PhaseManager()

        self.font = pygame.font.SysFont(
            "Arial",
            30
        )

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.shoot_sound = load_sound("shoot.wav")
        self.hit_sound = load_sound("hit.wav")

        self.player = Player(
            self.bullets,
            self.all_sprites,
            self.shoot_sound
        )

        self.all_sprites.add(self.player)

        self.menu_bg = load_image(
            "menu_background.png"
        )

        self.bg_y = 0

    def start_phase_music(self):

        phase = self.phase_manager.current_phase

        pygame.mixer.music.load(
            os.path.join(
                SOUND_DIR,
                f"bgm_fase{phase}.mp3"
            )
        )

        pygame.mixer.music.play(-1)

    def draw_hud(self):

        score = self.font.render(
            f"Pontos: {self.score}",
            True,
            WHITE
        )

        lives = self.font.render(
            f"Vidas: {self.player.lives}",
            True,
            WHITE
        )

        timer = self.font.render(
            f"Tempo: {self.phase_manager.remaining_time()}",
            True,
            WHITE
        )

        self.screen.blit(score,(20,20))
        self.screen.blit(lives,(20,60))
        self.screen.blit(timer,(20,100))

    def draw_menu(self):

        menu_bg = pygame.transform.scale(
            self.menu_bg,
            (WIDTH, HEIGHT)
        )

        title = self.font.render(
            "COMBAT GALAXY",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            (350,200)
        )

        if pygame.time.get_ticks() % 1000 < 500:

            start = self.font.render(
                "Digite ENTER para começar",
                True,
                GREEN
            )

            self.screen.blit(
                start,
                (300,600)
            )

    def run(self):

        pygame.mixer.music.load(
            os.path.join(
                SOUND_DIR,
                "background.mp3"
            )
        )

        pygame.mixer.music.play(-1)

        enemy_event = pygame.USEREVENT + 1

        pygame.time.set_timer(
            enemy_event,
            1000
        )

        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if self.menu:

                    if (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_RETURN
                    ):
                        self.menu = False

                        pygame.mixer.music.stop()
                        self.start_phase_music()

                else:

                    if (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE
                    ):
                        self.player.shoot()

                    if event.type == enemy_event:
                        enemy = Enemy()
                        self.enemies.add(enemy)
                        self.all_sprites.add(enemy)

            if self.menu:

                self.draw_menu()

            else:

                self.all_sprites.update()

                hits = pygame.sprite.groupcollide(
                    self.bullets,
                    self.enemies,
                    True,
                    True
                )

                if hits:
                    self.hit_sound.play()
                    self.score += 10

                if self.phase_manager.remaining_time() == 0:

                    self.phase_manager.next_phase()

                    if self.phase_manager.is_finished():
                        self.running = False

                    else:
                        self.start_phase_music()

                self.screen.fill(BLACK)

                self.all_sprites.draw(
                    self.screen
                )

                self.draw_hud()

            pygame.display.flip()