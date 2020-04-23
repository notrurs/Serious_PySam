import pygame

import config as c
from game_object import GameObject


class Kamikaze(GameObject):
    def __init__(self, x, y, picture, speed, sound, channel):
        GameObject.__init__(self, x, y, picture, speed)
        self.speed = speed
        self.sound = pygame.mixer.Sound(sound)
        self.channel = channel

    def update(self):
        self.move(-self.speed, 0)
        self.play_sound()

    def play_sound(self):
        self.channel.queue(self.sound)
