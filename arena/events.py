import random
import pickle
import pygame
from data import gameui, pyganim, splashscreen

from arena.battle import NewBattle, SideBattle
from arena.data_loader import (
    animations,
    dialogues,
    item_data,
    item_data_shop,
    monster_data,
    sequences,
    skills,
    sound_effects,
)
from arena.player import Player
from arena.ui import MainUi, SelectOptions, Shop
from arena.utils import Timer, fadein, fadeout, posfinder
import arena.state as state

alphatext = "Alpha v4.2 - Story and the Town"


class GameEvents(MainUi):
    """Class for all special events in the game."""

    def __init__(self):
        MainUi.__init__(self)
        self.town_bg_day = pygame.image.load(
            "data/backgrounds/The Medieval Town.jpg"
        ).convert_alpha()
        self.town_bg_eve = pygame.image.load(
            "data/backgrounds/The Medieval Town_eve.jpg"
        ).convert_alpha()
        self.town_bg_ngt = pygame.image.load(
            "data/backgrounds/The Medieval Town_night.jpg"
        ).convert_alpha()
        self.inn_bg = pygame.image.load("data/backgrounds/inn.png").convert_alpha()
        self.townDialogue = 0  # Progress for the dialogue while in the town.
        self.arenaDialogue = 0
        self.timekeep = Timer()  # Used to time the events and things
        self.dialoguecontrol = False
        self.startEvent = False
        self.thudSound = pygame.mixer.Sound("data/sounds&music/thud.wav")
        self.thudSound.set_volume(0.05)
        self.applauseSound = pygame.mixer.Sound("data/sounds&music/Applause1.ogg")
        self.applauseSound.set_volume(0.05)
        self.bossRoar = pygame.mixer.Sound("data/sounds&music/Monster2.ogg")
        self.bossRoar.set_volume(0.05)
        self.arena_bg = pygame.image.load(
            "data/backgrounds/arenaDay.png"
        ).convert_alpha()
        self.arena_bg = pygame.transform.scale(self.arena_bg, (1280, 720))
        self.arena_bg_night = pygame.image.load(
            "data/backgrounds/arenaNight.png"
        ).convert_alpha()
        self.arena_bg_night = pygame.transform.scale(self.arena_bg_night, (1280, 720))
        self.boss_face1 = pygame.image.load("data/sprites/Boss1.png")
        self.town_location = 0  # 0-Centre 1-Bar/Inn 2-Slums
        self.game_clock = GameClock()
        self.option_selector = SelectOptions()
        self.town_talk1 = False  # Flag for drawing options menu for the 'Talk' Screen
        self.talking = False  # Flag to know if dialogue is currently being spoken
        self.talk_val = 0  # Used to know which option was chosen.
        self.text_box = gameui.TextBox()
        self.ui_text = gameui.UiText()
        self.ui_text.main_font_colour = (255, 255, 255)
        self.casino_state = ""  # Current state of the casino
        self.dialogue = [[]]  # Current Dialogue

    def town_first_visit(self, player_data):
        event_done = False
        pygame.mixer.music.load("data/sounds&music/Bustling_Streets.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        global surf
        global screen
        runningsound = pygame.mixer.Sound("data/sounds&music/Person_running.wav")
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
            state.curwidth, state.curheight = state.screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    state.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL and self.dialoguecontrol:
                        if self.txtbox.progress_dialogue():
                            self.townDialogue += 1
                    if choice_select:
                        self.txtbox.select_choice_inputs(event)
                    if event.key == pygame.K_RETURN and choice_select:
                        if self.txtbox.choice_cursor_pos == 0:  # Pay the girl
                            dialogue_choice = 0
                            dialogue_choice2 = 0
                            choice_select = False
                            self.townDialogue += 1
                            self.dialoguecontrol = True
                        if self.txtbox.choice_cursor_pos == 1:  # Refuse the girl
                            dialogue_choice = 1
                            dialogue_choice2 = 1
                            choice_select = False
                            self.townDialogue += 1
                            self.dialoguecontrol = True
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()

            state.surf.blit(
                pygame.transform.scale(
                    self.town_bg_day, (state.curwidth, state.curheight)
                ),
                (0, 0),
            )

            if not self.startEvent:
                if self.timekeep.timing() == 2 and self.townDialogue < 1:
                    self.startEvent = True
            if self.startEvent:
                self.townDialogue = 1
                self.startEvent = False
                self.dialoguecontrol = True

            if self.townDialogue == 1:
                self.txtbox.draw_textbox(
                    [
                        [
                            "",
                            "",
                            """The town that the Arena is situated in gets very lively this time of the year as this is when most of the challengers arrive.""",
                        ]
                    ],
                    state.surf,
                )
            elif self.townDialogue == 2:
                self.txtbox.draw_textbox(
                    [
                        [
                            "",
                            "",
                            """You\'ve been here before but never really got the chance to look around, so the sights of this place are still very unfamiliar to you.""",
                        ]
                    ],
                    state.surf,
                )
            elif self.townDialogue == 3:
                self.txtbox.draw_textbox(
                    [
                        [
                            "",
                            "",
                            "Even if you had been familiar with this place in the past, It would still have been difficult finding your way through this place as the town has changed dramatically over the course of a few years.",
                        ]
                    ],
                    state.surf,
                )
            elif self.townDialogue == 4:
                self.txtbox.draw_textbox(
                    [
                        [
                            "",
                            "",
                            """This is mostly due to the overwhelming popularity of the arena which has brought visitors from all over the country to this one location. This has let the town flourish and expand at a very quick pace, with new buildings and stores being built seemingly everyday.""",
                        ]
                    ],
                    state.surf,
                )
            elif self.townDialogue == 5:
                self.txtbox.draw_textbox(
                    [
                        [
                            "",
                            "",
                            """The presence and influence of the arena played a major role in the growth of the town, so much so that the people of the town decided to change it\'s old name and give it a new more fitting name, \"Arena Town\".""",
                        ]
                    ],
                    state.surf,
                )
            elif self.townDialogue == 6:
                runningsound.play()
                self.timekeep.reset()
                self.townDialogue += 1
                self.dialoguecontrol = False
            elif self.townDialogue == 7 and timedflag1:
                self.dialoguecontrol = True
                self.txtbox.draw_textbox(
                    [["", "", "You see a young girl running towards your direction."]],
                    state.surf,
                )
            elif self.townDialogue == 8:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/girl.png",
                            "???",
                            "Oh no, I'm so late, Grandpa's gonna get so mad!",
                        ]
                    ],
                    state.surf,
                )
                timedflag1 = False

            elif self.townDialogue == 9:
                self.thudSound.play()
                self.townDialogue += 1
                self.dialoguecontrol = False
                self.timekeep.reset()
            elif self.townDialogue == 10 and timedflag1:
                self.txtbox.draw_textbox(
                    [["data/sprites/girl.png", "???", "Ouch!"]], state.surf
                )
                self.dialoguecontrol = True
            elif self.townDialogue == 11:
                self.txtbox.draw_textbox(
                    [
                        [
                            "",
                            "",
                            "The girl crashes into you at full speed and topples over onto the gravel road.",
                        ]
                    ],
                    state.surf,
                )
            elif self.townDialogue == 12:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/girl.png",
                            "???",
                            "Hey, watch where you're going!",
                        ]
                    ],
                    state.surf,
                )

            elif self.townDialogue == 13:
                self.txtbox.draw_textbox(
                    [["", "", "The girl gets up and brushes off her skirt."]],
                    state.surf,
                )
            elif self.townDialogue == 14:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/girl.png",
                            "???",
                            "There's a tear in my new dress! What are you going to do about this?",
                        ]
                    ],
                    state.surf,
                )
                choice_select = True
                self.txtbox.choice_flag = True
            elif self.townDialogue == 15:
                self.txtbox.draw_textbox([["", "", "What do you do?"]], state.surf)
                self.txtbox.select_choice(
                    ["Offer to pay her money", "Ignore her and walk away"], state.surf
                )
                self.dialoguecontrol = False
            elif (
                dialogue_choice == 0 and self.townDialogue >= 16
            ):  # Pay money dialogue tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/girl.png",
                                "???",
                                "Oh you're willing to pay? I'm going to need atleast 150 gold for the dress.",
                            ]
                        ],
                        state.surf,
                    )
                    choice_select = True
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox([["", "", "Pay 150 gold?"]], state.surf)
                    self.txtbox.select_choice(["Pay her", "Don't Pay"], state.surf)
                    self.dialoguecontrol = False
                elif self.townDialogue >= 18 and dialogue_choice2 == 0:  # Pay her
                    if (
                        player_data.gold < 150 and not paid_girl
                    ):  # if player doesn't have enough gold
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox(
                                [
                                    [
                                        "data/sprites/girl.png",
                                        "???",
                                        "Hey you don't even have enough gold to pay me!",
                                    ]
                                ]
                            ), state.surf
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox(
                                [
                                    [
                                        "data/sprites/girl.png",
                                        "???",
                                        "Don't waste my time if you don't have any money!",
                                    ]
                                ]
                            ), state.surf
                        if self.townDialogue == 20:
                            self.townDialogue = 21
                            dialogue_choice2 = 1
                    else:
                        if not paid_girl:
                            player_data.gold -= 150
                            player_data.paid_girl_flag = True
                        paid_girl = True
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox(
                                [
                                    [
                                        "data/sprites/girl.png",
                                        "???",
                                        "Well, I guess this will have to do.",
                                    ]
                                ],
                                state.surf,
                            )
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox(
                                [
                                    [
                                        "data/sprites/girl.png",
                                        "???",
                                        "You better be careful next time! Be grateful that I let you off easily!",
                                    ]
                                ],
                                state.surf,
                            )
                        elif self.townDialogue == 20:
                            self.txtbox.draw_textbox(
                                [
                                    [
                                        "",
                                        "",
                                        """The girl walks away after glaring at you in the eye. You could have sworn you saw a smile for a second.""",
                                    ]
                                ],
                                state.surf,
                            )
                        elif self.townDialogue == 21:
                            self.txtbox.draw_textbox(
                                [["", "", "The girl disappears into the crowd."]],
                                state.surf,
                            )

                elif self.townDialogue >= 18 and dialogue_choice2 == 1:  # Don't pay her
                    if self.townDialogue == 18:
                        self.txtbox.draw_textbox(
                            [
                                [
                                    "data/sprites/girl.png",
                                    "???",
                                    "...You're not going to pay?",
                                ]
                            ],
                            state.surf,
                        )
                    if self.townDialogue == 19:
                        self.txtbox.draw_textbox(
                            [
                                [
                                    "data/sprites/girl.png",
                                    "???",
                                    "Tch.. he didn't fall for it",
                                ]
                            ],
                            state.surf,
                        )
                    elif self.townDialogue == 20:
                        self.txtbox.draw_textbox(
                            [
                                [
                                    "data/sprites/girl.png",
                                    "???",
                                    "Well don't waste my time then, get out of my way!",
                                ]
                            ],
                            state.surf,
                        )
                    elif self.townDialogue == 21:
                        self.txtbox.draw_textbox(
                            [
                                [
                                    "",
                                    "",
                                    "The girl storms off and disappears into the crowd.",
                                ]
                            ],
                            state.surf,
                        )
            elif dialogue_choice == 1 and self.townDialogue >= 16:  # ignore girl tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox(
                        [["data/sprites/girl.png", "???", "...."]], state.surf
                    )
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox(
                        [["data/sprites/girl.png", "???", "Don't just ignore me!"]],
                        state.surf,
                    )
                elif self.townDialogue == 18:
                    self.txtbox.draw_textbox(
                        [
                            [
                                "",
                                "",
                                """You continue ignoring the girl while she makes a commotion in the middle of the street and proceed to the Town.""",
                            ]
                        ],
                        state.surf,
                    )
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
            state.screen.blit(state.surf, (0, 0))
            self.timekeep.timing()
            state.clock.tick(60)
            fps = "FPS:%d" % state.clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def firstfloor_boss(self, name="Zen"):
        # Cutscene when challenging the first_floor boss
        event_done = False
        pygame.mixer.music.load("data/sounds&music/Dungeon3.ogg")
        global surf
        global screen
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
                    state.done = True
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

            state.surf.blit(self.arena_bg, (0, 0))
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
                self.txtbox.draw_textbox(
                    [["data/sprites/host_face.png", "Chance", "Ladies and gentlemen!"]],
                    state.surf,
                )

            elif self.arenaDialogue == 2:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "It seems like it's been ages since we've had a challenger strong enough to finally get to this point!",
                        ]
                    ],
                    state.surf,
                )
            elif self.arenaDialogue == 3:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "But we finally have him here, someone who is both brave and foolish enough to step up and fight his way through some of the most powerful monsters, to be able to stand before you at this very moment and face against what many would consider suicide! ",
                        ]
                    ],
                    state.surf,
                )
            elif self.arenaDialogue == 4:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "Please put your hands together for.. " + name + "!",
                        ]
                    ],
                    state.surf,
                )
                applause_flag2 = True
            elif self.arenaDialogue == 5:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "And his opponent.. A beast that has destroyed the dreams of many young adventurers, said to be the 'Gatekeeper' of the Arena.",
                        ]
                    ],
                    state.surf,
                )
            elif self.arenaDialogue == 6:
                self.txtbox.draw_textbox(
                    [["data/sprites/host_face.png", "Chance", "Introducing.. Tho'k!"]],
                    state.surf,
                )
                boss_roar = True

            elif self.arenaDialogue == 7:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/Boss1.png",
                            "Tho'k",
                            "RAAAAAAAAAAAAAAAAAARRGGHHHHHH!!!!!",
                        ]
                    ],
                    state.surf,
                )
                if boss_roar:
                    self.bossRoar.play()
                    self.timekeep.reset()
                    boss_roar = False
                    self.dialoguecontrol = False
                if self.timekeep.timing() == 2:
                    self.dialoguecontrol = True

            elif self.arenaDialogue == 8:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "Now, the time has come. "
                            + name
                            + ", I assume you are ready?",
                        ]
                    ],
                    state.surf,
                )
                self.txtbox.select_choice(
                    ["Yes, I am ready.", "I don't think I am."], state.surf
                )
                self.dialoguecontrol = False
                choice_select = True
                self.txtbox.choice_flag = True
            elif self.arenaDialogue == 9:
                if dialogue_choice == 0:
                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/host_face.png",
                                "Chance",
                                "Good! That's what I expected from you!",
                            ]
                        ],
                        state.surf,
                    )
                elif dialogue_choice == 1:
                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/host_face.png",
                                "Chance",
                                "Well unfortunately it's too late to turn back now!",
                            ]
                        ],
                        state.surf,
                    )
            elif self.arenaDialogue == 10:
                self.txtbox.draw_textbox(
                    [["data/sprites/host_face.png", "Chance", "It is time! Fight!"]],
                    state.surf,
                )
            elif self.arenaDialogue == 11:
                event_done = True
            state.screen.blit(state.surf, (0, 0))
            self.timekeep.timing()
            state.clock.tick(60)
            fps = "FPS:%d" % state.clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def first_floor_victory(self, dialogues):
        # Cutscene after beating the first_floor boss
        event_done = False
        pygame.mixer.music.load("data/sounds&music/Infinite_Arena.mp3")
        global surf
        global screen
        pygame.mixer_music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        pygame.mixer_music.play()
        phase = 0
        cur_song = "data/sounds&music/Infinite_Arena.mp3"
        draw_tb = False
        cur_dialogue = dialogues["first_floor_victory1"]
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if self.dialoguecontrol and event.key == pygame.K_RCTRL:
                        if self.txtbox.progress_dialogue(cur_dialogue):
                            phase += 1
                            draw_tb = False
                            self.timekeep.reset()
                            self.txtbox.reset()
                            self.dialoguecontrol = False
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer_music.load(cur_song)
                    pygame.mixer_music.set_volume(state.vol)
                    pygame.mixer_music.play()
                    pygame.mixer_music.set_endevent(pygame.constants.USEREVENT)
                if event.type == pygame.QUIT:
                    state.done = True
                    event_done = True
                    pygame.quit()
            if phase == 0:
                if self.timekeep.timing() > 2:
                    self.applauseSound.play()
                    phase += 1
            elif phase == 1:
                self.dialoguecontrol = True
                draw_tb = True
            elif phase == 2:
                if self.timekeep.timing() <= 1:
                    self.applauseSound.play()
                if self.timekeep.timing() > 2:
                    fadeout(state.surf, 0.01, fade_in=True, optional_bg=self.arena_bg)
                    phase += 1
                    self.timekeep.reset()
            elif phase == 3:
                if self.timekeep.timing() > 1:
                    cur_dialogue = dialogues["first_floor_victory2"]
                    self.dialoguecontrol = True
                    draw_tb = True
            elif phase == 4:
                pygame.mixer_music.fadeout(200)
                fadeout(state.surf, 0.01, fade_in=True, optional_bg=self.arena_bg_night)
                pygame.mixer_music.load("data/sounds&music/Dungeon 2.ogg")
                pygame.mixer_music.set_volume(state.vol)
                cur_song = "data/sounds&music/Dungeon 2.ogg"
                pygame.mixer_music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer_music.play()
                phase += 1
                self.timekeep.reset()
            elif phase == 5:
                if self.timekeep.timing() > 3:
                    cur_dialogue = dialogues["first_floor_victory3"]
                    phase += 1
            elif phase == 6:
                self.dialoguecontrol = True
                draw_tb = True
            elif phase == 7:
                if self.timekeep.timing() > 2:
                    pygame.mixer_music.fadeout(200)
                    fadeout(state.surf)
                    event_done = True
            if phase < 5:
                state.surf.blit(self.arena_bg, (0, 0))
            else:
                state.surf.blit(self.arena_bg_night, (0, 0))
            if draw_tb:
                self.txtbox.draw_textbox(cur_dialogue, state.surf)
            state.clock.tick(60)
            state.screen.blit(state.surf, (0, 0))
            pygame.display.set_caption("FPS:{}".format(int(state.clock.get_fps())))
            pygame.display.flip()

    def intro_scene(self, intro_dialogue):
        event_done = False
        pygame.mixer.music.load("data/sounds&music/Church.mp3")
        door_sound = pygame.mixer.Sound("data/sounds&music/Door1.ogg")
        door_sound.set_volume(0.05)
        gate_sound = pygame.mixer.Sound("data/sounds&music/Door4.ogg")
        gate_sound.set_volume(0.05)
        global surf
        global screen
        text_surf = pygame.Surface((1280, 720))
        text_surf.set_alpha(0)
        text_surf.set_colorkey((0, 0, 0))
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        draw_tb = False
        intro_level = 0
        pygame.mixer_music.play()
        text_x = 100
        text_y = 100
        text = ""
        dialogue = "intro1"
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    state.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL:
                        if self.dialoguecontrol:
                            if self.text_box.progress_dialogue(
                                intro_dialogue[dialogue]
                            ):
                                intro_level += 1
                                self.timekeep.reset()
                    if event.key == pygame.K_s:
                        if intro_level < 20:
                            intro_level = 20
            if intro_level < 24:
                state.surf.fill((0, 0, 0, 255))
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
                    (text_x, text_y), "My name is...", False, text_surf, 1
                )
                if self.timekeep.timing(1) > 5:
                    intro_level += 1
                    pygame.mixer_music.fadeout(3000)
                    self.timekeep.reset()
            elif intro_level == 22:
                if self.timekeep.timing(1) > 6:
                    fadein(255)
                    door_sound.play()
                    intro_level += 1
                    self.timekeep.reset()
            elif intro_level == 23:
                if self.timekeep.timing(1) > 2:
                    draw_tb = True
                    self.dialoguecontrol = True
            elif intro_level == 24:
                gate_sound.play()
                fadein(255, 0.01)
                intro_level += 1
                dialogue = "intro2"
                draw_tb = False
                self.text_box.reset()
                pygame.mixer_music.load("data/sounds&music/Infinite_Arena.mp3")
                pygame.mixer_music.set_volume(state.vol)
                pygame.mixer_music.play()
                self.timekeep.reset()
            elif intro_level == 25:
                state.surf.blit(self.arena_bg, (0, 0))
                if self.timekeep.timing(1) > 2:
                    draw_tb = True
            elif intro_level == 26:
                event_done = True
            self.ui_text.draw_text((text_x, text_y), text, False, text_surf)
            state.surf.blit(text_surf, (0, 0))
            if draw_tb:
                self.text_box.draw_textbox(
                    intro_dialogue[dialogue], state.surf, (0, 400)
                )
            state.screen.blit(state.surf, (0, 0))
            state.clock.tick(60)
            pygame.display.set_caption("FPS:{}".format(int(state.clock.get_fps())))
            pygame.display.flip()

    def town(self, player_data, dialogues):
        """The town and all the locations present in it."""
        if not player_data.town_first_flag:
            self.town_first_visit(player_data)
        event_done = False
        global surf
        global screen
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        town_ui = True
        if self.town_location == 0:
            area_music = "data/sounds&music/Bustling_Streets.mp3"
            pygame.mixer.music.load(area_music)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)
        self.town_location = 0
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    state.done = True
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
                            if (
                                self.option_selector.rowpos == 0
                                and self.option_selector.colpos == 0
                            ):  # Option 1
                                self.talk_val = 0
                                self.option_selector.alert_off(1)
                            elif (
                                self.option_selector.rowpos == 0
                                and self.option_selector.colpos == 1
                            ):  # Option 2
                                self.talk_val = 1
                                self.option_selector.alert_off(2)
                            elif (
                                self.option_selector.rowpos == 0
                                and self.option_selector.colpos == 2
                            ):  # Option 3
                                self.talk_val = 2
                                self.option_selector.alert_off(3)
                            elif (
                                self.option_selector.rowpos == 1
                                and self.option_selector.colpos == 0
                            ):  # Option 4
                                self.talk_val = 3
                                self.option_selector.alert_off(4)
                            elif (
                                self.option_selector.rowpos == 1
                                and self.option_selector.colpos == 1
                            ):  # Option 5
                                self.talk_val = 4
                                self.option_selector.alert_off(5)
                            elif (
                                self.option_selector.rowpos == 1
                                and self.option_selector.colpos == 2
                            ):  # Option 6
                                self.talk_val = 5
                                self.option_selector.alert_off(6)
                            elif (
                                self.option_selector.rowpos == 1
                                and self.option_selector.colpos == 3
                            ):  # Back Option
                                self.town_talk1 = False
                                town_ui = True

                        if player_data.progress == 2:
                            if self.talk_val == 0:
                                self.dialogue = dialogues["town1_citizen"]
                            elif self.talk_val == 1:
                                self.dialogue = dialogues["town1_richlady"]
                            elif self.talk_val == 2:
                                self.dialogue = dialogues["town1_drunkman"]

                    elif event.key == pygame.K_RETURN:
                        if self.cursorpos == 0:  # Talk option
                            if self.town_location == 0:  # In main town square
                                self.town_talk1 = True
                                town_ui = False

                    if event.key == pygame.K_RCTRL:
                        if self.talking:
                            if self.text_box.progress_dialogue(self.dialogue):
                                self.talking = False
                                self.town_talk1 = True
                                self.text_box.reset()
                        elif self.town_talk1 and not self.talking:
                            self.town_talk1 = False
                            town_ui = True
                elif event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()
            if self.town_location == 0:
                if self.game_clock.time_state == "Morning":
                    state.surf.blit(self.town_bg_day, (0, 0))
                elif self.game_clock.time_state == "Noon":
                    state.surf.blit(self.town_bg_eve, (0, 0))
                else:
                    state.surf.blit(self.town_bg_ngt, (0, 0))
                if town_ui:
                    self.draw_town(player_data)
                if self.town_talk1:
                    if player_data.progress == 2:
                        self.option_selector.drawUi(
                            3, "Citizen", "Rich Lady", "Drunk Man"
                        )
                    else:
                        self.option_selector.drawUi(3, "How'd", "This", "Happen?")
                if self.talking:
                    self.text_box.draw_textbox(self.dialogue, state.surf, (0, 400))
                state.screen.blit(state.surf, (0, 0))
            self.game_clock.pass_time(player_data, area_music)
            state.clock.tick(60)
            fps = "FPS:%d" % state.clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.flip()

    def casino(self, player_data):
        # The inn in the town
        event_done = False
        global surf
        global screen
        area_music = "data/sounds&music/2000_Shop3.ogg"
        pygame.mixer.music.load(area_music)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        casino_ui = True
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    state.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.cursorpos += 1
                    if event.key == pygame.K_UP:
                        self.cursorpos -= 1
                    if event.key == pygame.K_RETURN:
                        if self.cursorpos == 0:
                            pass
                        elif self.cursorpos == 1:
                            pass
                        elif self.cursorpos == 2:
                            self.casino_state = "casino"
                            casino_ui = False
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()
            state.surf.blit(self.inn_bg, (0, 0))
            if casino_ui:
                self.draw_casino(player_data)
            if self.casino_state == "casino":
                pass
            state.surf.blit(ab, (0, 0))
            state.screen.blit(state.surf, (0, 0))
            self.game_clock.pass_time(player_data, area_music)
            state.clock.tick(60)
            fps = "FPS:%d" % state.clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.flip()


