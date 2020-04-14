import pygame

import config as c
from game_object import GameObject


class Bullet(GameObject):
    def __init__(self, x, y, picture, speed, sound):
        GameObject.__init__(self, x, y, picture, speed)
        self.speed = c.bullet_speed
        self.sound = pygame.mixer.Sound(sound)

    def update(self):
        self.move(self.speed, 0)
