import sys
from random import randint
from pathlib import Path

sys.path.append(str(Path().cwd().parent))

import pygame

from serious_pysam import config as c
from serious_pysam.game.game import Game
from serious_pysam.menu.menu import MainMenu
from serious_pysam.game_object.game_object import GameObject
from serious_pysam.text_object.text_object import TextObject
from serious_pysam.game_object.entity.bullet import Bullet
from serious_pysam.game_object.entity.hero import Hero
from serious_pysam.game_object.entity.kamikaze import Kamikaze
from serious_pysam.game_object.entity.ugh_zan import UghZan


class SeriousPySam(Game):
    """Main class for all project. Here's all game logic."""
    def __init__(self):
        """Initialization main game params."""
        Game.__init__(self, c.WINDOW_CAPTION, c.WINDOW_WIDTH, c.WINDOW_HEIGHT, c.GAME_BACKGROUND_IMAGE, c.FRAME_RATE)
        self.score = 0
        self.hero = None
        self.boss = None
        self.pause_menu = None
        self.hero_handle_keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
        self.create_objects()

    def create_objects(self):
        """Creates start game objects."""
        self.create_hero()
        self.create_enemy(c.ENEMY_COUNT)
        self.create_start_labels()

    def create_hero(self):
        """Creates hero, add him to the hero_objects, add key handles."""
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
        self.hero_objects.append(self.hero)

    def create_enemy(self, count=1):
        """Creates a given count enemy, adds each to enemies."""
        enemies = [Kamikaze(randint(c.ENEMY_SPAWN_START_X, c.WINDOW_WIDTH),
                            randint(0, c.ENEMY_SPAWN_END_Y),
                            c.ENEMY_KAMIKAZE_IMAGE,
                            c.ENEMY_SPEED,
                            c.ENEMY_KAMIKAZE_SOUND,
                            self.channel_enemy_sound) for enemy in range(count)]
        for enemy in enemies:
            self.enemies.append(enemy)

    def create_start_labels(self):
        """Creates start labels: hp and score."""
        self.create_label(c.LABEL_HERO_POS[0], c.LABEL_HERO_POS[1], lambda: f'HP: {self.hero.health}')
        self.create_label(c.LABEL_SCORE_POS[0], c.LABEL_SCORE_POS[1], lambda: f'Score: {self.score}')

    def create_label(self, x, y, text, centralized=False):
        """Creates label object and adds to hud_objects."""
        label = TextObject(x,
                           y,
                           text,
                           c.LABEL_TEXT_COLOR,
                           c.LABEL_FONT_NAME,
                           c.LABEL_FONT_SIZE,
                           centralized=centralized)
        self.hud_objects.append(label)

    def resume_game(self):
        """Resumes the game after menu."""
        self.pause_menu.toggle()
        pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
        self.channels_set_volume()
        self.update()

    def finish_game(self):
        """If user in menu exit from game, turn off game music, sets all params to
         start values and call main menu."""
        self.channels_set_volume('mute')
        self.reinitializied_game()
        self.score = 0
        self.create_objects()
        self.create_main_menu()

    def handle_pause_menu(self, key):
        """Handler for Escape button during the game, shows pause menu."""
        if key == pygame.K_ESCAPE:
            pygame.mixer.music.set_volume(c.MUSIC_VOLUME / 4)
            self.channels_set_volume('mute')

            self.pause_menu = MainMenu()
            self.pause_menu.add_button('Продолжить игру', self.resume_game)
            self.pause_menu.add_button('Завершить игру', self.finish_game)
            self.pause_menu.add_button('Выход', self.pause_menu.event_quit)
            self.pause_menu.mainloop(self.surface)

    def handle_bullets(self):
        """Handler for hero bullets."""
        if self.hero.state == 'fire':
            spawn_bullet_x = self.hero.rect.x + self.hero.rect.w - 12
            spawn_bullet_y = self.hero.rect.y + 21
            bullet = Bullet(spawn_bullet_x,
                            spawn_bullet_y,
                            c.BULLET_MINIGUN_IMAGE,
                            c.BULLET_SPEED,
                            c.BULLET_MINIGUN_SOUND,
                            c.HERO_DAMAGE)
            self.objects.append(bullet)
            self.bullets.append(bullet)
            self.channel_hero_fire.play(bullet.sound)

    def garbage_collector(self):
        """If any object is off the screen, garbage collector will kill it."""
        for obj in self.objects:
            if not 0 <= obj.x <= c.WINDOW_WIDTH:
                self.kill_object(obj)
            elif not 0 <= obj.y <= c.WINDOW_HEIGHT:
                self.kill_object(obj)

    def kill_object(self, obj):
        """Remove given object from all collections.

        :param obj: object to delete

        """
        if obj in self.objects:
            self.objects.remove(obj)
        if obj in self.enemies:
            self.enemies.remove(obj)
        if obj in self.bullets:
            self.bullets.remove(obj)
        if obj in self.enemy_bullets:
            self.enemy_bullets.remove(obj)

    def handle_hero_bullets_collisions(self):
        """Handler for hero bullets collisions with enemies."""
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= bullet.damage
                    self.kill_object(bullet)
                    if enemy.health <= 0:
                        self.score += 100
                        self.kill_object(enemy)
                        self.create_enemy()

    def handle_enemy_bullets_collisions(self):
        """Handler for enemy bullets collisions with hero."""
        for bullet in self.enemy_bullets:
            if bullet.rect.colliderect(self.hero.rect):
                self.hero.get_damage(bullet.damage)
                self.kill_object(bullet)

    def handle_enemy_collision(self):
        """Handler for enemy collisions with hero (when they collid)."""
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.hero.rect):
                self.hero.get_damage(enemy.damage)
                if isinstance(enemy, Kamikaze):
                    self.kill_object(enemy)

    def handle_boss_spawn(self):
        """Handler for boss spawn. Checks current score and if it's equal to a certain value, then boss spawn."""
        if not self.is_boss_spawn and self.score >= c.BOSS_SPAWN_SCORE:
            self.is_boss_spawn = True
            self.enemies = []
            self.boss = UghZan(c.BOSS_SPAWN_X,
                               c.BOSS_SPAWN_Y,
                               c.BOSS_IMAGE,
                               c.BOSS_IDLE_SPEED,
                               c.hero_start_level_random_dialog(),
                               self.channel_enemy_sound)
            self.enemies.append(self.boss)

            self.create_label(c.LABEL_BOSS_HP_POS[0],
                              c.LABEL_BOSS_HP_POS[1],
                              lambda: f'Boss: {self.boss.health}')

            pygame.mixer.music.load(c.BOSS_MUSIC)
            pygame.mixer.music.play(-1)

    def handle_boss_attacks(self):
        """Handler for boss attacks. Checks current boss state and do something depending on his state."""
        if self.is_boss_spawn:
            if self.boss.attack_state == 'idle' and self.boss.get_time() % 6 == self.boss.attack_period:
                self.boss.attack([*self.hero.center])

            if self.boss.attack_state == 'attack1':
                if not self.boss.is_boss_can_move() and self.boss.speed[0] < 0:
                    self.boss.set_speed(self.boss.attack1_speed)
                elif not self.boss.is_boss_can_move() and self.boss.speed[0] > 0:
                    self.boss.stop_attack()

            elif self.boss.attack_state == 'attack2' and self.boss.is_boss_fire:
                if self.boss.is_boss_can_move():
                    bullet_num = randint(0, 3)
                    rand_bullet = self.boss.get_bullets_pos()[bullet_num]
                    bullet = Bullet(rand_bullet[0],
                                    rand_bullet[1],
                                    self.boss.boss_bullets_images[bullet_num],
                                    -c.BOSS_BULLET_SPEED,
                                    c.BULLET_MINIGUN_SOUND,
                                    self.boss.bullets_damages[bullet_num])
                    self.enemy_bullets.append(bullet)
                    self.boss.attack2_current_steps += 1
                    if self.boss.attack2_current_steps >= self.boss.attack2_steps:
                        self.boss.stop_attack()
                else:
                    self.boss.stop_attack()

            elif self.boss.attack_state == 'attack3' and self.boss.is_boss_fire:
                hero_pos = self.hero.center

                # Boss has 4 weapons, so he need 4 bullets
                for bullet_num in range(4):
                    bullet_pos = self.boss.get_bullets_pos()[bullet_num]
                    bullet = Bullet(bullet_pos[0],
                                    bullet_pos[1],
                                    self.boss.boss_bullets_images[bullet_num],
                                    -c.BOSS_BULLET_SPEED,
                                    c.BULLET_MINIGUN_SOUND,
                                    self.boss.bullets_damages[bullet_num],
                                    (hero_pos, bullet_pos))
                    self.enemy_bullets.append(bullet)

                self.boss.stop_attack()

    def handle_player_death(self):
        """Handler for player death, ends the game."""
        if self.hero.health <= 0 and self.hero.is_hero_live:
            self.hero.is_hero_live = False
            self.hero.hero_death()
            self.hud_objects.clear()
            self.hero_objects.clear()
            screen_death = GameObject(0, 0, c.SCREEN_DEATH_IMAGE)
            self.hud_objects.append(screen_death)
            self.create_label(c.WINDOW_WIDTH // 2,
                              c.WINDOW_HEIGHT // 2 - 20,
                              lambda: f'Тебя убили. Твои очки: {self.score}',
                              centralized=True)
            self.create_label(c.WINDOW_WIDTH // 2,
                              c.WINDOW_HEIGHT // 2 + 20,
                              lambda: f'ESC - выход в меню',
                              centralized=True)

    def handle_win_game(self):
        """Handler for boss death, ends the game."""
        if self.hero.is_hero_live and self.boss is not None:
            if self.boss.health <= 0:
                self.boss.is_boss_live = False
                self.hud_objects.clear()
                self.enemies.clear()
                screen_death = GameObject(0, 0, c.SCREEN_WIN_IMAGE)
                self.hud_objects.append(screen_death)
                self.create_label(c.WINDOW_WIDTH // 2,
                                  c.WINDOW_HEIGHT // 2 - 20,
                                  lambda: f'Ты победил! Твои очки: {self.score}',
                                  centralized=True)
                self.create_label(c.WINDOW_WIDTH // 2,
                                  c.WINDOW_HEIGHT // 2 + 20,
                                  lambda: f'ESC - выход в меню',
                                  centralized=True)

    def update(self):
        """Extends super class method. Launches handlers, gc, then call super's update."""
        self.handle_bullets()
        self.handle_hero_bullets_collisions()
        self.handle_enemy_bullets_collisions()
        self.handle_boss_spawn()
        self.handle_boss_attacks()
        self.handle_enemy_collision()
        self.garbage_collector()
        self.handle_player_death()
        self.handle_win_game()
        super().update()


def main():
    """Starts the game."""
    SeriousPySam().run()


if __name__ == '__main__':
    main()
