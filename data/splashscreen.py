import pygame
from data import pyganim
from data import gameui

class Splash:
    def __init__(self, target_screen):
        self.splash_anim = pyganim.PygAnimation([['data/sprites/splash_animation/splash1.png', 0.6],
                                                 ['data/sprites/splash_animation/splash2.png', 0.6],
                                                 ['data/sprites/splash_animation/splash3.png', 0.6],
                                                 ['data/sprites/splash_animation/splash4.png', 0.6],
                                                 ['data/sprites/splash_animation/splash5.png', 0.6],
                                                 ['data/sprites/splash_animation/splash6.png', 0.6],
                                                 ['data/sprites/splash_animation/splash7.png', 0.6],
                                                 ['data/sprites/splash_animation/splash8.png', 0.6]], True)
        self.splash_surf = pygame.Surface(target_screen.get_size())
        self.splash_timer = gameui.Timer()
        self.splash_surf.fill((255, 255, 255))
        self.splash_start = False

    def draw_splash(self, target_screen, event):
        while self.splash_start:
            self.splash_anim.blit(self.splash_surf, (450, 200))
            target_screen.blit(self.splash_surf, (0, 0))
            self.check_inputs(event)
            pygame.display.flip()
            if self.splash_timer.timing() > 3:
                self.splash_start = False

    def toggle_splash(self):
        if self.splash_start:
            self.splash_start = False
        else:
            self.splash_start = True
            self.splash_timer.reset()
            self.splash_anim.play()

    def check_inputs(self, event):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.splash_start = False
            elif event.type == pygame.QUIT:
                pygame.quit()
