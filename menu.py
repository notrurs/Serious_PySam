from pygame.mixer import music

from pygame_menu import Menu
from pygame_menu.themes import Theme
from pygame_menu.baseimage import BaseImage
from pygame_menu.baseimage import IMAGE_MODE_SIMPLE
from pygame_menu.widgets import MENUBAR_STYLE_NONE
from pygame_menu.widgets.selection.none import NoneSelection
from pygame_menu.sound import Sound
from pygame_menu.sound import SOUND_TYPE_CLICK_MOUSE
from pygame_menu.sound import SOUND_TYPE_WIDGET_SELECTION
from pygame_menu import events

import config as c


class MainMenu(Menu):
    def __init__(self):
        _base_image = BaseImage(image_path=c.menu_background_image,
                                drawing_mode=IMAGE_MODE_SIMPLE)
        _selection = NoneSelection()
        _theme = Theme(background_color=_base_image,
                       title_shadow=False,
                       title_background_color=c.black_color,
                       title_bar_style=MENUBAR_STYLE_NONE,
                       selection_color=c.menu_selection_color,
                       widget_font=c.font_name,
                       widget_font_color=c.menu_font_color,
                       widget_font_size=c.menu_font_size,
                       widget_selection_effect=_selection
                       )
        Menu.__init__(self,
                      c.screen_height,
                      c.screen_width,
                      c.menu_title,
                      mouse_motion_selection=True,
                      theme=_theme,
                      center_content=True)
        self.event_quit = events.EXIT
        self.event_back = events.BACK
        _menu_sound = MenuSound()
        self.set_sound(_menu_sound, recursive=True)


class MenuSound(Sound):
    def __init__(self):
        Sound.__init__(self)
        self.set_sound(SOUND_TYPE_CLICK_MOUSE, c.menu_sound_click, volume=1)
        self.set_sound(SOUND_TYPE_WIDGET_SELECTION, c.menu_sound_select, volume=1)
