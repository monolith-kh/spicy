# -*- coding: utf-8 -*-

ARENA_WIDTH = 1900
ARENA_HEIGHT = 1380

SCREEN_SCALING = 1.0
SCREEN_WIDTH = ARENA_WIDTH * SCREEN_SCALING
SCREEN_HEIGHT = ARENA_HEIGHT * SCREEN_SCALING
SCREEN_TITLE = 'Spicy (with RINGGGO)'

SPLASH_TIME = 3.0

PING_ALL_TIME = 10.0

FONT = 'KenVector Future'
FONT_THIN = f'{FONT} Thin'

from .app import ArcadeState, ArcadeWindow, start_arcade, exit_arcade
from .cube import Cube
