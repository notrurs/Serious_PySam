from pathlib import Path
from random import choice

import colors


# Paths settings
BASE_DIR = Path.cwd()
FONTS_DIR = BASE_DIR / 'fonts'
IMAGES_DIR = BASE_DIR / 'images'
SOUND_EFFECTS_DIR = BASE_DIR / 'sound_effects'
ENEMIES_DIR = SOUND_EFFECTS_DIR / 'enemies'
HERO_DIR = SOUND_EFFECTS_DIR / 'hero'
MUSIC_DIR = SOUND_EFFECTS_DIR / 'music'
OTHER_DIR = SOUND_EFFECTS_DIR / 'other'
WEAPONS_DIR = SOUND_EFFECTS_DIR / 'weapons'

# General settings
screen_width = 800
screen_height = 533
window_caption = 'Serious PySam'
background_image = str(IMAGES_DIR / 'desert.png')
frame_rate = 60
music_fight = str(MUSIC_DIR / 'dunes_bfe.mp3')
music_volume = 0.6

# Menu settings
menu_height = 800
menu_width = 533
menu_title = ''
menu_background_image = str(IMAGES_DIR / 'bg_mainmenu.png')
menu_font_color = colors.GREEN2
menu_selection_color = colors.WHITE
menu_title_font_color = colors.GREEN2
menu_title_background_color = colors.GREEN3
menu_background_color = colors.GREEN4
menu_sound_click = str(OTHER_DIR / 'press.wav')
menu_sound_select = str(OTHER_DIR / 'select.wav')
menu_font_size = 49
menu_music = str(MUSIC_DIR / 'HPeace.mp3')
menu_music_volume = 0.3

# Hero settings
hero_speed = 5
hero_fire_image = str(IMAGES_DIR / 'hero_fire.png')
hero_idle_image = str(IMAGES_DIR / 'hero_idle.png')
hero_fire_volume = 0.4
hero_dialog_volume = 1
hero_start_level_dialogs = ['i_am_ready_for_some_serious_carnage.wav',
                            'sam_i_am.wav',
                            'say_hello_to_papa.wav',
                            'seriously_is_that_the_best_you_can_do.wav']
hero_start_level_random_dialog = str(HERO_DIR / choice(hero_start_level_dialogs))

# Bullet settings
bullet_speed = 10
bullet_minigun_image = str(IMAGES_DIR / 'bullet_minigun.png')
bullet_minigun_sound = str(WEAPONS_DIR / 'minigun.wav')

# Enemy settings
enemy_speed = 3
enemy_count = 10
enemy_kamikaze_image = str(IMAGES_DIR / 'kamikaze.png')
enemy_kamikaze_sound = str(ENEMIES_DIR / 'kamikaze.wav')
enemy_sound_volume = 0.3
enemy_spawn_start_x = 710
enemy_spawn_end_y = screen_height - 45  # enemy rect height

# Label settings
text_color = colors.YELLOW1
font_name = str(FONTS_DIR / 'boink.ttf')
font_size = 25
score_x = screen_width // 3
score_y = 0

# Other
black_color = colors.BLACK
menu_control_label = '''Управление клавишами WASD, стрелять на ЛКМ.'''
