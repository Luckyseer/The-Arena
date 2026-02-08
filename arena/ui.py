import pygame
import random
from data import pyganim, gameui

from arena.data_loader import item_data, dialogues
from arena.player import Player
import arena.state as state


class MainUi:
    """The Main UI of the game(outside of battle.)"""

    def __init__(self):
        self.bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
        self.status_bg = pygame.transform.scale(self.bg, (900, 700)).convert_alpha()
        self.status_menu_bg = pygame.transform.scale(
            self.bg, (200, 300)
        ).convert_alpha()
        self.equip_menu_bg = pygame.transform.scale(self.bg, (330, 400)).convert_alpha()
        self.min_pos = 0
        self.max_pos = 0
        self.window_x = 1600
        self.equip_flag1 = False
        self.confirm = False
        self.equip_flag2 = False
        self.stat_flag = False
        self.cur_id = 0  # The current id of the equipment being hovered in the change equip window
        self.status_cur_pos = 0
        self.equip_cursor1_pos = 0
        self.equip_cursor2_pos = 0
        self.stat_cursor_pos = 0
        self.orig_stat_points = 0
        self.orig_str = 0
        self.orig_def = 0
        self.orig_mag = 0
        self.txtcolor = (21, 57, 114)
        self.txtcolor2 = (117, 17, 67)
        self.txtcolor3 = (23, 18, 96)
        self.uitext = pygame.font.Font("data/fonts/runescape_uf.ttf", 35)
        # Smaller font for longer sentences
        self.uitext2 = pygame.font.Font("data/fonts/runescape_uf.ttf", 25)
        self.cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.cursor_down = pygame.transform.rotate(self.cursor, -90)
        self.cursor_up = pygame.transform.rotate(self.cursor, 90)
        self.cursor_left = pygame.transform.rotate(self.cursor, 180)
        self.cursorsound = pygame.mixer.Sound("data/sounds&music/Cursor1.ogg")
        self.cursorsound.set_volume(0.05)
        self.cursorpos = 0
        self.equip_txt = self.uitext.render("Equipment", False, self.txtcolor)
        self.buzzer_sound = pygame.mixer.Sound("data/sounds&music/Buzzer1.ogg")
        self.buzzer_sound.set_volume(0.05)
        self.stats_txt = self.uitext.render("Stats", False, self.txtcolor)
        self.talktxt = self.uitext.render("Talk", False, self.txtcolor)
        self.casino_text = self.uitext.render("Gamble", False, self.txtcolor)
        self.talkdesc = self.uitext.render(
            "Talk with people around the Arena.", False, self.txtcolor
        )
        self.talkdesc2 = self.uitext.render(
            "Talk with people around the Inn.", False, self.txtcolor
        )
        self.casino_desc = self.uitext.render(
            "Play the dice game.", False, self.txtcolor
        )
        self.talkdesc3 = self.uitext.render(
            "Talk with people around the Town.", False, self.txtcolor
        )
        self.battxt = self.uitext.render("Battle", False, self.txtcolor)
        self.batdesc = self.uitext.render(
            "Battle monsters in the Arena.", False, self.txtcolor
        )
        self.systxt = self.uitext.render("System", False, self.txtcolor)
        self.sysdesc = self.uitext.render("System options.", False, self.txtcolor)
        self.inntxt = self.uitext.render("Inn", False, self.txtcolor)
        self.inndesc = self.uitext.render("Go to the Inn.", False, self.txtcolor)
        self.shoptxt = self.uitext.render("Shop", False, self.txtcolor)
        self.slumstxt = self.uitext.render("Slums", False, self.txtcolor)
        self.slumsdesc = self.uitext.render("Go to the Slums.", False, self.txtcolor)
        self.shopdesc = self.uitext.render(
            "Buy items/equipment to use in the Arena.", False, self.txtcolor
        )
        self.stattxt = self.uitext.render("Status", False, self.txtcolor)
        self.statdesc = self.uitext.render(
            "Check player status/equipment", False, self.txtcolor
        )
        self.backtxt = self.uitext.render("Leave", False, self.txtcolor)
        self.back_txt = self.uitext.render("Back", False, self.txtcolor)
        self.backdesc = self.uitext.render("Return to the Arena", False, self.txtcolor)
        self.sleeptxt = self.uitext.render("Rest", False, self.txtcolor)
        self.sleepdesc = self.uitext.render(
            "Spend the night at the Inn. (20 Gold)", False, self.txtcolor
        )
        self.txtbox = gameui.TextBox()
        self.statustxt = self.uitext.render("- STATUS -", True, self.txtcolor)
        self.face = pygame.image.load("data/sprites/f1.png").convert_alpha()
        self.wepicon = pygame.image.load("data/sprites/wepicon.png").convert_alpha()
        self.armicon = pygame.image.load("data/sprites/armicon.png").convert_alpha()
        self.accicon = pygame.image.load("data/sprites/accicon.png").convert_alpha()
        self.sunIcon = pygame.image.load(
            "data/sprites/sun.png"
        ).convert_alpha()  # Icon for clock
        self.eveIcon = pygame.image.load(
            "data/sprites/eve.png"
        ).convert_alpha()  # Icon for clock
        self.moonIcon = pygame.image.load(
            "data/sprites/moon.png"
        ).convert_alpha()  # Icon for clock
        self.talked = False
        self.coinAnim = pyganim.PygAnimation(
            [
                ("data/sprites/coin1.png", 0.1),
                ("data/sprites/coin2.png", 0.1),
                ("data/sprites/coin3.png", 0.1),
                ("data/sprites/coin4.png", 0.1),
                ("data/sprites/coin5.png", 0.1),
                ("data/sprites/coin6.png", 0.1),
                ("data/sprites/coin7.png", 0.1),
                ("data/sprites/coin8.png", 0.1),
                ("data/sprites/coin9.png", 0.1),
            ]
        )
        self.coinAnim.play()
        self.shopkeep = True
        self.loaditems = False
        self.item_desc = ""
        self.buysound = pygame.mixer.Sound("data/sounds&music/Shop1.ogg")
        self.buysound.set_volume(0.05)
        self.equip_sound = pygame.mixer.Sound("data/sounds&music/Open1.ogg")
        self.equip_sound.set_volume(0.05)
        self.Talk = -1
        self.sysopt1 = self.uitext.render("Save Game", False, self.txtcolor)
        self.sysopt2 = self.uitext.render("Quit Game", False, self.txtcolor)
        self.sysopt3 = self.uitext.render("Cancel", False, self.txtcolor)
        self.syscursorpos = 0
        self.savesound = pygame.mixer.Sound("data/sounds&music/Save.ogg")
        self.savesound.set_volume(0.05)
        self.batopt1 = self.uitext.render("Fight a regular enemy", False, self.txtcolor)
        self.battalk = True
        self.batcursorpos = False
        self.popup_message = ""
        self.pb_dialogue = False
        self.pbtalk = 0
        self.cur_dialogue = [[]]  # Current dialogue in talk

    def arena(self, floor=1):  # Main ui in the arena
        state.surf.blit(
            pygame.transform.scale(self.bg, (int(state.curwidth / 1.5), 300)), (0, 430)
        )
        state.surf.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 48))
        state.surf.blit(pygame.transform.scale(self.bg, (300, 300)), (905, 430))
        state.surf.blit(self.talktxt, (946, 496))
        state.surf.blit(self.battxt, (946, 526))
        state.surf.blit(self.stattxt, (946, 556))
        state.surf.blit(self.shoptxt, (946, 586))
        state.surf.blit(self.inntxt, (946, 616))
        state.surf.blit(self.systxt, (946, 646))
        self.cur = self.uitext.render(
            "Floor:  %d" % floor, False, self.txtcolor
        )  # Current floor
        state.surf.blit(self.cur, (27, 61))
        if self.cursorpos == 0:
            state.surf.blit(self.cursor, (916, 496))
            state.surf.blit(self.talkdesc, (112, 490))
        if self.cursorpos == 1:
            state.surf.blit(self.cursor, (916, 526))
            state.surf.blit(self.batdesc, (112, 490))
        if self.cursorpos == 2:
            state.surf.blit(self.cursor, (916, 556))
            state.surf.blit(self.statdesc, (112, 490))
        if self.cursorpos == 3:
            state.surf.blit(self.cursor, (916, 586))
            state.surf.blit(self.shopdesc, (112, 490))
        if self.cursorpos == 4:
            state.surf.blit(self.cursor, (916, 616))
            state.surf.blit(self.inndesc, (112, 490))
        if self.cursorpos == 5:
            state.surf.blit(self.cursor, (916, 646))
            state.surf.blit(self.sysdesc, (112, 490))

    def clock(self, hours, minutes):  # draw ui for the clock
        if minutes == 0:
            minutes = "00"  # Double zeros because that's how clocks work
        timetxt = str(hours) + ":" + str(minutes)
        self.time = self.uitext.render(timetxt, False, self.txtcolor)
        state.surf.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 81))
        state.surf.blit(self.time, (27, 94))
        if hours >= 6 and hours < 14:  # Day
            state.surf.blit(pygame.transform.scale(self.sunIcon, (40, 30)), (90, 93))
        if hours >= 14 and hours < 20:  # Afternoon
            state.surf.blit(pygame.transform.scale(self.eveIcon, (20, 30)), (90, 93))
        if hours >= 20 or hours < 6:  # Night
            state.surf.blit(pygame.transform.scale(self.moonIcon, (35, 25)), (90, 97))

    def talk(self, val, player):
        state.drawui = False
        self.Talk = val
        if not self.talked:
            if player.progress == 1:
                self.cur_dialogue = [
                    []
                ]  # These are converted from the old textbox, so for compatibility
                if self.Talk == 0:
                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/oldman.png",
                                "Old Man",
                                "I heard the monsters on the first floor are quite weak. You mustn't underestimate them However!\nConsider Equipping yourself with new equipment from the Shop.",
                            ]
                        ],
                        state.surf,
                        (0, 400),
                    )
                elif self.Talk == 1:

                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/boy.png",
                                "Boy",
                                "Wow mister, you're going to fight in the Arena? So cool!",
                            ]
                        ],
                        state.surf,
                        (0, 400),
                    )

                elif self.Talk == 2:

                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/youngman.png",
                                "Young Man",
                                "In the 50 years that the Arena has been open, there has been only one winner. It was the legendary Hero known as Zen. That was 2 years ago though, nobody has seen him since.",
                            ]
                        ],
                        state.surf,
                        (0, 400),
                    )
                elif self.Talk == 3:
                    self.txtbox.draw_textbox(
                        [
                            [
                                "data/sprites/mysteryman.png",
                                "Stranger",
                                "You...\nNevermind. Good luck in the Arena, I'll be keeping an eye on you.",
                            ]
                        ],
                        state.surf,
                        (0, 400),
                    )
            elif player.progress == 2:
                if self.Talk == 0:
                    self.cur_dialogue = dialogues["floor2_oldman"]
                    self.txtbox.draw_textbox(self.cur_dialogue, state.surf, (0, 400))
                elif self.Talk == 1:
                    self.cur_dialogue = dialogues["floor2_boy"]
                    self.txtbox.draw_textbox(self.cur_dialogue, state.surf, (0, 400))
                elif self.Talk == 2:
                    if player.pclass == "mage":
                        self.cur_dialogue = dialogues["floor2_youngman_m"]
                    else:
                        self.cur_dialogue = dialogues["floor2_youngman_w"]
                    self.txtbox.draw_textbox(self.cur_dialogue, state.surf, (0, 400))
                elif self.Talk == 3:
                    self.cur_dialogue = dialogues["floor2_noble"]
                    self.txtbox.draw_textbox(self.cur_dialogue, state.surf, (0, 400))

    def status(self, player, item_data=item_data):
        state.surf.blit(self.status_bg, (53, 30))
        nametxt = self.uitext.render("Name: " + player.name, False, self.txtcolor)
        state.surf.blit(nametxt, (169, 200))
        stats_y = 235
        stats_step = 32
        str_y = stats_y
        def_y = stats_y + stats_step
        mag_y = stats_y + stats_step * 2
        spd_y = stats_y + stats_step * 3
        luck_y = stats_y + stats_step * 4
        strtxt = self.uitext.render("STR: %d" % player.stre, False, self.txtcolor)
        if player.add_stre > 0:
            strtxt2 = self.uitext.render("(+%d)" % player.add_stre, False, (0, 200, 0))
        elif player.add_stre == 0:
            strtxt2 = self.uitext.render(
                "(%d)" % player.add_stre, False, (95, 100, 100)
            )
        else:
            strtxt2 = self.uitext.render("(+%d)" % player.add_stre, False, (200, 0, 0))
        stat_points = self.uitext.render(
            "Stat points: %d" % player.stat_points, False, (46, 69, 184)
        )
        state.surf.blit(stat_points, (430, str_y))
        state.surf.blit(strtxt, (169, str_y))
        state.surf.blit(strtxt2, (299, str_y))
        deftxt = self.uitext.render("DEF: %d" % player.defe, False, self.txtcolor)
        if player.add_defe > 0:
            deftxt2 = self.uitext.render("(+%d)" % player.add_defe, False, (0, 200, 0))
        elif player.add_defe == 0:
            deftxt2 = self.uitext.render(
                "(+%d)" % player.add_defe, False, (95, 100, 100)
            )
        else:
            deftxt2 = self.uitext.render("(%d)" % player.add_defe, False, (200, 0, 0))
        state.surf.blit(deftxt, (169, def_y))
        state.surf.blit(deftxt2, (299, def_y))
        lucktxt = self.uitext.render("LUCK: %d" % player.luck, False, self.txtcolor)
        state.surf.blit(lucktxt, (169, luck_y))
        magtxt = self.uitext.render("MAG: %d" % player.mag, False, self.txtcolor)
        if player.add_mag > 0:
            magtxt2 = self.uitext.render("(+%d)" % player.add_mag, False, (0, 200, 0))
        elif player.add_mag == 0:
            magtxt2 = self.uitext.render(
                "(+%d)" % player.add_mag, False, (95, 100, 100)
            )
        else:
            magtxt2 = self.uitext.render("(%d)" % player.add_mag, False, (200, 0, 0))
        state.surf.blit(magtxt, (169, mag_y))
        state.surf.blit(magtxt2, (299, mag_y))
        spdtxt = self.uitext.render("SPD: %d" % player.speed, False, self.txtcolor)
        if player.add_speed > 0:
            spdtxt2 = self.uitext.render("(+%d)" % player.add_speed, False, (0, 200, 0))
        elif player.add_speed == 0:
            spdtxt2 = self.uitext.render(
                "(+%d)" % player.add_speed, False, (95, 100, 100)
            )
        else:
            spdtxt2 = self.uitext.render("(%d)" % player.add_speed, False, (200, 0, 0))
        state.surf.blit(spdtxt, (169, spd_y))
        state.surf.blit(spdtxt2, (299, spd_y))
        lvltxt = self.uitext.render("Level: %d" % player.level, False, self.txtcolor2)
        state.surf.blit(lvltxt, (607, 396))
        xp_txt = self.uitext2.render(
            "Exp till next level: {}".format(
                player.xp_till_levelup(player.level) - player.exp
            ),
            False,
            self.txtcolor2,
        )
        state.surf.blit(xp_txt, (607, 426))
        state.surf.blit(self.face, (679, 207))
        classtxt = self.uitext.render(player.pclass.capitalize(), False, self.txtcolor)
        state.surf.blit(classtxt, (697, 366))
        state.surf.blit(self.statustxt, (417, 141))
        weptxt = self.uitext2.render(
            "WEAPON: " + item_data["weapons"][player.cur_weapon]["name"],
            False,
            self.txtcolor2,
        )
        armtxt = self.uitext2.render(
            "ARMOR: " + item_data["armours"][player.cur_armour]["name"],
            False,
            self.txtcolor2,
        )
        acctxt = self.uitext2.render(
            "ACCESSORY: " + item_data["accessories"][player.cur_accessory]["name"],
            False,
            self.txtcolor2,
        )
        equip_y = luck_y + 40
        state.surf.blit(self.wepicon, (169, equip_y))
        state.surf.blit(weptxt, (209, equip_y))
        state.surf.blit(self.armicon, (169, equip_y + 40))
        state.surf.blit(armtxt, (209, equip_y + 40))
        state.surf.blit(self.accicon, (169, equip_y + 80))
        state.surf.blit(acctxt, (209, equip_y + 80))
        floorktxt = self.uitext.render(
            "Enemies killed on this floor: %d" % player.fkills, False, self.txtcolor3
        )
        totktxt = self.uitext.render(
            "Total enemies killed: %d" % player.tkills, False, self.txtcolor3
        )
        state.surf.blit(floorktxt, (169, 527))
        state.surf.blit(totktxt, (168, 567))
        self.status_menu(player)
        self.txtbox.popup_message(self.popup_message, state.surf)

    def change_equipment(self, player=Player(), item_data=item_data):
        state.surf.blit(self.equip_menu_bg, (self.window_x, 45))
        if self.window_x > 955:
            self.window_x -= 55
        if self.equip_cursor2_pos > self.max_pos - 1 or self.equip_cursor2_pos > 4:
            if self.min_pos + 5 < self.max_pos:
                self.min_pos += 1
                self.equip_cursor2_pos = 4
            else:
                self.min_pos = 0
                self.equip_cursor2_pos = 0
        if self.equip_cursor2_pos < 0:
            if self.min_pos != 0:
                self.min_pos -= 1
                self.equip_cursor2_pos = 0
            else:
                if self.max_pos - 1 < 4:
                    self.min_pos = 0
                    self.equip_cursor2_pos = self.max_pos - 1
                else:
                    self.min_pos = self.max_pos - 5
                    self.equip_cursor2_pos = 4
        if self.equip_cursor1_pos == 0:
            self.max_pos = len(player.wep_owned)
            if len(player.wep_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        for weapon in item_data["weapons"]:
                            if weapon["id"] == player.wep_owned[i]:
                                state.surf.blit(
                                    self.uitext.render(
                                        weapon["name"], False, self.txtcolor
                                    ),
                                    (980, 110 + 55 * (i - self.min_pos)),
                                )
                self.cur_id = player.wep_owned[self.min_pos + self.equip_cursor2_pos]
                if self.min_pos != 0:
                    state.surf.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    state.surf.blit(self.cursor_down, (1085, 360))

            else:
                no_item = True
                self.item_desc = ""
                state.surf.blit(
                    self.uitext.render("No weapons owned", False, self.txtcolor),
                    (980, 110),
                )
        elif self.equip_cursor1_pos == 1:
            self.max_pos = len(player.arm_owned)
            if len(player.arm_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        for armour in item_data["armours"]:
                            if armour["id"] == player.arm_owned[i]:
                                state.surf.blit(
                                    self.uitext.render(
                                        armour["name"], False, self.txtcolor
                                    ),
                                    (980, 110 + 55 * (i - self.min_pos)),
                                )
                self.cur_id = player.arm_owned[self.min_pos + self.equip_cursor2_pos]
                if self.min_pos != 0:
                    state.surf.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    state.surf.blit(self.cursor_down, (1085, 360))
            else:
                no_item = True
                state.surf.blit(
                    self.uitext.render("No armours owned", False, self.txtcolor),
                    (980, 110),
                )
        elif self.equip_cursor1_pos == 2:
            self.max_pos = len(player.acc_owned)
            if len(player.acc_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        for acc in item_data["accessories"]:
                            if acc["id"] == player.acc_owned[i]:
                                state.surf.blit(
                                    self.uitext.render(
                                        acc["name"], False, self.txtcolor
                                    ),
                                    (980, 110 + 55 * (i - self.min_pos)),
                                )
                self.cur_id = player.acc_owned[self.min_pos + self.equip_cursor2_pos]
                if self.min_pos != 0:
                    state.surf.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    state.surf.blit(self.cursor_down, (1085, 360))
            else:
                no_item = True
                self.item_desc = ""
                state.surf.blit(
                    self.uitext.render("No accessories owned", False, self.txtcolor),
                    (980, 110),
                )
        if self.equip_flag2:
            if self.equip_cursor2_pos == 0:
                state.surf.blit(self.cursor, (940, 110))
            elif self.equip_cursor2_pos == 1:
                state.surf.blit(self.cursor, (940, 170))
            elif self.equip_cursor2_pos == 2:
                state.surf.blit(self.cursor, (940, 225))
            elif self.equip_cursor2_pos == 3:
                state.surf.blit(self.cursor, (940, 280))
            elif self.equip_cursor2_pos == 4:
                state.surf.blit(self.cursor, (940, 335))
            if self.equip_cursor1_pos == 0:
                cur_desc = item_data["weapons"]
            elif self.equip_cursor1_pos == 1:
                cur_desc = item_data["armours"]
            elif self.equip_cursor1_pos == 2:
                cur_desc = item_data["accessories"]
            if not no_item:
                self.item_desc = self.uitext2.render(
                    cur_desc[self.cur_id]["description"], False, self.txtcolor2
                )
                hover_item_str = self.uitext2.render(
                    "STR:" + str(cur_desc[self.cur_id]["atk"]), False, self.txtcolor2
                )
                hover_item_def = self.uitext2.render(
                    "DEF:" + str(cur_desc[self.cur_id]["def"]), False, self.txtcolor2
                )
                hover_item_mag = self.uitext2.render(
                    "MAG:" + str(cur_desc[self.cur_id]["mag"]), False, self.txtcolor2
                )
                state.surf.blit(self.item_desc, (120, 620))
                state.surf.blit(hover_item_str, (605, 500))
                state.surf.blit(hover_item_def, (605, 540))
                state.surf.blit(hover_item_mag, (605, 580))

    def stat_point_alloc(self, player=Player()):
        if self.stat_cursor_pos == 0:
            state.surf.blit(self.cursor, (255, 250))
            state.surf.blit(self.cursor_left, (135, 247))
        elif self.stat_cursor_pos == 1:
            state.surf.blit(self.cursor, (255, 290))
            state.surf.blit(self.cursor_left, (135, 287))
        elif self.stat_cursor_pos == 2:
            state.surf.blit(self.cursor, (265, 330))
            state.surf.blit(self.cursor_left, (135, 327))
        if self.stat_cursor_pos > 2:
            self.stat_cursor_pos = 0
        elif self.stat_cursor_pos < 0:
            self.stat_cursor_pos = 2
        if self.confirm:
            self.txtbox.confirm_box("Confirm Changes?", state.surf)

    def status_menu(self, player=Player()):
        state.surf.blit(self.status_menu_bg, (955, 405))
        state.surf.blit(self.equip_txt, (990, 465))
        state.surf.blit(self.stats_txt, (990, 505))
        state.surf.blit(self.back_txt, (990, 545))
        if self.status_cur_pos == 0:
            state.surf.blit(self.cursor, (950, 465))
        elif self.status_cur_pos == 1:
            state.surf.blit(self.cursor, (950, 505))
        elif self.status_cur_pos == 2:
            state.surf.blit(self.cursor, (950, 545))
        if self.equip_flag1:
            if self.equip_cursor1_pos == 0:
                state.surf.blit(self.cursor, (140, 410))
            elif self.equip_cursor1_pos == 1:
                state.surf.blit(self.cursor, (140, 450))
            elif self.equip_cursor1_pos == 2:
                state.surf.blit(self.cursor, (140, 490))
        if self.status_cur_pos > 2:
            self.status_cur_pos = 0
        if self.status_cur_pos < 0:
            self.status_cur_pos = 2
        if self.equip_cursor1_pos > 2:
            self.equip_cursor1_pos = 0
        if self.equip_cursor1_pos < 0:
            self.equip_cursor1_pos = 2
        if self.equip_flag1:
            self.change_equipment(player)
        if self.stat_flag:
            self.stat_point_alloc(player)

    def handle_status_inputs(self, player=Player(), event=None):
        if event is None:
            return
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.cursorsound.play()
                if not self.equip_flag1 and not self.equip_flag2 and not self.stat_flag:
                    self.status_cur_pos += 1
                elif self.equip_flag1 and not self.equip_flag2:
                    self.equip_cursor1_pos += 1
                elif self.equip_flag2 and self.equip_flag1:
                    self.equip_cursor2_pos += 1
                elif self.stat_flag:
                    self.stat_cursor_pos += 1
            elif event.key == pygame.K_UP:
                self.cursorsound.play()
                if not self.equip_flag1 and not self.equip_flag2 and not self.stat_flag:
                    self.status_cur_pos -= 1
                elif self.equip_flag1 and not self.equip_flag2:
                    self.equip_cursor1_pos -= 1
                elif self.equip_flag2 and self.equip_flag1:
                    self.equip_cursor2_pos -= 1
                elif self.stat_flag:
                    self.stat_cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self.stat_flag:
                    if player.stat_points > 0:
                        if self.stat_cursor_pos == 0:
                            player.stre += 1
                            player.stat_points -= 1
                        elif self.stat_cursor_pos == 1:
                            player.defe += 1
                            player.stat_points -= 1
                        elif self.stat_cursor_pos == 2:
                            player.mag += 1
                            player.stat_points -= 1
            elif event.key == pygame.K_LEFT:
                if self.stat_flag:
                    if self.stat_cursor_pos == 0:
                        if self.orig_str < player.stre:
                            player.stre -= 1
                            player.stat_points += 1
                    elif self.stat_cursor_pos == 1:
                        if self.orig_def < player.defe:
                            player.defe -= 1
                            player.stat_points += 1
                    elif self.stat_cursor_pos == 2:
                        if self.orig_mag < player.mag:
                            player.mag -= 1
                            player.stat_points += 1
            elif event.key == pygame.K_RETURN:
                if self.status_cur_pos == 0:
                    if not self.equip_flag1 and not self.equip_flag2:
                        self.equip_flag1 = True
                        self.window_x = 1600
                    elif self.equip_flag1 and not self.equip_flag2:
                        self.equip_flag2 = True
                    elif self.equip_flag2:
                        if self.equip_cursor1_pos == 0 and len(player.wep_owned) > 0:
                            for i in range(len(player.wep_owned)):
                                if player.wep_owned[i] == self.cur_id:
                                    player.wep_owned.remove(self.cur_id)
                                    player.wep_owned.insert(i, player.cur_weapon)
                                    player.cur_weapon = self.cur_id
                        elif self.equip_cursor1_pos == 1 and len(player.arm_owned) > 0:
                            for i in range(len(player.arm_owned)):
                                if player.arm_owned[i] == self.cur_id:
                                    player.arm_owned.remove(self.cur_id)
                                    player.arm_owned.insert(i, player.cur_armour)
                                    player.cur_armour = self.cur_id
                        elif self.equip_cursor1_pos == 2 and len(player.acc_owned) > 0:
                            for i in range(len(player.acc_owned)):
                                if player.acc_owned[i] == self.cur_id:
                                    player.acc_owned.remove(self.cur_id)
                                    player.acc_owned.insert(i, player.cur_accessory)
                                    player.cur_accessory = self.cur_id
                        player.update_stats()
                        self.equip_sound.play()
                elif self.status_cur_pos == 1:
                    if not self.stat_flag:
                        if player.stat_points > 0:
                            self.stat_flag = True
                            self.orig_stat_points = player.stat_points
                            self.orig_str = player.stre
                            self.orig_def = player.defe
                            self.orig_mag = player.mag
                        else:
                            self.buzzer_sound.play()
                            self.txtbox.toggle_popup_flag()
                            self.popup_message = "You don't have any stat points!"
                    if self.confirm:
                        self.confirm = False
                        self.stat_flag = False

            elif event.key == pygame.K_RCTRL:
                if self.equip_flag1 and not self.equip_flag2:
                    self.equip_flag1 = False
                elif self.equip_flag1 and self.equip_flag2:
                    self.equip_flag2 = False
                    self.min_pos = 0
                    self.equip_cursor2_pos = 0
                elif self.confirm:
                    self.confirm = False
                    self.stat_flag = False
                    player.stre = self.orig_str
                    player.defe = self.orig_def
                    player.mag = self.orig_mag
                    player.stat_points = self.orig_stat_points
                elif self.stat_flag:
                    if self.orig_stat_points > player.stat_points:
                        self.confirm = True

    def system(self):
        state.surf.blit(
            pygame.transform.scale(
                self.bg, (int(state.curwidth / 2.7), int(state.curheight / 3))
            ),
            (470, 200),
        )
        state.surf.blit(self.sysopt1, (528, 259))
        state.surf.blit(self.sysopt2, (528, 299))
        state.surf.blit(self.sysopt3, (528, 339))
        if self.syscursorpos == 0:
            state.surf.blit(self.cursor, (498, 259))
        if self.syscursorpos == 1:
            state.surf.blit(self.cursor, (498, 299))
        if self.syscursorpos == 2:
            state.surf.blit(self.cursor, (498, 339))
        if self.syscursorpos > 2:
            self.syscursorpos = 0
        if self.syscursorpos < 0:
            self.syscursorpos = 2

    def battle_choice(self, monkill):
        if self.battalk:
            montokill = 5 - monkill
            if monkill < 5:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "You have %d monter(s) left to kill. You're almost there!"
                            % montokill,
                        ]
                    ],
                    state.surf,
                    (0, 400),
                )
            if monkill >= 5:
                self.txtbox.draw_textbox(
                    [
                        [
                            "data/sprites/host_face.png",
                            "Chance",
                            "You can challenge the floor boss! Are you prepared for it?",
                        ]
                    ],
                    state.surf,
                    (0, 400),
                )

        if not self.battalk:
            if monkill >= 5:
                self.batopt2 = self.uitext.render(
                    "Challenge the floor boss", False, self.txtcolor
                )
            elif monkill < 5:
                self.batopt2 = self.uitext.render(
                    "Challenge the floor boss", False, (105, 109, 114)
                )
            state.surf.blit(
                pygame.transform.scale(
                    self.bg, (int(state.curwidth / 2.7), int(state.curheight / 3))
                ),
                (470, 200),
            )
            state.surf.blit(self.batopt1, (528, 259))
            state.surf.blit(self.batopt2, (528, 299))
            state.surf.blit(self.sysopt3, (528, 339))
            if self.batcursorpos == 0:
                state.surf.blit(self.cursor, (498, 259))
            if self.batcursorpos == 1:
                state.surf.blit(self.cursor, (498, 299))
            if self.batcursorpos == 2:
                state.surf.blit(self.cursor, (498, 339))
            if self.batcursorpos > 2:
                self.batcursorpos = 0
            if self.batcursorpos < 0:
                self.batcursorpos = 2

                # where 'progress' is what point in the 'story' the player is on

    def post_battle(self, progress=1):
        if not self.pb_dialogue:
            self.pbtalk = random.randrange(0, 4)
        if self.pbtalk == 0 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "That was a good battle! If you're injured make sure to rest up at the inn.",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        elif self.pbtalk == 1 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "Good job! Make sure to use the gold from your battle to buy equipment from our Shop!",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        elif self.pbtalk == 2 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "Nice work! You're pretty skilled, are you sure you haven't done this before?",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        elif self.pbtalk == 3 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "Good work out there! I overheard some strange people talking about you. Something about.. A debt?",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        if self.pbtalk == 0 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "Good work! Maybe I should bet some money on you next time, huh? *laughs*",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        elif self.pbtalk == 1 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "... Oh you're already done? Good job, sorry about that I was a bit lost in my own thoughts!",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        elif self.pbtalk == 2 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "Great job! How'd you get so strong? What's your secret?",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        elif self.pbtalk == 3 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/host_face.png",
                        "Chance",
                        "If you would like to get stronger, don't forget to buy new equipment! Or just keep killing these monsters for experience!",
                    ]
                ],
                state.surf,
                (0, 400),
            )

    def draw_inn(self, gold):
        state.surf.blit(
            pygame.transform.scale(self.bg, (int(state.curwidth / 1.5), 300)), (0, 430)
        )  # Description box
        state.surf.blit(
            pygame.transform.scale(self.bg, (170, 50)), (10, 48)
        )  # Gold box
        state.surf.blit(
            pygame.transform.scale(self.bg, (300, 300)), (905, 430)
        )  # Actions box
        state.surf.blit(self.talktxt, (946, 496))
        state.surf.blit(self.sleeptxt, (946, 526))
        state.surf.blit(self.backtxt, (946, 556))
        # Current gold with the player
        self.cur = self.uitext2.render("Gold:  %d" % gold, False, self.txtcolor)
        self.coinAnim.blit(state.surf, (22, 62))  # Gold icon
        state.surf.blit(self.cur, (47, 62))
        if self.cursorpos == 0:
            state.surf.blit(self.cursor, (916, 496))
            state.surf.blit(self.talkdesc2, (112, 490))
        if self.cursorpos == 1:
            state.surf.blit(self.cursor, (916, 526))
            state.surf.blit(self.sleepdesc, (112, 490))
        if self.cursorpos == 2:
            state.surf.blit(self.cursor, (916, 556))
            state.surf.blit(self.backdesc, (112, 490))

    def draw_town(self, player):
        state.surf.blit(
            pygame.transform.scale(self.bg, (int(state.curwidth / 1.5), 300)), (0, 430)
        )  # Description box
        state.surf.blit(
            pygame.transform.scale(self.bg, (170, 50)), (10, 29)
        )  # Gold box
        state.surf.blit(
            pygame.transform.scale(self.bg, (300, 300)), (905, 430)
        )  # Actions box
        state.surf.blit(self.talktxt, (946, 496))
        state.surf.blit(self.inntxt, (946, 526))
        state.surf.blit(self.slumstxt, (946, 556))
        state.surf.blit(self.backtxt, (946, 586))
        # Current gold with the player
        gold = self.uitext2.render("Gold:  %d" % player.gold, False, self.txtcolor)
        self.coinAnim.blit(state.surf, (22, 45))  # Gold icon
        state.surf.blit(gold, (47, 45))
        if self.cursorpos == 0:
            state.surf.blit(self.cursor, (916, 496))
            state.surf.blit(self.talkdesc3, (112, 490))
        elif self.cursorpos == 1:
            state.surf.blit(self.cursor, (916, 526))
            state.surf.blit(self.inndesc, (112, 490))
        elif self.cursorpos == 2:
            state.surf.blit(self.cursor, (916, 556))
            state.surf.blit(self.slumsdesc, (112, 490))
        elif self.cursorpos == 3:
            state.surf.blit(self.cursor, (916, 586))
            state.surf.blit(self.backdesc, (112, 490))
        elif self.cursorpos > 3:
            self.cursorpos = 0
        elif self.cursorpos < 0:
            self.cursorpos = 3
        self.clock(player.hours, player.minutes)

    def draw_casino(self, player):  # Draws the casino UI
        state.surf.blit(
            pygame.transform.scale(self.bg, (int(state.curwidth / 1.5), 300)), (0, 430)
        )  # Description box
        state.surf.blit(
            pygame.transform.scale(self.bg, (170, 50)), (10, 29)
        )  # Gold box
        state.surf.blit(
            pygame.transform.scale(self.bg, (300, 300)), (905, 430)
        )  # Actions box
        state.surf.blit(self.talktxt, (946, 496))
        state.surf.blit(self.sleeptxt, (946, 526))
        state.surf.blit(self.casino_text, (946, 556))
        state.surf.blit(self.backtxt, (946, 586))
        # Current gold with the player
        gold = self.uitext2.render("Gold:  %d" % player.gold, False, self.txtcolor)
        self.coinAnim.blit(state.surf, (22, 45))  # Gold icon
        state.surf.blit(gold, (47, 45))
        if self.cursorpos == 0:
            state.surf.blit(self.cursor, (916, 496))
            state.surf.blit(self.talkdesc3, (112, 490))
        elif self.cursorpos == 1:
            state.surf.blit(self.cursor, (916, 526))
            state.surf.blit(self.inndesc, (112, 490))
        elif self.cursorpos == 2:
            state.surf.blit(self.cursor, (916, 556))
            state.surf.blit(self.casino_desc, (112, 490))
        elif self.cursorpos == 3:
            state.surf.blit(self.cursor, (916, 586))
            state.surf.blit(self.backdesc, (112, 490))
        elif self.cursorpos > 3:
            self.cursorpos = 0
        elif self.cursorpos < 0:
            self.cursorpos = 3
        self.clock(player.hours, player.minutes)


