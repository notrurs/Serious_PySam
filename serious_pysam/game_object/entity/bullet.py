from pygame.transform import rotate
from math import atan2
from math import degrees
from math import cos
from math import sin

from serious_pysam.game_object.game_object import GameObject


class Bullet(GameObject):
    """Describes bullet behaviour.

    The main goal of bullet is movement in a given direction.

    """
    def __init__(self, x, y, picture, speed, sound, damage, objects_positions=None):
        """Bullet has own vars:
        damage - bullet damage
        obj_pos - a tuple, which contains target position and attacker position

        """
        GameObject.__init__(self, x, y, picture, speed, sound)
        self.speed = (speed, 0)
        self.damage = damage
        self.obj_pos = objects_positions
        self.rotate_bullet(objects_positions)

    def rotate_bullet(self, objects_positions):
        """Rotate bullet picture and sets movement direction in two axises.

        :param objects_positions: contains target position and attacker position,
        so bullet can know in which direction it need to move. If value is None,
        bullet moves only X axis
        :type objects_positions: list, tuple

        """
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
