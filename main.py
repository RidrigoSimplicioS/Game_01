import pygame

from config import *
from code.game import Game

def main():

    pygame.init()

    pygame.mixer.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Combat Galaxy"
    )

    game = Game(screen)

    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()