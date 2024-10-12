import pygame
from .constants import *

"""
Chrono class to make the challenge timed
"""
class Chrono:

    def __init__(self, total_time, y_offset=10, time_up_callback=None):
        self.total_time = total_time
        self.time_left = total_time
        self.font = pygame.font.Font(None, 60)
        self.start_ticks = pygame.time.get_ticks()
        self.y_offset = y_offset
        self.time_up_callback = time_up_callback

    # We check if time is up, if it is we execute the callback (end game)
    def update(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.time_left = max(self.total_time - elapsed_time, 0)

        if self.is_time_up() and self.time_up_callback:
            self.time_up_callback()


    def draw(self, screen):
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        time_str = f"{minutes:02}:{seconds:02}"

        time_surface = self.font.render(time_str, True, (255, 255, 255))

        border_color = (0, 0, 0)
        for offset in [-2, -1, 1, 2]:
            border_surface = self.font.render(time_str, True, border_color)
            screen.blit(border_surface, (WINDOW_SIZE - 120 + offset, self.y_offset))
            screen.blit(border_surface, (WINDOW_SIZE - 120, self.y_offset + offset))

        screen.blit(time_surface, (WINDOW_SIZE - 120, self.y_offset))

    def is_time_up(self):
        return self.time_left <= 0
