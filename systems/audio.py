import pygame
import os

class AudioManager:

    @staticmethod
    def play_music(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()