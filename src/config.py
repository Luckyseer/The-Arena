import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
IS_FULLSCREEN = False

def get_screen():
    if not IS_FULLSCREEN:
        return pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.HWACCEL)
    else:
        return pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)
