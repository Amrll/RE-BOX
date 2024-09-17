"""
This module initializes the display and creates dictionaries of resources.
Also contained are various constants used throughout the program.
"""

import os
import pygame as pg

from . import tools

pg.init()

SCREEN_SIZE = (1920, 1080)
ORIGINAL_CAPTION = "ReBox"
COLOR_KEY = (255, 0, 255)
BACKGROUND_COLOR = (30, 40, 50)
SCREEN_RECT = pg.Rect((0,0), SCREEN_SIZE)
_FONT_PATH = os.path.join("assets", "fonts","Fixedsys500c.ttf")
BIG_FONT = pg.font.Font(_FONT_PATH, 100)

# Initialize the display with the screen size
pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption(ORIGINAL_CAPTION)

# General constants
PLAYER_HEALTH = 3

DIRECTIONS = ["left", "middle", "right"]


# Resource loading (Fonts and music just contain path names).
SAVE_PATH = os.path.join("assets", "save_data", "save_data.dat")
FONTS = tools.load_all_fonts(os.path.join("assets", "fonts"))
MUSIC = tools.load_all_music(os.path.join("assets", "music"))
SFX = tools.load_all_sfx(os.path.join("assets", "sound"))


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("assets", "graphics")
    GFX = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        GFX[directory] = tools.load_all_gfx(path)
    return GFX


_SUB_DIRECTORIES = ["enemies", "misc", "backgrounds"]
GFX = graphics_from_directories(_SUB_DIRECTORIES)