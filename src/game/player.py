import pygame
from .constants import *


class Player:
    def __init__(self, initial_pos):
        self.pos = initial_pos
        self.path_cost = 0
        self.tool = 1
        self.has_key = False
        
        self.player_skins = {
            1: pygame.image.load('imgs/player_1.png').convert_alpha(),
            2: pygame.image.load('imgs/player_2.png').convert_alpha(),
            3: pygame.image.load('imgs/player_3.png').convert_alpha(),
            4: pygame.image.load('imgs/player_4.png').convert_alpha(),
        }
        
        for key in self.player_skins:
            self.player_skins[key] = pygame.transform.scale(self.player_skins[key], (CELL_SIZE, CELL_SIZE))
        
        self.image = self.player_skins[self.tool]

    def draw(self, screen, y_offset=0):
        x_pos = self.pos[1] * CELL_SIZE
        y_pos = self.pos[0] * CELL_SIZE + y_offset
        
        screen.blit(self.image, (x_pos, y_pos))


    # Check if the tool selected is the correct one to make the move
    def check_valid_move(self, matrix, new_pos):
        return matrix[new_pos[0]][new_pos[1]] == self.tool


    # Checks if a move is inside the matrix limits and moves the player
    def move(self, direction, grid, notification_system, user_path_cost, win_screen):
        grid_rows = grid.rows
        grid_cols = grid.cols
        matrix = grid.matrix
        key_coords = grid.key_coords
        
        if direction == "up" and self.pos[0] > 1 and self.check_valid_move(matrix, (self.pos[0] - 1, self.pos[1])):
            self.pos[0] -= 1
            self.path_cost += matrix[self.pos[0]][self.pos[1]]
            user_path_cost.reduce_cost(matrix[self.pos[0]][self.pos[1]])
        elif direction == "down" and self.pos[0] < grid_rows - 2 and self.check_valid_move(matrix, (self.pos[0] + 1, self.pos[1])):
            self.pos[0] += 1
            self.path_cost += matrix[self.pos[0]][self.pos[1]]
            user_path_cost.reduce_cost(matrix[self.pos[0]][self.pos[1]])

        elif direction == "left" and self.pos[1] > 1 and self.check_valid_move(matrix, (self.pos[0], self.pos[1] - 1)):
            self.pos[1] -= 1
            self.path_cost += matrix[self.pos[0]][self.pos[1]]
            user_path_cost.reduce_cost(matrix[self.pos[0]][self.pos[1]])

        elif direction == "right" and self.pos[1] < grid_cols - 2 and self.check_valid_move(matrix, (self.pos[0], self.pos[1] + 1)):
            self.pos[1] += 1
            self.path_cost += matrix[self.pos[0]][self.pos[1]]
            user_path_cost.reduce_cost(matrix[self.pos[0]][self.pos[1]])

        else:
            notification_system.add_notification("That move is not valid, captain!")

        # Checks if the player is on the block with the key
        if self.pos[0] == key_coords[0] and self.pos[1] == key_coords[1]:
            self.has_key = True
            grid.hide_key()
            notification_system.add_notification("Good job getting the key, captain!")

        # Checks if the player is on the goal block, if the player is there, the end game callback pops up
        if self.pos[0] == grid_rows - 2 and self.pos[1] == grid_cols - 2 and self.has_key:
            win_screen()


    # Changes tool and costs 1
    def change_tool(self, new_tool, user_path_cost):
        if new_tool != self.tool:
            self.tool = new_tool
            self.path_cost += 1
            user_path_cost.reduce_cost()
            
            self.image = self.player_skins[self.tool]


