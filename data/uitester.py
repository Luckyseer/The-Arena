"""Just a small script to test the UI. Some things may be broken. Use the arrow keys to test things"""
import pygame
from gameui import *
import json

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
done = False
text = UiText()
text.main_font_colour = (0, 0, 0)
text.main_font_colour2 = (0, 0, 0)
fade = False
fade_out = False
bg = pygame.Surface((1280, 400))
bg.set_colorkey((255, 255, 255))
bg.set_alpha(255)
tb = TextBox()
draw_tb = False
with open("dialogue.json", "r") as f:
    data = json.load(f)
    dialogue = data["intro1"]
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
            if event.key == pygame.K_LEFT:
                draw_tb = True
            if event.key == pygame.K_RIGHT:
                draw_tb = False
                tb.reset()
            if event.key == pygame.K_RCTRL:
                tb.progress_dialogue(dialogue)

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
    if draw_tb:
        tb.draw_textbox(dialogue, screen)
    tb.confirm_box('Long confirmation message', screen)
    screen.blit(bg, (0, 0))
    clock.tick()
    fps = clock.get_fps()
    pygame.display.set_caption("FPS:{}".format(fps))
    pygame.display.flip()
