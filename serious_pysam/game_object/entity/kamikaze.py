from serious_pysam.game_object.game_object import GameObject


class Kamikaze(GameObject):
    def __init__(self, x, y, picture, speed, sound, channel):
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.speed = speed

    def update(self):
        self.move(-self.speed, 0)
        self.play_sound()
