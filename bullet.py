import config as c
from game_object import GameObject


class Bullet(GameObject):
    def __init__(self, x, y, picture, speed, sound):
        GameObject.__init__(self, x, y, picture, speed, sound)
        self.speed = c.bullet_speed

    def update(self):
        self.move(self.speed, 0)