class SelectOptions(MainUi):
    def __init__(self):
        MainUi.__init__(self)
        self.rowpos = 0  # Position of cursor in Option selection(Current row)
        # Position of cursor in Option selection(Current column)
        self.colpos = 0
        self.alert1 = True  # Flag for whether that option is new/updated
        self.alert2 = True  # Flag for whether that option is new/updated
        self.alert3 = True  # Flag for whether that option is new/updated
        self.alert4 = True  # Flag for whether that option is new/updated
        self.alert5 = True  # Flag for whether that option is new/updated
        self.alert6 = True  # Flag for whether that option is new/updated
        self.alertAnim = pyganim.PygAnimation(
            [("data/sprites/alert1.png", 0.4), ("data/sprites/alert2.png", 0.4)]
        )
        self.alertAnim.scale([35, 35])
        self.alertAnim.play()

    def drawUi(
        self, no=1, opt1="1", opt2="2", opt3="3", opt4="4", opt5="5", opt6="6"
    ):  # Select option among 6 or fewer choices,where no is the number of choices
        state.surf.blit(
            pygame.transform.scale(self.bg, (int(state.curwidth / 1.5), 300)), (0, 430)
        )
        Option1 = self.uitext.render(opt1, False, self.txtcolor)
        Option2 = self.uitext.render(opt2, False, self.txtcolor)
        Option3 = self.uitext.render(opt3, False, self.txtcolor)
        Option4 = self.uitext.render(opt4, False, self.txtcolor)
        Option5 = self.uitext.render(opt5, False, self.txtcolor)
        Option6 = self.uitext.render(opt6, False, self.txtcolor)
        backTxt = self.uitext.render("Back", False, self.txtcolor)
        state.surf.blit(Option1, (80, 490))  # Row 1
        if self.alert1:  # If the option is new/updated show alert.
            self.alertAnim.blit(state.surf, (80 + Option1.get_width(), 490))
        if no >= 2:
            state.surf.blit(Option2, (280, 490))
            if self.alert2:
                self.alertAnim.blit(state.surf, (280 + Option2.get_width(), 490))
            if no >= 3:
                state.surf.blit(Option3, (480, 490))
                if self.alert3:
                    self.alertAnim.blit(state.surf, (480 + Option3.get_width(), 490))
                if no >= 4:
                    state.surf.blit(Option4, (80, 590))  # Row 2
                    if self.alert4:
                        self.alertAnim.blit(state.surf, (80 + Option4.get_width(), 590))
                    if no >= 5:
                        state.surf.blit(Option5, (280, 590))
                        if self.alert5:
                            self.alertAnim.blit(
                                state.surf, (280 + Option5.get_width(), 590)
                            )
                        if no >= 6:
                            state.surf.blit(Option6, (480, 590))
                            if self.alert6:
                                self.alertAnim.blit(
                                    state.surf, (480 + Option6.get_width(), 590)
                                )
        state.surf.blit(backTxt, (680, 590))  # Exit
        if self.colpos > no or self.colpos > 3:
            self.colpos = 0
        if self.rowpos > 1 or no <= 3:
            self.rowpos = 0
        if self.colpos < 0:
            if no >= 3:
                self.colpos = 2
            else:
                self.colpos = 3
            if self.rowpos == 1:
                self.colpos = 3
        if self.rowpos < 0:
            if no > 3:
                if no == 4:
                    self.colpos = 0
                self.rowpos = 1
            else:
                self.rowpos = 0
        if self.rowpos == 0:  # Goes to exit when trying to go right on the end of row 1
            if self.colpos > 2:
                self.rowpos = 1
                self.colpos = 3
        if self.rowpos == 1:
            if no == 4:
                if self.colpos > 0 and self.colpos <= 2:
                    self.rowpos = 1
                    self.colpos = 0
            elif no == 5:
                if self.colpos > 1:
                    self.colpos = 3

        if self.rowpos == 0 and self.colpos == 0:  # Option 1
            state.surf.blit(self.cursor, (50, 490))
        if self.rowpos == 0 and self.colpos == 1:  # Option 2
            state.surf.blit(self.cursor, (250, 490))
        if self.rowpos == 0 and self.colpos == 2:  # Option 3
            state.surf.blit(self.cursor, (450, 490))
        if self.rowpos == 1 and self.colpos == 0:  # Option 4
            state.surf.blit(self.cursor, (50, 590))
        if self.rowpos == 1 and self.colpos == 1:  # Option 5
            state.surf.blit(self.cursor, (250, 590))
        if self.rowpos == 1 and self.colpos == 2:  # Option 6
            state.surf.blit(self.cursor, (450, 590))
        if self.rowpos == 1 and self.colpos == 3:  # Back
            state.surf.blit(self.cursor, (650, 590))

    def alert_off(self, alert):  # Switch off the specified alert(from 1 to 6)
        if alert == 1:
            self.alert1 = False
        if alert == 2:
            self.alert2 = False
        if alert == 3:
            self.alert3 = False
        if alert == 4:
            self.alert4 = False
        if alert == 5:
            self.alert5 = False
        if alert == 6:
            self.alert6 = False

    def alert_on(self, alert):  # Switch on the specified alert(from 1 to 6)
        if alert == 1:
            self.alert1 = True
        if alert == 2:
            self.alert2 = True
        if alert == 3:
            self.alert3 = True
        if alert == 4:
            self.alert4 = True
        if alert == 5:
            self.alert5 = True
        if alert == 6:
            self.alert6 = True


