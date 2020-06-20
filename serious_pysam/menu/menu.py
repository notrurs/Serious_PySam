from pygame.mixer import Channel
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

import serious_pysam.config as c


class MainMenu(Menu):
    def __init__(self):
        _base_image = BaseImage(image_path=c.MENU_BACKGROUND_IMAGE,
                                drawing_mode=IMAGE_MODE_SIMPLE)
        _selection = NoneSelection()
        _theme = Theme(background_color=_base_image,
                       title_shadow=False,
                       title_background_color=c.BLACK_COLOR,
                       title_bar_style=MENUBAR_STYLE_NONE,
                       selection_color=c.MENU_SELECTION_COLOR,
                       widget_font=c.LABEL_FONT_NAME,
                       widget_font_color=c.MENU_FONT_COLOR,
                       widget_font_size=c.MENU_FONT_SIZE,
                       widget_selection_effect=_selection
                       )
        Menu.__init__(self,
                      c.WINDOW_HEIGHT,
                      c.WINDOW_WIDTH,
                      c.MENU_TITLE,
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
        self._channel = Channel(3)
        self.set_sound(SOUND_TYPE_CLICK_MOUSE, c.MENU_SOUND_CLICK, volume=1.0)
        self.set_sound(SOUND_TYPE_WIDGET_SELECTION, c.MENU_SOUND_SELECT, volume=1.0)
