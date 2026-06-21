#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Uninter")

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 20))

    pygame.display.flip()

pygame.quit()
    screen.fill((30, 30, 30))  # fundo cinza escuro
    pygame.display.flip()

pygame.quit()