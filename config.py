import colors

# General settings
screen_width = 800
screen_height = 533
window_caption = 'Serious PySam'
background_image = 'images/desert.png'
frame_rate = 60
music_fight = 'sound_effects/music/dunes_bfe.mp3'
music_volume = 0.6

# Menu settings
menu_height = 800
menu_width = 533
menu_title = ''
menu_background_image = 'images/bg_mainmenu.png'
menu_font_color = colors.GREEN2
menu_selection_color = colors.WHITE
menu_title_font_color = colors.GREEN2
menu_title_background_color = colors.GREEN3
menu_background_color = colors.GREEN4
menu_sound_click = 'sound_effects/other/press.wav'
menu_sound_select = 'sound_effects/other/select.wav'
menu_font_size = 49
menu_music = 'sound_effects/music/HPeace.mp3'
menu_music_volume = 0.3

# Hero settings
hero_speed = 5
hero_fire_image = 'images/hero_fire.png'
hero_idle_image = 'images/hero_idle.png'
hero_fire_volume = 0.4

# Bullet settings
bullet_speed = 10
bullet_minigun_image = 'images/bullet_minigun.png'
bullet_minigun_sound = 'sound_effects/weapons/minigun.wav'

# Enemy settings
enemy_speed = 3
enemy_count = 10
enemy_kamikaze_image = 'images/kamikaze.png'
enemy_kamikaze_sound = 'sound_effects/enemies/kamikaze.wav'
enemy_sound_volume = 0.3
enemy_spawn_start_x = 710
enemy_spawn_end_y = screen_height - 45  # enemy rect height

# Label settings
text_color = colors.YELLOW1
font_name = 'fonts/boink.ttf'
font_size = 25
score_x = screen_width // 3
score_y = 0

# Other
black_color = colors.BLACK
menu_control_label = '''Управление клавишами WASD, стрелять на ЛКМ.'''
