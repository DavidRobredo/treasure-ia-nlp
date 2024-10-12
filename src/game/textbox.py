import pygame

class TextInputBox:
    def __init__(self, x, y, w, h, y_offset=0, font_size=32, padding=10, border_color=(0, 0, 0), bg_color=(200, 200, 200), text_color=(0, 0, 0), placeholder_text="Enter text..."):
        self.rect = pygame.Rect(x, y + y_offset, w, h)
        self.color_active = pygame.Color('dodgerblue2')
        self.color_inactive = border_color
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.text = ''
        self.active = False
        self.padding = padding

        self.placeholder_text = placeholder_text
        self.placeholder_color = (150, 150, 150)

    # Handle the input of text
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.color_active if self.active else self.color_inactive, self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + self.padding, self.rect.y + self.padding))

        if not self.text and not self.active:
            placeholder_surface = self.font.render(self.placeholder_text, True, self.placeholder_color)
            screen.blit(placeholder_surface, (self.rect.x + self.padding, self.rect.y + self.padding))

    def update(self):
        pass
