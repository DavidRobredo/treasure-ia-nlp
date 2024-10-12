import pygame
from .constants import CELL_SIZE, WINDOW_SIZE

"""
The inventory in the top of the screen to make clear which tool we are using
"""
class Inventory:
    def __init__(self, tool):
        self.images = {
            1: pygame.image.load('imgs/inventory_1.png').convert_alpha(),
            2: pygame.image.load('imgs/inventory_2.png').convert_alpha(),
            3: pygame.image.load('imgs/inventory_3.png').convert_alpha(),
            4: pygame.image.load('imgs/inventory_4.png').convert_alpha()
        }

        self.current_tool = tool

        self.scale_inventory()

    def scale_inventory(self):
        for key in self.images:
            original_width, original_height = self.images[key].get_size()

            new_width = original_width // 2
            new_height = original_height // 2

            self.images[key] = pygame.transform.scale(self.images[key], (new_width, new_height))

    def update(self, tool):
        self.current_tool = tool

    def get_height(self):
        return self.images[self.current_tool].get_height()

    def draw(self, screen):
        image = self.images[self.current_tool]

        x_pos = (WINDOW_SIZE - image.get_width()) // 2
        y_pos = (-10)

        screen.blit(image, (x_pos, y_pos))
