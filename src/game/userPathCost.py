import pygame

# Shows the maximum path cost that the user can reach, if it surpases, the player losses.
class UserPathCost:
    def __init__(self, algorithm_cost, end_game_callback, x_offset=45, y_offset=20):
        self.cost = algorithm_cost
        self.end_game_callback = end_game_callback
        self.font = pygame.font.Font(None, 60)
        self.text_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.x_offset = x_offset
        self.y_offset = y_offset

    # Updates the cost each time an action occurs
    def reduce_cost(self, amount=1):
        self.cost -= amount
        self.check_cost()

    # Checks if 0 has been reached, in that case, the end game screen pops up
    def check_cost(self):
        if self.cost <= 0:
            self.end_game_callback()

    def draw(self, screen):
        if self.cost <= 10:
            self.text_color = (255, 0, 0)

        cost_str = f"{int(self.cost)}"
        cost_surface = self.font.render(cost_str, True, self.text_color)

        for offset in [-2, -1, 1, 2]:
            border_surface = self.font.render(cost_str, True, self.border_color)
            screen.blit(border_surface, (self.x_offset + offset, self.y_offset))
            screen.blit(border_surface, (self.x_offset, self.y_offset + offset))

        screen.blit(cost_surface, (self.x_offset, self.y_offset))
