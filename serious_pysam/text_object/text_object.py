import pygame


class TextObject:
    def __init__(self,
                 x,
                 y,
                 text_func,
                 color,
                 font_name,
                 font_size,
                 centralized=False):
        self.x = x
        self.y = y
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.Font(font_name, font_size)
        self.bounds = self.get_surface(text_func())
        self.centralized = centralized

    def blit(self, surface):
        text_surface, self.bounds = self.get_surface(self.text_func())

        if self.centralized:
            pos = (self.x - self.bounds.width // 2, self.y - self.bounds.height // 2)
        else:
            pos = (self.x, self.y)

        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, True, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass
