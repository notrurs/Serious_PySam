from serious_pysam.game_object.game_object import GameObject
from serious_pysam.config import ENEMY_KAMIKAZE_HP
from serious_pysam.config import ENEMY_KAMIKAZE_DAMAGE


class Kamikaze(GameObject):
    def __init__(self, x, y, picture, speed, sound, channel):
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.speed = speed
        self.health = ENEMY_KAMIKAZE_HP
        self.damage = ENEMY_KAMIKAZE_DAMAGE

    def update(self):
        self.move(-self.speed, 0)
        self.play_sound()
