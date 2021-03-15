import pygame
import pyganim
from gameui import Timer


class Splash:
    def __init__(self, target_screen):
        self.splash_anim = pyganim.PygAnimation([['sprites/splash_animation/splash1', 0.3],
                                                 ['sprites/splash_animation/splash2', 0.3],
                                                 ['sprites/splash_animation/splash3', 0.3],
                                                 ['sprites/splash_animation/splash4', 0.3],
                                                 ['sprites/splash_animation/splash5', 0.3],
                                                 ['sprites/splash_animation/splash6', 0.3],
                                                 ['sprites/splash_animation/splash7', 0.3],
                                                 ['sprites/splash_animation/splash8', 0.3]], False)
        self.splash_surf = pygame.Surface(target_screen.get_size())
        self.splash_timer = Timer()
        self.splash_surf.fill((255, 255, 255))

    def draw_splash(self, target_screen):
        self.splash_surf.blit(self.splash_anim)

