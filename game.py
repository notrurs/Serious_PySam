import pygame
import sys
from collections import defaultdict
from pygame_menu.locals import ALIGN_CENTER

import config as c
from menu import MainMenu


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
        self.is_boss_spawn = False
        self.objects = []
        self.enemies = []
        self.bullets = []
        self.hud_objects = []
        self.hero_objects = []
        pygame.mixer.init(44100, 16, 2, 4096)
        pygame.init()
        self.channel_hero_fire = pygame.mixer.Channel(0)
        self.channel_hero_fire.set_volume(c.HERO_FIRE_VOLUME)
        self.channel_hero_dialog = pygame.mixer.Channel(1)
        self.channel_hero_dialog.set_volume(c.HERO_DIALOG_VOLUME)
        self.channel_enemy_sound = pygame.mixer.Channel(2)
        self.channel_enemy_sound.set_volume(c.ENEMY_SOUND_VOLUME)
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = defaultdict(list)

    def reinitializied_game(self):
        self.is_boss_spawn = False
        self.objects = []
        self.enemies = []
        self.bullets = []
        self.hud_objects = []
        self.hero_objects = []
        self.channel_hero_fire = pygame.mixer.Channel(0)
        self.channel_hero_dialog = pygame.mixer.Channel(1)
        self.channel_enemy_sound = pygame.mixer.Channel(2)
        self.channels_set_volume()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = defaultdict(list)

    def channels_set_volume(self, volume='default'):
        if volume == 'default':
            self.channel_hero_fire.set_volume(c.HERO_FIRE_VOLUME)
            self.channel_hero_dialog.set_volume(c.HERO_DIALOG_VOLUME)
            self.channel_enemy_sound.set_volume(c.ENEMY_SOUND_VOLUME)
        elif volume == 'mute':
            self.channel_hero_fire.set_volume(0)
            self.channel_hero_dialog.set_volume(0)
            self.channel_enemy_sound.set_volume(0)

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

    def start_game(self):
        pygame.mixer.music.load(c.MUSIC_FIGHT)
        pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

        hero_start_sound = pygame.mixer.Sound(c.hero_start_level_random_dialog())
        self.channel_hero_dialog.play(hero_start_sound)

        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))
            self.objects = [*self.enemies, *self.bullets, *self.hero_objects, *self.hud_objects]

            self.handle_events()
            self.update()
            self.blit(self.surface)

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def create_main_menu(self):
        pygame.mixer.music.load(c.MENU_MUSIC)
        pygame.mixer.music.set_volume(c.MENU_MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

        menu_control = MainMenu()
        menu_control.add_label(c.MENU_CONTROL_LABEL, align=ALIGN_CENTER, font_size=30,  margin=(0, 100))
        menu_control.add_button('Назад', menu_control.event_back)

        menu = MainMenu()
        menu.add_button('Новая игра', self.start_game)
        menu.add_button('Управление', menu_control)
        menu.add_button('Выход', menu.event_quit)

        menu.mainloop(self.surface)

    def background_function(self):
        bg_img = pygame.image.load(c.MENU_BACKGROUND_IMAGE)
        self.surface.blit(bg_img, (0, 0))

    def run(self):
        self.create_main_menu()
