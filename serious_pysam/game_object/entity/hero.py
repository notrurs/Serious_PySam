import pygame

import serious_pysam.config as c
from serious_pysam.game_object.game_object import GameObject


class Hero(GameObject):
    def __init__(self, x, y, picture, speed, sound, channel):
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.hero_idle = self.image_object
        self.hero_fire = pygame.image.load(c.HERO_FIRE_IMAGE).convert_alpha()
        self.health = c.HERO_HP
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.speed = speed
        self.state = 'idle'
        self.permitted_x = c.WINDOW_WIDTH - self.rect.w
        self.permitted_y = c.WINDOW_HEIGHT - self.rect.h - c.HERO_SPEED

    # handler for keyboard
    def handle(self, key):
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
        if event_type == pygame.MOUSEBUTTONDOWN:
            self.state = 'fire'
        elif event_type == pygame.MOUSEBUTTONUP:
            self.state = 'idle'

    def update(self):
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
