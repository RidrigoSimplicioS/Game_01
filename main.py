import pygame
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Galaxy combat")

clock = pygame.time.Clock()

# estados do jogo
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

game_state = MENU


def draw_menu():
    screen.fill((10, 10, 30))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Galaxy combat", True, (255, 255, 255))
    screen.blit(text, (150, 200))

    font2 = pygame.font.SysFont(None, 30)
    text2 = font2.render("Pressione ENTER para iniciar", True, (200, 200, 200))
    screen.blit(text2, (220, 300))


def draw_game():
    screen.fill((0, 0, 0))

    # nave simples (placeholder)
    pygame.draw.rect(screen, (0, 200, 255), (400, 500, 50, 50))


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == MENU and event.key == pygame.K_RETURN:
                game_state = PLAYING

    if game_state == MENU:
        draw_menu()

    elif game_state == PLAYING:
        draw_game()

    pygame.display.flip()

pygame.quit()