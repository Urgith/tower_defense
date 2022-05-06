from pygame.display import set_mode as pygame_display_set_mode
from pygame.display import update as pygame_display_update

from pygame.rect import Rect as pygame_Rect

from pygame.draw import rect as pygame_draw_rect
from pygame.draw import circle as pygame_draw_circle

from pygame.image import load as pygame_image_load
from pygame.transform import scale as pygame_transform_scale

from pygame.font import init as pygame_font_init
from pygame.font import SysFont as pygame_font_SysFont

from pygame.time import get_ticks as pygame_time_get_ticks
from pygame.time import Clock as pygame_time_Clock

from pygame.mouse import get_pos as pygame_mouse_get_pos
from pygame.event import get as pygame_event_get
from pygame.key import get_pressed as pygame_key_get_pressed

from pygame.locals import K_1, K_2, K_3, K_w, K_a, K_s, K_d, K_p, \
    K_SPACE, K_ESCAPE, QUIT, KEYDOWN, MOUSEBUTTONUP, FULLSCREEN

from random import random


def image_load(name, location=None, scale=None):
    image = pygame_image_load(name).convert()

    if location is not None: 
        image.set_colorkey(image.get_at(location))

    if scale is not None:
        image = pygame_transform_scale(image, scale)

    return image


def exit():
    import sys

    sys.exit()
