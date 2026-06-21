import pygame
import random
import os
import sys

# Força o Windows a centralizar a janela do jogo na tela
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Inicialização limpa e direta
pygame.init()
pygame.mixer.init()

# Aponta exatamente para a pasta onde o main.py está salvo (Game_Uninter)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def img(path):
    fixed_path = os.path.normpath(path)
    return pygame.image.load(os.path.join(BASE_DIR, fixed_path))

def snd(path):
    fixed_path = os.path.normpath(path)
    return pygame.mixer.Sound(os.path.join(BASE_DIR, fixed_path))

# ---------------- CONFIGURAÇÕES DA TELA (VOLTANDO AO MODO ESTÁVEL) ----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Removemos o DOUBLEBUF que causou o conflito com a sua placa de vídeo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Combat Galaxy")

clock = pygame.time.Clock()

# ---------------- CARREGAMENTO DE ASSETS ----------------
player_img = img("assets/images/player.png")
player_img = pygame.transform.rotate(player_img, 180)
player_rect = player_img.get_rect()

enemy_imgs_raw = [
    img("assets/images/enemy_red.png"),
    img("assets/images/enemy_blue.png"),
    img("assets/images/enemy_green.png"),
]
enemy_imgs = [pygame.transform.rotate(i, 180) for i in enemy_imgs_raw]

