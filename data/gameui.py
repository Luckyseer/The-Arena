# Author - Hameel Babu Rasheed
# This is a ui module that is gonna be used to replace most of the ui I already made for my game
# It should be better than what I have now but I still expect to see some issues here and there
import pygame


class TooManyChoicesError(Exception):
    """Exception raised when choice selection has too many choices."""
    def __init__(self, choices):
        self.choices = choices
        self.message = "Expected 3 or less choices, Instead got {}".format(len(choices))
        super().__init__(self.message)


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
    """The class for text used by UI with some convenient functions. The outline does not work properly currently"""
    def __init__(self, font_size=33):
        self.font_size = font_size
        self.main_font = pygame.font.Font("data/fonts/runescape_uf.ttf", self.font_size)
        self.main_font_outline = pygame.font.Font("data/fonts/runescape_uf.ttf", self.font_size + 1)
        self.main_font_colour = (21, 57, 114)   # The default font colour (Blue-ish)
        self.main_font_colour2 = (23, 18, 96)   # Secondary font colour (Darker than the main font)
        self.text_speed = 0  # The speed for text to be scrolling (upto 3)
        self.text_buffer = ''   # The current buffer for the text
        self.text_timer = Timer()
        self.scrolling_flag = True
        self.current_char = 0

    def get_next_character(self, text=''):
        if len(text) > self.current_char:
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
                rendered_word = self.main_font.render(word, True, self.main_font_colour).convert_alpha()
                word_width, word_height = rendered_word.get_size()
                if outline:
                    rendered_word_outline = self.main_font_outline.render(word, True, self.main_font_colour2)
                    word_width2, word_height2 = rendered_word_outline.get_size()
                if x + word_width >= width - 50:
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
            time = 0.3
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

    def fade_in(self, surface=pygame.Surface((0, 0)), delay=0.01):
        if surface.get_alpha() < 255:
            if self.text_timer.timing(1) > delay:
                surface.set_alpha(surface.get_alpha() + 5)
                self.text_timer.reset()

    def fade_out(self, surface=pygame.Surface((0, 0)), delay=0.01):
        if surface.get_alpha() > 0:
            if self.text_timer.timing(1) > delay:
                surface.set_alpha(surface.get_alpha() - 5)
                self.text_timer.reset()

    def reset_buffer(self):
        self.scrolling_flag = True
        self.current_char = 0
        self.text_buffer = ''


