import pygame
import random
from data import pyganim
from data import gameui
from src.models.player import Player

class MainUi:
    """The Main UI of the game(outside of battle.)"""

    def __init__(self, surface, item_data, dialogues):
        self.surface = surface
        self.item_data = item_data
        self.dialogues = dialogues
        self.bg = pygame.image.load(
            "data/backgrounds/rpgtxt.png").convert_alpha()
        self.status_bg = pygame.transform.scale(
            self.bg, (900, 700)).convert_alpha()
        self.status_menu_bg = pygame.transform.scale(
            self.bg, (200, 300)).convert_alpha()
        self.equip_menu_bg = pygame.transform.scale(
            self.bg, (330, 400)).convert_alpha()
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
        self.cursor = pygame.image.load(
            "data/sprites/Cursor.png").convert_alpha()
        self.cursor_down = pygame.transform.rotate(self.cursor, -90)
        self.cursor_up = pygame.transform.rotate(self.cursor, 90)
        self.cursor_left = pygame.transform.rotate(self.cursor, 180)
        self.cursorsound = pygame.mixer.Sound('data/sounds&music/Cursor1.ogg')
        self.cursorsound.set_volume(0.05)
        self.cursorpos = 0
        self.equip_txt = self.uitext.render('Equipment', False, self.txtcolor)
        self.buzzer_sound = pygame.mixer.Sound('data/sounds&music/Buzzer1.ogg')
        self.buzzer_sound.set_volume(0.05)
        self.stats_txt = self.uitext.render('Stats', False, self.txtcolor)
        self.talktxt = self.uitext.render('Talk', False, self.txtcolor)
        self.casino_text = self.uitext.render('Gamble', False, self.txtcolor)
        self.talkdesc = self.uitext.render(
            'Talk with people around the Arena.', False, self.txtcolor)
        self.talkdesc2 = self.uitext.render(
            'Talk with people around the Inn.', False, self.txtcolor)
        self.casino_desc = self.uitext.render(
            'Play the dice game.', False, self.txtcolor)
        self.talkdesc3 = self.uitext.render(
            'Talk with people around the Town.', False, self.txtcolor)
        self.battxt = self.uitext.render('Battle', False, self.txtcolor)
        self.batdesc = self.uitext.render(
            'Battle monsters in the Arena.', False, self.txtcolor)
        self.systxt = self.uitext.render('System', False, self.txtcolor)
        self.sysdesc = self.uitext.render(
            'System options.', False, self.txtcolor)
        self.inntxt = self.uitext.render('Inn', False, self.txtcolor)
        self.inndesc = self.uitext.render(
            'Go to the Inn.', False, self.txtcolor)
        self.shoptxt = self.uitext.render('Shop', False, self.txtcolor)
        self.slumstxt = self.uitext.render('Slums', False, self.txtcolor)
        self.slumsdesc = self.uitext.render(
            'Go to the Slums.', False, self.txtcolor)
        self.shopdesc = self.uitext.render(
            'Buy items/equipment to use in the Arena.', False, self.txtcolor)
        self.stattxt = self.uitext.render('Status', False, self.txtcolor)
        self.statdesc = self.uitext.render(
            'Check player status/equipment', False, self.txtcolor)
        self.backtxt = self.uitext.render('Leave', False, self.txtcolor)
        self.back_txt = self.uitext.render('Back', False, self.txtcolor)
        self.backdesc = self.uitext.render(
            'Return to the Arena', False, self.txtcolor)
        self.sleeptxt = self.uitext.render('Rest', False, self.txtcolor)
        self.sleepdesc = self.uitext.render(
            'Spend the night at the Inn. (20 Gold)', False, self.txtcolor)
        self.txtbox = gameui.TextBox()
        self.statustxt = self.uitext.render('- STATUS -', True, self.txtcolor)
        self.face = pygame.image.load("data/sprites/f1.png").convert_alpha()
        self.wepicon = pygame.image.load(
            "data/sprites/wepicon.png").convert_alpha()
        self.armicon = pygame.image.load(
            "data/sprites/armicon.png").convert_alpha()
        self.accicon = pygame.image.load(
            "data/sprites/accicon.png").convert_alpha()
        self.sunIcon = pygame.image.load(
            "data/sprites/sun.png").convert_alpha()  # Icon for clock
        self.eveIcon = pygame.image.load(
            "data/sprites/eve.png").convert_alpha()  # Icon for clock
        self.moonIcon = pygame.image.load(
            "data/sprites/moon.png").convert_alpha()  # Icon for clock
        self.talked = False
        self.coinAnim = pyganim.PygAnimation(
            [("data/sprites/coin1.png", 0.1), ("data/sprites/coin2.png", 0.1), ("data/sprites/coin3.png", 0.1),
             ("data/sprites/coin4.png", 0.1), ("data/sprites/coin5.png",
                                               0.1), ("data/sprites/coin6.png", 0.1),
             ("data/sprites/coin7.png", 0.1), ("data/sprites/coin8.png", 0.1), ("data/sprites/coin9.png", 0.1)])
        self.coinAnim.play()
        self.shopkeep = True
        self.loaditems = False
        self.item_desc = ''
        self.buysound = pygame.mixer.Sound('data/sounds&music/Shop1.ogg')
        self.buysound.set_volume(0.05)
        self.equip_sound = pygame.mixer.Sound('data/sounds&music/Open1.ogg')
        self.equip_sound.set_volume(0.05)
        self.Talk = -1
        self.sysopt1 = self.uitext.render('Save Game', False, self.txtcolor)
        self.sysopt2 = self.uitext.render('Quit Game', False, self.txtcolor)
        self.sysopt3 = self.uitext.render('Cancel', False, self.txtcolor)
        self.syscursorpos = 0
        self.savesound = pygame.mixer.Sound('data/sounds&music/Save.ogg')
        self.savesound.set_volume(0.05)
        self.batopt1 = self.uitext.render(
            'Fight a regular enemy', False, self.txtcolor)
        self.battalk = True
        self.batcursorpos = False
        self.popup_message = ''
        self.pb_dialogue = False
        self.pbtalk = 0
        self.cur_dialogue = [[]]  # Current dialogue in talk
        self.draw_ui_flag = True # Replaces global drawui

    def arena(self, floor=1):  # Main ui in the arena
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))
        self.surface.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 48))
        self.surface.blit(pygame.transform.scale(self.bg, (300, 300)), (905, 430))
        self.surface.blit(self.talktxt, (946, 496))
        self.surface.blit(self.battxt, (946, 526))
        self.surface.blit(self.stattxt, (946, 556))
        self.surface.blit(self.shoptxt, (946, 586))
        self.surface.blit(self.inntxt, (946, 616))
        self.surface.blit(self.systxt, (946, 646))
        self.cur = self.uitext.render(
            'Floor:  %d' % floor, False, self.txtcolor)  # Current floor
        self.surface.blit(self.cur, (27, 61))
        if self.cursorpos == 0:
            self.surface.blit(self.cursor, (916, 496))
            self.surface.blit(self.talkdesc, (112, 490))
        if self.cursorpos == 1:
            self.surface.blit(self.cursor, (916, 526))
            self.surface.blit(self.batdesc, (112, 490))
        if self.cursorpos == 2:
            self.surface.blit(self.cursor, (916, 556))
            self.surface.blit(self.statdesc, (112, 490))
        if self.cursorpos == 3:
            self.surface.blit(self.cursor, (916, 586))
            self.surface.blit(self.shopdesc, (112, 490))
        if self.cursorpos == 4:
            self.surface.blit(self.cursor, (916, 616))
            self.surface.blit(self.inndesc, (112, 490))
        if self.cursorpos == 5:
            self.surface.blit(self.cursor, (916, 646))
            self.surface.blit(self.sysdesc, (112, 490))

    def clock(self, hours, minutes):  # draw ui for the clock
        if minutes == 0:
            minutes = '00'  # Double zeros because that's how clocks work
        timetxt = str(hours) + ':' + str(minutes)
        self.time = self.uitext.render(timetxt, False, self.txtcolor)
        self.surface.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 81))
        self.surface.blit(self.time, (27, 94))
        if hours >= 6 and hours < 14:  # Day
            self.surface.blit(pygame.transform.scale(self.sunIcon, (40, 30)), (90, 93))
        if hours >= 14 and hours < 20:  # Afternoon
            self.surface.blit(pygame.transform.scale(self.eveIcon, (20, 30)), (90, 93))
        if hours >= 20 or hours < 6:  # Night
            self.surface.blit(pygame.transform.scale(
                self.moonIcon, (35, 25)), (90, 97))

    def talk(self, val, player):
        self.draw_ui_flag = False
        self.Talk = val
        if not self.talked:
            if player.progress == 1:
                self.cur_dialogue = [[]]  # These are converted from the old textbox, so for compatibility
                if self.Talk == 0:
                    self.txtbox.draw_textbox([["data/sprites/oldman.png", 'Old Man',
                                             'I heard the monsters on the first floor are quite weak. You mustn\'t underestimate them However!\nConsider Equipping yourself with new equipment from the Shop.',
                                               ]], self.surface, (0, 400))
                elif self.Talk == 1:

                    self.txtbox.draw_textbox(
                        [["data/sprites/boy.png", 'Boy', 'Wow mister, you\'re going to fight in the Arena? So cool!']], self.surface, (0, 400))

                elif self.Talk == 2:

                    self.txtbox.draw_textbox([["data/sprites/youngman.png", 'Young Man',
                                             'In the 50 years that the Arena has been open, there has been only one winner. It was the legendary Hero known as Zen. That was 2 years ago though, nobody has seen him since.']], self.surface, (0, 400))
                elif self.Talk == 3:
                    self.txtbox.draw_textbox([["data/sprites/mysteryman.png", 'Stranger',
                                             'You...\nNevermind. Good luck in the Arena, I\'ll be keeping an eye on you.']], self.surface, (0, 400))
            elif player.progress == 2:
                if self.Talk == 0:
                    self.cur_dialogue = self.dialogues["floor2_oldman"]
                    self.txtbox.draw_textbox(self.cur_dialogue, self.surface, (0, 400))
                elif self.Talk == 1:
                    self.cur_dialogue = self.dialogues["floor2_boy"]
                    self.txtbox.draw_textbox(self.cur_dialogue, self.surface, (0, 400))
                elif self.Talk == 2:
                    if player.pclass == "mage":
                        self.cur_dialogue = self.dialogues["floor2_youngman_m"]
                    else:
                        self.cur_dialogue = self.dialogues["floor2_youngman_w"]
                    self.txtbox.draw_textbox(self.cur_dialogue, self.surface, (0, 400))
                elif self.Talk == 3:
                    self.cur_dialogue = self.dialogues["floor2_noble"]
                    self.txtbox.draw_textbox(self.cur_dialogue, self.surface, (0, 400))

    def status(self, player):
        self.surface.blit(self.status_bg, (53, 30))
        nametxt = self.uitext.render(
            'Name: ' + player.name, False, self.txtcolor)
        self.surface.blit(nametxt, (169, 207))
        strtxt = self.uitext.render(
            'STR: %d' % player.stre, False, self.txtcolor)
        if player.add_stre > 0:
            strtxt2 = self.uitext.render(
                '(+%d)' % player.add_stre, False, (0, 200, 0))
        elif player.add_stre == 0:
            strtxt2 = self.uitext.render(
                '(%d)' % player.add_stre, False, (95, 100, 100))
        else:
            strtxt2 = self.uitext.render(
                '(+%d)' % player.add_stre, False, (200, 0, 0))
        stat_points = self.uitext.render(
            'Stat points: %d' % player.stat_points, False, (46, 69, 184))
        self.surface.blit(stat_points, (430, 247))
        self.surface.blit(strtxt, (169, 247))
        self.surface.blit(strtxt2, (299, 247))
        deftxt = self.uitext.render(
            'DEF: %d' % player.defe, False, self.txtcolor)
        if player.add_defe > 0:
            deftxt2 = self.uitext.render(
                '(+%d)' % player.add_defe, False, (0, 200, 0))
        elif player.add_defe == 0:
            deftxt2 = self.uitext.render(
                '(+%d)' % player.add_defe, False, (95, 100, 100))
        else:
            deftxt2 = self.uitext.render(
                '(%d)' % player.add_defe, False, (200, 0, 0))
        self.surface.blit(deftxt, (169, 287))
        self.surface.blit(deftxt2, (299, 287))
        lucktxt = self.uitext.render(
            'LUCK: %d' % player.luck, False, self.txtcolor)
        self.surface.blit(lucktxt, (169, 367))
        magtxt = self.uitext.render(
            'MAG: %d' % player.mag, False, self.txtcolor)
        if player.add_mag > 0:
            magtxt2 = self.uitext.render(
                '(+%d)' % player.add_mag, False, (0, 200, 0))
        elif player.add_mag == 0:
            magtxt2 = self.uitext.render(
                '(+%d)' % player.add_mag, False, (95, 100, 100))
        else:
            magtxt2 = self.uitext.render(
                '(%d)' % player.add_mag, False, (200, 0, 0))
        self.surface.blit(magtxt, (169, 327))
        self.surface.blit(magtxt2, (299, 327))
        lvltxt = self.uitext.render('Level: %d' %
                                    player.level, False, self.txtcolor2)
        self.surface.blit(lvltxt, (607, 396))
        xp_txt = self.uitext2.render('Exp till next level: {}'.format(
            player.xp_till_levelup(player.level) - player.exp), False, self.txtcolor2)
        self.surface.blit(xp_txt, (607, 426))
        self.surface.blit(self.face, (679, 207))
        classtxt = self.uitext.render(
            player.pclass.capitalize(), False, self.txtcolor)
        self.surface.blit(classtxt, (697, 366))
        self.surface.blit(self.statustxt, (417, 141))
        weptxt = self.uitext2.render(
            'WEAPON: ' + self.item_data['weapons'][player.cur_weapon]['name'], False, self.txtcolor2)
        armtxt = self.uitext2.render(
            'ARMOR: ' + self.item_data['armours'][player.cur_armour]['name'], False, self.txtcolor2)
        acctxt = self.uitext2.render('ACCESSORY: ' + self.item_data['accessories'][player.cur_accessory]['name'], False,
                                     self.txtcolor2)
        self.surface.blit(self.wepicon, (169, 407))
        self.surface.blit(weptxt, (209, 407))
        self.surface.blit(self.armicon, (169, 447))
        self.surface.blit(armtxt, (209, 447))
        self.surface.blit(self.accicon, (169, 487))
        self.surface.blit(acctxt, (209, 487))
        floorktxt = self.uitext.render(
            'Enemies killed on this floor: %d' % player.fkills, False, self.txtcolor3)
        totktxt = self.uitext.render(
            'Total enemies killed: %d' % player.tkills, False, self.txtcolor3)
        self.surface.blit(floorktxt, (169, 527))
        self.surface.blit(totktxt, (168, 567))
        self.status_menu(player)
        self.txtbox.popup_message(self.popup_message, self.surface)

    def change_equipment(self, player):
        self.surface.blit(self.equip_menu_bg, (self.window_x, 45))
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
                        weapon_idx = player.wep_owned[i]
                        weapon = self.item_data['weapons'][weapon_idx]
                        self.surface.blit(self.uitext.render(
                            weapon['name'], False, self.txtcolor), (980, 110 + 55 * (i - self.min_pos)))
                self.cur_id = player.wep_owned[self.min_pos +
                                               self.equip_cursor2_pos]
                if self.min_pos != 0:
                    self.surface.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    self.surface.blit(self.cursor_down, (1085, 360))

            else:
                no_item = True
                self.item_desc = ''
                self.surface.blit(self.uitext.render("No weapons owned",
                          False, self.txtcolor), (980, 110))
        elif self.equip_cursor1_pos == 1:
            self.max_pos = len(player.arm_owned)
            if len(player.arm_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        armour_idx = player.arm_owned[i]
                        armour = self.item_data['armours'][armour_idx]
                        self.surface.blit(self.uitext.render(
                            armour['name'], False, self.txtcolor), (980, 110 + 55 * (i - self.min_pos)))
                self.cur_id = player.arm_owned[self.min_pos +
                                               self.equip_cursor2_pos]
                if self.min_pos != 0:
                    self.surface.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    self.surface.blit(self.cursor_down, (1085, 360))
            else:
                no_item = True
                self.surface.blit(self.uitext.render("No armours owned",
                          False, self.txtcolor), (980, 110))
        elif self.equip_cursor1_pos == 2:
            self.max_pos = len(player.acc_owned)
            if len(player.acc_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        acc_idx = player.acc_owned[i]
                        acc = self.item_data['accessories'][acc_idx]
                        self.surface.blit(self.uitext.render(
                            acc['name'], False, self.txtcolor), (980, 110 + 55 * (i - self.min_pos)))
                self.cur_id = player.acc_owned[self.min_pos +
                                               self.equip_cursor2_pos]
                if self.min_pos != 0:
                    self.surface.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    self.surface.blit(self.cursor_down, (1085, 360))
            else:
                no_item = True
                self.item_desc = ''
                self.surface.blit(self.uitext.render("No accessories owned",
                          False, self.txtcolor), (980, 110))
        if self.equip_flag2:
            if self.equip_cursor2_pos == 0:
                self.surface.blit(self.cursor, (940, 110))
            elif self.equip_cursor2_pos == 1:
                self.surface.blit(self.cursor, (940, 170))
            elif self.equip_cursor2_pos == 2:
                self.surface.blit(self.cursor, (940, 225))
            elif self.equip_cursor2_pos == 3:
                self.surface.blit(self.cursor, (940, 280))
            elif self.equip_cursor2_pos == 4:
                self.surface.blit(self.cursor, (940, 335))
            if self.equip_cursor1_pos == 0:
                cur_desc = self.item_data["weapons"]
            elif self.equip_cursor1_pos == 1:
                cur_desc = self.item_data["armours"]
            elif self.equip_cursor1_pos == 2:
                cur_desc = self.item_data["accessories"]
            if not no_item:
                self.item_desc = self.uitext2.render(
                    cur_desc[self.cur_id]["description"], False, self.txtcolor2)
                hover_item_str = self.uitext2.render(
                    "STR:" + str(cur_desc[self.cur_id]["atk"]), False, self.txtcolor2)
                hover_item_def = self.uitext2.render(
                    "DEF:" + str(cur_desc[self.cur_id]["def"]), False, self.txtcolor2)
                hover_item_mag = self.uitext2.render(
                    "MAG:" + str(cur_desc[self.cur_id]["mag"]), False, self.txtcolor2)
                self.surface.blit(self.item_desc, (120, 620))
                self.surface.blit(hover_item_str, (605, 500))
                self.surface.blit(hover_item_def, (605, 540))
                self.surface.blit(hover_item_mag, (605, 580))

    def stat_point_alloc(self, player):
        if self.stat_cursor_pos == 0:
            self.surface.blit(self.cursor, (255, 250))
            self.surface.blit(self.cursor_left, (135, 247))
        elif self.stat_cursor_pos == 1:
            self.surface.blit(self.cursor, (255, 290))
            self.surface.blit(self.cursor_left, (135, 287))
        elif self.stat_cursor_pos == 2:
            self.surface.blit(self.cursor, (265, 330))
            self.surface.blit(self.cursor_left, (135, 327))
        if self.stat_cursor_pos > 2:
            self.stat_cursor_pos = 0
        elif self.stat_cursor_pos < 0:
            self.stat_cursor_pos = 2
        if self.confirm:
            self.txtbox.confirm_box('Confirm Changes?', self.surface)

    def status_menu(self, player):
        self.surface.blit(self.status_menu_bg, (955, 405))
        self.surface.blit(self.equip_txt, (990, 465))
        self.surface.blit(self.stats_txt, (990, 505))
        self.surface.blit(self.back_txt, (990, 545))
        if self.status_cur_pos == 0:
            self.surface.blit(self.cursor, (950, 465))
        elif self.status_cur_pos == 1:
            self.surface.blit(self.cursor, (950, 505))
        elif self.status_cur_pos == 2:
            self.surface.blit(self.cursor, (950, 545))
        if self.equip_flag1:
            if self.equip_cursor1_pos == 0:
                self.surface.blit(self.cursor, (140, 410))
            elif self.equip_cursor1_pos == 1:
                self.surface.blit(self.cursor, (140, 450))
            elif self.equip_cursor1_pos == 2:
                self.surface.blit(self.cursor, (140, 490))
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

    def handle_status_inputs(self, player, event):
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
                                    player.wep_owned.insert(
                                        i, player.cur_weapon)
                                    player.cur_weapon = self.cur_id
                        elif self.equip_cursor1_pos == 1 and len(player.arm_owned) > 0:
                            for i in range(len(player.arm_owned)):
                                if player.arm_owned[i] == self.cur_id:
                                    player.arm_owned.remove(self.cur_id)
                                    player.arm_owned.insert(
                                        i, player.cur_armour)
                                    player.cur_armour = self.cur_id
                        elif self.equip_cursor1_pos == 2 and len(player.acc_owned) > 0:
                            for i in range(len(player.acc_owned)):
                                if player.acc_owned[i] == self.cur_id:
                                    player.acc_owned.remove(self.cur_id)
                                    player.acc_owned.insert(
                                        i, player.cur_accessory)
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
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 2.7), int(curheight / 3))), (470, 200))
        self.surface.blit(self.sysopt1, (528, 259))
        self.surface.blit(self.sysopt2, (528, 299))
        self.surface.blit(self.sysopt3, (528, 339))
        if self.syscursorpos == 0:
            self.surface.blit(self.cursor, (498, 259))
        if self.syscursorpos == 1:
            self.surface.blit(self.cursor, (498, 299))
        if self.syscursorpos == 2:
            self.surface.blit(self.cursor, (498, 339))
        if self.syscursorpos > 2:
            self.syscursorpos = 0
        if self.syscursorpos < 0:
            self.syscursorpos = 2

    def battle_choice(self, monkill):
        curwidth, curheight = self.surface.get_size()
        if self.battalk:
            montokill = 5 - monkill
            if monkill < 5:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'You have %d monter(s) left to kill. You\'re almost there!' % montokill]], self.surface, (0, 400))
            if monkill >= 5:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'You can challenge the floor boss! Are you prepared for it?']], self.surface, (0, 400))

        if not self.battalk:
            if monkill >= 5:
                self.batopt2 = self.uitext.render(
                    'Challenge the floor boss', False, self.txtcolor)
            elif monkill < 5:
                self.batopt2 = self.uitext.render(
                    'Challenge the floor boss', False, (105, 109, 114))
            self.surface.blit(pygame.transform.scale(
                self.bg, (int(curwidth / 2.7), int(curheight / 3))), (470, 200))
            self.surface.blit(self.batopt1, (528, 259))
            self.surface.blit(self.batopt2, (528, 299))
            self.surface.blit(self.sysopt3, (528, 339))
            if self.batcursorpos == 0:
                self.surface.blit(self.cursor, (498, 259))
            if self.batcursorpos == 1:
                self.surface.blit(self.cursor, (498, 299))
            if self.batcursorpos == 2:
                self.surface.blit(self.cursor, (498, 339))
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
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                   'That was a good battle! If you\'re injured make sure to rest up at the inn.'
                                     ]], self.surface, (0, 400))
        elif self.pbtalk == 1 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                   'Good job! Make sure to use the gold from your battle to buy equipment from our Shop!']], self.surface, (0, 400))
        elif self.pbtalk == 2 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                   'Nice work! You\'re pretty skilled, are you sure you haven\'t done this before?'
                                     ]], self.surface, (0, 400))
        elif self.pbtalk == 3 and progress == 1:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     'Good work out there! I overheard some strange people talking about you. Something about.. A debt?']], self.surface, (0, 400))
        if self.pbtalk == 0 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "Good work! Maybe I should bet some money on you next time, huh? *laughs*"
                                     ]], self.surface, (0, 400))
        elif self.pbtalk == 1 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "... Oh you're already done? Good job, sorry about that I was a bit lost in my own thoughts!"]], self.surface, (0, 400))
        elif self.pbtalk == 2 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "Great job! How'd you get so strong? What's your secret?"
                                     ]], self.surface, (0, 400))
        elif self.pbtalk == 3 and progress == 2:
            self.pb_dialogue = True
            self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "If you would like to get stronger, don't forget to buy new equipment! Or just keep killing these monsters for experience!"]], self.surface, (0, 400))

    def draw_inn(self, gold):
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        self.surface.blit(pygame.transform.scale(
            self.bg, (170, 50)), (10, 48))  # Gold box
        self.surface.blit(pygame.transform.scale(self.bg, (300, 300)),
                  (905, 430))  # Actions box
        self.surface.blit(self.talktxt, (946, 496))
        self.surface.blit(self.sleeptxt, (946, 526))
        self.surface.blit(self.backtxt, (946, 556))
        # Current gold with the player
        self.cur = self.uitext2.render(
            'Gold:  %d' % gold, False, self.txtcolor)
        self.coinAnim.blit(self.surface, (22, 62))  # Gold icon
        self.surface.blit(self.cur, (47, 62))
        if self.cursorpos == 0:
            self.surface.blit(self.cursor, (916, 496))
            self.surface.blit(self.talkdesc2, (112, 490))
        if self.cursorpos == 1:
            self.surface.blit(self.cursor, (916, 526))
            self.surface.blit(self.sleepdesc, (112, 490))
        if self.cursorpos == 2:
            self.surface.blit(self.cursor, (916, 556))
            self.surface.blit(self.backdesc, (112, 490))

    def draw_town(self, player):
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        self.surface.blit(pygame.transform.scale(
            self.bg, (170, 50)), (10, 29))  # Gold box
        self.surface.blit(pygame.transform.scale(self.bg, (300, 300)),
                  (905, 430))  # Actions box
        self.surface.blit(self.talktxt, (946, 496))
        self.surface.blit(self.inntxt, (946, 526))
        self.surface.blit(self.slumstxt, (946, 556))
        self.surface.blit(self.backtxt, (946, 586))
        # Current gold with the player
        gold = self.uitext2.render('Gold:  %d' %
                                   player.gold, False, self.txtcolor)
        self.coinAnim.blit(self.surface, (22, 45))  # Gold icon
        self.surface.blit(gold, (47, 45))
        if self.cursorpos == 0:
            self.surface.blit(self.cursor, (916, 496))
            self.surface.blit(self.talkdesc3, (112, 490))
        elif self.cursorpos == 1:
            self.surface.blit(self.cursor, (916, 526))
            self.surface.blit(self.inndesc, (112, 490))
        elif self.cursorpos == 2:
            self.surface.blit(self.cursor, (916, 556))
            self.surface.blit(self.slumsdesc, (112, 490))
        elif self.cursorpos == 3:
            self.surface.blit(self.cursor, (916, 586))
            self.surface.blit(self.backdesc, (112, 490))
        elif self.cursorpos > 3:
            self.cursorpos = 0
        elif self.cursorpos < 0:
            self.cursorpos = 3
        self.clock(player.hours, player.minutes)

    def draw_casino(self, player):  # Draws the casino UI
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        self.surface.blit(pygame.transform.scale(
            self.bg, (170, 50)), (10, 29))  # Gold box
        self.surface.blit(pygame.transform.scale(self.bg, (300, 300)),
                  (905, 430))  # Actions box
        self.surface.blit(self.talktxt, (946, 496))
        self.surface.blit(self.sleeptxt, (946, 526))
        self.surface.blit(self.casino_text, (946, 556))
        self.surface.blit(self.backtxt, (946, 586))
        # Current gold with the player
        gold = self.uitext2.render('Gold:  %d' %
                                   player.gold, False, self.txtcolor)
        self.coinAnim.blit(self.surface, (22, 45))  # Gold icon
        self.surface.blit(gold, (47, 45))
        if self.cursorpos == 0:
            self.surface.blit(self.cursor, (916, 496))
            self.surface.blit(self.talkdesc3, (112, 490))
        elif self.cursorpos == 1:
            self.surface.blit(self.cursor, (916, 526))
            self.surface.blit(self.inndesc, (112, 490))
        elif self.cursorpos == 2:
            self.surface.blit(self.cursor, (916, 556))
            self.surface.blit(self.casino_desc, (112, 490))
        elif self.cursorpos == 3:
            self.surface.blit(self.cursor, (916, 586))
            self.surface.blit(self.backdesc, (112, 490))
        elif self.cursorpos > 3:
            self.cursorpos = 0
        elif self.cursorpos < 0:
            self.cursorpos = 3
        self.clock(player.hours, player.minutes)


