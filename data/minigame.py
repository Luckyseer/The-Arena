# This module contains all the code for the casino mini-games(blackjack and odds or evens)
import pygame
import gameui as ui


class Casino:
    def __init__(self):
        self.cur_bg = ""
        self.cur_state = "menu"
        self.cur_game = ""  # Current game being played
        self.txtbox = ui.TextBox()
        self.timer = ui.Timer()
        self.cur_bgm = ""

    def odds_evens_minigame(self, surf):
        surf.blit(self.cur_bg, (0, 0))
        surf.blit