class TextBox:
    """The textbox class, used to draw textboxes and anything related to dialogue."""

    def __init__(self):
        self.bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()  # Ui background
        self.bg_loaded = pygame.transform.scale(self.bg, (1280, 300)).convert_alpha()
        self.confirm_bg = pygame.transform.scale(self.bg, (300, 300)).convert_alpha()
        self.choice_bg1 = pygame.transform.scale(self.bg, (400, 300)).convert_alpha()
        self.choice_bg2 = pygame.transform.scale(self.bg, (400, 200)).convert_alpha()
        self.confirm_surf = pygame.Surface((300, 300))
        self.confirm_surf.set_colorkey((0, 0, 0))
        self.txtbox_surf = pygame.Surface((1260, 300))
        self.txtbox_surf.set_alpha(255)
        self.txtbox_surf.set_colorkey((0, 0, 0))
        self.txtcolor2 = (23, 18, 96)
        self.cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.dialogue_progress = 0  # Current 'Progress' of the dialogue
        self.txtbox_height = 300
        self.popup_flag = False  # Flag for popup animation
        self.popup_done = False  # Check if the popup animation is done or not
        self.ui_text = UiText()
        self.txtbox_timer = Timer()
        self.blink_timer = Timer()  # Timer for cursor blinking
        self.cursor_char = '_'  # The character that is displayed on the cursor
        self.ui_text_small = UiText(25)
        self.ui_text_confirm = UiText(27)
        self.ui_text_small.main_font_colour = (205, 21, 45)
        self.load_face = False
        self.speaker = pygame.image.load('data/sprites/boy.png').convert_alpha()
        self.confirm_flag = False
        self.choice_cursor_pos = 0
        self.choice_flag = False
        self.choice_surf = pygame.Surface((400, 300))
        self.choice_surf.set_colorkey((255, 255, 255))
        self.popup_message_pos_y = 400
        self.popup_message_flag = False
        self.popup_message_surf = pygame.Surface((1280, 300))
        self.popup_message_surf.set_colorkey((255, 255, 255))
        self.popup_message_surf.set_alpha(255)
        self.user_input = []
        self.pyg_k_alpha = {
            pygame.K_a: 'a', pygame.K_b: 'b', pygame.K_c: 'c', pygame.K_d: 'd', pygame.K_e: 'e',
            pygame.K_f: 'f', pygame.K_g: 'g', pygame.K_h: 'h', pygame.K_i: 'i', pygame.K_j: 'j',
            pygame.K_k: 'k', pygame.K_l: 'l', pygame.K_m: 'm', pygame.K_n: 'n', pygame.K_o: 'o',
            pygame.K_p: 'p', pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_s: 's', pygame.K_t: 't',
            pygame.K_u: 'u', pygame.K_v: 'v', pygame.K_w: 'w', pygame.K_x: 'x', pygame.K_y: 'y',
            pygame.K_z: 'z'
        }
        self.pyg_k_digit = {
            pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3',
            pygame.K_4: '4', pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8',
            pygame.K_9: '9'
        }
        self.pyg_k_special = {
            pygame.K_BACKSLASH: '\\', pygame.K_COMMA: ',', pygame.K_QUOTE: '\'',
            pygame.K_PERIOD: '.', pygame.K_SLASH: '/', pygame.K_SEMICOLON: ';',
            pygame.K_CARET: '^', pygame.K_LEFTBRACKET: '[', pygame.K_RIGHTBRACKET: ']',
            pygame.K_MINUS: '-', pygame.K_EQUALS: '=', pygame.K_BACKQUOTE: '`'
            }

    def reset(self):
        self.popup_flag = False
        self.popup_done = False
        self.load_face = False
        self.txtbox_height = 0
        self.dialogue_progress = 0
        self.ui_text.reset_buffer()
        self.choice_flag = False
        self.confirm_flag = False

    def popup(self):  # popup animation for the text box
        if not self.popup_flag:
            self.txtbox_height = 0
        self.popup_flag = True
        if self.popup_flag and self.txtbox_height < 300:
            self.txtbox_height += 50
        if self.txtbox_height >= 300:
            self.popup_done = True

    def toggle_popup_flag(self):
        if not self.popup_message_flag:
            self.popup_message_flag = True
            self.popup_message_pos_y = 400
            self.popup_message_surf.set_alpha(255)
            self.txtbox_timer.reset()

    def popup_message(self, message, surf):  # Creates a quick message on the screen and it scrolls up and fades away
        if self.popup_message_flag:
            self.popup_message_surf.fill((255, 255, 255))
            self.ui_text.draw_text((450, 150), message, False, self.popup_message_surf)
            surf.blit(self.popup_message_surf, (0, self.popup_message_pos_y))
            if self.popup_message_pos_y > -100:
                if self.txtbox_timer.timing(1) > 0.01:
                    self.popup_message_pos_y -= 5
                    self.txtbox_timer.reset()
                if self.popup_message_pos_y < 100:
                    self.ui_text.fade_out(self.popup_message_surf)
            else:
                self.popup_message_flag = False

    def progress_dialogue(self, dialogue=[[]]):
        if self.ui_text.scrolling_flag:
            self.ui_text.scrolling_flag = False
        else:
            if self.dialogue_progress < len(dialogue) - 1:
                self.dialogue_progress += 1
                self.ui_text.reset_buffer()
                self.load_face = False
                return False
            else:
                self.load_face = False
                self.ui_text.reset_buffer()
                return True

    def draw_textbox(self, dialogue, surface=pygame.Surface((0, 0)), pos=(0, 400)):
        if self.txtbox_height < 300:
            self.txtbox_surf.fill((0, 0, 0, 255))
            self.txtbox_surf.blit(pygame.transform.scale(self.bg, (1280, self.txtbox_height)), (0, 0))
        if not self.popup_done:
            self.popup()
        if self.popup_done:
            self.txtbox_surf.blit(self.bg_loaded, (0, 0))
            if dialogue[self.dialogue_progress][0] != "":   # Textbox dialogue head
                if not self.load_face:
                    self.speaker = pygame.image.load(dialogue[self.dialogue_progress][0]).convert_alpha()
                    self.load_face = True
                self.txtbox_surf.blit(self.speaker, (110, 70))
                self.ui_text_small.draw_text((150, 220), dialogue[self.dialogue_progress][1], False, self.txtbox_surf)    # Name of speaker
                pic_off = 0  # Offset for image when the text is drawn
            else:
                pic_off = 100

            self.ui_text.draw_scrolling_text((250 - pic_off, 60), dialogue[self.dialogue_progress][2], False, self.txtbox_surf, 3)
            self.ui_text_small.draw_text((300, 220), "Press RCTRL to continue...", False, self.txtbox_surf)
        surface.blit(self.txtbox_surf, pos)

    def confirm_box(self, message='', surface=pygame.Surface((0, 0)), confirm_text='ENTER: Confirm', deny_text='RCTRL: Cancel'):
        self.confirm_surf.fill((0, 0, 0))
        self.confirm_surf.blit(self.confirm_bg, (0, 0))
        self.ui_text_confirm.draw_text((50, 50), message, False, self.confirm_surf)
        self.ui_text_confirm.draw_text((50, 160), confirm_text, False, self.confirm_surf)
        self.ui_text_confirm.draw_text((50, 190), deny_text, False, self.confirm_surf)
        surface.blit(self.confirm_surf, (surface.get_width()/2 - 150, surface.get_height()/2 - 150))

    def select_choice(self, choices=[], surface=pygame.Surface((0, 0)), pos=(750, 200)):
        if len(choices) > 3:
            raise TooManyChoicesError(choices)
        if self.choice_flag:
            choice_string = '\n'    # We combine the choices into one string so that it will properly scroll over
            self.choice_surf.fill((255, 255, 255))
            if len(choices) >= 3:
                self.choice_surf.blit(self.choice_bg1, (0, 0))
            else:
                self.choice_surf.blit(self.choice_bg2, (0, 0))
            self.ui_text_small.draw_text((50, 60), choice_string.join(choices), False, self.choice_surf)
            if self.choice_cursor_pos > len(choices) - 1:
                self.choice_cursor_pos = 0
            elif self.choice_cursor_pos < 0:
                self.choice_cursor_pos = len(choices) - 1
            if self.choice_cursor_pos == 0:
                self.choice_surf.blit(self.cursor, (20, 60))
            elif self.choice_cursor_pos == 1:
                self.choice_surf.blit(self.cursor, (20, 90 + len(choices[0]) / 2))
            elif self.choice_cursor_pos == 2:
                self.choice_surf.blit(self.cursor, (20, 120 + len(choices[1]) / 2 + len(choices[0]) / 2))
            surface.blit(self.choice_surf, pos)

    def select_choice_inputs(self, event):
        if event.key == pygame.K_DOWN:
            self.choice_cursor_pos += 1
        elif event.key == pygame.K_UP:
            self.choice_cursor_pos -= 1

    def get_user_input(self, event, max_chars=32, no_alpha=False, no_special=False, no_digit=False, no_space=False):
        if len(self.user_input) > 0:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
        if len(self.user_input) < max_chars:
            if not no_alpha:
                if event.key in self.pyg_k_alpha:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.user_input += self.pyg_k_alpha[event.key].upper()
                    else:
                        self.user_input += self.pyg_k_alpha[event.key]
            if not no_special:
                if event.key in self.pyg_k_special:
                    self.user_input += self.pyg_k_special[event.key]
            if not no_digit:
                if event.key in self.pyg_k_digit:
                    self.user_input += self.pyg_k_digit[event.key]
            if not no_space:
                if event.key == pygame.K_SPACE:
                    self.user_input += ' '

    def display_user_input(self, surface, pos, display_cursor=True, blink_cursor=True):
        user_input_text = "".join(self.user_input)
        self.ui_text.draw_text((pos[0], pos[1]), user_input_text, False, surface)
        if display_cursor:  # The cursor currently only works properly for single line inputs
            rendered_word = self.ui_text.main_font.render(user_input_text, False, (0, 0, 0))
            if blink_cursor:
                if self.blink_timer.timing(mode=1) >= 0.3:
                    self.blink_timer.reset()
                    if self.cursor_char == '':
                        self.cursor_char = '_'
                    else:
                        self.cursor_char = ''
            self.ui_text.draw_text((pos[0] + rendered_word.get_size()[0], pos[1]), self.cursor_char, False, surface)
