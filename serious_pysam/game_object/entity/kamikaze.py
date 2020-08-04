from serious_pysam.game_object.game_object import GameObject
from serious_pysam.config import ENEMY_KAMIKAZE_HP
from serious_pysam.config import ENEMY_KAMIKAZE_DAMAGE


class Kamikaze(GameObject):
    """Describes kamikaze behaviour.

    The main goal of kamikaze is run from right to left.

    """
    def __init__(self, x, y, picture, speed, sound, channel):
        """Kamikaze has own vars:
        health - kamikaze's health value
        damage - kamikaze's damage

        """
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.speed = speed  # Overrided var because kamikaze can run along only one axis
        self.health = ENEMY_KAMIKAZE_HP
        self.damage = ENEMY_KAMIKAZE_DAMAGE

    def update(self):
        """Overrided method update() form GameObject.

        Move kamikaze from right to left.

        """
        self.move(-self.speed, 0)  # Negative is for from right to left running
        self.play_sound()
