import numpy as np
import pygame
from .constants import *

class Grid:

    # We load the matrix and the textures
    def __init__(self, matrix, key_coords=None):
        self.matrix = self.format_matrix(matrix)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.path_coords = []
        self.path_highlighted = False

        self.textures = {
            1: pygame.image.load('imgs/wool.png').convert(),
            2: pygame.image.load('imgs/dirt.png').convert(),
            3: pygame.image.load('imgs/wood.png').convert(),
            4: pygame.image.load('imgs/cobble.png').convert(),
            -1: pygame.image.load('imgs/bedrock.png').convert()
        }

        # Load block textures
        for key in self.textures:
            self.textures[key] = pygame.transform.scale(self.textures[key], (CELL_SIZE, CELL_SIZE))

        # Load the diamonds in the highlighted path
        self.diamond = pygame.image.load('imgs/diamond.png').convert_alpha()
        self.diamond = pygame.transform.scale(self.diamond, (CELL_SIZE, CELL_SIZE))

        # Load the key in the map
        self.key_image = pygame.image.load('imgs/key.png').convert_alpha()
        self.key_image = pygame.transform.scale(self.key_image, (CELL_SIZE, CELL_SIZE))

        # Load the chest in the goal position
        self.chest_image = pygame.image.load('imgs/chest.png').convert_alpha()
        self.chest_image = pygame.transform.scale(self.chest_image, (CELL_SIZE, CELL_SIZE))

        if key_coords is not None:
            self.key_coords = (key_coords[0] + 1, key_coords[1] + 1)
        else:
            self.key_coords = (-1, -1)

    # This creates a bedrock border
    def format_matrix(self, matrix):
        formatted_matrix = np.full((len(matrix) + 2, len(matrix[0]) + 2), -1)
        formatted_matrix[1:-1, 1:-1] = matrix
        return formatted_matrix

    def draw(self, screen, y_offset=0):
        
        total_width = self.cols * CELL_SIZE
        x_offset = (WINDOW_SIZE - total_width) // 2

        for row in range(self.rows):
            for col in range(self.cols):
                texture = self.get_texture(self.matrix[row][col])

                screen.blit(texture, (x_offset + col * CELL_SIZE, row * CELL_SIZE + y_offset))

                if self.path_highlighted and (row, col) in self.path_coords:
                    screen.blit(self.diamond, (x_offset + col * CELL_SIZE, row * CELL_SIZE + y_offset))

                if (row, col) == self.key_coords and self.key_coords != (-1, -1):
                    screen.blit(self.key_image, (x_offset + col * CELL_SIZE, row * CELL_SIZE + y_offset))

        chest_row = self.rows - 2
        chest_col = self.cols - 2
        screen.blit(self.chest_image, (x_offset + chest_col * CELL_SIZE, chest_row * CELL_SIZE + y_offset))

    def get_texture(self, value):
        return self.textures.get(value, self.textures[-1])

    # We highlight the path extracted from the coords
    def highlight_path(self, coords):
        self.path_highlighted = True
        if not self.path_coords:
            self.path_coords = [(x + 1, y + 1) for x, y in coords]

    def hide_key(self):
        self.key_coords = (-1, -1)
