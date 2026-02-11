# Alpha V4.2
from __future__ import print_function  # For compatibility with python 2.x
import pickle
import random
from math import floor
import pygame
from data import pyganim
from data import gameui
from data import splashscreen
import json
from pygame.locals import *

from arena.data_loader import (
    animations,
    dialogues,
    item_data,
    item_data_shop,
    monster_data,
    sequences,
    skills,
    sound_effects,
    weapons,
)
from arena.player import Player
from arena.battle import SideBattle, NewBattle
from arena.ui import MainUi, SelectOptions, Shop
from arena.events import GameEvents, GameClock, run_game
from arena.utils import Timer, fadein, fadeout
import arena.utils as arena_utils
import arena.state as state

icon = pygame.image.load("data/sprites/Icon2.png")
pygame.display.set_icon(icon)
alphatext = "Alpha v4.2 - Story and the Town"


if __name__ == "__main__":
    pygame.init()
    screen_width = 1280
    screen_height = 720
    is_fullscreen = False
    if not is_fullscreen:
        state.screen = pygame.display.set_mode(
            [screen_width, screen_height], pygame.HWACCEL
        )
    else:
        state.screen = pygame.display.set_mode(
            [screen_width, screen_height], pygame.FULLSCREEN
        )

    arena_utils.screen = state.screen

    # #Note to self: remove debug lines after done# #

    state.clock = pygame.time.Clock()
    pygame.display.set_caption("The Arena")
    state.done = False
    run_game()
