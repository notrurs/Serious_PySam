from pygame import image
from pygame.mixer import Sound


class GameObject:
    """A super class for hero, enemies, boss and bullets.

    Any subclasses has methods below:
    blit()
    move()
    play_sound()
    update()

    """
    def __init__(self, x, y, picture, speed=(0, 0), sound=None, channel=None):
        """
        :param x: Position on x coordinate
        :type x: int
        :param y: Position on y coordinate
        :type y: int
        :param picture: Object picture on screen
        :type picture: string path to picture
        :param speed: Object move speed on the screen
        :type speed: tuple
        :param sound: Object soundtrack (e.g. kamikaze scream)
        :type sound: pygame.mixer.Sound
        :param channel: Channel for object sound
        :type channel: pygame.mixer.Channel

        """
        self.image_object = image.load(picture).convert_alpha()
        self.rect = self.image_object.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        if sound is not None:
            self.sound = Sound(sound)
            self.channel = channel

    # There are some properties below which uses one-two times and don't need to store them in memory
    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def width(self):
        return self.rect.w

    @property
    def height(self):
        return self.rect.h

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def center(self):
        return self.rect.center

    def blit(self, surface):
        """Blits object on the screen.

        :param surface: Surface on the screen
        :type surface: pygame.Surface

        """
        surface.blit(self.image_object, (self.rect.x, self.rect.y))

    def move(self, dx, dy):
        """Calls rect method move() with dx and dy params.

        :param dx: x offset value
        :param dy: y offset value

        """
        self.rect = self.rect.move(dx, dy)

    def play_sound(self):
        """Play object sound"""
        if self.channel is not None:
            self.channel.queue(self.sound)

    def update(self):
        """Calls method move"""
        if self.speed == [0, 0]:
            return
        self.move(*self.speed)
