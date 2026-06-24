import pygame
import os

from config import *

from entities.player import Player
from entities.enemy import Enemy
from entities.explosion import Explosion
from entities.powerup import PowerUp

from systems.assets import load_image, load_sound, SOUND_DIR
from systems.phase_manager import PhaseManager


class Game:

    def __init__(self, screen):
        self.base_enemy_timer = 1200
        self.enemy_increment = 200

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.running = True
        self.menu = True

        self.score = 0

        self.phase_manager = PhaseManager()

        self.font = pygame.font.SysFont("Arial", 32)

        # CONFIGURAÇÃO DE EVENTOS CUSTOMIZADOS
        self.enemy_event = pygame.USEREVENT + 1
        self.power_event = pygame.USEREVENT + 2

        # GRUPOS
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # SONS
        self.shoot_sound = load_sound("shoot.wav")
        self.hit_sound = load_sound("hit.wav")

        # PLAYER
        self.player = Player(
            self.bullets,
            self.all_sprites,
            self.shoot_sound
        )

        self.all_sprites.add(self.player)

        # MENU BACKGROUND
        self.menu_bg = pygame.transform.smoothscale(
            load_image("menu_background.png"),
            (WIDTH, HEIGHT)
        )

        # BACKGROUNDS
        self.backgrounds = {
            1: pygame.transform.smoothscale(load_image("background1.png"), (WIDTH, HEIGHT)),
            2: pygame.transform.smoothscale(load_image("background2.png"), (WIDTH, HEIGHT)),
            3: pygame.transform.smoothscale(load_image("background3.png"), (WIDTH, HEIGHT))
        }

        self.bg_x = 0
        self.scroll_speed = 2

    # =========================
    # DIFICULDADE Atualizada para usar o self.enemy_event
    # =========================
    def update_difficulty(self):
        phase = self.phase_manager.current_phase

        # Aumenta a frequência de spawn
        new_timer = max(300, self.base_enemy_timer - (phase - 1) * self.enemy_increment)

        pygame.time.set_timer(self.enemy_event, new_timer)

    # =========================
    # RESET TOTAL
    # =========================
    def reset_game(self):
        self.score = 0
        self.phase_manager = PhaseManager()
        self.bg_x = 0

        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.effects.empty()
        self.powerups.empty()

        self.player = Player(
            self.bullets,
            self.all_sprites,
            self.shoot_sound
        )

        self.all_sprites.add(self.player)

        pygame.mixer.music.load(
            os.path.join(SOUND_DIR, "background.mp3")
        )
        pygame.mixer.music.play(-1)

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
        pygame.time.delay(2000)

    # =========================
    # MUSICA FASE
    # =========================
    def start_phase_music(self):
        phase = self.phase_manager.current_phase

        # Evita crash na fase 4,5,6... repetindo as músicas em ciclo
        music_index = ((phase - 1) % 3) + 1

        pygame.mixer.music.load(
            os.path.join(SOUND_DIR, f"bgm_fase{music_index}.mp3")
        )

        pygame.mixer.music.play(-1)

    # =========================
    # BACKGROUND (CORRIGIDO PARA EVITAR KEYERROR)
    # =========================
    def draw_background(self):
        # 🔥 Calcula o índice de 1 a 3 dinamicamente para aceitar fases 4, 5, 6...
        bg_index = ((self.phase_manager.current_phase - 1) % 3) + 1
        bg = self.backgrounds[bg_index]

        self.bg_x -= self.scroll_speed

        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(bg, (self.bg_x, 0))
        self.screen.blit(bg, (self.bg_x + WIDTH, 0))

    # =========================
    # HUD
    # =========================
    def draw_hud(self):
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 215, 0)), (20, 20))
        self.screen.blit(self.font.render(f"Life: {self.player.lives}", True, (0, 255, 100)), (20, 60))
        self.screen.blit(self.font.render(f"Time: {self.phase_manager.remaining_time()}", True, (0, 200, 255)),
                         (20, 100))

    # =========================
    # MENU
    # =========================
    def draw_menu(self):
        self.screen.blit(self.menu_bg, (0, 0))

        title_font = pygame.font.SysFont("Arial", 50, bold=True)
        title = title_font.render(
            "COMBAT GALAXY",
            True,
            (255, 140, 0)
        )

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 120)
        )

        button_font = pygame.font.SysFont("Arial", 28, bold=True)
        button_text = button_font.render(
            " ENTER ",
            True,
            WHITE
        )

        rect = pygame.Rect(WIDTH // 2 - 230, HEIGHT - 140, 460, 60)

        pygame.draw.rect(self.screen, (200, 0, 0), rect, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=12)

        self.screen.blit(
            button_text,
            (
                rect.centerx - button_text.get_width() // 2,
                rect.centery - button_text.get_height() // 2
            )
        )

    # =========================
    # LOOP PRINCIPAL
    # =========================
    def run(self):
        pygame.mixer.music.load(
            os.path.join(SOUND_DIR, "background.mp3")
        )
        pygame.mixer.music.play(-1)

        # Timers configurados usando as variáveis da classe
        pygame.time.set_timer(self.enemy_event, 1200)
        pygame.time.set_timer(self.power_event, 8000)

        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                # =========================
                # MENU
                # =========================
                if self.menu:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.menu = False
                        pygame.mixer.music.stop()
                        self.start_phase_music()

                # =========================
                # GAME
                # =========================
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.shoot()

                    if event.type == self.enemy_event:
                        enemy = Enemy()

                        # Deixa mais forte por level
                        enemy.speed += self.phase_manager.current_level

                        self.enemies.add(enemy)
                        self.all_sprites.add(enemy)

                    if event.type == self.power_event:
                        power = PowerUp()
                        self.powerups.add(power)
                        self.all_sprites.add(power)

            # =========================
            # UPDATE
            # =========================
            if not self.menu:

                self.all_sprites.update()
                self.effects.update()

                # TIROS vs INIMIGOS
                hits = pygame.sprite.groupcollide(
                    self.bullets,
                    self.enemies,
                    True,
                    True
                )

                if hits:
                    self.hit_sound.play()
                    self.score += len(hits) * 10

                    for bullet in hits:
                        for enemy in hits[bullet]:
                            explosion = Explosion(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )
                            self.effects.add(explosion)
                            self.all_sprites.add(explosion)

                # PLAYER vs INIMIGOS
                player_hits = pygame.sprite.spritecollide(
                    self.player,
                    self.enemies,
                    True
                )

                if player_hits:
                    self.player.take_damage()
                    self.hit_sound.play()

                    explosion = Explosion(
                        self.player.rect.centerx,
                        self.player.rect.centery
                    )
                    self.effects.add(explosion)
                    self.all_sprites.add(explosion)

                    if self.player.lives <= 0:
                        self.show_game_over()
                        self.reset_game()
                        self.menu = True

                # POWERUPS
                power_hits = pygame.sprite.spritecollide(
                    self.player,
                    self.powerups,
                    True
                )

                for power in power_hits:
                    self.player.apply_powerup(power.type)

                # =========================
                # MUDANÇA DE FASE
                # =========================
                if self.phase_manager.time_up():
                    self.phase_manager.next_phase()

                    # Verifica se terminou bloco de 3 fases
                    if self.phase_manager.current_phase > self.phase_manager.current_level * self.phase_manager.phases_per_level:
                        self.phase_manager.start_new_level()

                        # Dificuldade aumenta por level
                        new_timer = max(
                            300,
                            1200 - (self.phase_manager.current_level - 1) * 200
                        )
                        pygame.time.set_timer(self.enemy_event, new_timer)

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
                self.effects.draw(self.screen)
                self.draw_hud()

            pygame.display.flip()