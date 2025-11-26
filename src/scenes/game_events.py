import pygame
from data import gameui
from src.ui.main_ui import MainUi, SelectOptions
from src.utils.timer import Timer, fadein, fadeout
from src.engine.game_clock import GameClock

class GameEvents(MainUi):
    """Class for all special events in the game."""

    def __init__(self, surface, item_data, dialogues, clock):
        MainUi.__init__(self, surface, item_data, dialogues)
        self.surface = surface
        self.clock = clock
        self.town_bg_day = pygame.image.load(
            "data/backgrounds/The Medieval Town.jpg").convert_alpha()
        self.town_bg_eve = pygame.image.load(
            "data/backgrounds/The Medieval Town_eve.jpg").convert_alpha()
        self.town_bg_ngt = pygame.image.load(
            "data/backgrounds/The Medieval Town_night.jpg").convert_alpha()
        self.inn_bg = pygame.image.load(
            "data/backgrounds/inn.png").convert_alpha()
        self.townDialogue = 0  # Progress for the dialogue while in the town.
        self.arenaDialogue = 0
        self.timekeep = Timer()  # Used to time the events and things
        self.dialoguecontrol = False
        self.startEvent = False
        self.thudSound = pygame.mixer.Sound('data/sounds&music/thud.wav')
        self.thudSound.set_volume(0.05)
        self.applauseSound = pygame.mixer.Sound(
            'data/sounds&music/Applause1.ogg')
        self.applauseSound.set_volume(0.05)
        self.bossRoar = pygame.mixer.Sound('data/sounds&music/Monster2.ogg')
        self.bossRoar.set_volume(0.05)
        self.arena_bg = pygame.image.load(
            "data/backgrounds/arenaDay.png").convert_alpha()
        self.arena_bg = pygame.transform.scale(self.arena_bg, (1280, 720))
        self.arena_bg_night = pygame.image.load(
            "data/backgrounds/arenaNight.png").convert_alpha()
        self.arena_bg_night = pygame.transform.scale(
            self.arena_bg_night, (1280, 720))
        self.boss_face1 = pygame.image.load("data/sprites/Boss1.png")
        self.town_location = 0  # 0-Centre 1-Bar/Inn 2-Slums
        self.game_clock = GameClock()
        self.option_selector = SelectOptions(surface, item_data, dialogues)
        self.town_talk1 = False  # Flag for drawing options menu for the 'Talk' Screen
        self.talking = False  # Flag to know if dialogue is currently being spoken
        self.talk_val = 0  # Used to know which option was chosen.
        self.text_box = gameui.TextBox()
        self.ui_text = gameui.UiText()
        self.ui_text.main_font_colour = (255, 255, 255)
        self.casino_state = ''  # Current state of the casino
        self.dialogue = [[]]  # Current Dialogue

    def town_first_visit(self, player_data):
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Bustling_Streets.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        runningsound = pygame.mixer.Sound(
            'data/sounds&music/Person_running.wav')
        runningsound.set_volume(0.3)
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        timedflag1 = False  # To be activated for certain timed events
        timedflag2 = False  # ""    ""              ""            ""
        self.timekeep.reset()
        self.dialoguecontrol = False
        paid_girl = False
        dialogue_choice = 0
        dialogue_choice2 = 0
        choice_select = False
        player_data.town_first_flag = True
        while not event_done:
            curwidth, curheight = self.surface.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    return "QUIT" # Signal to quit game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL and self.dialoguecontrol:
                        if self.txtbox.progress_dialogue():
                            self.townDialogue += 1
                    if choice_select:
                        self.txtbox.select_choice_inputs(event)
                    if event.key == pygame.K_RETURN and choice_select:
                        if self.txtbox.choice_cursor_pos == 0:   # Pay the girl
                            dialogue_choice = 0
                            dialogue_choice2 = 0
                            choice_select = False
                            self.townDialogue += 1
                            self.dialoguecontrol = True
                        if self.txtbox.choice_cursor_pos == 1:   # Refuse the girl
                            dialogue_choice = 1
                            dialogue_choice2 = 1
                            choice_select = False
                            self.townDialogue += 1
                            self.dialoguecontrol = True
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()

            self.surface.blit(pygame.transform.scale(
                self.town_bg_day, (curwidth, curheight)), (0, 0))

            if not self.startEvent:
                if self.timekeep.timing() == 2 and self.townDialogue < 1:
                    self.startEvent = True
            if self.startEvent:
                self.townDialogue = 1
                self.startEvent = False
                self.dialoguecontrol = True

            if self.townDialogue == 1:
                self.txtbox.draw_textbox([['', '',
                                         '''The town that the Arena is situated in gets very lively this time of the year as this is when most of the challengers arrive.''']], self.surface)
            elif self.townDialogue == 2:
                self.txtbox.draw_textbox([['', '',
                                         """You\'ve been here before but never really got the chance to look around, so the sights of this place are still very unfamiliar to you."""]], self.surface
                                         )
            elif self.townDialogue == 3:
                self.txtbox.draw_textbox([['', '',
                                         'Even if you had been familiar with this place in the past, It would still have been difficult finding your way through this place as the town has changed dramatically over the course of a few years.']], self.surface)
            elif self.townDialogue == 4:
                self.txtbox.draw_textbox([['', '',
                                         '''This is mostly due to the overwhelming popularity of the arena which has brought visitors from all over the country to this one location. This has let the town flourish and expand at a very quick pace, with new buildings and stores being built seemingly everyday.''']], self.surface
                                         )
            elif self.townDialogue == 5:
                self.txtbox.draw_textbox([['', '',
                                         '''The presence and influence of the arena played a major role in the growth of the town, so much so that the people of the town decided to change it\'s old name and give it a new more fitting name, \"Arena Town\".''']], self.surface
                                         )
            elif self.townDialogue == 6:
                runningsound.play()
                self.timekeep.reset()
                self.townDialogue += 1
                self.dialoguecontrol = False
            elif self.townDialogue == 7 and timedflag1:
                self.dialoguecontrol = True
                self.txtbox.draw_textbox([['', '',
                                         'You see a young girl running towards your direction.']], self.surface
                                         )
            elif self.townDialogue == 8:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'Oh no, I\'m so late, Grandpa\'s gonna get so mad!']], self.surface
                                         )
                timedflag1 = False

            elif self.townDialogue == 9:
                self.thudSound.play()
                self.townDialogue += 1
                self.dialoguecontrol = False
                self.timekeep.reset()
            elif self.townDialogue == 10 and timedflag1:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'Ouch!']], self.surface
                                         )
                self.dialoguecontrol = True
            elif self.townDialogue == 11:
                self.txtbox.draw_textbox([['', '',
                                         'The girl crashes into you at full speed and topples over onto the gravel road.']], self.surface
                                         )
            elif self.townDialogue == 12:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'Hey, watch where you\'re going!']], self.surface
                                         )

            elif self.townDialogue == 13:
                self.txtbox.draw_textbox([['', '',
                                         'The girl gets up and brushes off her skirt.']], self.surface
                                         )
            elif self.townDialogue == 14:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'There\'s a tear in my new dress! What are you going to do about this?']], self.surface
                                         )
                choice_select = True
                self.txtbox.choice_flag = True
            elif self.townDialogue == 15:
                self.txtbox.draw_textbox([['', '',
                                         'What do you do?']], self.surface
                                         )
                self.txtbox.select_choice(
                    ['Offer to pay her money', 'Ignore her and walk away'], self.surface)
                self.dialoguecontrol = False
            elif dialogue_choice == 0 and self.townDialogue >= 16:  # Pay money dialogue tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                             'Oh you\'re willing to pay? I\'m going to need atleast 150 gold for the dress.']], self.surface
                                             )
                    choice_select = True
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox([['', '',
                                             'Pay 150 gold?']], self.surface
                                             )
                    self.txtbox.select_choice(['Pay her', 'Don\'t Pay'], self.surface)
                    self.dialoguecontrol = False
                elif self.townDialogue >= 18 and dialogue_choice2 == 0:  # Pay her
                    if player_data.gold < 150 and not paid_girl:  # if player doesn't have enough gold
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'Hey you don\'t even have enough gold to pay me!']]), self.surface
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'Don\'t waste my time if you don\'t have any money!']]), self.surface
                        if self.townDialogue == 20:
                            self.townDialogue = 21
                            dialogue_choice2 = 1
                    else:
                        if not paid_girl:
                            player_data.gold -= 150
                            player_data.paid_girl_flag = True
                        paid_girl = True
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'Well, I guess this will have to do.']], self.surface)
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'You better be careful next time! Be grateful that I let you off easily!']], self.surface)
                        elif self.townDialogue == 20:
                            self.txtbox.draw_textbox([['', '',
                                                     '''The girl walks away after glaring at you in the eye. You could have sworn you saw a smile for a second.''']], self.surface)
                        elif self.townDialogue == 21:
                            self.txtbox.draw_textbox([['', '',
                                                     'The girl disappears into the crowd.']], self.surface)

                elif self.townDialogue >= 18 and dialogue_choice2 == 1:  # Don't pay her
                    if self.townDialogue == 18:
                        self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                 '...You\'re not going to pay?']], self.surface)
                    if self.townDialogue == 19:
                        self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                 'Tch.. he didn\'t fall for it']], self.surface)
                    elif self.townDialogue == 20:
                        self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                 'Well don\'t waste my time then, get out of my way!']], self.surface)
                    elif self.townDialogue == 21:
                        self.txtbox.draw_textbox([['', '',
                                                 'The girl storms off and disappears into the crowd.']], self.surface)
            elif dialogue_choice == 1 and self.townDialogue >= 16:  # ignore girl tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                             '....']], self.surface
                                             )
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                             'Don\'t just ignore me!']], self.surface)
                elif self.townDialogue == 18:
                    self.txtbox.draw_textbox([['', '',
                                             '''You continue ignoring the girl while she makes a commotion in the middle of the street and proceed to the Town.''']], self.surface)
                elif self.townDialogue == 19:
                    self.townDialogue = 22
            if self.townDialogue >= 22:
                event_done = True
                if paid_girl:
                    return True
                else:
                    return False
            if self.townDialogue == 7 and self.timekeep.timing() == 4:
                timedflag1 = True
            if self.townDialogue == 10 and self.timekeep.timing() == 1:
                timedflag1 = True
            
            self.timekeep.timing()
            self.clock.tick(60)
            fps = "FPS:%d" % self.clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def firstfloor_boss(self, name='Zen'):
        # Cutscene when challenging the first_floor boss
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Dungeon3.ogg')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        applause_flag1 = False  # Initial flag for applause
        applause_flag2 = False  # Applause during name announcement
        post_applause = False
        boss_roar = False  # During Boss name announcement
        choice_select = False  # Flag for the choice selection part
        self.arenaDialogue = 0
        dialogue_choice = 0
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL and self.dialoguecontrol:
                        if self.txtbox.progress_dialogue():
                            self.arenaDialogue += 1
                    if event.key == pygame.K_UP and choice_select:
                        self.txtbox.select_choice_inputs(event)
                        self.cursorsound.play()
                    if event.key == pygame.K_DOWN and choice_select:
                        self.txtbox.select_choice_inputs(event)
                        self.cursorsound.play()
                    if event.key == pygame.K_RETURN and choice_select:
                        if self.txtbox.choice_cursor_pos == 0:
                            dialogue_choice = 0
                            choice_select = False
                            self.arenaDialogue += 1
                            self.dialoguecontrol = True
                        if self.txtbox.choice_cursor_pos == 1:
                            dialogue_choice = 1
                            choice_select = False
                            self.arenaDialogue += 1
                            self.dialoguecontrol = True
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

            self.surface.blit(self.arena_bg, (0, 0))
            if self.timekeep.timing() == 2:
                if not applause_flag1:
                    self.applauseSound.play()
                    applause_flag1 = True
                    self.arenaDialogue = 1
                    self.dialoguecontrol = True
            if applause_flag2:
                if not post_applause:
                    self.applauseSound.play()
                    pygame.mixer.music.play()
                    applause_flag2 = False
                    post_applause = True

            if self.arenaDialogue == 1:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'Ladies and gentlemen!']], self.surface
                                         )

            elif self.arenaDialogue == 2:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'It seems like it\'s been ages since we\'ve had a challenger strong enough to finally get to this point!']], self.surface
                                         )
            elif self.arenaDialogue == 3:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'But we finally have him here, someone who is both brave and foolish enough to step up and fight his way through some of the most powerful monsters, to be able to stand before you at this very moment and face against what many would consider suicide! ']], self.surface
                                         )
            elif self.arenaDialogue == 4:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'Please put your hands together for.. ' + name + '!']], self.surface
                                         )
                applause_flag2 = True
            elif self.arenaDialogue == 5:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'And his opponent.. A beast that has destroyed the dreams of many young adventurers, said to be the \'Gatekeeper\' of the Arena.']], self.surface
                                         )
            elif self.arenaDialogue == 6:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'Introducing.. Tho\'k!']], self.surface
                                         )
                boss_roar = True

            elif self.arenaDialogue == 7:
                self.txtbox.draw_textbox([["data/sprites/Boss1.png", 'Tho\'k',
                                         'RAAAAAAAAAAAAAAAAAARRGGHHHHHH!!!!!']], self.surface
                                         )
                if boss_roar:
                    self.bossRoar.play()
                    self.timekeep.reset()
                    boss_roar = False
                    self.dialoguecontrol = False
                if self.timekeep.timing() == 2:
                    self.dialoguecontrol = True

            elif self.arenaDialogue == 8:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'Now, the time has come. ' + name + ', I assume you are ready?']], self.surface
                                         )
                self.txtbox.select_choice(['Yes, I am ready.',
                                          'I don\'t think I am.'], self.surface)
                self.dialoguecontrol = False
                choice_select = True
                self.txtbox.choice_flag = True
            elif self.arenaDialogue == 9:
                if dialogue_choice == 0:
                    self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                             'Good! That\'s what I expected from you!']], self.surface
                                             )
                elif dialogue_choice == 1:
                    self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                             'Well unfortunately it\'s too late to turn back now!']], self.surface
                                             )
            elif self.arenaDialogue == 10:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'It is time! Fight!']], self.surface
                                         )
            elif self.arenaDialogue == 11:
                event_done = True
            
            self.timekeep.timing()
            self.clock.tick(60)
            fps = "FPS:%d" % self.clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def first_floor_victory(self, dialogues):
        # Cutscene after beating the first_floor boss
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        pygame.mixer.music.play()
        state = 0
        cur_song = 'data/sounds&music/Infinite_Arena.mp3'
        draw_tb = False
        cur_dialogue = dialogues["first_floor_victory1"]
        vol = 0.5 # Default volume
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if self.dialoguecontrol and event.key == pygame.K_RCTRL:
                        if self.txtbox.progress_dialogue(cur_dialogue):
                            state += 1
                            draw_tb = False
                            self.timekeep.reset()
                            self.txtbox.reset()
                            self.dialoguecontrol = False
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.load(cur_song)
                    pygame.mixer.music.set_volume(vol)
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                if event.type == pygame.QUIT:
                    event_done = True
                    return "QUIT"
            if state == 0:
                if self.timekeep.timing() > 2:
                    self.applauseSound.play()
                    state += 1
            elif state == 1:
                self.dialoguecontrol = True
                draw_tb = True
            elif state == 2:
                if self.timekeep.timing() <= 1:
                    self.applauseSound.play()
                if self.timekeep.timing() > 2:
                    fadeout(self.surface, 0.01, fade_in=True,
                            optional_bg=self.arena_bg)
                    state += 1
                    self.timekeep.reset()
            elif state == 3:
                if self.timekeep.timing() > 1:
                    cur_dialogue = dialogues['first_floor_victory2']
                    self.dialoguecontrol = True
                    draw_tb = True
            elif state == 4:
                pygame.mixer.music.fadeout(200)
                fadeout(self.surface, 0.01, fade_in=True,
                        optional_bg=self.arena_bg_night)
                pygame.mixer.music.load("data/sounds&music/Dungeon 2.ogg")
                pygame.mixer.music.set_volume(vol)
                cur_song = "data/sounds&music/Dungeon 2.ogg"
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.play()
                state += 1
                self.timekeep.reset()
            elif state == 5:
                if self.timekeep.timing() > 3:
                    cur_dialogue = dialogues['first_floor_victory3']
                    state += 1
            elif state == 6:
                self.dialoguecontrol = True
                draw_tb = True
            elif state == 7:
                if self.timekeep.timing() > 2:
                    pygame.mixer.music.fadeout(200)
                    fadeout(self.surface)
                    event_done = True
            if state < 5:
                self.surface.blit(self.arena_bg, (0, 0))
            else:
                self.surface.blit(self.arena_bg_night, (0, 0))
            if draw_tb:
                self.txtbox.draw_textbox(cur_dialogue, self.surface)
            self.clock.tick(60)
            pygame.display.set_caption("FPS:{}".format(int(self.clock.get_fps())))
            pygame.display.flip()

    def intro_scene(self, intro_dialogue):
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Church.mp3')
        door_sound = pygame.mixer.Sound('data/sounds&music/Door1.ogg')
        door_sound.set_volume(0.05)
        gate_sound = pygame.mixer.Sound('data/sounds&music/Door4.ogg')
        gate_sound.set_volume(0.05)
        text_surf = pygame.Surface((1280, 720))
        text_surf.set_alpha(0)
        text_surf.set_colorkey((0, 0, 0))
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        draw_tb = False
        intro_level = 0
        pygame.mixer.music.play()
        text_x = 100
        text_y = 100
        text = ''
        dialogue = 'intro1'
        vol = 0.5
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL:
                        if self.dialoguecontrol:
                            if self.text_box.progress_dialogue(intro_dialogue[dialogue]):
                                intro_level += 1
                                self.timekeep.reset()
                    if event.key == pygame.K_s:
                        if intro_level < 20:
                            intro_level = 20
            if intro_level < 24:
                self.surface.fill((0, 0, 0, 255))
            text_surf.fill((0, 0, 0, 0))
            if intro_level == 0:
                if self.timekeep.timing(1) > 3:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 1:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "I'm.. still alive?"
                if self.timekeep.timing(1) > 3:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 2:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 3:
                    text_x = 100
                    text_y = 200
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 3:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "Or is this what death feels like?"
                if self.timekeep.timing(1) > 3:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 4:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    text_x = 100
                    text_y = 300
                    self.timekeep.reset()
            elif intro_level == 5:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "Why did things have to turn out this way?"
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 6:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 400
                    self.timekeep.reset()
            elif intro_level == 7:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "I never wanted any of this.."
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 8:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 500
                    self.timekeep.reset()
            elif intro_level == 9:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "This.. This is all my fault.."
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 10:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 100
                    self.timekeep.reset()
            elif intro_level == 11:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "Because of me.. The world will.."
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 12:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 200
                    self.timekeep.reset()
            elif intro_level == 13:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "No.. Not yet.. I can't give up now."
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 14:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 300
                    self.timekeep.reset()
            elif intro_level == 15:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "There should still be time.. I've gotten this far.."
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 16:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 400
                    self.timekeep.reset()
            elif intro_level == 17:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "If I don't stand now.. It will truly be the end.."
                if self.timekeep.timing(1) > 4:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 18:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 500
                    self.timekeep.reset()
            elif intro_level == 19:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = "Mark my words... I will return.. "
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 20:
                text_x += 0.1
                self.ui_text.fade_out(text_surf)
                if self.timekeep.timing(1) > 2:
                    intro_level += 1
                    text_x = 100
                    text_y = 100
                    self.timekeep.reset()
            elif intro_level == 21:
                text_x += 0.1
                self.ui_text.fade_in(text_surf)
                text = ""
                self.ui_text.draw_scrolling_text(
                    (text_x, text_y), "My name is...", False, text_surf, 1)
                if self.timekeep.timing(1) > 5:
                    intro_level += 1
                    pygame.mixer.music.fadeout(3000)
                    self.timekeep.reset()
            elif intro_level == 22:
                if self.timekeep.timing(1) > 6:
                    fadein(self.surface, 255)
                    door_sound.play()
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 23:
                if self.timekeep.timing(1) > 2:
                    draw_tb = True
                    self.dialoguecontrol = True
            elif intro_level == 24:
                gate_sound.play()
                fadein(self.surface, 255, 0.01)
                intro_level += 1
                dialogue = "intro2"
                draw_tb = False
                self.text_box.reset()
                pygame.mixer.music.load("data/sounds&music/Infinite_Arena.mp3")
                pygame.mixer.music.set_volume(vol)
                pygame.mixer.music.play()
                self.timekeep.reset()
            elif intro_level == 25:
                self.surface.blit(self.arena_bg, (0, 0))
                if self.timekeep.timing(1) > 2:
                    draw_tb = True
            elif intro_level == 26:
                event_done = True
            self.ui_text.draw_text((text_x, text_y), text, False, text_surf)
            self.surface.blit(text_surf, (0, 0))
            if draw_tb:
                self.text_box.draw_textbox(
                    intro_dialogue[dialogue], self.surface, (0, 400))
            pygame.display.update()
            self.clock.tick(60)
            pygame.display.set_caption("FPS:{}".format(int(self.clock.get_fps())))

    def town(self, player_data, dialogues):
        """The town and all the locations present in it."""
        if not player_data.town_first_flag:
            result = self.town_first_visit(player_data)
            if result == "QUIT":
                return "QUIT"
        event_done = False
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        town_ui = True
        if self.town_location == 0:
            area_music = 'data/sounds&music/Bustling_Streets.mp3'
            pygame.mixer.music.load(area_music)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)
        self.town_location = 0
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if town_ui:
                        if event.key == pygame.K_DOWN:
                            self.cursorpos += 1
                            self.cursorsound.play()
                        elif event.key == pygame.K_UP:
                            self.cursorpos -= 1
                            self.cursorsound.play()
                    if self.town_talk1:
                        if event.key == pygame.K_DOWN:
                            self.option_selector.rowpos += 1
                        elif event.key == pygame.K_UP:
                            self.option_selector.rowpos -= 1
                        elif event.key == pygame.K_RIGHT:
                            self.option_selector.colpos += 1
                        elif event.key == pygame.K_LEFT:
                            self.option_selector.colpos -= 1
                        elif event.key == pygame.K_RETURN:
                            if self.option_selector.colpos != 3:
                                self.talking = True
                                self.town_talk1 = False
                            if self.option_selector.rowpos == 0 and self.option_selector.colpos == 0:  # Option 1
                                self.talk_val = 0
                                self.option_selector.alert_off(1)
                            elif self.option_selector.rowpos == 0 and self.option_selector.colpos == 1:  # Option 2
                                self.talk_val = 1
                                self.option_selector.alert_off(2)
                            elif self.option_selector.rowpos == 0 and self.option_selector.colpos == 2:  # Option 3
                                self.talk_val = 2
                                self.option_selector.alert_off(3)
                            elif self.option_selector.rowpos == 1 and self.option_selector.colpos == 0:  # Option 4
                                self.talk_val = 3
                                self.option_selector.alert_off(4)
                            elif self.option_selector.rowpos == 1 and self.option_selector.colpos == 1:  # Option 5
                                self.talk_val = 4
                                self.option_selector.alert_off(5)
                            elif self.option_selector.rowpos == 1 and self.option_selector.colpos == 2:  # Option 6
                                self.talk_val = 5
                                self.option_selector.alert_off(6)
                            elif self.option_selector.rowpos == 1 and self.option_selector.colpos == 3:  # Back Option
                                self.town_talk1 = False
                                town_ui = True

                        if player_data.progress == 2:
                            if self.talk_val == 0:
                                self.dialogue = dialogues['town1_citizen']
                            elif self.talk_val == 1:
                                self.dialogue = dialogues['town1_richlady']
                            elif self.talk_val == 2:
                                self.dialogue = dialogues['town1_drunkman']

                    elif event.key == pygame.K_RETURN:
                        if self.cursorpos == 0:  # Talk option
                            if self.town_location == 0:  # In main town square
                                self.town_talk1 = True
                                town_ui = False
                        elif self.cursorpos == 1: # Inn
                            self.town_location = 1
                            town_ui = False
                        elif self.cursorpos == 2: # Slums
                            self.town_location = 2
                            town_ui = False
                        elif self.cursorpos == 3: # Leave
                            event_done = True
                            return "LEAVE"

                    if event.key == pygame.K_RCTRL:
                        if self.talking:
                            if self.text_box.progress_dialogue(self.dialogue):
                                self.talking = False
                                self.town_talk1 = True

            if self.town_location == 0:
                self.surface.blit(pygame.transform.scale(
                    self.town_bg_day, (1280, 720)), (0, 0))
                if town_ui:
                    self.draw_town(player_data)
                if self.town_talk1:
                    self.option_selector.drawUi(3, 'Citizen', 'Rich Lady', 'Drunk Man')
                if self.talking:
                    self.text_box.draw_textbox(self.dialogue, self.surface, (0, 400))

            if self.town_location == 1: # Inn
                # ... Inn logic ...
                # For now, just go back to town square
                self.town_location = 0
                town_ui = True
                
            if self.town_location == 2: # Slums
                # ... Slums logic ...
                self.town_location = 0
                town_ui = True

            self.clock.tick(60)
            pygame.display.update()

    def casino(self, player_data):
        # Casino logic
        pass
