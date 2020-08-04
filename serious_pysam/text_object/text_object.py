import pygame


class TextObject:
    """Class for text objects like hp or score labels."""
    def __init__(self,
                 x,
                 y,
                 text_func,
                 color,
                 font_name,
                 font_size,
                 centralized=False):
        """
        :param x: Coordinate X
        :type x: int
        :param y: Coordinate Y
        :type y: int
        :param text_func: Function with text
        :type text_func: function
        :param color: (R, G, B) tuple with text color
        :type color: tuple, list
        :param font_name: path to the font
        :type font_name: str
        :param font_size: Font size
        :type font_size: int
        :param centralized: Centralized label or no
        :type centralized: bool
        """
        self.x = x
        self.y = y
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.Font(font_name, font_size)
        self.bounds = self.get_surface(text_func())
        self.centralized = centralized

    def blit(self, surface):
        """Blits text label"""
        text_surface, self.bounds = self.get_surface(self.text_func())

        if self.centralized:
            pos = (self.x - self.bounds.width // 2, self.y - self.bounds.height // 2)
        else:
            pos = (self.x, self.y)

        surface.blit(text_surface, pos)

    def get_surface(self, text):
        """Returns text surface and text rect"""
        text_surface = self.font.render(text, True, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        """All game objects must have this method, but labels don't need it, so use this plug"""
        pass
