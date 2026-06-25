import pygame
import os
import random

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
        self.paused = False  # Rastreia se o jogo está pausado

        self.score = 0
        self.high_score = 0  # Armazena a pontuação máxima

        self.phase_manager = PhaseManager()

        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 20, bold=True)
        # Nova fonte menor exclusiva para o manual de instruções do cantinho
        self.manual_font = pygame.font.SysFont("Arial", 16, bold=True)

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

        # RETÂNGULOS DOS BOTÕES (MENU INICIAL)
        self.play_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 230, 300, 50)
        self.exit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 160, 300, 50)

        # RETÂNGULOS DOS BOTÕES EM JOGO (HUD)
        self.pause_button_rect = pygame.Rect(WIDTH - 240, 20, 100, 40)
        self.game_exit_button_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)

    def update_difficulty(self):
        phase = self.phase_manager.current_phase
        new_timer = max(300, self.base_enemy_timer - (phase - 1) * self.enemy_increment)
        pygame.time.set_timer(self.enemy_event, new_timer)

    def reset_game(self):
        self.score = 0
        self.phase_manager = PhaseManager()
        self.bg_x = 0
        self.paused = False

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

        pygame.mixer.music.load(os.path.join(SOUND_DIR, "background.mp3"))
        pygame.mixer.music.play(-1)

    def show_game_over(self):
        self.screen.fill(BLACK)

        if self.score > self.high_score:
            self.high_score = self.score

        font_title = pygame.font.SysFont("Arial", 80, bold=True)
        font_score = pygame.font.SysFont("Arial", 36)

        text_game_over = font_title.render("GAME OVER", True, RED)
        text_current_score = font_score.render(f"Sua Pontuação: {self.score}", True, WHITE)
        text_high_score = font_score.render(f"Pontuação Máxima: {self.high_score}", True, (255, 215, 0))

        self.screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 2 - 100))
        self.screen.blit(text_current_score, (WIDTH // 2 - text_current_score.get_width() // 2, HEIGHT // 2 + 20))
        self.screen.blit(text_high_score, (WIDTH // 2 - text_high_score.get_width() // 2, HEIGHT // 2 + 80))

        pygame.display.flip()
        pygame.time.delay(3500)

    def show_victory(self):
        """Tela exibida quando o jogador alcança a condição de vitória."""
        self.screen.fill(BLACK)

        if self.score > self.high_score:
            self.high_score = self.score

        font_title = pygame.font.SysFont("Arial", 80, bold=True)
        font_score = pygame.font.SysFont("Arial", 36)

        text_victory = font_title.render("VITÓRIA!", True, (0, 255, 100))
        text_current_score = font_score.render(f"Sua Pontuação: {self.score}", True, WHITE)
        text_high_score = font_score.render(f"Pontuação Máxima: {self.high_score}", True, (255, 215, 0))

        self.screen.blit(text_victory, (WIDTH // 2 - text_victory.get_width() // 2, HEIGHT // 2 - 100))
        self.screen.blit(text_current_score, (WIDTH // 2 - text_current_score.get_width() // 2, HEIGHT // 2 + 20))
        self.screen.blit(text_high_score, (WIDTH // 2 - text_high_score.get_width() // 2, HEIGHT // 2 + 80))

        pygame.display.flip()
        pygame.time.delay(3500)

    def start_phase_music(self):
        phase = self.phase_manager.current_phase
        music_index = ((phase - 1) % 3) + 1
        pygame.mixer.music.load(os.path.join(SOUND_DIR, f"bgm_fase{music_index}.mp3"))
        pygame.mixer.music.play(-1)

    def draw_background(self):
        bg_index = ((self.phase_manager.current_phase - 1) % 3) + 1
        bg = self.backgrounds[bg_index]

        if not self.paused:
            self.bg_x -= self.scroll_speed

        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(bg, (self.bg_x, 0))
        self.screen.blit(bg, (self.bg_x + WIDTH, 0))

    def draw_hud(self):
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 215, 0)), (20, 20))
        self.screen.blit(self.font.render(f"Life: {self.player.lives}", True, (0, 255, 100)), (20, 60))
        self.screen.blit(self.font.render(f"Time: {self.phase_manager.remaining_time()}", True, (0, 200, 255)),
                         (20, 100))

        # BOTÃO PAUSE
        pause_txt_color = (255, 255, 0) if self.paused else WHITE
        pygame.draw.rect(self.screen, (50, 50, 50), self.pause_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, pause_txt_color, self.pause_button_rect, 2, border_radius=10)
        p_text = self.small_font.render("RESUME" if self.paused else "PAUSE", True, pause_txt_color)
        self.screen.blit(p_text, (self.pause_button_rect.centerx - p_text.get_width() // 2,
                                  self.pause_button_rect.centery - p_text.get_height() // 2))

        # BOTÃO QUIT (SAÍDA)
        pygame.draw.rect(self.screen, (150, 0, 0), self.game_exit_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, self.game_exit_button_rect, 2, border_radius=10)
        e_text = self.small_font.render("QUIT", True, WHITE)
        self.screen.blit(e_text, (self.game_exit_button_rect.centerx - e_text.get_width() // 2,
                                  self.game_exit_button_rect.centery - e_text.get_height() // 2))

    def draw_menu(self):
        self.screen.blit(self.menu_bg, (0, 0))

        title_font = pygame.font.SysFont("Arial", 50, bold=True)
        title = title_font.render("COMBAT GALAXY", True, (255, 140, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        # HIGH SCORE NA TELA INICIAL
        hs_font = pygame.font.SysFont("Arial", 28, bold=True)
        hs_text = hs_font.render(f"HIGH SCORE: {self.high_score}", True, (50, 50, 50))
        self.screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, 190))

        # ─── MANUAL ATUALIZADO: COR PRETA E MENOR TAMANHO ───
        linhas_manual = [
            "COMANDOS:",
            "• Clique nos botões para a opção desejada",
            "• Mover nave: SETAS do teclado",
            "• Combate: ESPAÇO para atirar",
            "• Vitória: Alcance 1000 pontos!"
        ]

        y_manual = HEIGHT - 110  # Ajustado sutilmente para acomodar a fonte menor (tamanho 16)
        for linha in linhas_manual:
            # Cor alterada permanentemente para Preto (0, 0, 0)
            texto_manual = self.manual_font.render(linha, True, (0, 0, 0))
            self.screen.blit(texto_manual, (20, y_manual))
            y_manual += 20  # Espaçamento menor entre linhas para reduzir o tamanho total do campo

        # Pega a posição atual do mouse
        mouse_pos = pygame.mouse.get_pos()

        # ------------------------------------
        # BOTÃO PLAY (Efeito de tamanho e cor Azul)
        # ------------------------------------
        if self.play_button_rect.collidepoint(mouse_pos):
            play_color = (0, 102, 204)  # Azul destacado
            current_play_rect = self.play_button_rect.inflate(20, 10)
            button_font_play = pygame.font.SysFont("Arial", 32, bold=True)
        else:
            play_color = (0, 180, 0)  # Verde padrão
            current_play_rect = self.play_button_rect
            button_font_play = pygame.font.SysFont("Arial", 28, bold=True)

        play_text = button_font_play.render(" PLAY ", True, WHITE)
        pygame.draw.rect(self.screen, play_color, current_play_rect, border_radius=40)
        pygame.draw.rect(self.screen, WHITE, current_play_rect, 2, border_radius=40)
        self.screen.blit(
            play_text,
            (
                current_play_rect.centerx - play_text.get_width() // 2,
                current_play_rect.centery - play_text.get_height() // 2
            )
        )

        # ------------------------------------
        # BOTÃO EXIT (Efeito de tamanho e cor Roxa)
        # ------------------------------------
        if self.exit_button_rect.collidepoint(mouse_pos):
            exit_color = (128, 0, 128)  # Roxo destacado
            current_exit_rect = self.exit_button_rect.inflate(20, 10)
            button_font_exit = pygame.font.SysFont("Arial", 32, bold=True)
        else:
            exit_color = (200, 0, 0)  # Vermelho padrão
            current_exit_rect = self.exit_button_rect
            button_font_exit = pygame.font.SysFont("Arial", 28, bold=True)

        exit_text = button_font_exit.render(" EXIT ", True, WHITE)
        pygame.draw.rect(self.screen, exit_color, current_exit_rect, border_radius=40)
        pygame.draw.rect(self.screen, WHITE, current_exit_rect, 2, border_radius=40)
        self.screen.blit(
            exit_text,
            (
                current_exit_rect.centerx - exit_text.get_width() // 2,
                current_exit_rect.centery - exit_text.get_height() // 2
            )
        )

    def run(self):
        pygame.mixer.music.load(os.path.join(SOUND_DIR, "background.mp3"))
        pygame.mixer.music.play(-1)

        pygame.time.set_timer(self.enemy_event, 1200)
        pygame.time.set_timer(self.power_event, 8000)

        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # EVENTOS DO MENU INICIAL
                if self.menu:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.menu = False
                        self.reset_game()
                        pygame.mixer.music.stop()
                        self.start_phase_music()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.play_button_rect.collidepoint(event.pos):
                            self.menu = False
                            self.reset_game()
                            pygame.mixer.music.stop()
                            self.start_phase_music()
                        elif self.exit_button_rect.collidepoint(event.pos):
                            self.running = False

                # EVENTOS DURANTE O JOGO
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.pause_button_rect.collidepoint(event.pos):
                            self.paused = not self.paused
                            if self.paused:
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()

                        elif self.game_exit_button_rect.collidepoint(event.pos):
                            self.reset_game()
                            self.menu = True

                    if not self.paused:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            self.player.shoot()

                        if event.type == self.enemy_event:
                            enemy = Enemy()
                            enemy.speed += (self.phase_manager.current_level - 1)
                            self.enemies.add(enemy)
                            self.all_sprites.add(enemy)

                        if event.type == self.power_event:
                            power = PowerUp()
                            self.powerups.add(power)
                            self.all_sprites.add(power)

            # ATUALIZAÇÃO DO MODELO
            if not self.menu and not self.paused:
                self.all_sprites.update()
                self.effects.update()

                # TIROS vs INIMIGOS
                hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
                if hits:
                    self.hit_sound.play()
                    self.score += len(hits) * 10
                    for bullet in hits:
                        for enemy in hits[bullet]:
                            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                            self.effects.add(explosion)
                            self.all_sprites.add(explosion)

                # PLAYER vs INIMIGOS
                player_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if player_hits:
                    self.player.take_damage()
                    self.hit_sound.play()
                    explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
                    self.effects.add(explosion)
                    self.all_sprites.add(explosion)

                    if self.player.lives <= 0:
                        self.show_game_over()
                        self.reset_game()
                        self.menu = True

                # POWERUPS
                power_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
                for power in power_hits:
                    self.player.apply_powerup(power.type)

                # ─── CONDIÇÃO DE VITÓRIA (1000 pontos) ───
                if self.score >= 1000:
                    self.show_victory()
                    self.reset_game()
                    self.menu = True

                if self.phase_manager.time_up():
                    self.phase_manager.next_phase()
                    if self.phase_manager.current_phase > self.phase_manager.current_level * self.phase_manager.phases_per_level:
                        self.phase_manager.start_new_level()
                        new_timer = max(300, 1200 - (self.phase_manager.current_level - 1) * 200)
                        pygame.time.set_timer(self.enemy_event, new_timer)
                    self.start_phase_music()

            # RENDERIZAÇÃO
            self.screen.fill(BLACK)

            if self.menu:
                self.draw_menu()
            else:
                self.draw_background()
                self.all_sprites.draw(self.screen)
                self.effects.draw(self.screen)
                self.draw_hud()

                if self.paused:
                    pause_font = pygame.font.SysFont("Arial", 64, bold=True)
                    pause_text = pause_font.render("PAUSED", True, WHITE)
                    self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2,
                                                  HEIGHT // 2 - pause_text.get_height() // 2))

            pygame.display.flip()