class GameClock:

    def __init__(self):
        self.clockTime = Timer()
        self.curTime = 0
        self.bellflag = False
        self.fadeoutflag = False
        # Music to be played in the area
        self.area_music = "data/sounds&music/Infinite_Arena.mp3"
        # Bell sound during nighttime
        self.bell = pygame.mixer.Sound("data/sounds&music/Bell1.ogg")
        self.bell.set_volume(0.05)
        self.rooster = pygame.mixer.Sound(
            "data/sounds&music/Roost.ogg"
        )  # Morning sound
        self.rooster.set_volume(0.05)
        self.paused = False
        self.time_state = "Morning"  # The time of day

    def toggle_clock(self):  # Pauses/Unpauses the flow of ingame time
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def reset(self):
        self.clockTime.reset()

    def pass_time(
        self, player_details, area_music="data/sounds&music/Infinite_Arena.mp3"
    ):
        player = player_details
        self.area_music = area_music
        self.curTime = self.clockTime.timing()  # Current time
        if not self.paused:  # If clock is not paused
            if self.curTime >= 10:  # Every 10 seconds 30 minutes passes on the clock
                player.minutes += 30
                self.clockTime.reset()

        if player.minutes >= 60:  # Self-explanatory
            player.hours += 1
            player.minutes = 0
        if player.hours > 23:  # 24-hour clock
            player.hours = 0

        if player.hours >= 6 and player.hours < 14:  # Day
            self.time_state = "Morning"
            state.surf.blit(
                pygame.transform.scale(
                    state.arena_bg1, (state.curwidth, state.curheight)
                ),
                (0, 0),
            )

        if player.hours >= 14 and player.hours < 20:  # Afternoon
            self.time_state = "Noon"
            state.surf.blit(
                pygame.transform.scale(
                    state.arena_bg2, (state.curwidth, state.curheight)
                ),
                (0, 0),
            )

        if player.hours >= 20 or player.hours < 6:  # Night
            self.time_state = "Night"
            state.surf.blit(
                pygame.transform.scale(
                    state.arena_bg3, (state.curwidth, state.curheight)
                ),
                (0, 0),
            )

        if (player.hours == 19 and player.minutes == 30) and (
            not self.bellflag
        ):  # Music fading out
            if not self.fadeoutflag:
                pygame.mixer.music.fadeout(6000)  # 8 seconds
                self.fadeoutflag = True

                # Playing bell sound when it becomes night
        if (player.hours >= 20 or player.hours < 6) and (not self.bellflag):
            self.bell.play()
            Currentmusic = "data/sounds&music/night.mp3"
            pygame.mixer.music.stop()
            pygame.mixer.music.load(Currentmusic)
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
            self.bellflag = True

            # Playing rooster sound when it becomes day
        if (player.hours >= 6 and player.hours < 14) and self.bellflag:
            self.rooster.play()
            pygame.mixer.music.load(self.area_music)
            pygame.mixer.music.play()
            self.bellflag = False
            self.fadeoutflag = False


