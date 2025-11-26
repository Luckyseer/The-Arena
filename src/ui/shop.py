import pygame
from src.ui.main_ui import MainUi
from src.models.player import Player

class Shop(MainUi):
    def __init__(self, surface, item_data, dialogues):
        MainUi.__init__(self, surface, item_data, dialogues)
        self.item_data = item_data
        self.weapons_list = item_data['weapons']
        self.armour_list = item_data['armours']
        self.acc_list = item_data['accessories']
        self.consume_list = item_data['consumables']
        self.player_data = Player(item_data) # Default player, will be overwritten
        self.shopbg = pygame.image.load(
            "data/backgrounds/shopbg.png").convert_alpha()
        self.pstr = 1
        self.pdef = 1
        self.pmag = 1
        self.pluck = 1
        self.shoptxt = ['Weapons', 'Armour', 'Accessories', 'Items']
        self.shoptxt2 = ['Name', 'Cost']
        self.title_text = pygame.font.Font("data/fonts/Daisy_Roots.otf", 50)
        self.shop_cursor_pos1 = 0  # for choosing the type of item
        self.shop_cursor_pos2 = 0  # for choosing from the list of items
        self.min_pos = 0  # minimum position for the item in the list
        self.max_pos = 0  # maximum position for an item in the list
        self.shop_page = 0
        self.no_sell_flag = False  # Flag for when the shop has no items in a category
        self.shop_selection_flag = True
        self.status_bg = pygame.transform.scale(
            self.bg, (300, 500)).convert_alpha()
        self.status_anim = False
        self.green_rgb = (0, 200, 0)
        self.red_rgb = (200, 0, 0)
        self.box_pos = 2000
        self.current_list = []  # which set of items you're currently viewing
        self.buzzer = pygame.mixer.Sound('data/sounds&music/Buzzer1.ogg')
        self.buzzer.set_volume(0.05)

    def get_player_stats(self, player_data):
        self.player_data = player_data
        self.pstr = self.player_data.stre + self.player_data.add_stre
        self.pdef = self.player_data.defe + self.player_data.add_defe
        self.pmag = self.player_data.mag + self.player_data.add_mag
        self.pluck = self.player_data.luck

    def status_window(self, item, player_data):
        self.get_player_stats(player_data)
        if self.current_list == self.consume_list:
            item_desc = self.uitext2.render(
                item['description'], False, self.txtcolor2)
            self.surface.blit(item_desc, (120, 660))
            if self.min_pos != 0:
                self.surface.blit(self.cursor_up, (212, 303))
            if self.min_pos + 5 != self.max_pos:
                # Downward facing arrow to show that more items are available
                self.surface.blit(self.cursor_down, (212, 623))
        else:
            if not self.status_anim:
                self.box_pos = 2000
                self.status_anim = True
            if self.status_anim:
                if self.box_pos > 950:
                    self.box_pos -= 50

            self.surface.blit(self.status_bg, (self.box_pos, 222))
            if self.box_pos <= 950:
                str_txt = self.uitext.render(
                    'STR: ' + str(self.pstr), False, self.txtcolor3)
                def_txt = self.uitext.render(
                    'DEF: ' + str(self.pdef), False, self.txtcolor3)
                mag_txt = self.uitext.render(
                    'MAG: ' + str(self.pmag), False, self.txtcolor3)
                luk_txt = self.uitext.render(
                    'LUCK: ' + str(self.pluck), False, self.txtcolor3)
                item_desc = self.uitext2.render(
                    item['description'], False, self.txtcolor2)
                if self.current_list == self.weapons_list:
                    player_item = player_data.cur_weapon

                elif self.current_list == self.armour_list:
                    player_item = player_data.cur_armour
                else:
                    player_item = player_data.cur_accessory

                str_dif = self.pstr + \
                    item['atk'] - \
                    (self.pstr + self.current_list[player_item]['atk'])
                def_dif = self.pdef + \
                    item['def'] - \
                    (self.pdef + self.current_list[player_item]['def'])
                mag_dif = self.pmag + \
                    item['mag'] - \
                    (self.pmag + self.current_list[player_item]['mag'])
                if str_dif >= 0:
                    str_diftxt = self.uitext.render(
                        '(+' + str(str_dif) + ')', False, self.green_rgb)
                    self.surface.blit(str_diftxt, (1120, 300))
                else:
                    str_diftxt = self.uitext.render(
                        '(' + str(str_dif) + ')', False, self.red_rgb)
                    self.surface.blit(str_diftxt, (1120, 300))
                if def_dif >= 0:
                    def_diftxt = self.uitext.render(
                        '(+' + str(def_dif) + ')', False, self.green_rgb)
                    self.surface.blit(def_diftxt, (1120, 370))
                else:
                    def_diftxt = self.uitext.render(
                        '(' + str(def_dif) + ')', False, self.red_rgb)
                    self.surface.blit(def_diftxt, (1120, 370))
                if mag_dif >= 0:
                    mag_diftxt = self.uitext.render(
                        '(+' + str(mag_dif) + ')', False, self.green_rgb)
                    self.surface.blit(mag_diftxt, (1120, 440))
                else:
                    mag_diftxt = self.uitext.render(
                        '(' + str(mag_dif) + ')', False, self.red_rgb)
                    self.surface.blit(mag_diftxt, (1120, 440))
                if self.min_pos + 5 != self.max_pos:
                    # Downward facing arrow to show that more items are available
                    self.surface.blit(self.cursor_down, (212, 623))
                if self.min_pos != 0:
                    self.surface.blit(self.cursor_up, (212, 303))
                self.surface.blit(item_desc, (120, 660))
                self.surface.blit(str_txt, (1000, 300))
                self.surface.blit(def_txt, (1000, 370))
                self.surface.blit(mag_txt, (1000, 440))
                self.surface.blit(luk_txt, (1000, 510))

    def buy_item(self, item_id):
        if self.player_data.gold < self.current_list[item_id]['cost']:
            self.buzzer.play()
            self.popup_message = "Not enough gold!"
            self.txtbox.toggle_popup_flag()
        elif self.current_list == self.weapons_list and (item_id in self.player_data.wep_owned or self.player_data.cur_weapon == item_id):
            self.buzzer.play()
            self.popup_message = "You already own that weapon!"
            self.txtbox.toggle_popup_flag()
        elif self.current_list == self.armour_list and (item_id in self.player_data.arm_owned or self.player_data.cur_armour == item_id):
            self.popup_message = "You already own that armour!"
            self.txtbox.toggle_popup_flag()
            self.buzzer.play()
        elif self.current_list == self.acc_list and (item_id in self.player_data.acc_owned or self.player_data.cur_accessory == item_id):
            self.buzzer.play()
            self.popup_message = "You already own that accessory!"
            self.txtbox.toggle_popup_flag()
        else:
            self.buysound.play()
            return True

    def draw_shop(self, shop_name='', player_data=None):
        if player_data is None:
            player_data = self.player_data
        
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
                wepnamelist.append(weapon['name'])
                wepcostlist.append(str(weapon['cost']))
                wepstatlist.append(
                    str([weapon['atk'], weapon['def'], weapon['mag']]))
                wepattributelist.append(weapon['attributes'])
            for armour in self.armour_list:
                armnamelist.append(armour['name'])
                armcostlist.append(str(armour['cost']))
                armstatlist.append(
                    str([armour['atk'], armour['def'], armour['mag']]))
                armattributelist.append(armour['attributes'])
            for accessory in self.acc_list:
                accnamelist.append(accessory['name'])
                acccostlist.append(str(accessory['cost']))
                accstatlist.append(
                    str([accessory['atk'], accessory['def'], accessory['mag']]))
                accattributelist.append(accessory['attributes'])
            for consumable in self.consume_list:
                connamelist.append(consumable['name'])
                concostlist.append(str(consumable['cost']))
                constatlist.append(str([consumable['hp'], consumable['mp']]))
            shop_title = self.title_text.render(
                shop_name, True, self.txtcolor2)

        if self.shopkeep:
            self.txtbox.draw_textbox([["data/sprites/shopkeep.png", 'Shopkeeper',
                                     'Welcome to the Arena shop! How can I help you?']], self.surface, (0, 400))
        if not self.shopkeep:
            self.surface.blit(self.shopbg, (53, 30))
            self.surface.blit(shop_title, (360, 57))
            self.surface.blit(self.uitext.render(
                self.shoptxt[0], False, self.txtcolor3), (shop_text_pos, 150))
            self.surface.blit(self.uitext.render(
                self.shoptxt[1], False, self.txtcolor3), (shop_text_pos + 150, 150))
            self.surface.blit(self.uitext.render(
                self.shoptxt[2], False, self.txtcolor3), (shop_text_pos + 300, 150))
            self.surface.blit(self.uitext.render(
                self.shoptxt[3], False, self.txtcolor3), (shop_text_pos + 510, 150))
            self.surface.blit(self.uitext2.render(
                self.shoptxt2[0], False, (186, 31, 34)), (161, 290))
            self.surface.blit(self.uitext2.render(
                self.shoptxt2[1], True, (186, 31, 34)), (449, 290))
            self.surface.blit(pygame.transform.scale(self.bg, (170, 50)),
                      (925, 42))  # Gold box 10,48
            self.cur = self.uitext2.render('Gold:  %d' % player_data.gold, False,
                                           self.txtcolor)  # Current gold with the player
            self.coinAnim.blit(self.surface, (937, 56))  # Gold icon
            self.surface.blit(self.cur, (962, 56))
            if self.shop_page == 0:
                self.max_pos = len(self.weapons_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell weapons.", False, self.txtcolor3)
                    cost1 = self.uitext.render(
                        "", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    if self.min_pos in player_data.wep_owned or self.min_pos == self.player_data.cur_weapon:
                        item1 = self.uitext.render(
                            wepnamelist[self.min_pos], False, (86, 91, 99))
                        cost1 = self.uitext.render(
                            wepcostlist[self.min_pos], False, (86, 91, 99))
                        self.surface.blit(self.uitext2.render(
                            "Owned", False, (186, 31, 34)), (600, 339))
                    else:
                        item1 = self.uitext.render(
                            wepnamelist[self.min_pos], False, self.txtcolor3)
                        cost1 = self.uitext.render(
                            wepcostlist[self.min_pos], False, self.txtcolor3)
                    if self.max_pos >= 2:
                        if self.min_pos + 1 in player_data.wep_owned or self.min_pos + 1 == self.player_data.cur_weapon:
                            item2 = self.uitext.render(
                                wepnamelist[self.min_pos + 1], False, (86, 91, 99))
                            cost2 = self.uitext.render(
                                wepcostlist[self.min_pos + 1], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 399))
                        else:
                            item2 = self.uitext.render(
                                wepnamelist[self.min_pos + 1], False, self.txtcolor3)
                            cost2 = self.uitext.render(
                                wepcostlist[self.min_pos + 1], False, self.txtcolor3)
                    if self.max_pos >= 3:
                        if self.min_pos + 2 in player_data.wep_owned or self.min_pos + 2 == self.player_data.cur_weapon:
                            item3 = self.uitext.render(
                                wepnamelist[self.min_pos + 2], False, (86, 91, 99))
                            cost3 = self.uitext.render(
                                wepcostlist[self.min_pos + 2], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 459))
                        else:
                            item3 = self.uitext.render(
                                wepnamelist[self.min_pos + 2], False, self.txtcolor3)
                            cost3 = self.uitext.render(
                                wepcostlist[self.min_pos + 2], False, self.txtcolor3)
                    if self.max_pos >= 4:
                        if self.min_pos + 3 in player_data.wep_owned or self.min_pos + 3 == self.player_data.cur_weapon:
                            item4 = self.uitext.render(
                                wepnamelist[self.min_pos + 3], False, (86, 91, 99))
                            cost4 = self.uitext.render(
                                wepcostlist[self.min_pos + 3], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 519))
                        else:
                            item4 = self.uitext.render(
                                wepnamelist[self.min_pos + 3], False, self.txtcolor3)
                            cost4 = self.uitext.render(
                                wepcostlist[self.min_pos + 3], False, self.txtcolor3)
                    if self.max_pos >= 5:
                        if self.min_pos + 4 in player_data.wep_owned or self.min_pos + 4 == self.player_data.cur_weapon:
                            item5 = self.uitext.render(
                                wepnamelist[self.min_pos + 4], False, (86, 91, 99))
                            cost5 = self.uitext.render(
                                wepcostlist[self.min_pos + 4], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 579))
                        else:
                            item5 = self.uitext.render(
                                wepnamelist[self.min_pos + 4], False, self.txtcolor3)
                            cost5 = self.uitext.render(
                                wepcostlist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 1:
                self.max_pos = len(self.armour_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell armours.", False, self.txtcolor3)
                    cost1 = self.uitext.render(
                        "", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    if self.min_pos in player_data.arm_owned or self.min_pos == self.player_data.cur_armour:
                        item1 = self.uitext.render(
                            armnamelist[self.min_pos], False, (86, 91, 99))
                        cost1 = self.uitext.render(
                            armcostlist[self.min_pos], False, (86, 91, 99))
                        self.surface.blit(self.uitext2.render(
                            "Owned", False, (186, 31, 34)), (600, 339))
                    else:
                        item1 = self.uitext.render(
                            armnamelist[self.min_pos], False, self.txtcolor3)
                        cost1 = self.uitext.render(
                            armcostlist[self.min_pos], False, self.txtcolor3)
                    if self.max_pos >= 2:
                        if self.min_pos + 1 in player_data.arm_owned or self.min_pos + 1 == self.player_data.cur_armour:
                            item2 = self.uitext.render(
                                armnamelist[self.min_pos + 1], False, (86, 91, 99))
                            cost2 = self.uitext.render(
                                armcostlist[self.min_pos + 1], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 399))
                        else:
                            item2 = self.uitext.render(
                                armnamelist[self.min_pos + 1], False, self.txtcolor3)
                            cost2 = self.uitext.render(
                                armcostlist[self.min_pos + 1], False, self.txtcolor3)
                    if self.max_pos >= 3:
                        if self.min_pos + 2 in player_data.arm_owned or self.min_pos + 2 == self.player_data.cur_armour:
                            item3 = self.uitext.render(
                                armnamelist[self.min_pos + 2], False, (86, 91, 99))
                            cost3 = self.uitext.render(
                                armcostlist[self.min_pos + 2], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 459))
                        else:
                            item3 = self.uitext.render(
                                armnamelist[self.min_pos + 2], False, self.txtcolor3)
                            cost3 = self.uitext.render(
                                armcostlist[self.min_pos + 2], False, self.txtcolor3)
                    if self.max_pos >= 4:
                        if self.min_pos + 3 in player_data.arm_owned or self.min_pos + 3 == self.player_data.cur_armour:
                            item4 = self.uitext.render(
                                armnamelist[self.min_pos + 3], False, (86, 91, 99))
                            cost4 = self.uitext.render(
                                armcostlist[self.min_pos + 3], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 519))
                        else:
                            item4 = self.uitext.render(
                                armnamelist[self.min_pos + 3], False, self.txtcolor3)
                            cost4 = self.uitext.render(
                                armcostlist[self.min_pos + 3], False, self.txtcolor3)
                    if self.max_pos >= 5:
                        if self.min_pos + 4 in player_data.arm_owned or self.min_pos + 4 == self.player_data.cur_armour:
                            item5 = self.uitext.render(
                                armnamelist[self.min_pos + 4], False, (86, 91, 99))
                            cost5 = self.uitext.render(
                                armcostlist[self.min_pos + 4], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 579))
                        else:
                            item5 = self.uitext.render(
                                armnamelist[self.min_pos + 4], False, self.txtcolor3)
                            cost5 = self.uitext.render(
                                armcostlist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 2:
                self.max_pos = len(self.acc_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell accessories.", False, self.txtcolor3)
                    cost1 = self.uitext.render(
                        "", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    if self.min_pos in player_data.acc_owned or self.min_pos == self.player_data.cur_accessory:
                        item1 = self.uitext.render(
                            accnamelist[self.min_pos], False, (86, 91, 99))
                        cost1 = self.uitext.render(
                            acccostlist[self.min_pos], False, (86, 91, 99))
                        self.surface.blit(self.uitext2.render(
                            "Owned", False, (186, 31, 34)), (600, 339))
                    else:
                        item1 = self.uitext.render(
                            accnamelist[self.min_pos], False, self.txtcolor3)
                        cost1 = self.uitext.render(
                            acccostlist[self.min_pos], False, self.txtcolor3)
                    if self.max_pos >= 2:
                        if self.min_pos + 1 in player_data.acc_owned or self.min_pos + 1 == self.player_data.cur_accessory:
                            item2 = self.uitext.render(
                                accnamelist[self.min_pos + 1], False, (86, 91, 99))
                            cost2 = self.uitext.render(
                                acccostlist[self.min_pos + 1], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 399))
                        else:
                            item2 = self.uitext.render(
                                accnamelist[self.min_pos + 1], False, self.txtcolor3)
                            cost2 = self.uitext.render(
                                acccostlist[self.min_pos + 1], False, self.txtcolor3)
                    if self.max_pos >= 3:
                        if self.min_pos + 2 in player_data.acc_owned or self.min_pos + 2 == self.player_data.cur_accessory:
                            item3 = self.uitext.render(
                                accnamelist[self.min_pos + 2], False, (86, 91, 99))
                            cost3 = self.uitext.render(
                                acccostlist[self.min_pos + 2], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 459))
                        else:
                            item3 = self.uitext.render(
                                accnamelist[self.min_pos + 2], False, self.txtcolor3)
                            cost3 = self.uitext.render(
                                acccostlist[self.min_pos + 2], False, self.txtcolor3)
                    if self.max_pos >= 4:
                        if self.min_pos + 3 in player_data.acc_owned or self.min_pos + 3 == self.player_data.cur_accessory:
                            item4 = self.uitext.render(
                                accnamelist[self.min_pos + 3], False, (86, 91, 99))
                            cost4 = self.uitext.render(
                                acccostlist[self.min_pos + 3], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 519))
                        else:
                            item4 = self.uitext.render(
                                accnamelist[self.min_pos + 3], False, self.txtcolor3)
                            cost4 = self.uitext.render(
                                acccostlist[self.min_pos + 3], False, self.txtcolor3)
                    if self.max_pos >= 5:
                        if self.min_pos + 4 in player_data.acc_owned or self.min_pos + 4 == self.player_data.cur_accessory:
                            item5 = self.uitext.render(
                                accnamelist[self.min_pos + 4], False, (86, 91, 99))
                            cost5 = self.uitext.render(
                                acccostlist[self.min_pos + 4], False, (86, 91, 99))
                            self.surface.blit(self.uitext2.render(
                                "Owned", False, (186, 31, 34)), (600, 579))
                        else:
                            item5 = self.uitext.render(
                                accnamelist[self.min_pos + 4], False, self.txtcolor3)
                            cost5 = self.uitext.render(
                                acccostlist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 3:
                self.surface.blit(self.uitext2.render("In Inventory",
                          False, (186, 31, 34)), (590, 290))
                self.max_pos = len(self.consume_list)
                if self.max_pos == 0:
                    item1 = self.uitext.render(
                        "This shop does not sell consumables.", False, self.txtcolor3)
                    cost1 = self.uitext.render(
                        "", False, self.txtcolor3)
                    self.no_sell_flag = True
                else:
                    self.no_sell_flag = False
                    item1 = self.uitext.render(
                        connamelist[self.min_pos], False, self.txtcolor3)
                    cost1 = self.uitext.render(
                        concostlist[self.min_pos], False, self.txtcolor3)
                    for i in range(self.min_pos, self.max_pos):
                        for item in self.player_data.inventory:
                            if item["name"] == connamelist[i] and i <= self.min_pos + 4:
                                self.surface.blit(self.uitext2.render(
                                    str(item["amount"]), False, (31, 22, 21)), (610, 339 + 60 * (i - self.min_pos)))
                    if self.max_pos >= 2:
                        item2 = self.uitext.render(
                            connamelist[self.min_pos + 1], False, self.txtcolor3)
                        cost2 = self.uitext.render(
                            concostlist[self.min_pos + 1], False, self.txtcolor3)
                    if self.max_pos >= 3:
                        item3 = self.uitext.render(
                            connamelist[self.min_pos + 2], False, self.txtcolor3)
                        cost3 = self.uitext.render(
                            concostlist[self.min_pos + 2], False, self.txtcolor3)
                    if self.max_pos >= 4:
                        item4 = self.uitext.render(
                            connamelist[self.min_pos + 3], False, self.txtcolor3)
                        cost4 = self.uitext.render(
                            concostlist[self.min_pos + 3], False, self.txtcolor3)
                    if self.max_pos >= 5:
                        item5 = self.uitext.render(
                            connamelist[self.min_pos + 4], False, self.txtcolor3)
                        cost5 = self.uitext.render(
                            concostlist[self.min_pos + 4], False, self.txtcolor3)

            self.surface.blit(item1, (161, 339))
            self.surface.blit(cost1, (449, 339))

            if self.max_pos >= 2:
                self.surface.blit(item2, (161, 399))
                self.surface.blit(cost2, (449, 399))

            if self.max_pos >= 3:
                self.surface.blit(item3, (161, 459))
                self.surface.blit(cost3, (449, 459))

            if self.max_pos >= 4:
                self.surface.blit(item4, (161, 519))
                self.surface.blit(cost4, (449, 519))

            if self.max_pos >= 5:
                self.surface.blit(item5, (161, 579))
                self.surface.blit(cost5, (449, 579))

            if self.shop_selection_flag:  # while using cursor 1
                self.min_pos = 0
                self.shop_cursor_pos2 = 0
                self.status_anim = False
                if self.shop_cursor_pos1 == 0:
                    self.surface.blit(self.cursor, (shop_text_pos - 35, 150))
                    self.shop_page = 0
                    self.current_list = self.weapons_list
                if self.shop_cursor_pos1 == 1:
                    self.surface.blit(self.cursor, (shop_text_pos + 150 - 35, 150))
                    self.shop_page = 1
                    self.current_list = self.armour_list
                if self.shop_cursor_pos1 == 2:
                    self.surface.blit(self.cursor, (shop_text_pos + 300 - 35, 150))
                    self.shop_page = 2
                    self.current_list = self.acc_list
                if self.shop_cursor_pos1 == 3:
                    self.surface.blit(self.cursor, (shop_text_pos + 510 - 35, 150))
                    self.shop_page = 3
                    self.current_list = self.consume_list
                if self.shop_cursor_pos1 > 3:
                    self.shop_cursor_pos1 = 0
                elif self.shop_cursor_pos1 < 0:
                    self.shop_cursor_pos1 = 3
            if not self.shop_selection_flag:  # while using cursor 2
                if self.shop_cursor_pos2 == 0:
                    self.surface.blit(self.cursor, (120, 339))
                elif self.shop_cursor_pos2 == 1:
                    self.surface.blit(self.cursor, (120, 399))
                elif self.shop_cursor_pos2 == 2:
                    self.surface.blit(self.cursor, (120, 459))
                elif self.shop_cursor_pos2 == 3:
                    self.surface.blit(self.cursor, (120, 519))
                elif self.shop_cursor_pos2 == 4:
                    self.surface.blit(self.cursor, (120, 579))
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
                    self.current_list[self.shop_cursor_pos2 + self.min_pos], player_data)
            self.txtbox.popup_message(self.popup_message, self.surface)
