import pygame
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

        self.font = pygame.font.SysFont("Arial", 32)

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Sounds
        self.shoot_sound = load_sound("shoot.wav")
        self.hit_sound = load_sound("hit.wav")

        # Player
        self.player = Player(
            self.bullets,
            self.all_sprites,
            self.shoot_sound
        )

        self.all_sprites.add(self.player)

        # Menu background
        self.menu_bg = pygame.transform.smoothscale(
            load_image("menu_background.png"),
            (WIDTH, HEIGHT)
        )

        # Phase backgrounds
        self.backgrounds = {
            1: pygame.transform.smoothscale(load_image("background1.png"), (WIDTH, HEIGHT)),
            2: pygame.transform.smoothscale(load_image("background2.png"), (WIDTH, HEIGHT)),
            3: pygame.transform.smoothscale(load_image("background3.png"), (WIDTH, HEIGHT))
        }

        self.bg_x = 0
        self.scroll_speed = 2

    # =========================
    # GAME OVER
    # =========================
    def show_game_over(self):

        self.screen.fill(BLACK)

        font = pygame.font.SysFont("Arial", 80)

        text = font.render("GAME OVER", True, RED)

        self.screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - text.get_height() // 2
            )
        )

        pygame.display.flip()
        pygame.time.delay(3000)

    # =========================
    # MUSIC
    # =========================
    def start_phase_music(self):

        phase = self.phase_manager.current_phase

        pygame.mixer.music.load(
            os.path.join(SOUND_DIR, f"bgm_fase{phase}.mp3")
        )

        pygame.mixer.music.play(-1)

    # =========================
    # BACKGROUND (SCROLL)
    # =========================
    def draw_background(self):

        bg = self.backgrounds[self.phase_manager.current_phase]

        self.bg_x -= self.scroll_speed

        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(bg, (self.bg_x, 0))
        self.screen.blit(bg, (self.bg_x + WIDTH, 0))

    # =========================
    # HUD
    # =========================
    def draw_hud(self):

        score_text = self.font.render(
            f"Pontos: {self.score}",
            True,
            WHITE
        )

        lives_text = self.font.render(
            f"Vidas: {self.player.lives}",
            True,
            WHITE
        )

        timer_text = self.font.render(
            f"Tempo: {self.phase_manager.remaining_time()}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (20, 60))
        self.screen.blit(timer_text, (20, 100))

    # =========================
    # MENU
    # =========================
    def draw_menu(self):

        self.screen.blit(self.menu_bg, (0, 0))

        title = self.font.render("COMBAT GALAXY", True, WHITE)

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 150)
        )

        if pygame.time.get_ticks() % 1000 < 500:

            start = self.font.render(
                "Pressione ENTER para começar",
                True,
                GREEN
            )

            self.screen.blit(
                start,
                (WIDTH // 2 - start.get_width() // 2, HEIGHT - 100)
            )

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):

        pygame.mixer.music.load(
            os.path.join(SOUND_DIR, "background.mp3")
        )
        pygame.mixer.music.play(-1)

        enemy_event = pygame.USEREVENT + 1
        pygame.time.set_timer(enemy_event, 1200)

        while self.running:

            self.clock.tick(FPS)

            # =========================
            # EVENTS
            # =========================
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                # MENU
                if self.menu:

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.menu = False
                        pygame.mixer.music.stop()
                        self.start_phase_music()

                # GAME
                else:

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.shoot()

                    if event.type == enemy_event:
                        enemy = Enemy()
                        self.enemies.add(enemy)
                        self.all_sprites.add(enemy)

            # =========================
            # UPDATE
            # =========================
            if not self.menu:

                self.all_sprites.update()

                # COLISÃO TIRO x INIMIGO
                hits = pygame.sprite.groupcollide(
                    self.bullets,
                    self.enemies,
                    True,
                    True
                )

                if hits:
                    self.hit_sound.play()
                    self.score += len(hits) * 10

                # COLISÃO JOGADOR x INIMIGO
                player_hits = pygame.sprite.spritecollide(
                    self.player,
                    self.enemies,
                    True
                )

                if player_hits:

                    self.player.take_damage()
                    self.hit_sound.play()

                    if self.player.lives <= 0:
                        self.show_game_over()
                        self.running = False

                # FASE
                if self.phase_manager.remaining_time() == 0:

                    self.phase_manager.next_phase()

                    if self.phase_manager.is_finished():
                        self.running = False
                    else:
                        self.start_phase_music()

            # =========================
            # RENDER
            # =========================
            self.screen.fill(BLACK)

            if self.menu:
                self.draw_menu()

            else:
                self.draw_background()
                self.all_sprites.draw(self.screen)
                self.draw_hud()

            pygame.display.flip()