def run_game():
    inn_bg = pygame.image.load("data/backgrounds/inn.png").convert_alpha()
    logo = pygame.image.load(
        "data/backgrounds/logo3.png"
    ).convert_alpha()  # Main menu logo
    cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
    # New game screen background
    newgbg = pygame.image.load("data/backgrounds/Meadow.png").convert_alpha()
    loadsound = pygame.mixer.Sound("data/sounds&music/Load.ogg")
    loadsound.set_volume(0.05)
    cursorpos = 0
    Textbox = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()

    player = Player(item_data=item_data)
    eventManager = GameEvents()
    warrior = pyganim.PygAnimation(
        [
            ("data/sprites/idle1.png", 0.2),
            ("data/sprites/idle2.png", 0.2),
            ("data/sprites/idle3.png", 0.2),
        ]
    )

    mage = pyganim.PygAnimation(
        [
            ("data/sprites/midle1.png", 0.3),
            ("data/sprites/midle2.png", 0.3),
            ("data/sprites/midle3.png", 0.3),
        ]
    )

    castanim = [
        ("data/sprites/b1.png", 0.3),
        ("data/sprites/b2.png", 0.3),
        ("data/sprites/b3.png", 0.3),
    ]
    old_battler = SideBattle(
        monster_data,
        "mage",
        castanim,
        "data/backgrounds/Ruins2.png",
        "data/sounds&music/yousayrun2.mp3",
    )

    floor_talk = SelectOptions()  # Choices for 'Talk' in floor 1
    arena_shop = Shop(item_data_shop["arena_shop"])
    #####

    randbattle = 0
    timepassed = False  # Flag to check if the time passed or not
    newgtxtbox = 0
    pygame.mixer.music.load("data/sounds&music/Theme2.ogg")
    pygame.mixer.music.play()
    state.vol = 0.05
    state.surf = pygame.Surface((1366, 768))
    pygame.mixer.music.set_volume(state.vol)
    # I deeply apologize for the code below(and above)
    talked = False  # Ui flags
    options = False
    status = False
    shop = False
    system = False
    talking = False
    state.battle_choice = False
    state.post_battle = False  # After battle shenanigans
    state.controlui = True  # Flag to check if player can control ui
    talkval = 0
    text = pygame.font.Font("data/fonts/runescape_uf.ttf", 30)
    seltext = pygame.font.Font("data/fonts/runescape_uf.ttf", 40)
    secretbattle = SideBattle(
        monster_data,
        "warrior",
        castanim,
        "data/backgrounds/LavaCave.png",
        "data/sounds&music/Battle3.ogg",
        phealth=1000,
        pmana=100,
        pstr=1000,
        pstrmod=14,
        pdef=100,
        pmag=2000,
        pluck=9,
    )
    secretbattle.plevel = 50
    debugbattle = SideBattle(
        monster_data,
        "mage",
        castanim,
        "data/backgrounds/DemonicWorld.png",
        "data/sounds&music/Dungeon2.ogg",
        phealth=10000,
        pmana=1000,
        pstr=1000,
        pstrmod=14,
        pdef=100,
        pmag=2000,
        pluck=9,
    )
    debugbattle.plevel = 50
    healsound = pygame.mixer.Sound("data/sounds&music/Recovery.ogg")
    healsound.set_volume(0.05)
    mage.play()
    warrior.play()
    menutext = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40)
    ab = text.render(alphatext, False, (255, 255, 0))  # debug
    sel1 = seltext.render("Enter your name:", False, (255, 255, 0))
    sel2 = seltext.render("Press RCTRL to continue..", False, (255, 255, 0))
    MageDesc = seltext.render(
        "Mages are proficient at magic but weak physically.", False, (178, 57, 63)
    )
    WarDesc = seltext.render(
        "Warriors specialize in physical attacks and buffs.", False, (178, 57, 63)
    )
    clockTime = GameClock()  # Clock for the day/night system
    sel3 = seltext.render("Select your class:", False, secretbattle.txtcolor)
    sel4 = text.render("Mage", False, secretbattle.txtcolor)
    sel5 = text.render("Warrior", False, secretbattle.txtcolor)
    loadgamecolor = (255, 255, 0)
    nosavefile = True  # Check if a savefile is already present or not
    load_flag = False
    if not load_flag:
        try:
            rfile = open("savegame.dat", "rb")
            rfile.close()
            loadgamecolor = (255, 255, 0)
            nosavefile = False
            load_flag = True
        except:
            loadgamecolor = (105, 109, 114)
            nosavefile = True
            load_flag = True
    newgame = menutext.render("New Game", True, (255, 255, 0))  # Things for main menu
    loadgame = menutext.render("Load Game", True, loadgamecolor)
    quitgame = menutext.render("Quit Game", True, (255, 255, 0))
    namelist = [""]
    state.curwidth, state.curheight = state.screen.get_size()
    menubg1 = pygame.transform.scale(
        pygame.image.load("data/backgrounds/bg2.jpg").convert_alpha(),
        (state.curwidth, state.curheight),
    )
    arena_bg1 = pygame.image.load(
        "data/backgrounds/arenaDay.png"
    ).convert_alpha()  # day time arena
    arena_bg2 = pygame.image.load("data/backgrounds/arenaEvening.png").convert_alpha()
    arena_bg3 = pygame.image.load("data/backgrounds/arenaNight.png").convert_alpha()
    state.arena_bg1 = arena_bg1
    state.arena_bg2 = arena_bg2
    state.arena_bg3 = arena_bg3

    state.scene = "splash"
    state.drawui = True
    popup_message = ""
    Currentmusic = "data/sounds&music/Infinite_Arena.mp3"
    ui = MainUi()
    splash_screen = splashscreen.Splash(state.screen)
    splash_screen.toggle_splash()
    shh = []
    battler = NewBattle(
        monster_data, item_data, sound_effects, animations, skills, sequences
    )  # New battle tester
    bellflag = False  # Flag for bell sound to play during time change
    txtbox = gameui.TextBox()
    timer = Timer()
    fadeoutflag = False  # Flag for music to fade out

    while not state.done:
        # main

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # All the required controls
                posfinder()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and state.scene == "menu":
                    shh.append("b")

                    print(shh)
                if event.key == pygame.K_o and state.scene == "menu":
                    shh.append("o")
                    print(shh)
                if event.key == pygame.K_s and state.scene == "menu":
                    shh.append("s")
                    print(shh)
                if event.key == pygame.K_t and state.scene == "menu":
                    shh.append("t")
                    print(shh)
                if event.key == pygame.K_e and state.scene == "menu":
                    shh.append("e")
                    print(shh)
                if event.key == pygame.K_w and state.scene == "menu":
                    shh.append("w")
                    print(shh)
                if event.key == pygame.K_n and state.scene == "menu":
                    shh.append("n")
                    print(shh)
                if event.key == pygame.K_m and state.scene == "menu":
                    shh.append("m")
                    print(shh)
                if event.key == pygame.K_v and state.scene == "menu":
                    shh.append("v")
                    print(shh)
                if event.key == pygame.K_BACKSPACE and state.scene == "menu":
                    if shh != []:
                        shh.pop(0)
                    print(shh)
                if (
                    event.key == pygame.K_RETURN
                    and cursorpos == 0
                    and state.scene == "menu"
                ):  # newgame
                    pygame.mixer.music.stop()
                    loadsound.play()
                    fadeout(state.surf)
                    pygame.time.wait(1000)
                    pygame.mixer.music.load("data/sounds&music/Castle1.ogg")
                    pygame.mixer.music.play()
                    load_flag = False
                    state.scene = "new_game"

                if (
                    event.key == pygame.K_RETURN
                    and cursorpos == 1
                    and state.scene == "menu"
                ) and not nosavefile:  # load
                    try:
                        player = Player(item_data=item_data)
                        rfile = open("savegame.dat", "rb+")
                        pygame.mixer.music.stop()
                        loadsound.play()
                        player = pickle.load(rfile)
                        rfile.close()
                        fadein(255)
                        state.scene = "arena"
                        load_flag = False
                        ui.cursorpos = 9
                        pygame.mixer.music.load("data/sounds&music/Infinite_Arena.mp3")
                        pygame.mixer.music.play()
                    except FileNotFoundError:
                        print("Could not open")
                        popup_message = "Could not open save file!"
                        txtbox.toggle_popup_flag()

                if (
                    event.key == pygame.K_RETURN
                    and cursorpos == 2
                    and state.scene == "menu"
                ):  # quit
                    state.done = True
                if event.key == pygame.K_UP and state.scene == "menu":
                    secretbattle.cursorsound.play()
                    cursorpos -= 1
                if event.key == pygame.K_DOWN and state.scene == "menu":
                    cursorpos += 1
                    secretbattle.cursorsound.play()

                    # Keyboard entry for name.
                if event.key == pygame.K_q and state.scene == "new_game":
                    namelist.append("q")
                if event.key == pygame.K_w and state.scene == "new_game":
                    namelist.append("w")
                if event.key == pygame.K_e and state.scene == "new_game":
                    namelist.append("e")
                if event.key == pygame.K_r and state.scene == "new_game":
                    namelist.append("r")
                if event.key == pygame.K_t and state.scene == "new_game":
                    namelist.append("t")
                if event.key == pygame.K_y and state.scene == "new_game":
                    namelist.append("y")
                if event.key == pygame.K_u and state.scene == "new_game":
                    namelist.append("u")
                if event.key == pygame.K_i and state.scene == "new_game":
                    namelist.append("i")
                if event.key == pygame.K_o and state.scene == "new_game":
                    namelist.append("o")
                if event.key == pygame.K_p and state.scene == "new_game":
                    namelist.append("p")
                if event.key == pygame.K_a and state.scene == "new_game":
                    namelist.append("a")
                if event.key == pygame.K_s and state.scene == "new_game":
                    namelist.append("s")
                if event.key == pygame.K_d and state.scene == "new_game":
                    namelist.append("d")
                if event.key == pygame.K_f and state.scene == "new_game":
                    namelist.append("f")
                if event.key == pygame.K_g and state.scene == "new_game":
                    namelist.append("g")
                if event.key == pygame.K_h and state.scene == "new_game":
                    namelist.append("h")
                if event.key == pygame.K_j and state.scene == "new_game":
                    namelist.append("j")
                if event.key == pygame.K_k and state.scene == "new_game":
                    namelist.append("k")
                if event.key == pygame.K_l and state.scene == "new_game":
                    namelist.append("l")
                if event.key == pygame.K_z and state.scene == "new_game":
                    namelist.append("z")
                if event.key == pygame.K_x and state.scene == "new_game":
                    namelist.append("x")
                if event.key == pygame.K_c and state.scene == "new_game":
                    namelist.append("c")
                if event.key == pygame.K_v and state.scene == "new_game":
                    namelist.append("v")
                if event.key == pygame.K_b and state.scene == "new_game":
                    namelist.append("b")
                if event.key == pygame.K_n and state.scene == "new_game":
                    namelist.append("n")
                if event.key == pygame.K_m and state.scene == "new_game":
                    namelist.append("m")
                if event.key == pygame.K_BACKSPACE and state.scene == "new_game":
                    if len(namelist) > 0:
                        namelist.pop()
                if (event.key == pygame.K_RCTRL and state.scene == "new_game") and len(
                    namelist
                ) > 1:
                    state.scene = "new_game2"
                    name = "".join(namelist).capitalize()
                    player.name = name
                if event.key == pygame.K_LEFT and state.scene == "new_game2":
                    cursorpos -= 1
                if event.key == pygame.K_RIGHT and state.scene == "new_game2":
                    cursorpos += 1
                if (
                    event.key == pygame.K_RETURN
                    and state.scene == "new_game2"
                    and cursorpos == 0
                ):
                    player = Player(item_data=item_data)
                    player.name = name.capitalize()
                    player.pclass = "mage"
                    rfile = open("savegame.dat", "wb+")
                    state.scene = "new_game3"
                    pygame.mixer.music.stop()
                    try:
                        pickle.dump(player, rfile)
                        rfile.close()
                    except:
                        print("Could not create save file.")
                        pass
                    timer.reset()
                if (
                    event.key == pygame.K_RETURN
                    and state.scene == "new_game2"
                    and cursorpos == 1
                ):
                    player = Player(item_data=item_data)
                    player.name = name.capitalize()
                    player.pclass = "warrior"
                    rfile = open("savegame.dat", "wb+")
                    state.scene = "new_game3"
                    pygame.mixer.music.stop()
                    try:
                        pickle.dump(player, rfile)
                        rfile.close()
                    except EOFError:
                        print("Could not create save file.")
                        pass
                    timer.reset()
                if (
                    event.key == pygame.K_RCTRL
                    and (state.scene == "new_game3" or state.scene == "new_game4")
                    or state.scene == "credits"
                ):
                    newgtxtbox += 1
                if (
                    event.key == pygame.K_DOWN
                    and (state.scene == "arena" or state.scene == "inn")
                ) and state.controlui:
                    ui.cursorsound.play()
                    ui.cursorpos += 1

                if (
                    event.key == pygame.K_UP
                    and (state.scene == "arena" or state.scene == "inn")
                ) and state.controlui:
                    ui.cursorsound.play()
                    ui.cursorpos -= 1
                if (event.key == pygame.K_DOWN and state.scene == "arena") and system:
                    ui.cursorsound.play()
                    ui.syscursorpos += 1
                if (event.key == pygame.K_UP and state.scene == "arena") and system:
                    ui.cursorsound.play()
                    ui.syscursorpos -= 1
                if (
                    event.key == pygame.K_DOWN and state.scene == "arena"
                ) and state.battle_choice:
                    ui.cursorsound.play()
                    ui.batcursorpos += 1
                if (
                    event.key == pygame.K_UP and state.scene == "arena"
                ) and state.battle_choice:
                    ui.cursorsound.play()
                    ui.batcursorpos -= 1
                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 0)
                    and state.scene == "arena"
                    and state.controlui
                ):  # Talk option
                    options = True
                    drawUi = False
                    state.controlui = False
                    # So that it doesn't automatically pick the first option(input is annoying on pygame)
                    event.key = 1

                if (event.key == pygame.K_RCTRL and options) or (
                    event.key == pygame.K_RCTRL and talking
                ):
                    if ui.txtbox.progress_dialogue(ui.cur_dialogue):
                        state.drawui = True
                        state.controlui = True
                        ui.talked = False
                        options = False
                        talking = False

                if event.key == pygame.K_LEFT and options:  # Option screen control
                    floor_talk.colpos -= 1
                    ui.cursorsound.play()
                if event.key == pygame.K_RIGHT and options:
                    floor_talk.colpos += 1
                    ui.cursorsound.play()
                if event.key == pygame.K_UP and options:
                    floor_talk.rowpos -= 1
                    ui.cursorsound.play()
                if event.key == pygame.K_DOWN and options:
                    floor_talk.rowpos += 1
                    ui.cursorsound.play()
                if event.key == pygame.K_RETURN and options:
                    ui.txtbox.reset()
                    if floor_talk.rowpos == 0 and floor_talk.colpos == 0:  # Option 1
                        talkval = 0
                        options = False
                        talking = True
                        floor_talk.alert_off(1)
                    if floor_talk.rowpos == 0 and floor_talk.colpos == 1:  # Option 2
                        talkval = 1
                        options = False
                        talking = True
                        floor_talk.alert_off(2)
                    if floor_talk.rowpos == 0 and floor_talk.colpos == 2:  # Option 3
                        talkval = 2
                        options = False
                        talking = True
                        floor_talk.alert_off(3)
                    if floor_talk.rowpos == 1 and floor_talk.colpos == 0:  # Option 4
                        talkval = 3
                        options = False
                        talking = True
                        floor_talk.alert_off(4)
                    if floor_talk.rowpos == 1 and floor_talk.colpos == 1:  # Option 5
                        talkval = 4
                        options = False
                        talking = True
                        floor_talk.alert_off(5)
                    if floor_talk.rowpos == 1 and floor_talk.colpos == 2:  # Option 6
                        talkval = 5
                        options = False
                        talking = True
                        floor_talk.alert_off(6)
                    if floor_talk.rowpos == 1 and floor_talk.colpos == 3:  # Back
                        state.drawui = True
                        state.controlui = True
                        ui.talked = False
                        options = False
                        talking = False

                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 1)
                    and state.scene == "arena"
                    and state.controlui
                ):  # Battle option
                    state.drawui = False
                    state.controlui = False
                    state.battle_choice = True
                    ui.txtbox.reset()
                    ui.battalk = True
                    ui.batcursorpos = 4

                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 2)
                    and state.scene == "arena"
                    and state.controlui
                ):  # Status option
                    state.drawui = False
                    state.controlui = False
                    status = True
                    event.key = ""
                if status:
                    if event.key == pygame.K_RCTRL and (
                        not ui.equip_flag1 and not ui.equip_flag2 and not ui.stat_flag
                    ):
                        state.drawui = True
                        state.controlui = True
                        status = False
                    elif event.key == pygame.K_RETURN and ui.status_cur_pos == 2:
                        state.drawui = True
                        state.controlui = True
                        status = False
                    ui.handle_status_inputs(player, event)
                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 3)
                    and state.scene == "arena"
                    and state.controlui
                ):  # Shop option
                    state.drawui = False
                    state.controlui = False
                    arena_shop.txtbox.reset()
                    shop = True
                if (event.key == pygame.K_RCTRL and shop) and arena_shop.shopkeep:
                    if arena_shop.txtbox.progress_dialogue([[]]):
                        arena_shop.shopkeep = False
                        event.key = 0  # to stop pygame from being dumb
                if (event.key == pygame.K_RCTRL and shop) and not arena_shop.shopkeep:
                    if arena_shop.shop_selection_flag:
                        state.drawui = True
                        state.controlui = True
                        shop = False
                        arena_shop.shopkeep = True
                    else:
                        arena_shop.shop_selection_flag = True
                if (
                    (event.key == pygame.K_RETURN and shop)
                    and not arena_shop.shopkeep
                    and arena_shop.shop_selection_flag
                ):
                    if arena_shop.no_sell_flag:
                        secretbattle.buzzer.play()
                    else:
                        arena_shop.shop_selection_flag = False
                        event.key = 0
                if (event.key == pygame.K_LEFT and shop) and not arena_shop.shopkeep:
                    arena_shop.shop_cursor_pos1 -= 1
                if (event.key == pygame.K_RIGHT and shop) and not arena_shop.shopkeep:
                    arena_shop.shop_cursor_pos1 += 1
                if (event.key == pygame.K_DOWN and shop) and not arena_shop.shopkeep:
                    arena_shop.shop_cursor_pos2 += 1
                    """if (arena_shop.max_pos > arena_shop.min_pos + 5) and arena_shop.shop_cursor_pos2 == 5:
                        arena_shop.min_pos += 1"""
                if (event.key == pygame.K_UP and shop) and not arena_shop.shopkeep:
                    arena_shop.shop_cursor_pos2 -= 1
                    """if (arena_shop.max_pos >= arena_shop.min_pos + 5 and arena_shop.min_pos > 0) and arena_shop.shop_cursor_pos2 == 0:
                        arena_shop.min_pos -= 1"""
                if (
                    event.key == pygame.K_RETURN and shop
                ) and not arena_shop.shop_selection_flag:
                    if arena_shop.buy_item(
                        arena_shop.min_pos + arena_shop.shop_cursor_pos2
                    ):
                        # Buying item from shop
                        player.gold -= arena_shop.current_list[
                            arena_shop.min_pos + arena_shop.shop_cursor_pos2
                        ]["cost"]
                        if arena_shop.current_list == arena_shop.weapons_list:
                            player.wep_owned.append(
                                arena_shop.min_pos + arena_shop.shop_cursor_pos2
                            )
                        elif arena_shop.current_list == arena_shop.armour_list:
                            player.arm_owned.append(
                                arena_shop.min_pos + arena_shop.shop_cursor_pos2
                            )
                        elif arena_shop.current_list == arena_shop.acc_list:
                            player.acc_owned.append(
                                arena_shop.min_pos + arena_shop.shop_cursor_pos2
                            )
                        elif arena_shop.current_list == arena_shop.consume_list:
                            for consumable in arena_shop.consume_list:
                                if (
                                    consumable["id"]
                                    == arena_shop.min_pos + arena_shop.shop_cursor_pos2
                                ):
                                    if len(player.inventory) > 0:
                                        item_in_inventory = False
                                        for item in player.inventory:
                                            if item["name"] == consumable["name"]:
                                                item["amount"] += 1
                                                item_in_inventory = True
                                        if not item_in_inventory:
                                            player.inventory.append(
                                                {
                                                    "name": consumable["name"],
                                                    "amount": 1,
                                                }
                                            )
                                    else:
                                        player.inventory.append(
                                            {"name": consumable["name"], "amount": 1}
                                        )
                        player.update_stats()

                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 4)
                    and state.scene == "arena"
                    and state.controlui
                ):  # Inn option
                    pygame.mixer.music.pause()
                    fadein(255)
                    pygame.mixer.music.load("data/sounds&music/Town2.ogg")
                    pygame.mixer.music.play()
                    state.scene = "inn"
                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 5)
                    and state.scene == "arena"
                    and state.controlui
                ):  # System option
                    state.drawui = False
                    state.controlui = False
                    system = True
                    ui.syscursorpos = 4
                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 1)
                    and state.scene == "inn"
                    and state.controlui
                ):
                    if player.gold >= 20:  # rest
                        player.curhp = player.hp
                        player.curmp = player.mp
                        player.hours = 6  # Set time to 6:00 after resting at inn
                        player.minutes = 0
                        healsound.play()
                        fadein(255)
                        player.gold -= 20
                if (
                    (event.key == pygame.K_RETURN and ui.cursorpos == 2)
                    and state.scene == "inn"
                    and state.controlui
                ):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("data/sounds&music/Infinite_Arena.mp3")
                    fadein(255)
                    pygame.mixer.music.play()
                    state.scene = "arena"
                if (event.key == pygame.K_RETURN and ui.syscursorpos == 0) and system:
                    try:
                        rfile = open("savegame.dat", "wb+")
                        pickle.dump(player, rfile)
                        ui.savesound.play()
                        state.drawui = True
                        state.controlui = True
                        system = False
                        rfile.close()
                    except:
                        print("Could not create save file")
                if (event.key == pygame.K_RETURN and ui.syscursorpos == 1) and system:
                    state.done = True
                if (event.key == pygame.K_RETURN and ui.syscursorpos == 2) and system:
                    state.drawui = True
                    state.controlui = True
                    system = False

                if event.key == pygame.K_RCTRL and system:
                    state.drawui = True
                    state.controlui = True
                    system = False
                if (
                    event.key == pygame.K_RETURN and ui.batcursorpos == 0
                ) and state.battle_choice:
                    if player.progress == 1:
                        monster_list = ["rat", "snake", "hornet", "imp"]
                    elif player.progress == 2:
                        monster_list = ["skeleton", "zombie", "slime", "scorpion"]
                    randbattle = random.randrange(len(monster_list))
                    rand_mon = monster_list[randbattle]

                    battler.battle(rand_mon, player_data=player)
                    fight = battler.check_victory()
                    if fight:
                        player.fkills += 1
                        player.tkills += 1
                        state.battle_choice = False
                        state.post_battle = True
                        pygame.mixer.music.load("data/sounds&music/Infinite_Arena.mp3")
                        pygame.mixer.music.play()
                    else:
                        state.scene = "menu"
                        pygame.mixer_music.load("data/sounds&music/Theme2.ogg")
                        pygame.mixer_music.set_volume(0.1)
                        pygame.mixer_music.play()
                        state.battle_choice = False
                        state.post_battle = False
                        state.drawui = True
                        state.controlui = True
                        ui.pb_dialogue = False
                if (
                    event.key == pygame.K_RETURN and ui.batcursorpos == 1
                ) and state.battle_choice:
                    if player.fkills >= 5 and player.progress == 1:
                        fadein(255)
                        eventManager.firstfloor_boss(player.name)
                        battler.battle("floor_boss1", player, set_music=1)
                        if battler.check_victory():
                            eventManager.first_floor_victory(dialogues)
                            player.progress += 1
                            player.fkills = 0
                            state.battle_choice = False
                            state.post_battle = False
                            state.drawui = True
                            state.controlui = True
                            ui.pb_dialogue = False
                            state.scene = "arena"
                            player.hours = 6
                            player.minutes = 0
                            pygame.mixer.music.load(
                                "data/sounds&music/Infinite_Arena.mp3"
                            )
                            pygame.mixer.music.play()
                        else:
                            state.scene = "menu"
                            pygame.mixer_music.load("data/sounds&music/Theme2.ogg")
                            pygame.mixer_music.set_volume(0.1)
                            pygame.mixer_music.play()
                            state.battle_choice = False
                            state.post_battle = False
                            state.drawui = True
                            state.controlui = True
                            ui.pb_dialogue = False
                    else:
                        secretbattle.buzzer.play()
                if (
                    event.key == pygame.K_RETURN and ui.batcursorpos == 2
                ) and state.battle_choice:
                    state.drawui = True
                    state.controlui = True
                    state.battle_choice = False
                if (event.key == pygame.K_RCTRL and state.battle_choice) and ui.battalk:
                    if ui.txtbox.progress_dialogue([[]]):
                        ui.battalk = False
                if event.key == pygame.K_RCTRL and state.post_battle:
                    ui.pb_dialogue = False
                    state.post_battle = False
                    state.drawui = True
                    state.controlui = True

            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.load(Currentmusic)
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

        name = "".join(namelist)
        if state.scene == "splash":
            splash_screen.draw_splash(state.screen, event)
            fadeout(state.surf, fade_in=True, optional_bg=menubg1)
            state.scene = "menu"
        elif state.scene == "menu":  # Main menu of the game(What you see on start-up)
            state.surf.blit(menubg1, (0, 0))
            state.surf.blit(logo, (state.curwidth - 1100, state.curheight - 600))
            state.surf.blit(pygame.transform.scale(Textbox, (250, 180)), (450, 368))
            state.surf.blit(newgame, (474, 391))
            state.surf.blit(loadgame, (474, 431))
            state.surf.blit(quitgame, (474, 471))
            if shh == ["b", "o", "s", "s"] and state.scene == "menu":
                shh = []
                secretbattle.battle(
                    "secret_battle1", -10, False, bgm="data/sounds&music/Battle3.ogg"
                )
            if shh == ["t", "e", "s", "t"] and state.scene == "menu":
                shh = []
                Zen = Player()
                Zen.set_player_stats(
                    stre=1000, mag=2000, health=10000, mana=1000, luck=9, level=90
                )
                battler.battle("debug_fight", Zen, set_music=2)
            if shh == ["m", "o", "v", "e"] and state.scene == "menu":
                shh = []
                Zen = Player()
                Zen.set_player_stats(
                    stre=1000, mag=2000, health=10000, mana=1000, luck=9, level=90
                )
                battler.battle("move_tester", Zen, set_music=3)
            if shh == ["t", "o", "w", "n"] and state.scene == "menu":
                shh = []
                fadeout(state.surf)
                eventManager.town_first_visit(player)
                fadeout(state.surf)
                pygame.mixer_music.load(Currentmusic)
                pygame.mixer_music.play()
            if shh == ["t", "e", "t"] and state.scene == "menu":
                player.set_player_stats(level=20, health=1000, mana=1000)
                battler.battle("arena_wave_2", player)
                shh = []
            if shh == ["t", "o", "t"] and state.scene == "menu":
                player.town_first_flag = True
                player.progress = 2
                eventManager.town(player, dialogues)
                shh = []
            if shh == ["t", "s", "t"] and state.scene == "menu":
                eventManager.intro_scene(dialogues)
                shh = []
            if shh == ["t", "o", "s"] and state.scene == "menu":
                eventManager.casino(player)
                shh = []
            if cursorpos == 0:
                state.surf.blit(cursor, (434, 400))
            elif cursorpos == 1:
                state.surf.blit(cursor, (434, 443))
            elif cursorpos == 2:
                state.surf.blit(cursor, (434, 483))
            if cursorpos < 0:
                cursorpos = 2
            if cursorpos > 2:
                cursorpos = 0
        elif state.scene == "new_game":
            state.surf.blit(
                pygame.transform.scale(newgbg, (state.curwidth, state.curheight)),
                (0, 0),
            )
            sel1 = seltext.render(
                "Enter your name:" + name.capitalize(), False, secretbattle.txtcolor
            )
            if len(namelist) > 11:
                del namelist[len(namelist) - 1]
                secretbattle.buzzer.play()
            state.surf.blit(sel2, (500, 500))
            state.surf.blit(sel1, (300, 300))
            cursorpos = 0
        elif state.scene == "new_game2":
            state.surf.blit(
                pygame.transform.scale(newgbg, (state.curwidth, state.curheight)),
                (0, 0),
            )
            state.surf.blit(sel3, (300, 300))
            state.surf.blit(sel4, (300, 375))
            state.surf.blit(sel5, (778, 375))
            warrior.blit(state.surf, (778, 429))
            mage.blit(state.surf, (300, 435))
            if cursorpos == 0:
                player.stre = 10
                player.mag = 25
                player.defe = 15
                player.speed = 14
                statstxt = seltext.render(
                    "STR:%d MAG:%d DEF:%d LUCK:%d SPD:%d"
                    % (player.stre, player.mag, player.defe, player.luck, player.speed),
                    False,
                    (10, 33, 147),
                )
                state.surf.blit(cursor, (260, 375))
                state.surf.blit(MageDesc, (260, 45))
                state.surf.blit(statstxt, (260, 95))

            elif cursorpos == 1:
                player.stre = 20
                player.mag = 10
                player.defe = 20
                player.speed = 10
                statstxt = seltext.render(
                    "STR:%d MAG:%d DEF:%d LUCK:%d SPD:%d"
                    % (player.stre, player.mag, player.defe, player.luck, player.speed),
                    False,
                    (10, 33, 147),
                )
                state.surf.blit(cursor, (738, 375))
                state.surf.blit(WarDesc, (260, 45))
                state.surf.blit(statstxt, (260, 95))
            if cursorpos < 0:
                cursorpos = 1
            elif cursorpos > 1:
                cursorpos = 0
        elif state.scene == "new_game3":
            fadeout(state.surf, 0.01)
            eventManager = GameEvents()
            eventManager.intro_scene(dialogues)
            state.scene = "arena"
        elif state.scene == "arena":
            clockTime.pass_time(player)  # passage of ingame time
            if clockTime.time_state == "Morning":
                state.surf.blit(
                    pygame.transform.scale(
                        state.arena_bg1, (state.curwidth, state.curheight)
                    ),
                    (0, 0),
                )  # day bg
            elif clockTime.time_state == "Noon":
                state.surf.blit(
                    pygame.transform.scale(
                        state.arena_bg2, (state.curwidth, state.curheight)
                    ),
                    (0, 0),
                )  # Noon bg
            else:
                state.surf.blit(
                    pygame.transform.scale(
                        state.arena_bg3, (state.curwidth, state.curheight)
                    ),
                    (0, 0),
                )  # Night bg

            if state.drawui:
                ui.clock(player.hours, player.minutes)
                ui.arena(player.progress)
                if ui.cursorpos > 5:
                    ui.cursorpos = 0
                if ui.cursorpos < 0:
                    ui.cursorpos = 5
            if talking:
                ui.talk(talkval, player)
            if options:
                if player.progress == 1:
                    floor_talk.drawUi(4, "Old Man", "Boy", "Villager", "Stranger")
                elif player.progress == 2:
                    floor_talk.drawUi(4, "Old Man", "Boy", "Villager", "Pompous Noble")
            if status:
                ui.status(player, item_data)
            if shop:
                arena_shop.draw_shop("Arena Shop", player)
            if system:
                ui.system()
            if state.battle_choice:
                ui.battle_choice(player.fkills)
            if state.post_battle:
                ui.post_battle(player.progress)
        elif state.scene == "inn":
            state.surf.blit(
                pygame.transform.scale(inn_bg, (state.curwidth, state.curheight)),
                (0, 0),
            )
            if state.drawui:
                ui.draw_inn(player.gold)
            if ui.cursorpos > 2:
                ui.cursorpos = 0
            if ui.cursorpos < 0:
                ui.cursorpos = 2
        elif state.scene == "credits":
            state.surf.fill((0, 0, 0))

        timer.timing()
        state.surf.blit(ab, (0, 0))
        txtbox.popup_message(popup_message, state.surf)
        state.screen.blit(state.surf, (0, 0))
        pygame.display.update()
        state.clock.tick(60)
        fps = "FPS:%d" % state.clock.get_fps()
        pygame.display.set_caption(fps)
    pygame.quit()
