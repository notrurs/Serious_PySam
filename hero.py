import pygame

import config as c
from game_object import GameObject


class Hero(GameObject):
    def __init__(self, x, y, picture, speed, sound, channel):
        GameObject.__init__(self, x, y, picture, speed, sound, channel)
        self.hero_idle = self.image_object
        self.hero_fire = pygame.image.load(c.hero_fire_image).convert_alpha()
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.speed = speed
        self.state = 'idle'
        self.permitted_x = c.screen_width - self.rect.w
        self.permitted_y = c.screen_height - self.rect.h - c.hero_speed

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
        if self.moving_left and self.rect.x > c.hero_speed:
            dx = -self.speed
        if self.moving_right and self.rect.x < self.permitted_x:
            dx = self.speed
        if self.moving_up and self.rect.y > c.hero_speed:
            dy = -self.speed
        if self.moving_down and self.rect.y < self.permitted_y:
            dy = self.speed
        if self.state == 'fire':
            self.image_object = self.hero_fire
        else:
            self.image_object = self.hero_idle

        self.move(dx, dy)
