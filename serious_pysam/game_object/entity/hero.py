import pygame
from time import monotonic

import serious_pysam.config as c
from serious_pysam.game_object.game_object import GameObject


class Hero(GameObject):
    """Describes hero behaviour.

    Hero can move in two axises and shoot. He has immortality time, that fires every time,
    when hero get damage. And hero knows about his permitted area on the screen, so doesn't
    go beyond the screen.

    """
    def __init__(self, x, y, picture, speed, sound, channel):
        """Hero has own vars:

        hero_idle - picture when hero idle
        hero_fire - picture when hero open fire
        health - health indicator
        is_hero_life - current life state
        moving_left - current moving left state
        moving_right - current moving right state
        moving_up - current moving up state
        moving_down - current moving down state
        speed - hero speed
        state - current hero state
        permitted_x - permitted area in X axis
        permitted_y - permitted area in Y axis
        immortality_time - in secs, how many seconds hero gain immortality after get damage
        time_get_damage - timer when renew each time when hero get damage

        """
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.hero_idle = self.image_object
        self.hero_fire = pygame.image.load(c.HERO_FIRE_IMAGE).convert_alpha()
        self.health = c.HERO_HP
        self.is_hero_live = True
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.speed = speed
        self.state = 'idle'
        self.permitted_x = c.WINDOW_WIDTH - self.rect.w
        self.permitted_y = c.WINDOW_HEIGHT - self.rect.h - c.HERO_SPEED
        self.immortality_time = c.HERO_IMMORTALITY_TIME
        self.time_get_damage = monotonic()

    # handler for keyboard
    def handle(self, key):
        """Keyboard handler

        :param key: button
        :type key: int

        """
        if self.is_hero_live:
            if key == pygame.K_w:
                self.moving_up = not self.moving_up
            elif key == pygame.K_s:
                self.moving_down = not self.moving_down
            elif key == pygame.K_a:
                self.moving_left = not self.moving_left
            elif key == pygame.K_d:
                self.moving_right = not self.moving_right

    # handler for mouse
    def handle_mouse(self, event_type, pos):
        """Mouse handler.

        :param event_type: mouse button
        :type key: int
        :param pos: coordinates of mouse event
        :type key: pygame.event

        """
        if self.is_hero_live:
            if event_type == pygame.MOUSEBUTTONDOWN:
                self.state = 'fire'
            elif event_type == pygame.MOUSEBUTTONUP:
                self.state = 'idle'

    def get_damage(self, damage):
        """If hero live, health decreases by damage.

        :param damage: damage taken
        :type damage: int

        """
        if self.is_hero_live:
            if monotonic() - self.time_get_damage >= self.immortality_time:
                self.health -= damage
                self.time_get_damage = monotonic()

    def hero_death(self):
        """Changes params below, so hero disappear and stands still."""
        self.is_hero_live = False
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.state = 'idle'
        self.speed = (0, 0)
        self.hero_idle.set_alpha(0)
        self.hero_fire.set_alpha(0)
        self.image_object.set_alpha(0)

    def update(self):
        """Hero can move only in permitted area."""
        dx = dy = 0
        if self.moving_left and self.rect.x > c.HERO_SPEED:
            dx = -self.speed
        if self.moving_right and self.rect.x < self.permitted_x:
            dx = self.speed
        if self.moving_up and self.rect.y > c.HERO_SPEED:
            dy = -self.speed
        if self.moving_down and self.rect.y < self.permitted_y:
            dy = self.speed
        if self.state == 'fire':
            self.image_object = self.hero_fire
        else:
            self.image_object = self.hero_idle

        self.move(dx, dy)
