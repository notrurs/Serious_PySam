from pathlib import Path
from random import choice

from serious_pysam import colors

# Paths settings
_BASE_DIR = Path.cwd()
_RESOURCES_DIR = _BASE_DIR / 'resources'
_FONTS_DIR = _RESOURCES_DIR / 'fonts'
_IMAGES_DIR = _RESOURCES_DIR / 'images'
_SOUND_EFFECTS_DIR = _RESOURCES_DIR / 'sound_effects'
_ENEMIES_DIR = _SOUND_EFFECTS_DIR / 'enemies'
_HERO_DIR = _SOUND_EFFECTS_DIR / 'hero'
_MUSIC_DIR = _SOUND_EFFECTS_DIR / 'music'
_OTHER_DIR = _SOUND_EFFECTS_DIR / 'other'
_WEAPONS_DIR = _SOUND_EFFECTS_DIR / 'weapons'

# General settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 533
WINDOW_CAPTION = 'Serious PySam'
GAME_BACKGROUND_IMAGE = str(_IMAGES_DIR / 'desert.png')
FRAME_RATE = 60
MUSIC_FIGHT = str(_MUSIC_DIR / 'dunes_bfe.mp3')
MUSIC_VOLUME = 0.6

# Menu settings
MENU_HEIGHT = WINDOW_HEIGHT
MENU_WIDTH = WINDOW_WIDTH
MENU_TITLE = ''
MENU_BACKGROUND_IMAGE = str(_IMAGES_DIR / 'bg_mainmenu.png')
MENU_FONT_COLOR = colors.GREEN2
MENU_SELECTION_COLOR = colors.WHITE
MENU_TITLE_FONT_COLOR = colors.GREEN2
MENU_TITLE_BACKGROUND_COLOR = colors.GREEN3
MENU_BACKGROUND_COLOR = colors.GREEN4
MENU_SOUND_CLICK = str(_OTHER_DIR / 'press.wav')
MENU_SOUND_SELECT = str(_OTHER_DIR / 'select.wav')
MENU_FONT_SIZE = 49
MENU_MUSIC = str(_MUSIC_DIR / 'HPeace.mp3')
MENU_MUSIC_VOLUME = 0.3
MENU_CONTROL_LABEL = '''Управление клавишами WASD, стрелять на ЛКМ.'''

# Hero settings
HERO_SPEED = 5
HERO_FIRE_IMAGE = str(_IMAGES_DIR / 'hero_fire.png')
HERO_IDLE_IMAGE = str(_IMAGES_DIR / 'hero_idle.png')
HERO_DAMAGE = 15
HERO_FIRE_VOLUME = 0.4
HERO_DIALOG_VOLUME = 1.0
HERO_START_LEVEL_DIALOGS = ['i_am_ready_for_some_serious_carnage.wav',
                            'sam_i_am.wav',
                            'say_hello_to_papa.wav',
                            'seriously_is_that_the_best_you_can_do.wav',
                            'cmon_you_ugly_freaks.wav',
                            'come_on_play_with_me_now.wav']


def hero_start_level_random_dialog():
    return str(_HERO_DIR / choice(HERO_START_LEVEL_DIALOGS))


# Bullet settings
BULLET_SPEED = 10
BULLET_MINIGUN_IMAGE = str(_IMAGES_DIR / 'bullet_minigun.png')
BULLET_MINIGUN_SOUND = str(_WEAPONS_DIR / 'minigun.wav')

# Enemy settings
ENEMY_SPEED = 1
ENEMY_COUNT = 10
ENEMY_KAMIKAZE_IMAGE = str(_IMAGES_DIR / 'kamikaze.png')
ENEMY_KAMIKAZE_SOUND = str(_ENEMIES_DIR / 'kamikaze.wav')
ENEMY_SOUND_VOLUME = 0.3
ENEMY_SPAWN_START_X = 710
ENEMY_SPAWN_END_Y = WINDOW_HEIGHT - 45  # 45 is enemy rect height
ENEMY_KAMIKAZE_HP = 15
ENEMY_KAMIKAZE_DAMAGE = 20

# Boss settings
BOSS_MUSIC = str(_MUSIC_DIR / 'LastFight.ogg')
BOSS_SPAWN_X = WINDOW_WIDTH - 250  # 250 is boss rect width
BOSS_SPAWN_Y = WINDOW_HEIGHT // 4
BOSS_HP = 10000
BOSS_IDLE_SPEED = 0
BOSS_ATTACK_PERIOD = 5
BOSS_END_X_ATTACK = 50
BOSS_IMAGE = str(_IMAGES_DIR / 'ugh-zan.png')
BOSS_SOUND = str(_ENEMIES_DIR / 'kamikaze.wav')
BOSS_VOLUME = 0.3
BOSS_BULLET_SPEED = 10
BOSS_ATTACK1_SPEED = 20
BOSS_ATTACK1_PERMITTED_X = (30, WINDOW_WIDTH - 30)
BOSS_ATTACK2_SPEED = 10
BOSS_ATTACK2_STEPS = 15
BOSS_PERMITTED_POSITION_X = (20, WINDOW_WIDTH - 20)
BOSS_PERMITTED_POSITION_Y = (20, WINDOW_HEIGHT - 20)
BOSS_BULLET_IMAGES = [str(_IMAGES_DIR / 'bullet_electrogun.png'),
                      str(_IMAGES_DIR / 'bullet_rocket.png'),
                      str(_IMAGES_DIR / 'bullet_laser.png'),
                      str(_IMAGES_DIR / 'bullet_lavaball.png')]

# Label settings
LABEL_TEXT_COLOR = colors.YELLOW1
LABEL_FONT_NAME = str(_FONTS_DIR / 'boink.ttf')
LABEL_FONT_SIZE = 25
LABEL_SCORE_POS = (WINDOW_WIDTH // 3, 0)
LABEL_BOSS_HP_POS = (WINDOW_WIDTH - 200, 0)
LABEL_HERO_POS = (0, 0)

# Other
BLACK_COLOR = colors.BLACK
