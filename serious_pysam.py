import pygame
from random import randint

import config as c
from game import Game
from hero import Hero
from kamikaze import Kamikaze
from bullet import Bullet
from text_object import TextObject


class SeriousPySam(Game):
    def __init__(self):
        Game.__init__(self, c.window_caption, c.screen_width, c.screen_height, c.background_image, c.frame_rate)
        self.score = 0
        self.is_game_running = False
        self.hero = None
        self.create_objects()

    def create_objects(self):
        self.create_hero()
        self.create_enemy(c.enemy_count)
        self.create_labels()
        self.create_menu()

    def create_hero(self):
        hero = Hero(c.screen_width // 5,
                    c.screen_height // 2,
                    c.hero_idle_image,
                    c.hero_speed)

        self.keydown_handlers[pygame.K_w].append(hero.handle)
        self.keydown_handlers[pygame.K_s].append(hero.handle)
        self.keydown_handlers[pygame.K_a].append(hero.handle)
        self.keydown_handlers[pygame.K_d].append(hero.handle)
        self.mouse_handlers[pygame.MOUSEBUTTONDOWN].append(hero.handle_mouse)

        self.keyup_handlers[pygame.K_w].append(hero.handle)
        self.keyup_handlers[pygame.K_s].append(hero.handle)
        self.keyup_handlers[pygame.K_a].append(hero.handle)
        self.keyup_handlers[pygame.K_d].append(hero.handle)
        self.mouse_handlers[pygame.MOUSEBUTTONUP].append(hero.handle_mouse)

        self.hero = hero
        self.objects.append(self.hero)

    def create_enemy(self, count):
        enemies = [Kamikaze(randint(710, c.screen_width),
                            randint(0, c.screen_height - 45),
                            c.enemy_kamikaze_image,
                            c.enemy_speed,
                            c.enemy_kamikaze_sound,
                            self.channel_enemy_sound) for enemy in range(count)]
        for enemy in enemies:
            self.objects.append(enemy)
            self.enemies.append(enemy)

    def create_labels(self):
        score_label = TextObject(c.score_x,
                                 c.score_y,
                                 lambda: f'Score: {self.score}',
                                 c.text_color,
                                 c.font_name,
                                 c.font_size)
        self.objects.append(score_label)

    def create_menu(self):
        pass

    def handle_bullets(self):
        if self.hero.state == 'fire':
            spawn_bullet_x = self.hero.rect.x + self.hero.rect.w - 12
            spawn_bullet_y = self.hero.rect.y + 21
            bullet = Bullet(spawn_bullet_x,
                            spawn_bullet_y,
                            c.bullet_minigun_image,
                            c.bullet_speed,
                            c.bullet_minigun_sound)
            self.objects.append(bullet)
            self.bullets.append(bullet)
            self.channel_hero_fire.play(bullet.sound)

    def garbage_collector(self):
        for obj in self.objects:
            if not 0 <= obj.x <= c.screen_width:
                self.kill_object(obj)
            elif not 0 <= obj.y <= c.screen_height:
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
                    self.create_enemy(1)

    def update(self):
        # if not self.is_game_running:
        #     return
        self.handle_bullets()
        self.handle_bullets_collisions()
        self.garbage_collector()
        super().update()


def main():
    SeriousPySam().run()


if __name__ == '__main__':
    main()
