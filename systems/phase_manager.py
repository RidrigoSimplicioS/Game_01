import pygame


class PhaseManager:

    def __init__(self):

        self.current_phase = 1

        self.max_phases = 3

        self.phase_duration = 30

        self.phase_start_time = pygame.time.get_ticks()

    def remaining_time(self):

        elapsed = (
            pygame.time.get_ticks()
            - self.phase_start_time
        ) // 1000

        remaining = self.phase_duration - elapsed

        return max(0, remaining)

    def time_up(self):

        return self.remaining_time() <= 0

    def next_phase(self):

        self.current_phase += 1

        self.phase_start_time = pygame.time.get_ticks()

    def is_finished(self):

        return self.current_phase > self.max_phases