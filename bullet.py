from pygame.transform import rotate
from math import atan2
from math import degrees
from math import cos
from math import sin

from game_object import GameObject


class Bullet(GameObject):
    def __init__(self, x, y, picture, speed, sound, objects_positions=None):
        GameObject.__init__(self, x, y, picture, speed, sound)
        self.speed = (speed, 0)
        self.obj_pos = objects_positions
        self.rotate_bullet(objects_positions)

    def rotate_bullet(self, objects_positions):
        if objects_positions is not None:
            target_pos = objects_positions[0]
            attacker_pos = objects_positions[1]
            angle = atan2(attacker_pos[1] - target_pos[1], attacker_pos[0] - target_pos[0])

            dx = -round(10 * cos(abs(angle)))
            if attacker_pos[1] < target_pos[1]:
                dy = round(10 * sin(abs(angle)))
            else:
                dy = -round(10 * sin(abs(angle)))

            self.image_object = rotate(self.image_object, 180 - degrees(angle))  # 180 is for correct rotation
            self.speed = (dx, dy)
