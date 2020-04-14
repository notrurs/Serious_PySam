from pygame import image
from pygame import display


class GameObject:
    def __init__(self, x, y, picture, speed=(0, 0)):
        self.image_object = image.load(picture).convert_alpha()
        self.rect = self.image_object.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    def blit(self, surface):
        surface.blit(self.image_object, (self.rect.x, self.rect.y))

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        if self.speed == [0, 0]:
            return
        self.move(*self.speed)
