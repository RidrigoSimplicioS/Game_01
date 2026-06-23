import pygame

from config import PHASE_TIME


class PhaseManager:

    def __init__(self):

        self.current_phase = 1

        self.phase_start = pygame.time.get_ticks()

    def remaining_time(self):

        elapsed = (
            pygame.time.get_ticks()
            - self.phase_start
        ) // 1000

        return max(
            0,
            PHASE_TIME - elapsed
        )

    def next_phase(self):

        self.current_phase += 1

        self.phase_start = pygame.time.get_ticks()

    def is_finished(self):

        return self.current_phase > 3