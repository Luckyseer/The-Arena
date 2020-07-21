# Author - Hameel Babu Rasheed
# This is a ui module that is gonna be used to replace most of the ui I already made for my game
# It should be better than what I have now but I still expect to see some issues here and there
import pygame


class Timer:
    """The Timer class, used to time things in-game."""

    def __init__(self):
        self.start = int(pygame.time.get_ticks())
        self.seconds = 0

    def timing(self, mode=0):
        # Set mode = 0 to return the time in seconds,set mode = 1 to return the time in milliseconds.
        if mode == 0:
            self.seconds = int((pygame.time.get_ticks() - self.start) / 1000)  # How many seconds passed
        elif mode == 1:
            self.seconds = (pygame.time.get_ticks() - self.start) / 1000  # How many milliseconds passed
        return self.seconds

    def reset(self):
        self.start = int(pygame.time.get_ticks())

    def dothing(self, time):
        seconds = self.timing()
        if seconds >= time:
            print("Doing thing")  # debug
            return True


class UiText:
    """The class for text used by UI with some convenient functions"""
    def __init__(self, font_size=33):
        self.main_font = pygame.font.Font("fonts/runescape_uf.ttf", font_size)
        self.main_font_outline = pygame.font.Font("fonts/runescape_uf.ttf", font_size + 1)
        self.main_font_colour = (21, 57, 114)   # The default font colour (Blue-ish)
        self.main_font_colour2 = (23, 18, 96)   # Secondary font colour (Darker than the main font)
        self.text_speed = 0  # The speed for text to be scrolling (upto 3)
        self.text_buffer = ''   # The current buffer for the text
        self.text_timer = Timer()
        self.scrolling_flag = True
        self.current_char = 0

    def get_next_character(self, text=''):
        if len(text) - 1 > self.current_char:
            self.text_buffer += text[self.current_char]
            self.current_char += 1

    def draw_text(self, pos, text='', outline=False, surface=pygame.Surface((0, 0))):
        height = surface.get_height()
        width = surface.get_width()
        words = [word.split(' ') for word in text.splitlines()]
        space = self.main_font.size(' ')[0]  # The size of whitespace
        space_outline = self.main_font_outline.size(' ')[0]
        x, y = pos
        x_outline = x + 1
        y_outline = y + 1
        for line in words:
            for word in line:
                rendered_word = self.main_font.render(word, True, self.main_font_colour)
                word_width, word_height = rendered_word.get_size()
                if outline:
                    rendered_word_outline = self.main_font_outline.render(word, True, self.main_font_colour2)
                    word_width2, word_height2 = rendered_word_outline.get_size()
                if x + word_width >= width:
                    x = pos[0]
                    x_outline = pos[0]
                    y += word_height
                    if outline:
                        y_outline += word_height2
                if outline:
                    surface.blit(rendered_word_outline, (x, y))
                surface.blit(rendered_word, (x, y))
                x += word_width + space
                if outline:
                    x_outline += word_width2 + space_outline
            x = pos[0]
            x_outline = pos[0]
            y += word_height
            if outline:
                y_outline += word_height2

    def draw_scrolling_text(self, pos, text='', outline=False, surface=pygame.Surface((0, 0)), text_speed=0):
        if text_speed <= 0:
            self.scrolling_flag = False
        elif text_speed == 1:
            time = 0.05
        elif text_speed == 2:
            time = 0.03
        else:
            time = 0.01
        if text_speed > 0 and self.scrolling_flag:
            if self.text_timer.timing(1) >= time:
                self.get_next_character(text)
                self.text_timer.reset()
        if self.text_buffer == text:
            self.scrolling_flag = False
        if self.scrolling_flag:
            self.draw_text(pos, self.text_buffer, outline, surface)
        else:
            self.draw_text(pos, text, outline, surface)

    def fade_in(self, surface=pygame.Surface((0, 0))):
        if surface.get_alpha() < 255:
            surface.set_alpha(surface.get_alpha() + 5)

    def fade_out(self, surface=pygame.Surface((0, 0))):
        if surface.get_alpha() > 0:
            surface.set_alpha(surface.get_alpha() - 5)


class TextBox:
    """The textbox class, used to draw textboxes and anything related to dialogue."""

    def __init__(self, txtcolor=(21, 57, 114), convo_flag=False):
        self.bg = pygame.image.load("backgrounds/rpgtxt.png").convert_alpha()  # Ui background
        self.bg_loaded = pygame.transform.scale(self.bg, (1280, 300)).convert_alpha()
        self.txtcolor = txtcolor  # Default font colour
        self.txtcolor2 = (23, 18, 96)
        self.cursor = pygame.image.load("sprites/Cursor.png").convert_alpha()
        self.ch_cursorpos = 0  # Position of cursor for choice selection
        self.dialogue_progress = 0  # Current 'Progress' of the dialogue
        self.txtbox_height = 300
        self.popup_flag = False  # Flag for popup animation
        self.popup_done = False  # Check if the popup animation is done or not
        self.convo_flag = convo_flag  # if it is a conversation(aka story part) the popup animation won't repeat

    def draw_textbox(self, dialogue):
        pass