menu_bg = pygame.transform.scale(img("assets/images/menu_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_fases = {
    1: pygame.transform.scale(img("assets/images/background1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    2: pygame.transform.scale(img("assets/images/background2.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    3: pygame.transform.scale(img("assets/images/background3.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
}

shoot_sound = snd("assets/sounds/shoot.wav")
hit_sound = snd("assets/sounds/hit.wav")
life_sound = snd("assets/sounds/life.wav")
start_sound = snd("assets/sounds/start.wav")
level_sound = snd("assets/sounds/level.wav")
game_over_sound = snd("assets/sounds/game_over.wav")

musicas_fases = {
    "menu": os.path.normpath("assets/sounds/background.mp3"),
    1: os.path.normpath("assets/sounds/bgm_fase1.mp3"),
    2: os.path.normpath("assets/sounds/bgm_fase2.mp3"),
    3: os.path.normpath("assets/sounds/bgm_fase3.mp3"),
}

# ---------------- ESTADOS DO JOGO ----------------
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"
state = MENU

# ---------------- CONFIGURAÇÕES DO JOGADOR ----------------
player_x = 50
player_y = 300
player_speed = 5
lives = 3
MAX_LIVES = 3

bullets = []
bullet_speed = 10

enemies = []
enemy_speed = 3
spawn_timer = 0

# ---------------- SISTEMA DE SCROLLING ----------------
bg_x1 = 0
bg_x2 = SCREEN_WIDTH
scroll_speed = 2

# ---------------- DADOS DA PARTIDA ----------------
score = 0
fase_atual = 1
FASE_DURACAO = 30
tempo_restante = FASE_DURACAO
fps_counter = 0

def play_bgm(chave_musica):
    pygame.mixer.music.stop()
    try:
        full_path = os.path.join(BASE_DIR, musicas_fases[chave_musica])
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Aviso de Áudio: Não foi possível tocar {chave_musica} ({e})")

def spawn_enemy():
    enemy_img = random.choice(enemy_imgs)
    max_y = SCREEN_HEIGHT - enemy_img.get_height()
    rect = enemy_img.get_rect(topleft=(SCREEN_WIDTH, random.randint(0, max_y)))
    enemies.append({"img": enemy_img, "rect": rect})

def iniciar_fase(fase):
    global fase_atual, tempo_restante, fps_counter, enemies, bullets, enemy_speed, scroll_speed
    fase_atual = fase
    tempo_restante = FASE_DURACAO
    fps_counter = 0
    enemies = []
    bullets = []
    enemy_speed = 2 + fase_atual
    scroll_speed = 1 + fase_atual

    try: level_sound.play()
    except: pass
    play_bgm(fase_atual)

def reset_game_total():
    global player_x, player_y, lives, score, state, bg_x1, bg_x2
    player_x = 50
    player_y = 300
    lives = MAX_LIVES
    score = 0
    bg_x1 = 0
    bg_x2 = SCREEN_WIDTH
    state = PLAYING

    try: start_sound.play()
    except: pass
    iniciar_fase(1)

def draw_text(text, x, y, size=30, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    img_surface = font.render(text, True, color)
    screen.blit(img_surface, (x, y))

# Inicializa tocando a música do menu
play_bgm("menu")

# ---------------- LOOP PRINCIPAL ----------------
running = True
texto_pisca_timer = 0

while running:
    clock.tick(60)
    texto_pisca_timer += 1

    # Limpa a tela a cada iteração para evitar rastros gráficos
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == MENU and event.key == pygame.K_RETURN:
                reset_game_total()

            elif state in [GAME_OVER, VICTORY] and event.key == pygame.K_RETURN:
                state = MENU
                play_bgm("menu")

            elif state == PLAYING and event.key == pygame.K_SPACE:
                largura_player = player_rect.width if 'player_rect' in locals() else 50
                altura_player = player_rect.height if 'player_rect' in locals() else 50
                b_x = player_x + largura_player
                b_y = player_y + (altura_player // 2) - 3
                bullets.append(pygame.Rect(b_x, b_y, 10, 6))

                try:
                    if shoot_sound is not None: shoot_sound.play()
                except Exception as som_erro:
                    print(f"Aviso de Áudio Silenciado: {som_erro}")

    keys = pygame.key.get_pressed()

    # ---- ATUALIZAÇÕES DA LÓGICA (UPDATE) ----
    if state == PLAYING:
        fps_counter += 1
        if fps_counter >= 60:
            tempo_restante -= 1
            fps_counter = 0

            if tempo_restante <= 0:
                if fase_atual < 3: iniciar_fase(fase_atual + 1)
                else:
                    pygame.mixer.music.stop()
                    state = VICTORY

        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed
        if bg_x1 <= -SCREEN_WIDTH: bg_x1 = SCREEN_WIDTH
        if bg_x2 <= -SCREEN_WIDTH: bg_x2 = SCREEN_WIDTH

        if keys[pygame.K_LEFT]: player_x -= player_speed
        if keys[pygame.K_RIGHT]: player_x += player_speed
        if keys[pygame.K_UP]: player_y -= player_speed
        if keys[pygame.K_DOWN]: player_y += player_speed

        player_x = max(0, min(SCREEN_WIDTH - player_rect.width, player_x))
        player_y = max(0, min(SCREEN_HEIGHT - player_rect.height, player_y))
        player_rect.topleft = (player_x, player_y)

        spawn_timer += 1
        if spawn_timer > max(15, 50 - fase_atual * 8):
            spawn_enemy()
            spawn_timer = 0

        for e in enemies: e["rect"].x -= enemy_speed
        for b in bullets: b.x += bullet_speed

        bullets_to_remove = []
        enemies_to_remove = []

        for b in bullets:
            for e in enemies:
                if b.colliderect(e["rect"]):
                    if b not in bullets_to_remove: bullets_to_remove.append(b)
                    if id(e) not in enemies_to_remove: enemies_to_remove.append(id(e))
                    score += 10
                    try: hit_sound.play()
                    except: pass

        bullets = [b for b in bullets if b not in bullets_to_remove and b.x < SCREEN_WIDTH]
        enemies = [e for e in enemies if id(e) not in enemies_to_remove and e["rect"].x > -50]

        # Processamento linear estável de impacto Jogador x Inimigos sem quebras
        enemies_hit_player = [e for e in enemies if e["rect"].colliderect(player_rect)]
        for e in enemies_hit_player:
            lives -= 1
            try: life_sound.play()
            except: pass
            enemies.remove(e)

        if lives <= 0:
            try: game_over_sound.play()
            except: pass
            pygame.mixer.music.stop()
            state = GAME_OVER

    # ---- DESENHO NA TELA (DRAW) ----
    if state == MENU:
        screen.blit(menu_bg, (0, 0))
        draw_text("Combat Galaxy", 260, 200, 55, (0, 210, 255))
        if (texto_pisca_timer // 30) % 2 == 0:
            draw_text("Digite ENTER para comecar", 255, 340, 28, (255, 255, 255))

    elif state == PLAYING:
        screen.blit(bg_fases[fase_atual], (bg_x1, 0))
        screen.blit(bg_fases[fase_atual], (bg_x2, 0))

        draw_text(f"SCORE: {score}", 20, 20, 26, (255, 255, 0))
        draw_text(f"VIDAS: {lives}/{MAX_LIVES}", 20, 50, 26, (255, 50, 50))
        draw_text(f"FASE: {fase_atual}", 350, 20, 28, (0, 255, 100))
        draw_text(f"TEMPO: {tempo_restante}s", 650, 20, 26, (255, 255, 255))

        screen.blit(player_img, (player_x, player_y))
        for e in enemies: screen.blit(e["img"], e["rect"])
        for b in bullets: pygame.draw.rect(screen, (255, 255, 0), b)

    elif state == GAME_OVER:
        screen.fill((20, 0, 0))
        draw_text("GAME OVER", 260, 230, 65, (255, 0, 0))
        draw_text(f"Pontuacao Final: {score}", 300, 310, 30, (255, 255, 255))
        draw_text("Pressione ENTER para ir ao Menu", 230, 380, 26, (150, 150, 150))

    elif state == VICTORY:
        screen.fill((0, 20, 0))
        draw_text("VITÓRIA CELESTIAL!", 180, 220, 60, (0, 255, 0))
        draw_text(f"Pontuação Máxima: {score}", 280, 300, 32, (255, 255, 255))
        draw_text("Missão Cumprida. ENTER para reiniciar.", 205, 380, 26, (150, 150, 150))

    pygame.display.flip()

pygame.quit()
sys.exit()
