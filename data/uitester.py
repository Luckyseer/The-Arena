"""Just a small script to test the functions for the UI. Some things may be broken."""
import pygame
from gameui import *

pygame.init()

screen = pygame.display.set_mode((400, 400), pygame.NOFRAME)
clock = pygame.time.Clock()
done = False
text = UiText()
text.main_font_colour = (0, 0, 0)
text.main_font_colour2 = (0, 0, 0)
fade = False
fade_out = False
bg = pygame.Surface((400, 400))
bg.set_alpha(255)
tb = TextBox()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if not fade:
                    print('yup')
                    fade_out = True
            if event.key == pygame.K_UP:
                if not fade_out:
                    fade = True
                    print('nope')

    if fade_out:
        text.fade_out(bg)
        if bg.get_alpha() <= 0:
            fade_out = False
    if fade:
        text.fade_in(bg)
        if bg.get_alpha() >= 255:
            fade = False
    screen.fill((255, 255, 255))
    bg.fill((255, 255, 255, 255))
    text.draw_scrolling_text((0, 0), "This is a test line I want to see if this text works properly as intended\nLike this\nOr this.", False, bg, 3)
    screen.blit(bg, (0, 0))
    clock.tick(60)
    fps = clock.get_fps()
    pygame.display.set_caption("FPS:{}".format(fps))
    pygame.display.flip()
