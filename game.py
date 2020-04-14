import pygame
import sys

import config as c
from collections import defaultdict


class Game:
    def __init__(self,
                 caption,
                 width,
                 height,
                 back_image_filename,
                 frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        self.enemies = []
        self.bullets = []
        pygame.mixer.init(44100, 16, 2, 4096)
        pygame.init()
        pygame.mixer.music.load(c.music_fight)
        pygame.mixer.music.play(-1)
        self.channel_hero_fire = pygame.mixer.Channel(0)
        self.channel_hero_fire.set_volume(0.5)
        self.channel_enemy_sound = pygame.mixer.Channel(1)
        self.channel_enemy_sound.set_volume(0.3)
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = defaultdict(list)

    def update(self):
        for o in self.objects:
            o.update()

    def blit(self, surface):
        for o in self.objects:
            o.blit(surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers[event.type]:
                    handler(event.type, event.pos)

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.blit(self.surface)

            pygame.display.update()
            self.clock.tick(self.frame_rate)
