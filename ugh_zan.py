from time import monotonic
from random import choice

from game_object import GameObject
from config import BOSS_PERMITTED_POSITION_X
from config import BOSS_PERMITTED_POSITION_Y
from config import BOSS_ATTACK_SPEED
from config import BOSS_ATTACK_PERIOD
from config import BOSS_BULLET_SPEED
from config import BOSS_ATTACK2_SPEED
from config import BOSS_ATTACK2_STEPS


class UghZan(GameObject):
    def __init__(self, x, y, picture, speed, sound, channel):
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.speed = (speed, 0)
        self.time = monotonic()
        self.attack_period = BOSS_ATTACK_PERIOD
        self.attack_state = 'idle'
        self.is_boss_fire = False
        self.permitted_x = BOSS_PERMITTED_POSITION_X
        self.permitted_y = BOSS_PERMITTED_POSITION_Y
        self.bullet_speed = BOSS_BULLET_SPEED
        self.attack1_speed = BOSS_ATTACK_SPEED
        self.attack2_speed = BOSS_ATTACK2_SPEED
        self.attack2_steps = BOSS_ATTACK2_STEPS
        self.attack2_current_steps = 0

    def get_time(self):
        return int(monotonic() - self.time)

    def attack1(self, hero_position):
        self.set_speed(-self.attack1_speed)

    def attack2(self, hero_position):
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
        self.change_fire_state(True)

    def attack(self, hero_position):
        if self.attack_state == 'idle':
            list_attacks = [self.attack1, self.attack2, self.attack3]
            attack = choice(list_attacks)
            self.change_attack_state(attack.__name__)
            attack(hero_position)
            self.time = monotonic()

    def stop_attack(self):
        self.change_attack_state()
        self.change_fire_state()
        self.attack2_current_steps = 0

    def set_speed(self, offset_x=0, offset_y=0):
        self.speed = (offset_x, offset_y)

    def is_boss_can_move(self):
        if self.left + self.speed[0] > self.permitted_x[0] and \
                self.right + self.speed[0] < self.permitted_x[1] and \
                self.top + self.speed[1] > self.permitted_y[0] and \
                self.bottom + self.speed[1] < self.permitted_y[1]:
            return True
        else:
            return False

    def change_attack_state(self, state='idle'):
        self.attack_state = state

    def change_fire_state(self, state=False):
        self.is_boss_fire = state