class SelectOptions(MainUi):
    def __init__(self, surface, item_data, dialogues):
        MainUi.__init__(self, surface, item_data, dialogues)
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
            [("data/sprites/alert1.png", 0.4), ("data/sprites/alert2.png", 0.4)])
        self.alertAnim.scale([35, 35])
        self.alertAnim.play()

    def drawUi(self, no=1, opt1='1', opt2='2', opt3='3', opt4='4', opt5='5',
               opt6='6'):  # Select option among 6 or fewer choices,where no is the number of choices
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))
        Option1 = self.uitext.render(opt1, False, self.txtcolor)
        Option2 = self.uitext.render(opt2, False, self.txtcolor)
        Option3 = self.uitext.render(opt3, False, self.txtcolor)
        Option4 = self.uitext.render(opt4, False, self.txtcolor)
        Option5 = self.uitext.render(opt5, False, self.txtcolor)
        Option6 = self.uitext.render(opt6, False, self.txtcolor)
        backTxt = self.uitext.render('Back', False, self.txtcolor)
        self.surface.blit(Option1, (80, 490))  # Row 1
        if self.alert1:  # If the option is new/updated show alert.
            self.alertAnim.blit(self.surface, (80 + Option1.get_width(), 490))
        if no >= 2:
            self.surface.blit(Option2, (280, 490))
            if self.alert2:
                self.alertAnim.blit(self.surface, (280 + Option2.get_width(), 490))
            if no >= 3:
                self.surface.blit(Option3, (480, 490))
                if self.alert3:
                    self.alertAnim.blit(self.surface, (480 + Option3.get_width(), 490))
                if no >= 4:
                    self.surface.blit(Option4, (80, 590))  # Row 2
                    if self.alert4:
                        self.alertAnim.blit(
                            self.surface, (80 + Option4.get_width(), 590))
                    if no >= 5:
                        self.surface.blit(Option5, (280, 590))
                        if self.alert5:
                            self.alertAnim.blit(
                                self.surface, (280 + Option5.get_width(), 590))
                        if no >= 6:
                            self.surface.blit(Option6, (480, 590))
                            if self.alert6:
                                self.alertAnim.blit(
                                    self.surface, (480 + Option6.get_width(), 590))
        self.surface.blit(backTxt, (680, 590))  # Exit
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
                self.colpos = 0
                self.rowpos = 1
        if self.rowpos == 1:
            if self.colpos == 0:
                self.surface.blit(self.cursor, (40, 590))
            elif self.colpos == 1:
                self.surface.blit(self.cursor, (240, 590))
            elif self.colpos == 2:
                self.surface.blit(self.cursor, (440, 590))
            elif self.colpos == 3:
                self.surface.blit(self.cursor, (640, 590))
        elif self.rowpos == 0:
            if self.colpos == 0:
                self.surface.blit(self.cursor, (40, 490))
            elif self.colpos == 1:
                self.surface.blit(self.cursor, (240, 490))
            elif self.colpos == 2:
                self.surface.blit(self.cursor, (440, 490))
