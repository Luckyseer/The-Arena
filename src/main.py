import pygame
import sys
import pickle
import random
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config
from src.data_loader import load_game_data
from src.models.player import Player
from src.ui.main_ui import MainUi, SelectOptions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
from src.ui.shop import Shop
from src.scenes.game_events import GameEvents
from src.engine.game_clock import GameClock
from src.engine.battle import NewBattle
from src.utils.timer import Timer, fadein, fadeout, posfinder
from data import splashscreen
from data import gameui
from data import pyganim

# Initialize Pygame
pygame.init()
pygame.mixer.init()

class Game:
    def __init__(self):
        self.screen = config.get_screen()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load Data
        self.game_data = load_game_data()
        self.item_data = self.game_data['item_data']
        self.raw_item_data = self.game_data['raw_item_data']
        self.monster_data = self.game_data['monster_data']
        self.sound_effects = self.game_data['sound_effects']
        self.animations = self.game_data['animations']
        self.skills = self.game_data['skills']
        self.sequences = self.game_data['sequences']
        self.dialogues = self.game_data['dialogues']
        
        # Initialize Components
        self.player = Player(item_data=self.item_data)
        self.game_clock = GameClock()
        self.ui = MainUi(self.screen, self.item_data, self.dialogues)
        self.event_manager = GameEvents(self.screen, self.item_data, self.dialogues, self.clock)
        self.battler = NewBattle(self.monster_data, self.item_data, self.sound_effects, 
                                 self.animations, self.skills, self.sequences)
        self.battler.surface = self.screen
        self.battler.clock = self.clock

        # Shops
        self.arena_shop = Shop(self.screen, self.raw_item_data["arena_shop"], self.dialogues)
        self.floor_talk = SelectOptions(self.screen, self.item_data, self.dialogues)

        # Animations
        self.warrior_anim = pyganim.PygAnimation(
            [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        self.mage_anim = pyganim.PygAnimation([("data/sprites/midle1.png", 0.3),
                                    ("data/sprites/midle2.png", 0.3), ("data/sprites/midle3.png", 0.3)])
        self.mage_anim.play()
        self.warrior_anim.play()

        self.castanim = [("data/sprites/b1.png", 0.3),
                    ("data/sprites/b2.png", 0.3), ("data/sprites/b3.png", 0.3)]


        # Game State
        self.scene = 'splash'
        self.cursorpos = 0
        self.shh = []
        self.namelist = ['']
        self.popup_message = ""
        self.current_music = 'data/sounds&music/Infinite_Arena.mp3'
        
        # UI Flags
        self.drawui = True
        self.controlui = True
        self.talking = False
        self.options = False
        self.status = False
        self.shop = False
        self.system = False
        self.battle_choice = False
        self.post_battle = False
        self.talkval = 0
        self.newgtxtbox = 0
        self.nosavefile = True
        self.load_flag = False

        # Assets
        self.menubg1 = pygame.transform.scale(pygame.image.load("data/backgrounds/bg2.jpg").convert_alpha(), self.screen.get_size())
        self.logo = pygame.image.load("data/backgrounds/logo3.png").convert_alpha()
        self.textbox_bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
        self.newgame_text = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40).render('New Game', True, (255, 255, 0))
        self.loadgame_text = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40).render('Load Game', True, (255, 255, 0)) # Color updated in loop
        self.quitgame_text = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40).render('Quit Game', True, (255, 255, 0))
        self.cursor_img = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.newgbg = pygame.image.load("data/backgrounds/Meadow.png").convert_alpha()
        self.inn_bg = pygame.image.load("data/backgrounds/inn.png").convert_alpha()
        
        self.seltext = pygame.font.Font("data/fonts/runescape_uf.ttf", 40)
        self.text_font = pygame.font.Font("data/fonts/runescape_uf.ttf", 30)
        
        self.sel1 = self.seltext.render('Enter your name:', False, (255, 255, 0))
        self.sel2 = self.seltext.render('Press RCTRL to continue..', False, (255, 255, 0))
        self.mage_desc = self.seltext.render('Mages are proficient at magic but weak physically.', False, (178, 57, 63))
        self.war_desc = self.seltext.render('Warriors specialize in physical attacks and buffs.', False, (178, 57, 63))
        self.sel3 = self.seltext.render('Select your class:', False, self.ui.txtcolor)
        self.sel4 = self.text_font.render('Mage', False, self.ui.txtcolor)
        self.sel5 = self.text_font.render('Warrior', False, self.ui.txtcolor)

        # Sounds
        self.loadsound = pygame.mixer.Sound('data/sounds&music/Load.ogg')
        self.loadsound.set_volume(0.05)
        self.healsound = pygame.mixer.Sound('data/sounds&music/Recovery.ogg')
        self.healsound.set_volume(0.05)

        # Splash Screen
        self.splash_screen = splashscreen.Splash(self.screen)
        self.splash_screen.toggle_splash()

        # Check save file
        self.check_save_file()

        # Music
        pygame.mixer.music.load('data/sounds&music/Theme2.ogg')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.05)
        
        self.txtbox = gameui.TextBox()
        self.timer = Timer()

    def check_save_file(self):
        try:
            with open('savegame.dat', 'rb') as f:
                self.nosavefile = False
                self.loadgame_color = (255, 255, 0)
        except:
            self.nosavefile = True
            self.loadgame_color = (105, 109, 114)
        self.loadgame_text = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40).render('Load Game', True, self.loadgame_color)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            pygame.display.set_caption(f"FPS:{int(self.clock.get_fps())}")
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posfinder()
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.load(self.current_music)
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
            
            # Scene specific handling
            if self.scene == 'menu':
                self.handle_menu_input(event)
            elif self.scene.startswith('new_game'):
                self.handle_new_game_input(event)
            elif self.scene == 'arena':
                self.handle_arena_input(event)
            elif self.scene == 'inn':
                self.handle_inn_input(event)
            elif self.scene == 'credits':
                pass # TODO

    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Cheat codes
            key_name = pygame.key.name(event.key)
            if len(key_name) == 1:
                self.shh.append(key_name)
                print(self.shh)
            if event.key == pygame.K_BACKSPACE:
                if self.shh:
                    self.shh.pop(0)
                print(self.shh)

            if event.key == pygame.K_RETURN:
                if self.cursorpos == 0: # New Game
                    pygame.mixer.music.stop()
                    self.loadsound.play()
                    fadeout(self.screen)
                    pygame.time.wait(1000)
                    pygame.mixer.music.load('data/sounds&music/Castle1.ogg')
                    pygame.mixer.music.play()
                    self.scene = 'new_game'
                elif self.cursorpos == 1 and not self.nosavefile: # Load Game
                    try:
                        with open('savegame.dat', 'rb+') as rfile:
                            pygame.mixer.music.stop()
                            self.loadsound.play()
                            self.player = pickle.load(rfile)
                            fadein(self.screen, 255)
                            self.scene = 'arena'
                            self.ui.cursorpos = 9 # Reset cursor?
                            pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
                            pygame.mixer.music.play()
                    except FileNotFoundError:
                        print("Could not open")
                        self.popup_message = "Could not open save file!"
                        self.txtbox.toggle_popup_flag()
                elif self.cursorpos == 2: # Quit
                    self.running = False
            
            if event.key == pygame.K_UP:
                self.ui.cursorsound.play()
                self.cursorpos -= 1
            if event.key == pygame.K_DOWN:
                self.ui.cursorsound.play()
                self.cursorpos += 1
            
            if self.cursorpos < 0: self.cursorpos = 2
            if self.cursorpos > 2: self.cursorpos = 0

    def handle_new_game_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.scene == 'new_game':
                if event.key == pygame.K_BACKSPACE:
                    if self.namelist:
                        self.namelist.pop()
                elif event.key == pygame.K_RCTRL and len(self.namelist) > 1:
                    self.scene = "new_game2"
                    self.player.name = "".join(self.namelist).capitalize()
                elif len(pygame.key.name(event.key)) == 1:
                    self.namelist.append(pygame.key.name(event.key))
            
            elif self.scene == 'new_game2':
                if event.key == pygame.K_LEFT:
                    self.cursorpos -= 1
                if event.key == pygame.K_RIGHT:
                    self.cursorpos += 1
                if self.cursorpos < 0: self.cursorpos = 1
                if self.cursorpos > 1: self.cursorpos = 0
                
                if event.key == pygame.K_RETURN:
                    self.player = Player(item_data=self.item_data)
                    self.player.name = "".join(self.namelist).capitalize()
                    if self.cursorpos == 0:
                        self.player.pclass = 'mage'
                    else:
                        self.player.pclass = 'warrior'
                    
                    try:
                        with open('savegame.dat', 'wb+') as rfile:
                            pickle.dump(self.player, rfile)
                    except:
                        print("Could not create save file.")
                    
                    self.scene = 'new_game3'
                    pygame.mixer.music.stop()
                    self.timer.reset()

            elif self.scene == 'new_game3':
                 if event.key == pygame.K_RCTRL:
                     self.newgtxtbox += 1

    def handle_arena_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.controlui:
                if event.key == pygame.K_DOWN:
                    self.ui.cursorsound.play()
                    self.ui.cursorpos += 1
                if event.key == pygame.K_UP:
                    self.ui.cursorsound.play()
                    self.ui.cursorpos -= 1
                
                if self.ui.cursorpos > 5: self.ui.cursorpos = 0
                if self.ui.cursorpos < 0: self.ui.cursorpos = 5

                if event.key == pygame.K_RETURN:
                    if self.ui.cursorpos == 0: # Talk
                        self.options = True
                        self.drawui = False
                        self.controlui = False
                    elif self.ui.cursorpos == 1: # Battle
                        self.drawui = False
                        self.controlui = False
                        self.battle_choice = True
                        self.ui.txtbox.reset()
                        self.ui.battalk = True
                        self.ui.batcursorpos = 4
                    elif self.ui.cursorpos == 2: # Status
                        self.drawui = False
                        self.controlui = False
                        self.status = True
                    elif self.ui.cursorpos == 3: # Shop
                        self.drawui = False
                        self.controlui = False
                        self.arena_shop.txtbox.reset()
                        self.shop = True
                    elif self.ui.cursorpos == 4: # Inn
                        pygame.mixer.music.pause()
                        fadein(self.screen, 255)
                        pygame.mixer.music.load('data/sounds&music/Town2.ogg')
                        pygame.mixer.music.play()
                        self.scene = 'inn'
                    elif self.ui.cursorpos == 5: # System
                        self.drawui = False
                        self.controlui = False
                        self.system = True
                        self.ui.syscursorpos = 4

            # Sub-menus
            elif self.options:
                self.handle_options_input(event)
            elif self.status:
                self.handle_status_input(event)
            elif self.shop:
                self.handle_shop_input(event)
            elif self.system:
                self.handle_system_input(event)
            elif self.battle_choice:
                self.handle_battle_choice_input(event)
            elif self.post_battle:
                if event.key == pygame.K_RCTRL:
                    self.ui.pb_dialogue = False
                    self.post_battle = False
                    self.drawui = True
                    self.controlui = True
            elif self.talking:
                if event.key == pygame.K_RCTRL:
                    if self.ui.txtbox.progress_dialogue(self.ui.cur_dialogue):
                        self.drawui = False
                        self.controlui = False
                        self.ui.talked = False
                        self.talking = False
                        self.options = True

    def handle_options_input(self, event):
        old_row = self.floor_talk.rowpos
        old_col = self.floor_talk.colpos

        if event.key == pygame.K_LEFT:
            self.floor_talk.colpos -= 1
            self.ui.cursorsound.play()
        if event.key == pygame.K_RIGHT:
            self.floor_talk.colpos += 1
            self.ui.cursorsound.play()
        if event.key == pygame.K_UP:
            self.floor_talk.rowpos -= 1
            self.ui.cursorsound.play()
        if event.key == pygame.K_DOWN:
            self.floor_talk.rowpos += 1
            self.ui.cursorsound.play()

        # Navigation logic for 4 options (skip empty slots)
        if self.player.progress in [1, 2]:
            if self.floor_talk.rowpos == 1:
                if self.floor_talk.colpos in [1, 2]:
                    if old_row == 0: # Came from Up
                        if self.floor_talk.colpos == 1: self.floor_talk.colpos = 0
                        elif self.floor_talk.colpos == 2: self.floor_talk.colpos = 3
                    elif old_row == 1: # Came from Left/Right
                        if self.floor_talk.colpos > old_col: # Moving Right
                            self.floor_talk.colpos = 3
                        elif self.floor_talk.colpos < old_col: # Moving Left
                            self.floor_talk.colpos = 0
        if event.key == pygame.K_RETURN:
            self.ui.txtbox.reset()
            # ... mapping logic ...
            # Simplified for brevity, assume mapping exists
            # For now, just back
            if self.floor_talk.rowpos == 1 and self.floor_talk.colpos == 3: # Back
                self.drawui = True
                self.controlui = True
                self.options = False
            else:
                self.options = False
                self.talking = True
                if self.floor_talk.rowpos == 0:
                    if self.floor_talk.colpos == 0:
                        self.talkval = 0
                        self.floor_talk.alert1 = False
                    elif self.floor_talk.colpos == 1:
                        self.talkval = 1
                        self.floor_talk.alert2 = False
                    elif self.floor_talk.colpos == 2:
                        self.talkval = 2
                        self.floor_talk.alert3 = False
                elif self.floor_talk.rowpos == 1:
                    if self.floor_talk.colpos == 0:
                        self.talkval = 3
                        self.floor_talk.alert4 = False

    def handle_status_input(self, event):
        if event.key == pygame.K_RCTRL and (not self.ui.equip_flag1 and not self.ui.equip_flag2 and not self.ui.stat_flag):
            self.drawui = True
            self.controlui = True
            self.status = False
        elif event.key == pygame.K_RETURN and self.ui.status_cur_pos == 2:
            self.drawui = True
            self.controlui = True
            self.status = False
        self.ui.handle_status_inputs(self.player, event) # Pass event to handle_status_inputs if modified

    def handle_shop_input(self, event):
        # ... logic from main.py lines 5425-5485 ...
        if event.key == pygame.K_RCTRL and self.arena_shop.shopkeep:
            if self.arena_shop.txtbox.progress_dialogue([[]]):
                self.arena_shop.shopkeep = False
        elif event.key == pygame.K_RCTRL and not self.arena_shop.shopkeep:
            if self.arena_shop.shop_selection_flag:
                self.drawui = True
                self.controlui = True
                self.shop = False
                self.arena_shop.shopkeep = True
            else:
                self.arena_shop.shop_selection_flag = True
        elif event.key == pygame.K_RETURN and not self.arena_shop.shopkeep and self.arena_shop.shop_selection_flag:
            if self.arena_shop.no_sell_flag:
                self.ui.buzzer_sound.play()
            else:
                self.arena_shop.shop_selection_flag = False
        elif not self.arena_shop.shopkeep:
            if event.key == pygame.K_LEFT: self.arena_shop.shop_cursor_pos1 -= 1
            if event.key == pygame.K_RIGHT: self.arena_shop.shop_cursor_pos1 += 1
            if event.key == pygame.K_DOWN: self.arena_shop.shop_cursor_pos2 += 1
            if event.key == pygame.K_UP: self.arena_shop.shop_cursor_pos2 -= 1
            
            if event.key == pygame.K_RETURN and not self.arena_shop.shop_selection_flag:
                if self.arena_shop.buy_item(self.arena_shop.min_pos + self.arena_shop.shop_cursor_pos2):
                    # Buying logic
                    item_idx = self.arena_shop.min_pos + self.arena_shop.shop_cursor_pos2
                    item = self.arena_shop.current_list[item_idx]
                    self.player.gold -= item['cost']
                    # Add to inventory
                    if self.arena_shop.current_list == self.arena_shop.weapons_list:
                        self.player.wep_owned.append(item_idx)
                    elif self.arena_shop.current_list == self.arena_shop.armour_list:
                        self.player.arm_owned.append(item_idx)
                    elif self.arena_shop.current_list == self.arena_shop.acc_list:
                        self.player.acc_owned.append(item_idx)
                    elif self.arena_shop.current_list == self.arena_shop.consume_list:
                         # Consumable logic
                         found = False
                         for inv_item in self.player.inventory:
                             if inv_item["name"] == item["name"]:
                                 inv_item["amount"] += 1
                                 found = True
                         if not found:
                             self.player.inventory.append({"name": item["name"], "amount": 1})
                    self.player.update_stats()

    def handle_system_input(self, event):
        if event.key == pygame.K_DOWN: self.ui.syscursorpos += 1
        if event.key == pygame.K_UP: self.ui.syscursorpos -= 1
        
        if event.key == pygame.K_RETURN:
            if self.ui.syscursorpos == 0: # Save
                try:
                    with open('savegame.dat', 'wb+') as rfile:
                        pickle.dump(self.player, rfile)
                    self.ui.savesound.play()
                    self.drawui = True
                    self.controlui = True
                    self.system = False
                except:
                    print("Could not create save file")
            elif self.ui.syscursorpos == 1: # Quit
                self.running = False
            elif self.ui.syscursorpos == 2: # Back
                self.drawui = True
                self.controlui = True
                self.system = False
        
        if event.key == pygame.K_RCTRL:
            self.drawui = True
            self.controlui = True
            self.system = False

    def handle_battle_choice_input(self, event):
        if event.key == pygame.K_DOWN: self.ui.batcursorpos += 1
        if event.key == pygame.K_UP: self.ui.batcursorpos -= 1
        
        if event.key == pygame.K_RETURN:
            if self.ui.batcursorpos == 0: # Random Battle
                if self.player.progress == 1:
                    monster_list = ["rat", "snake", "hornet", "imp"]
                elif self.player.progress == 2:
                    monster_list = ["skeleton", "zombie", "slime", "scorpion"]
                rand_mon = random.choice(monster_list)
                
                self.battler.battle(rand_mon, player_data=self.player)
                if self.battler.check_victory():
                    self.player.fkills += 1
                    self.player.tkills += 1
                    self.battle_choice = False
                    self.post_battle = True
                    pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
                    pygame.mixer.music.play()
                else:
                    self.scene = 'menu'
                    pygame.mixer.music.load('data/sounds&music/Theme2.ogg')
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play()
                    self.battle_choice = False
                    self.post_battle = False
                    self.drawui = True
                    self.controlui = True
                    self.ui.pb_dialogue = False
            elif self.ui.batcursorpos == 1: # Boss Battle
                 if self.player.fkills >= 5 and self.player.progress == 1:
                        fadein(self.screen, 255)
                        self.event_manager.firstfloor_boss(self.player.name)
                        self.battler.battle('floor_boss1', self.player, set_music=1)
                        if self.battler.check_victory():
                            self.event_manager.first_floor_victory(self.dialogues)
                            self.player.progress += 1
                            self.player.fkills = 0
                            self.battle_choice = False
                            self.post_battle = False
                            self.drawui = True
                            self.controlui = True
                            self.ui.pb_dialogue = False
                            self.scene = 'arena'
                            self.player.hours = 6
                            self.player.minutes = 0
                            pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
                            pygame.mixer.music.play()
                        else:
                            self.scene = 'menu'
                            pygame.mixer.music.load('data/sounds&music/Theme2.ogg')
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play()
                            self.battle_choice = False
                            self.post_battle = False
                            self.drawui = True
                            self.controlui = True
                            self.ui.pb_dialogue = False
                 else:
                     self.ui.buzzer_sound.play()

            elif self.ui.batcursorpos == 2: # Back
                self.drawui = True
                self.controlui = True
                self.battle_choice = False
        
        if event.key == pygame.K_RCTRL and self.ui.battalk:
            if self.ui.txtbox.progress_dialogue([[]]):
                self.ui.battalk = False

    def handle_inn_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.controlui:
                if event.key == pygame.K_DOWN: self.ui.cursorpos += 1
            if event.key == pygame.K_UP: self.ui.cursorpos -= 1
            if self.ui.cursorpos > 2: self.ui.cursorpos = 0
            if self.ui.cursorpos < 0: self.ui.cursorpos = 2
            
            if event.key == pygame.K_RETURN:
                if self.ui.cursorpos == 1: # Rest
                    if self.player.gold >= 20:
                        self.player.curhp = self.player.hp
                        self.player.curmp = self.player.mp
                        self.player.hours = 6
                        self.player.minutes = 0
                        self.healsound.play()
                        fadein(self.screen, 255)
                        self.player.gold -= 20
                elif self.ui.cursorpos == 2: # Leave
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
                    fadein(self.screen, 255)
                    pygame.mixer.music.play()
                    self.scene = 'arena'

    def update(self):
        # Cheat codes check
        if self.scene == 'menu':
            if self.shh == ['b', 'o', 's', 's']:
                self.shh = []
                # self.secretbattle.battle('secret_battle1', -10, False, bgm='data/sounds&music/Battle3.ogg')
            # ... other cheats ...
            if self.shh == ['t', 'o', 'w', 'n']:
                self.shh = []
                fadeout(self.screen)
                self.event_manager.town_first_visit(self.player)
                fadeout(self.screen)
                pygame.mixer.music.load(self.current_music)
                pygame.mixer.music.play()
            if self.shh == ['t', 'o', 't']:
                self.player.town_first_flag = True
                self.player.progress = 2
                self.event_manager.town(self.player, self.dialogues)
                self.shh = []

        if self.scene == 'new_game3':
            fadeout(self.screen, 0.01)
            self.event_manager.intro_scene(self.dialogues)
            self.scene = 'arena'

        if self.scene == 'arena':
            self.game_clock.pass_time(self.screen, self.player)

        self.timer.timing()

    def draw(self):
        if self.scene == 'splash':
            self.splash_screen.draw_splash(self.screen, None) # Event passed as None?
            fadeout(self.screen, fade_in=True, optional_bg=self.menubg1)
            self.scene = 'menu'
        
        elif self.scene == 'menu':
            self.screen.blit(self.menubg1, (0, 0))
            curwidth, curheight = self.screen.get_size()
            self.screen.blit(self.logo, (curwidth - 1100, curheight - 600))
            self.screen.blit(pygame.transform.scale(self.textbox_bg, (250, 180)), (450, 368))
            self.screen.blit(self.newgame_text, (474, 391))
            self.screen.blit(self.loadgame_text, (474, 431))
            self.screen.blit(self.quitgame_text, (474, 471))
            
            if self.cursorpos == 0: self.screen.blit(self.cursor_img, (434, 400))
            elif self.cursorpos == 1: self.screen.blit(self.cursor_img, (434, 443))
            elif self.cursorpos == 2: self.screen.blit(self.cursor_img, (434, 483))
            
        elif self.scene == 'new_game':
            self.screen.blit(pygame.transform.scale(self.newgbg, self.screen.get_size()), (0, 0))
            name_text = self.seltext.render('Enter your name:' + "".join(self.namelist), False, self.ui.txtcolor)
            self.screen.blit(self.sel2, (500, 500))
            self.screen.blit(name_text, (300, 300))
            
        elif self.scene == 'new_game2':
            self.screen.blit(pygame.transform.scale(self.newgbg, self.screen.get_size()), (0, 0))
            self.screen.blit(self.sel3, (300, 300))
            self.screen.blit(self.sel4, (300, 375))
            self.screen.blit(self.sel5, (778, 375))
            self.warrior_anim.blit(self.screen, (778, 429))
            self.mage_anim.blit(self.screen, (300, 435))
            
            if self.cursorpos == 0:
                self.screen.blit(self.cursor_img, (260, 375))
                self.screen.blit(self.mage_desc, (260, 45))
            else:
                self.screen.blit(self.cursor_img, (738, 375))
                self.screen.blit(self.war_desc, (260, 45))
                
        elif self.scene == 'arena':
            # Background is drawn by game_clock.pass_time in update()
            if self.drawui:
                self.ui.clock(self.player.hours, self.player.minutes)
                self.ui.arena(self.player.progress)
            if self.talking:
                self.ui.talk(self.talkval, self.player)
            if self.options:
                 if self.player.progress == 1:
                    self.floor_talk.drawUi(4, 'Old Man', 'Boy', 'Villager', 'Stranger')
                 elif self.player.progress == 2:
                    self.floor_talk.drawUi(4, 'Old Man', 'Boy', 'Villager', 'Pompous Noble')
            if self.status:
                self.ui.status(self.player)
            if self.shop:
                self.arena_shop.draw_shop('Arena Shop', self.player)
            if self.system:
                self.ui.system()
            if self.battle_choice:
                self.ui.battle_choice(self.player.fkills)
            if self.post_battle:
                self.ui.post_battle(self.player.progress)

        elif self.scene == 'inn':
             self.screen.blit(pygame.transform.scale(
                 self.inn_bg, self.screen.get_size()), (0, 0))
             if self.drawui:
                 self.ui.draw_inn(self.player.gold)
             if self.ui.cursorpos > 2:
                 self.ui.cursorpos = 0
             if self.ui.cursorpos < 0:
                 self.ui.cursorpos = 2

        self.txtbox.popup_message(self.popup_message, self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
