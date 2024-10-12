import pygame
import time

"""
Show a message in screen to give info or just to cheer the player
"""
class NotificationSystem:
    def __init__(self, font_size=36):
        self.notifications = []
        self.font = pygame.font.Font(None, font_size)
        
        self.villager_image = pygame.image.load('imgs/villager.png').convert_alpha()
        self.villager_image = pygame.transform.scale(self.villager_image, (120, 120))

    def add_notification(self, message, duration=2):
        current_time = time.time()
        self.notifications.append({"message": message, "start_time": current_time, "duration": duration})

    def draw(self, screen):
        current_time = time.time()
        screen_width, screen_height = screen.get_size()

        self.notifications = [n for n in self.notifications if current_time - n["start_time"] < n["duration"]]

        for i, notification in enumerate(self.notifications):
            text_surface = self.font.render(notification["message"], True, (0, 0, 0))
            
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()

            padding = 20
            rect_width = text_width + padding * 2
            rect_height = text_height + padding * 2

            rect_x = (screen_width - rect_width - 20 - self.villager_image.get_width()) // 2
            rect_y = (screen_height - max(rect_height, self.villager_image.get_height())) // 2

            pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_radius=10)

            text_x = rect_x + padding
            text_y = rect_y + padding
            screen.blit(text_surface, (text_x, text_y))

            villager_x = rect_x + rect_width + 20
            villager_y = rect_y + (rect_height - self.villager_image.get_height()) // 2

            screen.blit(self.villager_image, (villager_x, villager_y))

