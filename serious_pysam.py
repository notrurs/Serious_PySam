import pygame
from random import randint

import config as c
from game import Game
from hero import Hero
from kamikaze import Kamikaze
from bullet import Bullet
from text_object import TextObject
from menu import MainMenu


class SeriousPySam(Game):
    def __init__(self):
        Game.__init__(self, c.WINDOW_CAPTION, c.WINDOW_WIDTH, c.WINDOW_HEIGHT, c.GAME_BACKGROUND_IMAGE, c.FRAME_RATE)
        self.score = 0
        self.hero = None
        self.pause_menu = None
        self.hero_handle_keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
        self.create_objects()

    def create_objects(self):
        self.create_hero()
        self.create_enemy(c.ENEMY_COUNT)
        self.create_labels()

    def create_hero(self):
        hero = Hero(c.WINDOW_WIDTH // 5,
                    c.WINDOW_HEIGHT // 2,
                    c.HERO_IDLE_IMAGE,
                    c.HERO_SPEED,
                    c.hero_start_level_random_dialog(),
                    self.channel_hero_dialog)

        for key in self.hero_handle_keys:
            self.keydown_handlers[key].append(hero.handle)
            self.keyup_handlers[key].append(hero.handle)

        self.keydown_handlers[pygame.K_ESCAPE].append(self.handle_pause_menu)
        self.mouse_handlers[pygame.MOUSEBUTTONDOWN].append(hero.handle_mouse)

        self.keyup_handlers[pygame.K_ESCAPE].append(self.handle_pause_menu)
        self.mouse_handlers[pygame.MOUSEBUTTONUP].append(hero.handle_mouse)

        self.hero = hero
        self.objects.append(self.hero)

    def create_enemy(self, count=1):
        enemies = [Kamikaze(randint(c.ENEMY_SPAWN_START_X, c.WINDOW_WIDTH),
                            randint(0, c.ENEMY_SPAWN_END_Y),
                            c.ENEMY_KAMIKAZE_IMAGE,
                            c.ENEMY_SPEED,
                            c.ENEMY_KAMIKAZE_SOUND,
                            self.channel_enemy_sound) for enemy in range(count)]
        for enemy in enemies:
            self.objects.append(enemy)
            self.enemies.append(enemy)

    def create_labels(self):
        score_label = TextObject(c.LABEL_SCORE_X,
                                 c.LABEL_SCORE_Y,
                                 lambda: f'Score: {self.score}',
                                 c.LABEL_TEXT_COLOR,
                                 c.LABEL_FONT_NAME,
                                 c.LABEL_FONT_SIZE)
        self.objects.append(score_label)

    def resume_game(self):
        self.pause_menu.toggle()
        pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
        self.channels_set_volume()
        self.update()

    def finish_game(self):
        self.channels_set_volume('mute')
        self.reinitializied_game()
        self.score = 0
        self.create_objects()
        self.create_main_menu()

    def handle_pause_menu(self, key):
        if key == pygame.K_ESCAPE:
            pygame.mixer.music.set_volume(c.MUSIC_VOLUME / 4)
            self.channels_set_volume('mute')

            self.pause_menu = MainMenu()
            self.pause_menu.add_button('Продолжить игру', self.resume_game)
            self.pause_menu.add_button('Завершить игру', self.finish_game)
            self.pause_menu.add_button('Выход', self.pause_menu.event_quit)
            self.pause_menu.mainloop(self.surface)

    def handle_bullets(self):
        if self.hero.state == 'fire':
            spawn_bullet_x = self.hero.rect.x + self.hero.rect.w - 12
            spawn_bullet_y = self.hero.rect.y + 21
            bullet = Bullet(spawn_bullet_x,
                            spawn_bullet_y,
                            c.BULLET_MINIGUN_IMAGE,
                            c.BULLET_SPEED,
                            c.BULLET_MINIGUN_SOUND)
            self.objects.append(bullet)
            self.bullets.append(bullet)
            self.channel_hero_fire.play(bullet.sound)

    def garbage_collector(self):
        for obj in self.objects:
            if not 0 <= obj.x <= c.WINDOW_WIDTH:
                self.kill_object(obj)
            elif not 0 <= obj.y <= c.WINDOW_HEIGHT:
                self.kill_object(obj)

    def kill_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
        if obj in self.enemies:
            self.enemies.remove(obj)
        if obj in self.bullets:
            self.bullets.remove(obj)

    def handle_bullets_collisions(self):
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.score += 100
                    self.kill_object(bullet)
                    self.kill_object(enemy)
                    self.create_enemy()

    def update(self):
        self.handle_bullets()
        self.handle_bullets_collisions()
        self.garbage_collector()
        super().update()


def main():
    SeriousPySam().run()


if __name__ == '__main__':
    main()