class Shop(MainUi):
    def __init__(self, item_data):
        MainUi.__init__(self)
        self.item_data = item_data
        self.weapons_list = item_data["weapons"]
        self.armour_list = item_data["armours"]
        self.acc_list = item_data["accessories"]
        self.consume_list = item_data["consumables"]
        self.player_data = Player()
        self.shopbg = pygame.image.load("data/backgrounds/shopbg.png").convert_alpha()
        self.pstr = 1
        self.pdef = 1
        self.pmag = 1
        self.pluck = 1
        self.shoptxt = ["Weapons", "Armour", "Accessories", "Items"]
        self.shoptxt2 = ["Name", "Cost"]
        self.title_text = pygame.font.Font("data/fonts/Daisy_Roots.otf", 50)
        self.shop_cursor_pos1 = 0  # for choosing the type of item
        self.shop_cursor_pos2 = 0  # for choosing from the list of items
        self.min_pos = 0  # minimum position for the item in the list
        self.max_pos = 0  # maximum position for an item in the list
        self.shop_page = 0
        self.no_sell_flag = False  # Flag for when the shop has no items in a category
        self.shop_selection_flag = True
        self.status_bg = pygame.transform.scale(self.bg, (300, 500)).convert_alpha()
        self.status_anim = False
        self.green_rgb = (0, 200, 0)
        self.red_rgb = (200, 0, 0)
        self.box_pos = 2000
        self.current_list = []  # which set of items you're currently viewing
        self.buzzer = pygame.mixer.Sound("data/sounds&music/Buzzer1.ogg")
        self.buzzer.set_volume(0.05)

    def get_player_stats(self, player_data):
        self.player_data = player_data
        self.pstr = self.player_data.stre + self.player_data.add_stre
        self.pdef = self.player_data.defe + self.player_data.add_defe
        self.pmag = self.player_data.mag + self.player_data.add_mag
        self.pluck = self.player_data.luck
        self.pspeed = self.player_data.speed + self.player_data.add_speed

    def status_window(self, item, player_data):
        self.get_player_stats(player_data)
        if self.current_list == self.consume_list:
            item_desc = self.uitext2.render(item["description"], False, self.txtcolor2)
            state.surf.blit(item_desc, (120, 660))
            if self.min_pos != 0:
                state.surf.blit(self.cursor_up, (212, 303))
            if self.min_pos + 5 != self.max_pos:
                # Downward facing arrow to show that more items are available
                state.surf.blit(self.cursor_down, (212, 623))
        else:
            if not self.status_anim:
                self.box_pos = 2000
                self.status_anim = True
            if self.status_anim:
                if self.box_pos > 950:
                    self.box_pos -= 50

            state.surf.blit(self.status_bg, (self.box_pos, 222))
            if self.box_pos <= 950:
                str_txt = self.uitext.render(
                    "STR: " + str(self.pstr), False, self.txtcolor3
                )
                def_txt = self.uitext.render(
                    "DEF: " + str(self.pdef), False, self.txtcolor3
                )
                mag_txt = self.uitext.render(
                    "MAG: " + str(self.pmag), False, self.txtcolor3
                )
                spd_txt = self.uitext.render(
                    "SPD: " + str(self.pspeed), False, self.txtcolor3
                )
                luk_txt = self.uitext.render(
                    "LUCK: " + str(self.pluck), False, self.txtcolor3
                )
                item_desc = self.uitext2.render(
                    item["description"], False, self.txtcolor2
                )
                if self.current_list == self.weapons_list:
                    player_item = player_data.cur_weapon

                elif self.current_list == self.armour_list:
                    player_item = player_data.cur_armour
                else:
                    player_item = player_data.cur_accessory

                str_dif = (
                    self.pstr
                    + item["atk"]
                    - (self.pstr + self.current_list[player_item]["atk"])
                )
                def_dif = (
                    self.pdef
                    + item["def"]
                    - (self.pdef + self.current_list[player_item]["def"])
                )
                mag_dif = (
                    self.pmag
                    + item["mag"]
                    - (self.pmag + self.current_list[player_item]["mag"])
                )
                spd_dif = (
                    self.pspeed
                    + item["spd"]
                    - (self.pspeed + self.current_list[player_item]["spd"])
                )
                if str_dif >= 0:
                    str_diftxt = self.uitext.render(
                        "(+" + str(str_dif) + ")", False, self.green_rgb
                    )
                    state.surf.blit(str_diftxt, (1120, 300))
                else:
                    str_diftxt = self.uitext.render(
                        "(" + str(str_dif) + ")", False, self.red_rgb
                    )
                    state.surf.blit(str_diftxt, (1120, 300))
                if def_dif >= 0:
                    def_diftxt = self.uitext.render(
                        "(+" + str(def_dif) + ")", False, self.green_rgb
                    )
                    state.surf.blit(def_diftxt, (1120, 370))
                else:
                    def_diftxt = self.uitext.render(
                        "(" + str(def_dif) + ")", False, self.red_rgb
                    )
                    state.surf.blit(def_diftxt, (1120, 370))
                if mag_dif >= 0:
                    mag_diftxt = self.uitext.render(
                        "(+" + str(mag_dif) + ")", False, self.green_rgb
                    )
                    state.surf.blit(mag_diftxt, (1120, 440))
                else:
                    mag_diftxt = self.uitext.render(
                        "(" + str(mag_dif) + ")", False, self.red_rgb
                    )
                    state.surf.blit(mag_diftxt, (1120, 440))
                if spd_dif >= 0:
                    spd_diftxt = self.uitext.render(
                        "(+" + str(spd_dif) + ")", False, self.green_rgb
                    )
                    state.surf.blit(spd_diftxt, (1120, 510))
                else:
                    spd_diftxt = self.uitext.render(
                        "(" + str(spd_dif) + ")", False, self.red_rgb
                    )
                    state.surf.blit(spd_diftxt, (1120, 510))
                if self.min_pos + 5 != self.max_pos:
                    # Downward facing arrow to show that more items are available
                    state.surf.blit(self.cursor_down, (212, 623))
                if self.min_pos != 0:
                    state.surf.blit(self.cursor_up, (212, 303))
                state.surf.blit(item_desc, (120, 660))
                state.surf.blit(str_txt, (1000, 300))
                state.surf.blit(def_txt, (1000, 370))
                state.surf.blit(mag_txt, (1000, 440))
                state.surf.blit(spd_txt, (1000, 510))
                state.surf.blit(luk_txt, (1000, 580))

    def buy_item(self, item_id):
        if self.player_data.gold < self.current_list[item_id]["cost"]:
            self.buzzer.play()
            self.popup_message = "Not enough gold!"
            self.txtbox.toggle_popup_flag()
        elif self.current_list == self.weapons_list and (
            item_id in self.player_data.wep_owned
            or self.player_data.cur_weapon == item_id
        ):
            self.buzzer.play()
            self.popup_message = "You already own that weapon!"
            self.txtbox.toggle_popup_flag()
        elif self.current_list == self.armour_list and (
            item_id in self.player_data.arm_owned
            or self.player_data.cur_armour == item_id
        ):
            self.popup_message = "You already own that armour!"
            self.txtbox.toggle_popup_flag()
            self.buzzer.play()
        elif self.current_list == self.acc_list and (
            item_id in self.player_data.acc_owned
            or self.player_data.cur_accessory == item_id
        ):
            self.buzzer.play()
            self.popup_message = "You already own that accessory!"
            self.txtbox.toggle_popup_flag()
        else:
            self.buysound.play()
            return True

    def draw_shop(self, shop_name="", player_data=Player()):
        if not self.loaditems:
            shop_text_pos = 160
            wepnamelist = []
            wepcostlist = []
            wepstatlist = []
            wepattributelist = []
            armnamelist = []
            armcostlist = []
            armstatlist = []
            armattributelist = []
            accnamelist = []
            acccostlist = []
            accstatlist = []
            accattributelist = []
            connamelist = []
            concostlist = []
            constatlist = []
            for weapon in self.weapons_list:
                wepnamelist.append(weapon["name"])
                wepcostlist.append(str(weapon["cost"]))
                wepstatlist.append(str([weapon["atk"], weapon["def"], weapon["mag"]]))
                wepattributelist.append(weapon["attributes"])
            for armour in self.armour_list:
                armnamelist.append(armour["name"])
                armcostlist.append(str(armour["cost"]))
                armstatlist.append(str([armour["atk"], armour["def"], armour["mag"]]))
                armattributelist.append(armour["attributes"])
            for accessory in self.acc_list:
                accnamelist.append(accessory["name"])
                acccostlist.append(str(accessory["cost"]))
                accstatlist.append(
                    str([accessory["atk"], accessory["def"], accessory["mag"]])
                )
                accattributelist.append(accessory["attributes"])
            for consumable in self.consume_list:
                connamelist.append(consumable["name"])
                concostlist.append(str(consumable["cost"]))
                constatlist.append(str([consumable["hp"], consumable["mp"]]))
            shop_title = self.title_text.render(shop_name, True, self.txtcolor2)

        if self.shopkeep:
            self.txtbox.draw_textbox(
                [
                    [
                        "data/sprites/shopkeep.png",
                        "Shopkeeper",
                        "Welcome to the Arena shop! How can I help you?",
                    ]
                ],
                state.surf,
                (0, 400),
            )
        if not self.shopkeep:
            state.surf.blit(self.shopbg, (53, 30))
            state.surf.blit(shop_title, (360, 57))
            state.surf.blit(
                self.uitext.render(self.shoptxt[0], False, self.txtcolor3),
                (shop_text_pos, 150),
            )
            state.surf.blit(
                self.uitext.render(self.shoptxt[1], False, self.txtcolor3),
                (shop_text_pos + 150, 150),
            )
            state.surf.blit(
                self.uitext.render(self.shoptxt[2], False, self.txtcolor3),
                (shop_text_pos + 300, 150),
            )
            state.surf.blit(
                self.uitext.render(self.shoptxt[3], False, self.txtcolor3),
                (shop_text_pos + 510, 150),
            )
            state.surf.blit(
                self.uitext2.render(self.shoptxt2[0], False, (186, 31, 34)), (161, 290)
            )
            state.surf.blit(
                self.uitext2.render(self.shoptxt2[1], True, (186, 31, 34)), (449, 290)
            )
            state.surf.blit(
                pygame.transform.scale(self.bg, (170, 50)), (925, 42)
            )  # Gold box 10,48
            self.cur = self.uitext2.render(
                "Gold:  %d" % player_data.gold, False, self.txtcolor
            )  # Current gold with the player
            self.coinAnim.blit(state.surf, (937, 56))  # Gold icon
            state.surf.blit(self.cur, (962, 56))
            if self.shop_page == 0:
                self.max_pos = len(self.weapons_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell weapons.", False, self.txtcolor3
                    )
                    cost1 = self.uitext.render("", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    if (
                        self.min_pos in player_data.wep_owned
                        or self.min_pos == self.player_data.cur_weapon
                    ):
                        item1 = self.uitext.render(
                            wepnamelist[self.min_pos], False, (86, 91, 99)
                        )
                        cost1 = self.uitext.render(
                            wepcostlist[self.min_pos], False, (86, 91, 99)
                        )
                        state.surf.blit(
                            self.uitext2.render("Owned", False, (186, 31, 34)),
                            (600, 339),
                        )
                    else:
                        item1 = self.uitext.render(
                            wepnamelist[self.min_pos], False, self.txtcolor3
                        )
                        cost1 = self.uitext.render(
                            wepcostlist[self.min_pos], False, self.txtcolor3
                        )
                    if self.max_pos >= 2:
                        if (
                            self.min_pos + 1 in player_data.wep_owned
                            or self.min_pos + 1 == self.player_data.cur_weapon
                        ):
                            item2 = self.uitext.render(
                                wepnamelist[self.min_pos + 1], False, (86, 91, 99)
                            )
                            cost2 = self.uitext.render(
                                wepcostlist[self.min_pos + 1], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 399),
                            )
                        else:
                            item2 = self.uitext.render(
                                wepnamelist[self.min_pos + 1], False, self.txtcolor3
                            )
                            cost2 = self.uitext.render(
                                wepcostlist[self.min_pos + 1], False, self.txtcolor3
                            )
                    if self.max_pos >= 3:
                        if (
                            self.min_pos + 2 in player_data.wep_owned
                            or self.min_pos + 2 == self.player_data.cur_weapon
                        ):
                            item3 = self.uitext.render(
                                wepnamelist[self.min_pos + 2], False, (86, 91, 99)
                            )
                            cost3 = self.uitext.render(
                                wepcostlist[self.min_pos + 2], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 459),
                            )
                        else:
                            item3 = self.uitext.render(
                                wepnamelist[self.min_pos + 2], False, self.txtcolor3
                            )
                            cost3 = self.uitext.render(
                                wepcostlist[self.min_pos + 2], False, self.txtcolor3
                            )
                    if self.max_pos >= 4:
                        if (
                            self.min_pos + 3 in player_data.wep_owned
                            or self.min_pos + 3 == self.player_data.cur_weapon
                        ):
                            item4 = self.uitext.render(
                                wepnamelist[self.min_pos + 3], False, (86, 91, 99)
                            )
                            cost4 = self.uitext.render(
                                wepcostlist[self.min_pos + 3], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 519),
                            )
                        else:
                            item4 = self.uitext.render(
                                wepnamelist[self.min_pos + 3], False, self.txtcolor3
                            )
                            cost4 = self.uitext.render(
                                wepcostlist[self.min_pos + 3], False, self.txtcolor3
                            )
                    if self.max_pos >= 5:
                        if (
                            self.min_pos + 4 in player_data.wep_owned
                            or self.min_pos + 4 == self.player_data.cur_weapon
                        ):
                            item5 = self.uitext.render(
                                wepnamelist[self.min_pos + 4], False, (86, 91, 99)
                            )
                            cost5 = self.uitext.render(
                                wepcostlist[self.min_pos + 4], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 579),
                            )
                        else:
                            item5 = self.uitext.render(
                                wepnamelist[self.min_pos + 4], False, self.txtcolor3
                            )
                            cost5 = self.uitext.render(
                                wepcostlist[self.min_pos + 4], False, self.txtcolor3
                            )
            if self.shop_page == 1:
                self.max_pos = len(self.armour_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell armours.", False, self.txtcolor3
                    )
                    cost1 = self.uitext.render("", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    if (
                        self.min_pos in player_data.arm_owned
                        or self.min_pos == self.player_data.cur_armour
                    ):
                        item1 = self.uitext.render(
                            armnamelist[self.min_pos], False, (86, 91, 99)
                        )
                        cost1 = self.uitext.render(
                            armcostlist[self.min_pos], False, (86, 91, 99)
                        )
                        state.surf.blit(
                            self.uitext2.render("Owned", False, (186, 31, 34)),
                            (600, 339),
                        )
                    else:
                        item1 = self.uitext.render(
                            armnamelist[self.min_pos], False, self.txtcolor3
                        )
                        cost1 = self.uitext.render(
                            armcostlist[self.min_pos], False, self.txtcolor3
                        )
                    if self.max_pos >= 2:
                        if (
                            self.min_pos + 1 in player_data.arm_owned
                            or self.min_pos + 1 == self.player_data.cur_armour
                        ):
                            item2 = self.uitext.render(
                                armnamelist[self.min_pos + 1], False, (86, 91, 99)
                            )
                            cost2 = self.uitext.render(
                                armcostlist[self.min_pos + 1], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 399),
                            )
                        else:
                            item2 = self.uitext.render(
                                armnamelist[self.min_pos + 1], False, self.txtcolor3
                            )
                            cost2 = self.uitext.render(
                                armcostlist[self.min_pos + 1], False, self.txtcolor3
                            )
                    if self.max_pos >= 3:
                        if (
                            self.min_pos + 2 in player_data.arm_owned
                            or self.min_pos + 2 == self.player_data.cur_armour
                        ):
                            item3 = self.uitext.render(
                                armnamelist[self.min_pos + 2], False, (86, 91, 99)
                            )
                            cost3 = self.uitext.render(
                                armcostlist[self.min_pos + 2], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 459),
                            )
                        else:
                            item3 = self.uitext.render(
                                armnamelist[self.min_pos + 2], False, self.txtcolor3
                            )
                            cost3 = self.uitext.render(
                                armcostlist[self.min_pos + 2], False, self.txtcolor3
                            )
                    if self.max_pos >= 4:
                        if (
                            self.min_pos + 3 in player_data.arm_owned
                            or self.min_pos + 3 == self.player_data.cur_armour
                        ):
                            item4 = self.uitext.render(
                                armnamelist[self.min_pos + 3], False, (86, 91, 99)
                            )
                            cost4 = self.uitext.render(
                                armcostlist[self.min_pos + 3], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 519),
                            )
                        else:
                            item4 = self.uitext.render(
                                armnamelist[self.min_pos + 3], False, self.txtcolor3
                            )
                            cost4 = self.uitext.render(
                                armcostlist[self.min_pos + 3], False, self.txtcolor3
                            )
                    if self.max_pos >= 5:
                        if (
                            self.min_pos + 4 in player_data.arm_owned
                            or self.min_pos + 4 == self.player_data.cur_armour
                        ):
                            item5 = self.uitext.render(
                                armnamelist[self.min_pos + 4], False, (86, 91, 99)
                            )
                            cost5 = self.uitext.render(
                                armcostlist[self.min_pos + 4], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 579),
                            )
                        else:
                            item5 = self.uitext.render(
                                armnamelist[self.min_pos + 4], False, self.txtcolor3
                            )
                            cost5 = self.uitext.render(
                                armcostlist[self.min_pos + 4], False, self.txtcolor3
                            )
            if self.shop_page == 2:
                self.max_pos = len(self.acc_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell accessories.", False, self.txtcolor3
                    )
                    cost1 = self.uitext.render("", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    if (
                        self.min_pos in player_data.acc_owned
                        or self.min_pos == self.player_data.cur_accessory
                    ):
                        item1 = self.uitext.render(
                            accnamelist[self.min_pos], False, (86, 91, 99)
                        )
                        cost1 = self.uitext.render(
                            acccostlist[self.min_pos], False, (86, 91, 99)
                        )
                        state.surf.blit(
                            self.uitext2.render("Owned", False, (186, 31, 34)),
                            (600, 339),
                        )
                    else:
                        item1 = self.uitext.render(
                            accnamelist[self.min_pos], False, self.txtcolor3
                        )
                        cost1 = self.uitext.render(
                            acccostlist[self.min_pos], False, self.txtcolor3
                        )
                    if self.max_pos >= 2:
                        if (
                            self.min_pos + 1 in player_data.acc_owned
                            or self.min_pos + 1 == self.player_data.cur_accessory
                        ):
                            item2 = self.uitext.render(
                                accnamelist[self.min_pos + 1], False, (86, 91, 99)
                            )
                            cost2 = self.uitext.render(
                                acccostlist[self.min_pos + 1], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 399),
                            )
                        else:
                            item2 = self.uitext.render(
                                accnamelist[self.min_pos + 1], False, self.txtcolor3
                            )
                            cost2 = self.uitext.render(
                                acccostlist[self.min_pos + 1], False, self.txtcolor3
                            )
                    if self.max_pos >= 3:
                        if (
                            self.min_pos + 2 in player_data.acc_owned
                            or self.min_pos + 2 == self.player_data.cur_accessory
                        ):
                            item3 = self.uitext.render(
                                accnamelist[self.min_pos + 2], False, (86, 91, 99)
                            )
                            cost3 = self.uitext.render(
                                acccostlist[self.min_pos + 2], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 459),
                            )
                        else:
                            item3 = self.uitext.render(
                                accnamelist[self.min_pos + 2], False, self.txtcolor3
                            )
                            cost3 = self.uitext.render(
                                acccostlist[self.min_pos + 2], False, self.txtcolor3
                            )
                    if self.max_pos >= 4:
                        if (
                            self.min_pos + 3 in player_data.acc_owned
                            or self.min_pos + 3 == self.player_data.cur_accessory
                        ):
                            item4 = self.uitext.render(
                                accnamelist[self.min_pos + 3], False, (86, 91, 99)
                            )
                            cost4 = self.uitext.render(
                                acccostlist[self.min_pos + 3], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 519),
                            )
                        else:
                            item4 = self.uitext.render(
                                accnamelist[self.min_pos + 3], False, self.txtcolor3
                            )
                            cost4 = self.uitext.render(
                                acccostlist[self.min_pos + 3], False, self.txtcolor3
                            )
                    if self.max_pos >= 5:
                        if (
                            self.min_pos + 4 in player_data.acc_owned
                            or self.min_pos + 4 == self.player_data.cur_accessory
                        ):
                            item5 = self.uitext.render(
                                accnamelist[self.min_pos + 4], False, (86, 91, 99)
                            )
                            cost5 = self.uitext.render(
                                acccostlist[self.min_pos + 4], False, (86, 91, 99)
                            )
                            state.surf.blit(
                                self.uitext2.render("Owned", False, (186, 31, 34)),
                                (600, 579),
                            )
                        else:
                            item5 = self.uitext.render(
                                accnamelist[self.min_pos + 4], False, self.txtcolor3
                            )
                            cost5 = self.uitext.render(
                                acccostlist[self.min_pos + 4], False, self.txtcolor3
                            )
            if self.shop_page == 3:
                state.surf.blit(
                    self.uitext2.render("In Inventory", False, (186, 31, 34)),
                    (590, 290),
                )
                self.max_pos = len(self.consume_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell consumables.", False, self.txtcolor3
                    )
                    cost1 = self.uitext.render("", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    item1 = self.uitext.render(
                        connamelist[self.min_pos], False, self.txtcolor3
                    )
                    cost1 = self.uitext.render(
                        concostlist[self.min_pos], False, self.txtcolor3
                    )
                    for i in range(self.min_pos, self.max_pos):
                        for item in self.player_data.inventory:
                            if item["name"] == connamelist[i] and i <= self.min_pos + 4:
                                state.surf.blit(
                                    self.uitext2.render(
                                        str(item["amount"]), False, (31, 22, 21)
                                    ),
                                    (610, 339 + 60 * (i - self.min_pos)),
                                )
                    if self.max_pos >= 2:
                        item2 = self.uitext.render(
                            connamelist[self.min_pos + 1], False, self.txtcolor3
                        )
                        cost2 = self.uitext.render(
                            concostlist[self.min_pos + 1], False, self.txtcolor3
                        )
                    if self.max_pos >= 3:
                        item3 = self.uitext.render(
                            connamelist[self.min_pos + 2], False, self.txtcolor3
                        )
                        cost3 = self.uitext.render(
                            concostlist[self.min_pos + 2], False, self.txtcolor3
                        )
                    if self.max_pos >= 4:
                        item4 = self.uitext.render(
                            connamelist[self.min_pos + 3], False, self.txtcolor3
                        )
                        cost4 = self.uitext.render(
                            concostlist[self.min_pos + 3], False, self.txtcolor3
                        )
                    if self.max_pos >= 5:
                        item5 = self.uitext.render(
                            connamelist[self.min_pos + 4], False, self.txtcolor3
                        )
                        cost5 = self.uitext.render(
                            concostlist[self.min_pos + 4], False, self.txtcolor3
                        )

            state.surf.blit(item1, (161, 339))
            state.surf.blit(cost1, (449, 339))

            if self.max_pos >= 2:
                state.surf.blit(item2, (161, 399))
                state.surf.blit(cost2, (449, 399))

            if self.max_pos >= 3:
                state.surf.blit(item3, (161, 459))
                state.surf.blit(cost3, (449, 459))

            if self.max_pos >= 4:
                state.surf.blit(item4, (161, 519))
                state.surf.blit(cost4, (449, 519))

            if self.max_pos >= 5:
                state.surf.blit(item5, (161, 579))
                state.surf.blit(cost5, (449, 579))

            if self.shop_selection_flag:  # while using cursor 1
                self.min_pos = 0
                self.shop_cursor_pos2 = 0
                self.status_anim = False
                if self.shop_cursor_pos1 == 0:
                    state.surf.blit(self.cursor, (shop_text_pos - 35, 150))
                    self.shop_page = 0
                    self.current_list = self.weapons_list
                if self.shop_cursor_pos1 == 1:
                    state.surf.blit(self.cursor, (shop_text_pos + 150 - 35, 150))
                    self.shop_page = 1
                    self.current_list = self.armour_list
                if self.shop_cursor_pos1 == 2:
                    state.surf.blit(self.cursor, (shop_text_pos + 300 - 35, 150))
                    self.shop_page = 2
                    self.current_list = self.acc_list
                if self.shop_cursor_pos1 == 3:
                    state.surf.blit(self.cursor, (shop_text_pos + 510 - 35, 150))
                    self.shop_page = 3
                    self.current_list = self.consume_list
                if self.shop_cursor_pos1 > 3:
                    self.shop_cursor_pos1 = 0
                elif self.shop_cursor_pos1 < 0:
                    self.shop_cursor_pos1 = 3
            if not self.shop_selection_flag:  # while using cursor 2
                if self.shop_cursor_pos2 == 0:
                    state.surf.blit(self.cursor, (120, 339))
                elif self.shop_cursor_pos2 == 1:
                    state.surf.blit(self.cursor, (120, 399))
                elif self.shop_cursor_pos2 == 2:
                    state.surf.blit(self.cursor, (120, 459))
                elif self.shop_cursor_pos2 == 3:
                    state.surf.blit(self.cursor, (120, 519))
                elif self.shop_cursor_pos2 == 4:
                    state.surf.blit(self.cursor, (120, 579))
                if self.shop_cursor_pos2 > 4:
                    if self.min_pos + 5 < self.max_pos:
                        self.min_pos += 1
                        self.shop_cursor_pos2 = 4
                    else:
                        self.shop_cursor_pos2 = 0
                        self.min_pos = 0
                elif self.shop_cursor_pos2 < 0:
                    if self.max_pos > 5:
                        if self.min_pos != 0:
                            self.min_pos -= 1
                            self.shop_cursor_pos2 = 0
                        else:
                            self.shop_cursor_pos2 = 4
                            self.min_pos = self.max_pos - 5
                    else:
                        self.shop_cursor_pos2 = self.max_pos - 1
                self.status_window(
                    self.current_list[self.shop_cursor_pos2 + self.min_pos], player_data
                )
            self.txtbox.popup_message(self.popup_message, state.surf)
