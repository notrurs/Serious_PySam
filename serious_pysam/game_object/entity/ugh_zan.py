from time import monotonic
from random import choice

from serious_pysam.game_object.game_object import GameObject
from serious_pysam.config import BOSS_PERMITTED_POSITION_X
from serious_pysam.config import BOSS_PERMITTED_POSITION_Y
from serious_pysam.config import BOSS_ATTACK1_SPEED
from serious_pysam.config import BOSS_ATTACK1_PERMITTED_X
from serious_pysam.config import BOSS_ATTACK_PERIOD
from serious_pysam.config import BOSS_BULLET_SPEED
from serious_pysam.config import BOSS_ATTACK2_SPEED
from serious_pysam.config import BOSS_ATTACK2_STEPS
from serious_pysam.config import BOSS_BULLET_IMAGES
from serious_pysam.config import BOSS_HP
from serious_pysam.config import BOSS_DAMAGE
from serious_pysam.config import BOSS_BULLETS_DAMAGES


class UghZan(GameObject):
    """Describes boss behaviour.

    Boss can move in two axes and shoot. There is some interval between
    boss's attacks. And he knows about his permitted area on the screen,
    so doesn't go beyond the screen.

    """
    def __init__(self, x, y, picture, speed, sound, channel):
        """UghZan has own vars:

        time - timer responsible for intervals between attacks
        health - health indicator
        damage - melee damage if touch hero
        bullets_damages - list with bullet damages for all weapons
        attack_period - given interval between attacks
        is_boss_live - current life state
        attack_state - responsible for current boss state (idle, attack1, attack2, ... etc.)
        is_boss_fire - current fire state
        permitted_x - permitted area in X axis
        permitted_y - permitted area in Y axis
        bullet_speed - bullet movement speed
        attack1_speed - boost speed
        attack1_permitted_x - permitted area in X axis for attack1
        attack2_speed - movement speed for attack2
        attack2_steps - count of steps (how far) for attack2
        attack2_current_steps - counter current attack2 steps

        """
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.speed = (speed, 0)
        self.time = monotonic()
        self.health = BOSS_HP
        self.damage = BOSS_DAMAGE
        self.bullets_damages = BOSS_BULLETS_DAMAGES
        self.attack_period = BOSS_ATTACK_PERIOD
        self.is_boss_live = True
        self.attack_state = 'idle'
        self.is_boss_fire = False
        self.permitted_x = BOSS_PERMITTED_POSITION_X
        self.permitted_y = BOSS_PERMITTED_POSITION_Y
        self.bullet_speed = BOSS_BULLET_SPEED
        self.attack1_speed = BOSS_ATTACK1_SPEED
        self.attack1_permitted_x = BOSS_ATTACK1_PERMITTED_X
        self.attack2_speed = BOSS_ATTACK2_SPEED
        self.attack2_steps = BOSS_ATTACK2_STEPS
        self.attack2_current_steps = 0

        # These nums is offsets from boss positions for each bullet pos
        self.boss_bullets_pos = ([self.x + 8, self.y + 88],
                                 [self.x + 165, self.y + 77],
                                 [self.x + 32, self.y + 165],
                                 [self.x + 118, self.y + 139])
        self.boss_bullets_images = BOSS_BULLET_IMAGES

    def get_time(self):
        """Returns current time."""
        return int(monotonic() - self.time)

    def attack1(self, hero_position):
        """Changes current speed.

        hero_position is not a required parameter, but it is there for ease of
        writing code.

        """
        self.set_speed(-self.attack1_speed)

    def attack2(self, hero_position):
        """Changes speed and fire state. This functions knows in which direction
        boss need move."""
        self.attack2_current_steps = 0

        if self.top <= self.permitted_y[0]:
            self.set_speed(0, self.attack2_speed)
        elif self.bottom >= self.permitted_y[1]:
            self.set_speed(0, -self.attack2_speed)
        elif hero_position[1] > self.center[1]:
            self.set_speed(0, self.attack2_speed)
        else:
            self.set_speed(0, -self.attack2_speed)

        self.change_fire_state(True)

    def attack3(self, hero_position):
        """Changes fire state."""
        self.change_fire_state(True)

    def get_bullets_pos(self):
        """Returns bullets start positions for each weapon with offsets."""
        # These nums is offsets from boss positions for each bullet pos
        self.boss_bullets_pos = ([self.x + 8, self.y + 88],
                                 [self.x + 165, self.y + 77],
                                 [self.x + 32, self.y + 165],
                                 [self.x + 118, self.y + 139])
        return self.boss_bullets_pos

    def attack(self, hero_position):
        """Randomly call one of the attacks.

        :param hero_position: hero coordinates
        :type hero_position: list, tuple

        """
        if self.attack_state == 'idle':
            list_attacks = [self.attack1, self.attack2, self.attack3]
            attack = choice(list_attacks)
            self.change_attack_state(attack.__name__)
            attack(hero_position)
            self.time = monotonic()

    def stop_attack(self):
        """Changes all params responsible for shooting and movement to start values."""
        self.change_attack_state()
        self.change_fire_state()
        self.set_speed()
        self.attack2_current_steps = 0

    def set_speed(self, offset_x=0, offset_y=0):
        """Set boss speed to a given offsets for each axis.

        :param offset_x: speed for X axis
        :type offset_x: int
        :param offset_y: speed for Y axis
        :type offset_y: int

        """
        self.speed = (offset_x, offset_y)

    def is_boss_can_move(self):
        """Checks is the boss in the allowed area. Returns True if yes, False if no."""
        if self.left + self.speed[0] > self.permitted_x[0] and \
                self.right + self.speed[0] < self.permitted_x[1] and \
                self.top + self.speed[1] > self.permitted_y[0] and \
                self.bottom + self.speed[1] < self.permitted_y[1]:
            return True
        else:
            return False

    def change_attack_state(self, state='idle'):
        """Changes attack state to a given state.

        :param state: attack state
        :type state: string

        """
        self.attack_state = state

    def change_fire_state(self, state=False):
        """Changes fire state to a given state.

        :param state: attack state
        :type state: bool

        """
        self.is_boss_fire = state
