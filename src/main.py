import pygame
from maps.Map import Map
from search.SearchProblem import SearchProblem
from search.Algorithm import run_algorithm
from game.grid import Grid
from game.constants import *
from game.player import Player
from game.textbox import TextInputBox
from nlp.commands import CommandProcessor
from game.inventory import Inventory
from game.notificationSystem import NotificationSystem
from game.chrono import Chrono
from game.userPathCost import UserPathCost
import sys

# Function to show the instruction screens before playing the game
def show_image_with_text(screen, image_path, message, wait_key, y_offset=20):
    
    image = pygame.image.load(image_path).convert_alpha()

    window_width, window_height = WINDOW_SIZE, WINDOW_SIZE

    image_width, image_height = image.get_size()
    aspect_ratio = image_width / image_height

    if image_width > window_width - 100:
        image_width = window_width - 100
        image_height = image_width / aspect_ratio

    if image_height > window_height - 150:
        image_height = window_height - 150
        image_width = image_height * aspect_ratio

    image = pygame.transform.scale(image, (int(image_width), int(image_height)))

    image_rect = image.get_rect(center=(window_width // 2, (window_height // 2) - y_offset))

    font = pygame.font.Font(None, 36)
    text_surface = font.render(message, True, (0, 0, 0))

    text_rect = text_surface.get_rect(center=(window_width // 2, image_rect.bottom + 10))

    screen.fill((255, 255, 255))
    screen.blit(image, image_rect)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == wait_key:
                    waiting = False

# Function to send as a callback to active the end of the game
def game_over():
    screen = pygame.display.get_surface()
    show_image_with_text(screen, 'imgs/villager_2.png', "Press ENTER to exit", pygame.K_RETURN)

    pygame.quit()
    sys.exit()

# Function to send as a callback to active the victory screen
def win_screen():
    screen = pygame.display.get_surface()
    show_image_with_text(screen, 'imgs/villager_3.png', "Press ENTER to exit", pygame.K_RETURN)

    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    # Create the screen and the window
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 200))
    pygame.display.set_caption("Find the treasure")

    icon = pygame.image.load('imgs/key.png')
    pygame.display.set_icon(icon)

    # Instructions
    show_image_with_text(screen, 'imgs/info.png', "Press SPACE to continue", pygame.K_SPACE)
    show_image_with_text(screen, 'imgs/info_2.png', "Press SPACE to continue", pygame.K_SPACE)
    show_image_with_text(screen, 'imgs/info_3.png', "Press SPACE to continue", pygame.K_SPACE)
    show_image_with_text(screen, 'imgs/info_4.png', "Press ENTER to start", pygame.K_RETURN)


    # We create the matrix and execute the path path finding algorithm to find the key and the chest
    map = Map(GRID_SIZE)

    search_problem1 = SearchProblem(
        goal=map.key,
        initial=map.initial_pos,
        n_columns=map.n_columns,
        n_rows=map.n_rows,
        matrix=map.matrix
    )
    search_problem2 = SearchProblem(
        goal=map.final_pos,
        initial=map.key,
        n_columns=map.n_columns,
        n_rows=map.n_rows,
        matrix=map.matrix
    )
    result1 = run_algorithm(search_problem1)
    cost_1 = result1.path_cost
    result1 = map.format_path_coordinates(result1.path())
    result2 = run_algorithm(search_problem2)
    cost_2 = result2.path_cost
    result2 = map.format_path_coordinates(result2.path())

    # We get the cost of the algorithm (we will use it to set a maximum cost for the player to complete the game)
    algorithm_cost = cost_1 + cost_2

    highlighted_path = result1[1:-1] + result2[1:-1]

    # We create all the elements on screen

    # grid
    grid = Grid(map.matrix, map.key)

    # player
    player = Player([1, 1])

    # procesor for natural language
    command_processor = CommandProcessor()  

    # inventory
    inventory = Inventory(1)
    inventory_height = inventory.get_height()

    # textbox
    textbox_height = 80
    textbox_y = WINDOW_SIZE + 40 - textbox_height
    if textbox_y + textbox_height > WINDOW_SIZE + 100:
        textbox_y = WINDOW_SIZE + 100 - textbox_height
    textbox = TextInputBox(10, textbox_y, WINDOW_SIZE - 20, textbox_height, y_offset=inventory_height + 20)  # Cuadro de texto ajustado a la parte inferior
    
    # cost indicator
    user_path_cost = UserPathCost(algorithm_cost, game_over, y_offset = (inventory_height//2) - 30)

    # notification messages
    notification_system = NotificationSystem()

    # chronometre
    chrono = Chrono(total_time=90, y_offset = (inventory_height//2) - 30, time_up_callback=game_over)

    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If the player presses a key we activate the processor
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and textbox.active:
                    command_processor.process_command(textbox.text, 
                                                        player, 
                                                        grid, 
                                                        inventory, 
                                                        highlighted_path, 
                                                        notification_system, 
                                                        user_path_cost,
                                                        win_screen)
                    textbox.text = ''

            textbox.handle_event(event)

        # Background colorr
        screen.fill(BLUESKY)

        # Drawn chronometre on screen and update it
        chrono.update()
        chrono.draw(screen)

        # grid on screen
        grid.draw(screen, y_offset=inventory_height - 20)

        # player on screen
        player.draw(screen, y_offset=inventory_height - 20)

        # inventory on screen
        inventory.draw(screen)

        # textbox on screen
        textbox.draw(screen)

        # show notifications
        notification_system.draw(screen)

        # path cost on screen
        user_path_cost.draw(screen)


        pygame.display.flip()

    # Finish
    pygame.quit()


if __name__ == "__main__":
    main()
