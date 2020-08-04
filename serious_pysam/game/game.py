import pygame
import sys
from collections import defaultdict
from pygame_menu.locals import ALIGN_CENTER

from serious_pysam import config as c
from serious_pysam.menu.menu import MainMenu


class Game:
    """Main super class for Game object."""
    def __init__(self,
                 caption,
                 width,
                 height,
                 back_image_filename,
                 frame_rate):
        """Game has own vars:
        background_image - picture for background on the screen
        frame_rate - pfs of the game
        game_over - current state of game over
        is_boss_spawn - current state boss spawn
        objects - contains all game objects
        enemies - contains only enemies objects
        bullets - contains only bullets objects
        enemy_bullets - contains only enemy_bullets objects
        hud_objects - contains only hud_objects objects
        hero_objects - contains only hero_objects objects
        channel_hero_fire - sound channel for hero shooting
        channel_hero_dialog - sound channel for hero dialog
        channel_enemy_sound - sound channel for enemy sound
        surface - screen object
        keydown_handlers - dict with all button down handlers for keyboard buttons
        keyup_handlers - dict with all button up handlers for keyboard buttons
        mouse_handlers - dict with all handlers for mouse buttons

        """
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.is_boss_spawn = False
        self.objects = []
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
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
        """Sets params below to start values."""
        self.is_boss_spawn = False
        self.objects = []
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
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
        """Sets game volume.

        :param volume: volume level
        :type volume: str

        """
        if volume == 'default':
            self.channel_hero_fire.set_volume(c.HERO_FIRE_VOLUME)
            self.channel_hero_dialog.set_volume(c.HERO_DIALOG_VOLUME)
            self.channel_enemy_sound.set_volume(c.ENEMY_SOUND_VOLUME)
        elif volume == 'mute':
            self.channel_hero_fire.set_volume(0)
            self.channel_hero_dialog.set_volume(0)
            self.channel_enemy_sound.set_volume(0)

    def update(self):
        """Updates all objects on the screen."""
        for o in self.objects:
            o.update()

    def blit(self, surface):
        """Blits all objects on the screen."""
        for o in self.objects:
            o.blit(surface)

    def handle_events(self):
        """Handler for game events."""
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
        """Starts game. Turn ob music, blits and updates all objects, set fps and
        checks handlers."""
        pygame.mixer.music.load(c.MUSIC_FIGHT)
        pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

        hero_start_sound = pygame.mixer.Sound(c.hero_start_level_random_dialog())
        self.channel_hero_dialog.play(hero_start_sound)

        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))
            self.objects = [*self.enemies, *self.bullets, *self.enemy_bullets, *self.hero_objects, *self.hud_objects]

            self.handle_events()
            self.update()
            self.blit(self.surface)

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def create_main_menu(self):
        """Starts main menu and turn on menu music."""
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
        """Blits background for menu."""
        bg_img = pygame.image.load(c.MENU_BACKGROUND_IMAGE)
        self.surface.blit(bg_img, (0, 0))

    def run(self):
        """Runs game."""
        self.create_main_menu()
