import pygame


class PhaseManager:

    def __init__(self):

        # FASE E LEVEL
        self.current_phase = 1
        self.current_level = 1

        # 3 fases por level
        self.phases_per_level = 3

        # tempo de cada fase
        self.phase_duration = 30
        self.phase_start_time = pygame.time.get_ticks()

    # -------------------------
    # TIMER
    # -------------------------
    def remaining_time(self):

        elapsed = (
            pygame.time.get_ticks()
            - self.phase_start_time
        ) // 1000

        return max(0, self.phase_duration - elapsed)

    def time_up(self):
        return self.remaining_time() <= 0

    # -------------------------
    # FASE
    # -------------------------
    def next_phase(self):

        self.current_phase += 1
        self.phase_start_time = pygame.time.get_ticks()

    # -------------------------
    # LEVEL CONTROL
    # -------------------------
    def is_level_finished(self):

        return self.current_phase > self.current_level * self.phases_per_level

    def start_new_level(self):

        self.current_level += 1

        # começa nova sequência de 3 fases
        self.current_phase = (self.current_level - 1) * self.phases_per_level + 1

        self.phase_start_time = pygame.time.get_ticks()