import pygame
import random
from data import pyganim
from src.utils.timer import Timer, fadein, fadeout
from src.models.player import Player

class NewBattle:

    """The new battle system. A lot better than the old one."""

    def __init__(self, monsterdata, itemdata, sounddata, animationdata, skilldata, sequence_data):
        #  Data
        self.monster_data = monsterdata
        self.consumable_data = itemdata['consumables']
        self.weapon_data = itemdata['weapons']
        self.armour_data = itemdata['armours']
        self.acc_data = itemdata['accessories']
        self.sound_data = sounddata['battle']
        self.animation_data = animationdata
        self.skill_data = skilldata
        self.warrior_skills = skilldata['warrior']
        self.sequences = sequence_data
        #  Player Details
        self.p_name = 'Zen'
        self.p_level = 5
        self.p_max_health = 100
        self.p_health = 1
        self.p_max_mana = 100
        self.p_mana = 100
        self.p_str = 20
        self.p_def = 10
        self.p_mag = 20
        self.p_luck = 2
        self.p_class = 'warrior'
        self.p_status = []
        self.p_inventory = []
        self.p_item_equipped = []
        self.p_item_effects = []    # Attributes from items
        #  Monster Details
        self.m_name = ""
        self.m_str = 30
        self.m_max_health = 1
        self.m_cur_health = 1
        self.m_def = 1
        self.m_mag = 1
        self.m_luck = 1
        self.m_sprite = ""
        self.m_gold = 1
        self.m_exp = 1
        self.m_luck = 1
        self.f_gold = 0
        self.f_exp = 0
        self.m_gold = 0
        self.m_move_list = []
        self.m_status = []
        self.m_weakness = []
        self.m_strengths = []
        #  Ui elements and etc.
        self.draw_menu = True
        self.ui_bg = pygame.image.load(
            "data/backgrounds/rpgtxt.png").convert_alpha()
        self.alert_box = pygame.image.load(
            "data/backgrounds/titlebar.png").convert_alpha()
        self.ui_font = pygame.font.Font("data/fonts/alagard.ttf", 25)
        self.title_font = pygame.font.Font("data/fonts/Daisy_Roots.otf", 25)
        self.dmg_font = pygame.font.Font("data/fonts/Vecna.otf", 30)
        self.ui_text = ["Menu", "Attack", "Skill", "Item",
                        "HP:", "MP:", "Info", "MP Cost:", "Level required:"]
        self.dmg_font_colour = {"none": (255, 255, 255),
                                "fire": (209, 63, 10),
                                "water": (22, 104, 219),
                                "light": (221, 237, 38),
                                "dark": (39, 14, 74),
                                "earth": (94, 58, 21)}   # Colour of font changes with element
        self.atk_txt = self.ui_font.render(
            self.ui_text[1], True, (200, 200, 200))
        self.skill_txt = self.ui_font.render(
            self.ui_text[2], True, (200, 200, 200))
        self.item_txt = self.ui_font.render(
            self.ui_text[3], True, (200, 200, 200))
        self.lvl_up_txt = self.ui_font.render(
            'Level Up!', True, (120, 240, 66))
        self.stat_up_txt = self.ui_font.render(
            'All stats up!', True, (110, 255, 66))
        # Rough x coordinate of player on pygame.display.get_surface() (For animations)
        self.player_x = 920
        self.player_y = 270
        self.add_flag = False  # flag for the gold and exp adding up on the victory pygame.display.get_surface()
        self.check_level = False
        self.dmg_txt = '0'
        self.cursor = pygame.image.load("data/sprites/Cursor.png")
        self.cursor_down = pygame.transform.rotate(self.cursor, -90)
        self.cursor_up = pygame.transform.rotate(self.cursor, 90)
        self.vic_img = pygame.image.load(
            "data/sprites/victory.png").convert_alpha()
        self.def_font = pygame.font.Font("data/fonts/Daisy_Roots.otf", 70)
        self.current_title = 0
        #  Sound effects
        self.sound_effect = ''
        self.cursor_sound = pygame.mixer.Sound(sounddata['system']['cursor'])
        
        # Missing attributes fix
        self.font = pygame.font.Font("data/fonts/runescape_uf.ttf", 40)
        self.alphatext = "Battle Start!"
        self.buzzer_sound = pygame.mixer.Sound(sounddata['system']['buzzer'])
        self.level_up_sound = pygame.mixer.Sound(
            'data/sounds&music/levelup.wav')
        #  State control
        self.battling = True
        self.turn = 'player'
        self.vol = 0.5
        self.turn_count = 0
        self.game_state = 'player'
        self.ui_state = 'main'
        self.ui_flag = True
        # Flag to know whether the alert box should be drawn or not
        self.alert_box_flag = False
        self.alert_text = "Undefined"
        self.player_flag = True
        self.sequence_flag = False
        self.sequence_done = False
        self.healthbar_flag = False
        self.player_dmg_flag = False    # Flag to display damage dealt to player
        self.checked = False
        self.level_up = False
        self.wait_time = 0
        self.sequence_to_play = ""
        self.sequence_timer = Timer()
        self.sequence_target = ""
        self.turns_to_wait_player = 0  # Turns to wait after a sequence
        self.post_wait_sequence_player = ""    # sequence to play after waiting
        self.wait_flag_player = False  # Flag to signify if we are waiting this turn
        self.turns_to_wait_enemy = 0  # Turns to wait after a sequence
        self.post_wait_sequence_enemy = ""  # sequence to play after waiting
        self.wait_flag_enemy = False  # Flag to signify if we are waiting this turn
        self.action_count = 0
        self.monster_flag = True
        self.focus = False
        self.focus_target = 'player'
        self.cursor_pos = 0
        self.cursor_max = 3
        # What skill is currently being hovered by the cursor.
        self.hover_skill = 0
        self.global_timer = Timer()
        self.camera_x = 0
        self.camera_y = 0
        self.element = "none"
        self.cur_level = 0
        self.victory_flag = False
        #  Temp stuff remove later
        self.crit_text = self.dmg_font.render("Critical!", True, (225, 0, 100))
        self.weak_text = self.dmg_font.render("Weak!", True, (225, 0, 100))
        self.strong_text = self.dmg_font.render("Strong!", True, (4, 19, 219))
        self.crit_chance = 1
        self.loaded_anim = pyganim.PygAnimation(
            [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        self.anim_pos = [300, 300]
        # Loaded animation for the animation function
        self.player_sprites = pyganim.PygAnimation(
            [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        self.player_sprites_burst = pyganim.PygAnimation(
            [("data/sprites/burst1.png", 0.2), ("data/sprites/burst2.png", 0.2), ("data/sprites/burst3.png", 0.2)])
        self.player_sprites_burst.play()
        self.player_sprites.play()
        self.death_sprite = pygame.image.load(
            "data/sprites/death.png").convert_alpha()  # player death sprite
        self.player_pos = 1200  # Player x position
        self.player_y = 300  # Player y position
        self.target_pos = [0, 0]  # Target x and y position
        self.move_target = "player"  # Target for move t
        self.move_flag = False  # Flag to know whether the player/monster is moving or not
        self.window_pos = 1400
        self.initial_window_pos = 0  # For the description window
        self.monster_pos = -1600  # Monster x position
        self.monster_y = 300    # monster y position
        self.monster_y_offset = 0
        self.shake = False
        #  images to load
        self.battle_ui = pygame.transform.scale(pygame.image.load("data/backgrounds/battle_menu.png").convert_alpha(),
                                                (175, 200))
        self.battle_ui2 = pygame.transform.scale(pygame.image.load("data/backgrounds/battle_menu.png").convert_alpha(),
                                                 (500, 200))
        self.battle_ui3 = pygame.transform.scale(pygame.image.load("data/backgrounds/UiElement.png").convert_alpha(),
                                                 (250, 250))  # player info ui
        self.status_icons = {"burst": pygame.image.load("data/sprites/attack+.png"),
                             "defend": pygame.image.load("data/sprites/defence+.png"),
                             "atk_down": pygame.image.load("data/sprites/atk_down.png"),
                             "def_down": pygame.image.load("data/sprites/def_down.png"),
                             "mag_down": pygame.image.load("data/sprites/mag_down.png")
                             }
        self.title_bar = pygame.image.load(
            "data/backgrounds/titlebar.png").convert_alpha()
        self.background = ""
        self.hp_bar_Empty = pygame.image.load(
            "data/sprites/hpbar1.png").convert_alpha()
        self.hp_bar_Full = pygame.image.load(
            "data/sprites/hpbar2.png").convert_alpha()
        self.virtualMonsterHealth = self.m_cur_health
        self.skill_min = 0  # The minimum value for the top position of the skill selection window
        self.item_min = 0
        self.skill_desc = ""  # Description of skill

    def focus_cam(self, target='player'):
        """Centres the camera on either the player or the enemy"""
        self.monster_flag = False
        self.player_flag = False
        if target == 'player':
            self.player_sprites.blit(self.surface, (600, 300))
        elif target == 'enemy':
            self.surface.blit(self.m_sprite, (600, 300))

    def reset_cam(self):
        """Resets the camera back to its initial state."""
        self.monster_flag = True
        self.player_flag = True
        self.focus = False
        self.shake = False

    def check_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.battling = False
            if event.type == pygame.constants.USEREVENT:
                pygame.mixer_music.set_volume(self.vol)
                pygame.mixer_music.play()
            if event.type == pygame.KEYDOWN:
                if self.draw_menu:
                    if event.key == pygame.K_UP:
                        self.cursor_pos -= 1
                        if self.ui_state == 'skill':
                            if self.cursor_pos < 0:
                                if self.skill_min != 0:
                                    self.skill_min -= 1
                                    self.cursor_pos = 0
                                else:
                                    self.cursor_pos = 3
                                    self.skill_min = len(
                                        self.skill_data[self.p_class]) - 4
                        elif self.ui_state == 'item':
                            if self.cursor_pos < 0:
                                if self.item_min != 0:
                                    self.item_min -= 1
                                    self.cursor_pos = 0
                                else:
                                    self.cursor_pos = 3
                                    self.item_min = len(self.p_inventory) - 4
                    if event.key == pygame.K_DOWN:
                        self.cursor_pos += 1
                        if self.ui_state == 'skill':
                            if self.cursor_pos > self.cursor_max:
                                if self.skill_min + 4 < len(self.skill_data[self.p_class]):
                                    self.skill_min += 1
                                    self.cursor_pos = 3
                                else:
                                    self.cursor_pos = 0
                                    self.skill_min = 0
                        elif self.ui_state == 'item':
                            if self.cursor_pos > self.cursor_max:
                                if self.item_min + 4 < len(self.p_inventory):
                                    self.item_min += 1
                                    self.cursor_pos = 3
                                else:
                                    self.cursor_pos = 0
                                    self.item_min = 0
                    if event.key == pygame.K_RETURN:
                        if self.ui_state == 'main':
                            if self.cursor_pos == 0:
                                self.game_state = 'player_attack'
                                self.global_timer.reset()
                                self.draw_menu = False
                            if self.cursor_pos == 1:
                                self.ui_state = 'skill'
                                self.initial_window_pos = 0
                                self.cursor_pos = 0
                            if self.cursor_pos == 2:
                                self.ui_state = 'item'
                                self.initial_window_pos = 0
                                self.cursor_pos = 0
                        elif self.ui_state == 'skill':
                            if self.p_level >= self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['level_req']:
                                if self.p_mana >= self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['mp_cost']:
                                    self.game_state = 'player_skill'
                                    self.global_timer.reset()
                                    self.p_mana -= self.skill_data[self.p_class][self.skill_min +
                                                                                 self.cursor_pos]['mp_cost']
                                    self.draw_menu = False
                                else:
                                    self.buzzer_sound.play()
                            else:
                                self.buzzer_sound.play()
                        elif self.ui_state == 'item':
                            if len(self.p_inventory) > 0:
                                self.game_state = 'player_item'
                                self.global_timer.reset()
                                self.p_inventory[self.item_min +
                                                 self.cursor_pos]["amount"] -= 1
                                self.draw_menu = False
                            else:
                                self.buzzer_sound.play()
                    if event.key == pygame.K_RCTRL:
                        if self.ui_state == 'skill':
                            self.ui_state = 'main'
                            self.cursor_pos = 0
                        elif self.ui_state == 'item':
                            self.ui_state = 'main'
                            self.cursor_pos = 0

                if self.game_state == 'victory' or self.game_state == 'defeat_done':
                    if event.key == pygame.K_RETURN or event.key == pygame.K_RCTRL:
                        if self.game_state == 'victory':
                            if self.f_exp != self.m_exp or self.f_gold != self.m_gold:
                                self.f_exp = self.m_exp
                                self.f_gold = self.m_gold
                                self.check_level = True
                            elif self.f_exp == self.m_exp and not self.check_level:
                                self.battling = False
                                self.victory_flag = True

                        else:
                            self.battling = False
                            fadeout(self.surface, 0.001)
                            self.victory_flag = False

    def draw_sprites(self):
        self.surface.blit(self.background, (0, 0))
        if self.player_flag:
            self.player_sprites.blit(self.surface, (self.player_pos, 300))
            if self.player_pos > 950:
                self.player_pos -= 50
        for status in self.p_status:
            if "burst" in status[0]:
                self.player_sprites_burst.blit(self.surface, (self.player_pos, 300))
                self.player_flag = False
        else:
            self.player_flag = True
        if self.monster_flag:
            self.surface.blit(self.m_sprite, (self.monster_pos,
                      self.monster_y + self.monster_y_offset))
            self.loaded_anim.blit(self.surface, self.anim_pos)  # Loaded animation
            if self.monster_pos < 200:
                self.monster_pos += 50

    def play_sound(self, sound):
        self.sound_effect = pygame.mixer.Sound(self.sound_data[sound])
        self.sound_effect.set_volume(self.vol)
        self.sound_effect.play()

    def play_animation(self, animation, pos=(920, 270)):
        self.loaded_anim = pyganim.PygAnimation(
            self.animation_data[animation], False)
        self.anim_pos = pos
        if pos == (920, 270):   # If animation on player(aka enemy using skill) we flip it (bad solution)
            self.loaded_anim.flip(True, False)
        self.loaded_anim.play()

    def move_to(self, target="player", pos=(0, 0)):
        """Moves the player or monster to a specific position"""
        if target == "player":
            if self.player_pos > pos[0]:
                self.player_pos -= 5
            elif self.player_pos < pos[0]:
                self.player_pos += 5
            if self.player_y > pos[1]:
                self.player_y -= 5
            elif self.player_y < pos[1]:
                self.player_y += 5
        elif target == "enemy":
            if self.monster_pos > pos[0]:
                self.monster_pos -= 5
            elif self.monster_pos < pos[0]:
                self.monster_pos += 5
            if self.monster_y - self.monster_y_offset > pos[1]:
                self.monster_y -= 5
            elif self.monster_y - self.monster_y_offset < pos[1]:
                self.monster_y += 5

    def check_state(self, player):
        """Keeps track of the game state and updates it accordingly"""
        if self.game_state == 'player_attack':  # Player regular attack
            player_attacking = False
            if self.player_pos > 900:
                self.player_pos -= 5
                self.global_timer.reset()
            if self.global_timer.timing(1) >= 0.4 and not player_attacking:
                self.play_animation('slash', (self.monster_pos, 300))
                self.play_sound('slash')
                dmg = self.calc_damage('attack')
                self.dmg_txt = self.dmg_font.render(
                    str(dmg), True, self.dmg_font_colour[self.element])
                self.m_cur_health -= dmg
                player_attacking = True
                self.game_state = 'player_attack_done'
                self.global_timer.reset()
        if self.game_state == 'player_attack_done':  # Player regular attack is done
            self.healthbar_flag = True
            if self.player_pos < 950:
                self.player_pos += 5
                self.global_timer.reset()
            if self.global_timer.timing(1) >= 1.5 and self.virtualMonsterHealth == self.m_cur_health:
                self.turn = 'enemy'
                self.healthbar_flag = False
                self.game_state = 'enemy_turn'
                self.global_timer.reset()
        if self.game_state == 'player_skill':
            if self.sequence_done:
                self.sequence_done = False
                self.global_timer.reset()
                self.game_state = 'player_skill_done'
            else:
                self.sequence_flag = True
                self.sequence_to_play = self.skill_data[self.p_class][self.skill_min +
                                                                      self.cursor_pos]['name'].lower()
                if self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['type'] != 'buff':
                    self.sequence_target = (self.monster_pos, self.monster_y)
                else:
                    self.sequence_target = (900, 270)
                self.global_timer.reset()
        if self.game_state == 'player_item':
            if self.sequence_done:
                self.sequence_done = False
                self.global_timer.reset()
                self.game_state = 'player_item_done'
            else:
                self.sequence_flag = True
                self.crit_chance = 0
                self.sequence_to_play = "use_item"
                self.sequence_target = (900, 270)
                self.global_timer.reset()
        if self.game_state == 'player_skill_done' or self.game_state == 'player_item_done':
            if self.global_timer.timing(1) >= 1.5:
                self.update_player_inventory()
                self.turn = 'enemy'
                self.game_state = 'enemy_turn'
                self.global_timer.reset()
        if self.game_state == 'player_skill_invalid':
            if self.global_timer.timing(1) >= 3.5:
                self.sequence_done = False
                self.turn = 'enemy'
                self.game_state = 'enemy_turn'
        if self.game_state == 'enemy_turn' and self.m_cur_health > 0:  # Enemy turn begins
            if not self.wait_flag_enemy:
                choose_move = random.randrange(0, len(self.m_move_list))
                enemy_action = self.m_move_list[choose_move]
                if enemy_action == 'attack':
                    self.game_state = 'enemy_attack'
                    self.global_timer.reset()
                else:
                    self.sequence_to_play = enemy_action
                    self.game_state = 'enemy_skill'
                    self.global_timer.reset()
            else:
                if self.turns_to_wait_enemy >= self.turn_count:
                    self.sequence_to_play = self.post_wait_sequence_enemy
                    self.game_state = 'enemy_skill'
                    self.wait_flag_enemy = False
                    self.global_timer.reset()
                else:
                    self.game_state = 'enemy_skill_done'
        if self.game_state == 'enemy_skill':
            if self.sequence_done:
                self.sequence_done = False
                self.global_timer.reset()
                self.game_state = 'enemy_skill_done'
            else:
                self.sequence_flag = True
                for skill in self.skill_data["monster"]:
                    if skill["name"].lower() == self.sequence_to_play:
                        if skill["type"] == "buff":
                            self.sequence_target = (
                                self.monster_pos, self.monster_y)
                        else:
                            self.sequence_target = (920, 270)
                        break
                    else:
                        self.sequence_target = (920, 270)
                self.global_timer.reset()
        if self.game_state == 'enemy_skill_done':
            if self.global_timer.timing(1) >= 1.5:
                self.turn = 'player'
                self.game_state = 'check_player_wait'
                self.global_timer.reset()
                self.turn_count += 1
                self.ui_state = 'main'
        if self.game_state == 'enemy_attack':  # Enemy regular attack
            enemy_attacking = False
            if self.monster_pos < 250:
                self.monster_pos += 5
                self.global_timer.reset()
            if self.global_timer.timing(1) >= 0.4 and not enemy_attacking:
                self.play_animation('claw', (self.player_pos, 300))
                self.play_sound('slash2')
                dmg = self.calc_damage('attack')
                self.dmg_txt = self.dmg_font.render(
                    str(dmg), True, self.dmg_font_colour[self.element])
                self.p_health -= dmg
                enemy_attacking = True
                self.game_state = 'enemy_attack_done'
                self.global_timer.reset()
        if self.game_state == 'enemy_attack_done':  # Enemy regular attack done
            self.player_dmg_flag = True
            if self.monster_pos > 200:
                self.monster_pos -= 5
            if self.global_timer.timing(1) >= 1.5:
                self.player_dmg_flag = False
                self.turn_count += 1
                self.turn = 'player'
                self.game_state = 'check_player_wait'
        if self.game_state == 'check_player_wait':
            if not self.wait_flag_player:
                self.draw_menu = True
                self.ui_state = 'main'
                self.game_state = ''
            else:
                if self.turns_to_wait_player >= self.turn_count:
                    self.sequence_to_play = self.post_wait_sequence_player
                    self.game_state = 'player_skill'
                    self.wait_flag_player = False
                else:
                    self.game_state = 'player_skill_done'
        # Enemy dies
        if self.game_state == 'enemy_death' and self.global_timer.timing(1) >= 1.5:
            self.monster_flag = False
            self.play_sound('enemy_dead')
            self.game_state = 'victory'
            self.global_timer.reset()
        # Victory state
        if self.game_state == 'victory' and self.global_timer.timing(1) >= 1:
            self.victory(player)
        if self.game_state == 'defeat_done':
            self.surface.blit(self.death_sprite,
                      (self.player_x + 20, self.player_y + 20))
            if self.global_timer.timing(1) >= 1:
                self.player_dmg_flag = False
                self.defeat()
        if self.p_health <= 0 and (self.game_state != 'defeat_done' and self.game_state != 'defeat'):
            self.game_state = 'defeat'
            self.global_timer.reset()
        if self.game_state == 'defeat':
            if self.global_timer.timing(1) >= 1.5:
                self.player_sprites.stop()
                self.player_sprites_burst.stop()
                self.surface.blit(self.death_sprite,
                          (self.player_x + 20, self.player_y + 20))
                self.game_state = 'defeat_done'
                print('dead')
                self.global_timer.reset()
        if 0 >= self.m_cur_health == self.virtualMonsterHealth and self.game_state != 'victory':
            if self.global_timer.timing(1) >= 1.5:
                self.game_state = 'enemy_death'
        if self.m_cur_health > self.m_max_health:
            self.m_cur_health = self.m_max_health
        if self.m_cur_health < 0:
            self.m_cur_health = 0
        if self.p_health > self.p_max_health:
            self.p_health = self.p_max_health
        if self.p_health < 0:
            self.p_health = 0
        if self.p_mana > self.p_max_mana:
            self.p_mana = self.p_max_mana
        if self.p_mana < 0:
            self.p_mana = 0

    def play_sequence(self, sequence, target=(920, 270)):
        """A sequence is a set of actions/things that should happen in a row i.e. something like a skill
        All sequences are defined in sequences.json, Can be used for things like cutscenes as well"""
        if self.sequence_flag:
            if sequence in self.sequences:
                if self.action_count < len(self.sequences[sequence]):
                    action = self.sequences[sequence][self.action_count]
                    if self.sequence_timer.timing(1) >= self.wait_time:
                        # ALL sequences must end with "end_sequence"
                        if action[0] == "end_sequence":
                            self.action_count = 0
                            self.wait_time = 0
                            self.sequence_flag = False
                            self.sequence_done = True
                            self.healthbar_flag = False
                            self.alert_box_flag = False
                            self.player_dmg_flag = False
                            self.move_flag = False
                        elif action[0] == "alert_box":
                            self.alert_box_flag = True
                            self.alert_text = action[1]
                            if action[1] == "item_name":
                                self.alert_text = self.p_inventory[self.item_min +
                                                                   self.cursor_pos]["name"]
                        elif action[0] == "animation":
                            if action[1] != "cast":
                                self.play_animation(action[1], target)
                            else:
                                if self.turn == "player":
                                    # Mage cast animation
                                    self.play_animation(action[1], (880, 230))
                                else:
                                    self.play_animation(
                                        action[1], (self.monster_pos - 50, self.monster_y))
                        elif action[0] == "sound":
                            self.play_sound(action[1])
                        elif action[0] == "add_status":  # Buff
                            status_in = False
                            duration = 0
                            if self.turn == "player":
                                for status in self.p_status:
                                    if action[1] in status:
                                        status_in = True  # statuses don't stack or refresh
                            elif self.turn == "enemy":
                                for status in self.m_status:
                                    if action[1] in status:
                                        status_in = True  # statuses don't stack or refresh
                            if not status_in:
                                if action[1] == "burst":
                                    duration = self.turn_count + 1  # the amount of time the effect lasts
                                elif action[1] == "defend":
                                    duration = self.turn_count + 2
                                if self.turn == "player":
                                    self.p_status.append([action[1], duration])
                                elif self.turn == "enemy":
                                    self.m_status.append([action[1], duration])
                        elif action[0] == "add_status_target":  # Debuff
                            status_in = False
                            duration = 0
                            if self.turn == "player":
                                for status in self.m_status:
                                    if action[1] in status:
                                        status_in = True  # statuses don't stack or refresh
                            elif self.turn == "enemy":
                                for status in self.p_status:
                                    if action[1] in status:
                                        status_in = True  # statuses don't stack or refresh
                            if not status_in:
                                if action[1] == "atk_down":
                                    duration = self.turn_count + 2  # the amount of time the effect lasts
                                elif action[1] == "def_down":
                                    duration = self.turn_count + 2
                                elif action[1] == "mag_down":
                                    duration = self.turn_count + 2
                                if self.turn == "player":
                                    self.m_status.append([action[1], duration])
                                elif self.turn == "enemy":
                                    self.p_status.append([action[1], duration])
                        elif action[0] == "deal_damage":
                            dmg = self.calc_damage(action[1])
                            if self.turn == "player":
                                self.m_cur_health -= dmg
                                self.dmg_txt = self.dmg_font.render(
                                    str(dmg), True, self.dmg_font_colour[self.element])
                                self.healthbar_flag = True
                            else:
                                self.player_dmg_flag = True
                                self.p_health -= dmg
                                self.dmg_txt = self.dmg_font.render(
                                    str(dmg), True, self.dmg_font_colour[self.element])
                        elif action[0] == "heal_hp":
                            if self.turn == "player":
                                if action[1] == "item":
                                    if self.turn == "player":
                                        item = self.p_inventory[self.item_min +
                                                                self.cursor_pos]["name"]
                                        for items in self.consumable_data:
                                            if items["name"] == item:
                                                hp_heal = items["hp"]
                                    if hp_heal != 0:
                                        self.dmg_txt = self.dmg_font.render(
                                            str(hp_heal), True, (3, 102, 16))
                                        self.p_health += hp_heal
                                        self.player_dmg_flag = True
                        elif action[0] == "heal_mp":
                            if self.turn == "player":
                                if action[1] == "item":
                                    if self.turn == "player":
                                        item = self.p_inventory[self.item_min +
                                                                self.cursor_pos]["name"]
                                        for items in self.consumable_data:
                                            if items["name"] == item:
                                                mp_heal = items["mp"]
                                    if mp_heal != 0:
                                        self.dmg_txt = self.dmg_font.render(
                                            str(mp_heal), True, (40, 43, 158))
                                        self.p_mana += mp_heal
                                        self.player_dmg_flag = True
                        # sequence syntax: ["move_to", "target", x, y, 0]
                        elif action[0] == "move_to":
                            self.move_flag = True
                            # will move who is currently on the turn
                            if action[1] == "cur_target":
                                # Only to be used for moving during skill/attack anims
                                self.move_target = self.turn
                                if self.move_target == "player":  # Bad solution, but it works
                                    self.target_pos[0] = 900
                                    self.target_pos[1] = 300
                                else:
                                    self.target_pos[0] = 250
                                    self.target_pos[1] = 300
                            else:
                                self.move_target = action[1]
                                self.target_pos[0] = action[2]
                                self.target_pos[1] = action[3]
                        elif action[0] == "reset_pos":
                            self.move_flag = True
                            if action[1] == "player":
                                self.move_target = "player"
                                self.target_pos[0] = 950
                                self.target_pos[1] = 300
                            elif action[1] == "enemy":
                                self.move_target = "enemy"
                                self.target_pos[0] = 200
                                self.target_pos[1] = 300
                            elif action[1] == "cur_target":
                                if self.turn == "player":
                                    self.move_target = "player"
                                    self.target_pos[0] = 950
                                    self.target_pos[1] = 300
                                else:
                                    self.move_target = "enemy"
                                    self.target_pos[0] = 200
                                    self.target_pos[1] = 300
                        elif action[0] == "toggle_screen_shake":
                            if not self.shake:
                                self.shake = True
                            else:
                                self.shake = False
                        elif action[0] == "wait_turn":
                            if self.turn == "player":
                                self.turns_to_wait_player = self.turn_count + action[1]
                                self.post_wait_sequence_player = action[2]
                                self.wait_flag_player = True
                            else:
                                self.turns_to_wait_enemy = self.turn_count + action[1]
                                self.post_wait_sequence_enemy = action[2]
                                self.wait_flag_enemy = True
                        if action[0] != "end_sequence":
                            self.action_count += 1
                            self.sequence_timer.reset()
                            # Getting the time to wait for the next action
                            self.wait_time = action[-1]
            else:
                self.sequence_to_play = "invalid"
                self.game_state = "player_skill_invalid"
                print("Invalid Sequence!")

    def draw_cursor(self):
        if self.cursor_pos > self.cursor_max:
            self.cursor_pos = 0
        if self.cursor_pos < 0:
            self.cursor_pos = self.cursor_max
        if self.ui_state == 'main':
            self.cursor_max = 2
        if self.ui_state == 'skill':
            self.cursor_max = 3
        if self.cursor_pos == 0:
            self.surface.blit(self.cursor, (890, 475))
        if self.cursor_pos == 1:
            self.surface.blit(self.cursor, (890, 500))
        if self.cursor_pos == 2:
            self.surface.blit(self.cursor, (890, 525))
        if self.cursor_pos == 3:
            self.surface.blit(self.cursor, (890, 550))

    def update_status_effects(self):
        """Updating and removing status effects according to duration"""
        if self.turn == "enemy":    # At end of enemies turn update player's effects
            for status in self.p_status:
                if status[1] <= self.turn_count:
                    self.p_status.remove(status)
        elif self.turn == "player":   # At end of player's turn update enemy's effects
            for status in self.m_status:
                if status[1] <= self.turn_count:
                    self.m_status.remove(status)

    def draw_healthbar(self, cur_health):  # Enemy health bar
        if cur_health > self.virtualMonsterHealth:
            if self.virtualMonsterHealth % 100 == 0 and not self.virtualMonsterHealth + 100 > cur_health:
                self.virtualMonsterHealth += 100
            elif self.virtualMonsterHealth % 50 == 0 and not self.virtualMonsterHealth + 50 > cur_health:
                self.virtualMonsterHealth += 50
            elif self.virtualMonsterHealth % 5 == 0 and not self.virtualMonsterHealth + 5 > cur_health:
                self.virtualMonsterHealth += 5
            else:
                self.virtualMonsterHealth += 1
        elif cur_health < self.virtualMonsterHealth:
            if self.virtualMonsterHealth % 100 == 0 and not self.virtualMonsterHealth - 100 < cur_health:
                self.virtualMonsterHealth -= 100
            elif self.virtualMonsterHealth % 50 == 0 and not self.virtualMonsterHealth - 50 < cur_health:
                self.virtualMonsterHealth -= 50
            elif self.virtualMonsterHealth % 5 == 0 and not self.virtualMonsterHealth - 5 < cur_health:
                self.virtualMonsterHealth -= 5
            else:
                self.virtualMonsterHealth -= 1
        health_percent = (self.virtualMonsterHealth / self.m_max_health) * 100
        if health_percent <= 0:
            health_percent = 0.1
        self.surface.blit(pygame.transform.scale(self.hp_bar_Empty,
                  (260, 18)), (self.monster_pos, self.monster_y))
        self.surface.blit(pygame.transform.scale(self.hp_bar_Full, (int(246 * (health_percent / 100)), 18)),
                  (self.monster_pos + 7, self.monster_y + 1))

    def draw_alertbox(self):
        """The alert box or the skill box that gets drawn when a skill is used."""
        if self.alert_box_flag:
            self.surface.blit(self.alert_box, (430, 80))
            txt = self.ui_font.render(self.alert_text, False, (55, 0, 200))
            self.surface.blit(txt, (500, 120))

    def draw_ui(self):
        self.surface.blit(self.battle_ui, (self.window_pos, 400))
        self.surface.blit(self.battle_ui3, (self.window_pos - 30, -10))
        if self.window_pos > 900:
            self.window_pos -= 50

        if self.window_pos <= 900:  # when the 'animation' finishes
            hp_text = self.ui_font.render(
                "HP: %d/%d" % (self.p_health, self.p_max_health), True, (230, 0, 50))
            mp_text = self.ui_font.render(
                "MP: %d/%d" % (self.p_mana, self.p_max_mana), True, (20, 0, 230))

            self.surface.blit(hp_text, (920, 90))  # Text for hp
            self.surface.blit(mp_text, (920, 110))  # Text for mp
            for index, status in enumerate(self.p_status):
                if status[0] in self.status_icons:
                    self.surface.blit(
                        self.status_icons[status[0]], (900 + (40 * index), 140))
            if self.ui_state == 'main':
                self.current_title = 0
                self.surface.blit(self.atk_txt, (945, 475))
                self.surface.blit(self.skill_txt, (945, 500))
                self.surface.blit(self.item_txt, (945, 525))
            elif self.ui_state == 'skill':    # Skill selection
                self.current_title = 2
                cur_mp_cost = self.skill_data[self.p_class][self.skill_min +
                                                            self.cursor_pos]['mp_cost']
                self.skill_desc = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['desc'], True, (200, 200, 200))
                self.surface.blit(self.battle_ui2, (self.initial_window_pos, 400))
                skill_text1 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min]['name'], True, (200, 200, 200))
                skill_text2 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + 1]['name'], True, (200, 200, 200))
                skill_text3 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + 2]['name'], True, (200, 200, 200))
                skill_text4 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + 3]['name'], True, (200, 200, 200))
                self.surface.blit(skill_text1, (915, 475))
                self.surface.blit(skill_text2, (915, 500))
                self.surface.blit(skill_text3, (915, 525))
                self.surface.blit(skill_text4, (915, 550))
                if self.skill_min != 0:
                    self.surface.blit(self.cursor_up, (960, 430))
                if self.skill_min + 4 < len(self.skill_data[self.p_class]):
                    self.surface.blit(self.cursor_down, (960, 590))
                if self.initial_window_pos < 300:
                    self.initial_window_pos += 30
                if self.initial_window_pos == 300:
                    self.surface.blit(self.skill_desc, (340, 480))
                    title_text2 = self.title_font.render(
                        self.ui_text[6], True, (200, 30, 30))
                    self.surface.blit(title_text2, (520, 413))
                    mp_cost_txt = self.ui_font.render(
                        "Mp Cost: %d" % cur_mp_cost, True, (200, 60, 130))
                    self.surface.blit(mp_cost_txt, (340, 540))
                    if self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['level_req'] > self.p_level:
                        self.surface.blit(self.ui_font.render("Not learned!",
                                  True, (204, 55, 87)), (570, 540))
                    if self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['mp_cost'] > self.p_mana and \
                            self.skill_data[self.p_class][self.skill_min + self.cursor_pos][
                                'level_req'] <= self.p_level:
                        self.surface.blit(self.ui_font.render(
                            "Insufficient MP!", True, (49, 61, 224)), (340, 510))
            elif self.ui_state == 'item':
                self.current_title = 3
                self.surface.blit(self.battle_ui2, (self.initial_window_pos, 400))
                if len(self.p_inventory) < 4:
                    self.cursor_max = len(self.p_inventory)
                else:
                    self.cursor_max = 3
                if len(self.p_inventory) > 0:
                    for item in self.consumable_data:
                        if self.p_inventory[self.item_min + self.cursor_pos]["name"] == item["name"]:
                            item_desc = self.ui_font.render(
                                item['battle_desc'], True, (200, 200, 200))

                    if self.item_min != 0:
                        self.surface.blit(self.cursor_up, (960, 430))
                    if len(self.p_inventory) >= 4:
                        if self.item_min + 4 < len(self.p_inventory):
                            self.surface.blit(self.cursor_down, (960, 590))
                    amount_in_inventory = self.ui_font.render("In Inventory: {}".format(
                        self.p_inventory[self.item_min + self.cursor_pos]["amount"]), True, (255, 0, 85))
                    item1 = self.ui_font.render(
                        self.p_inventory[self.item_min]["name"], True, (200, 200, 200))
                    self.surface.blit(item1, (915, 475))
                    if len(self.p_inventory) >= 2:
                        item2 = self.ui_font.render(
                            self.p_inventory[self.item_min + 1]["name"], True, (200, 200, 200))
                        self.surface.blit(item2, (915, 500))
                    if len(self.p_inventory) >= 3:
                        item3 = self.ui_font.render(
                            self.p_inventory[self.item_min + 2]["name"], True, (200, 200, 200))
                        self.surface.blit(item3, (915, 525))
                    if len(self.p_inventory) >= 4:
                        item3 = self.ui_font.render(
                            self.p_inventory[self.item_min + 3]["name"], True, (200, 200, 200))
                        self.surface.blit(item3, (915, 550))
                if self.initial_window_pos < 300:
                    self.initial_window_pos += 30
                if self.initial_window_pos == 300:
                    if len(self.p_inventory) <= 0:
                        item_desc = self.ui_font.render(
                            "No items in inventory.", True, (200, 200, 200))
                        amount_in_inventory = self.ui_font.render(
                            "", True, (200, 200, 200))
                    self.surface.blit(item_desc, (340, 480))
                    self.surface.blit(amount_in_inventory, (340, 540))
                    title_text2 = self.title_font.render(
                        self.ui_text[6], True, (200, 30, 30))
                    self.surface.blit(title_text2, (520, 413))
            title_text = self.title_font.render(
                self.ui_text[self.current_title], True, (200, 30, 30))  # Title for the ui
            self.surface.blit(title_text, (959, 412))

    def get_monster_details(self, monster_name):
        self.m_max_health = self.monster_data[monster_name]['health']
        self.m_cur_health = self.m_max_health
        self.virtualMonsterHealth = self.m_cur_health
        self.m_str = self.monster_data[monster_name]['str']
        self.m_def = self.monster_data[monster_name]['def']
        self.m_mag = self.monster_data[monster_name]['mag']
        self.m_luck = self.monster_data[monster_name]['luck']
        self.m_sprite = pygame.image.load(
            self.monster_data[monster_name]['sprites'])
        self.m_move_list = self.monster_data[monster_name]['move_list']
        self.m_gold = self.monster_data[monster_name]['gold']
        self.m_exp = self.monster_data[monster_name]['exp']
        self.background = pygame.transform.scale(pygame.image.load(self.monster_data[monster_name]['bg']).convert_alpha(),
                                                 (1280, 720))
        self.m_weakness = self.monster_data[monster_name]['weakness']
        self.m_strengths = self.monster_data[monster_name]['strengths']
        self.m_status = []
        height = self.m_sprite.get_height()
        if height > 220:
            self.monster_y_offset = -100
        else:
            self.monster_y_offset = 0

    def get_player_details(self, player_data):
        player_data.update_stats()
        self.p_health = player_data.curhp
        self.p_max_health = player_data.hp
        self.p_mana = player_data.curmp
        self.p_max_mana = player_data.mp
        self.p_class = player_data.pclass
        self.p_luck = player_data.luck
        self.p_level = player_data.level
        self.p_mag = player_data.mag + player_data.add_mag
        self.p_str = player_data.stre + player_data.add_stre
        self.p_def = player_data.defe + player_data.add_defe
        self.p_name = player_data.name
        self.p_inventory = player_data.inventory
        self.p_item_effects = []
        self.p_item_equipped = [self.weapon_data[player_data.cur_weapon],
                                self.armour_data[player_data.cur_armour], self.acc_data[player_data.cur_accessory]]
        for items in self.p_item_equipped:
            if items['attributes'] != 'null':
                self.p_item_effects.append(items['attributes'])

    # Updates the player object with the cur hp and mana
    def update_player_details(self, player_data):
        """I don't remember the original reason that I didn't just directly update the player object.
        Well, this works  for now lol."""
        player_data.curhp = self.p_health
        player_data.curmp = self.p_mana
        player_data.gold += self.m_gold
        player_data.exp += self.m_exp
        player_data.inventory = self.p_inventory
        while player_data.check_levelup():
            print(player_data.level)
            player_data.level += 1
            player_data.hp += 25
            player_data.mp += 5
            player_data.stat_points += 2
            self.level_up = True

    def update_player_inventory(self):
        """For removing items from inventory after consumption"""
        for items in self.p_inventory:
            if items["amount"] <= 0:
                self.p_inventory.remove(items)

    def calc_damage(self, atk_type):
        self.crit_chance = 0
        self.element = "none"
        if self.turn == "player":
            strength = self.p_str
            defence = self.m_def    # Monster's defence
            magic = self.p_mag
            luck = self.p_luck
            status = self.p_status
            e_status = self.m_status    # Monster's status
        else:
            strength = self.m_str
            defence = self.p_def    # Player's defence
            magic = self.m_mag
            luck = self.m_luck
            status = self.m_status
            e_status = self.p_status    # Player's status
        for effect in status:
            if effect[0] == "burst":
                strength += strength + \
                    (strength * 0.5)  # increase strength by 50%
                if self.turn == "player":
                    self.p_status.remove(effect)
                else:
                    self.m_status.remove(effect)
            elif effect[0] == "atk_down":
                strength = strength * 0.5   # Reduce strength by 50%
            elif effect[0] == "mag_down":
                magic = magic * 0.5     # Reduce magic by 50%
            elif effect[0] == "def_down":
                defence = defence * 0.5  # decreases defence by Half
        for effect in e_status:
            if effect[0] == "defend":
                defence = defence + \
                    (defence * 2.0)   # increase defence by 200%
            elif effect[0] == "def_down":
                defence = defence * 0.5  # decreases defence by Half
        if atk_type == "attack":    # Regular attack
            self.element = "none"
            # Will take a range of their current strength
            dmg_range = strength + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            if luck >= 10:
                luck = 10
            # will always crit with 10 luck.
            self.crit_chance = random.randrange(luck, 11)
            if self.crit_chance == 10:
                damage = (dmg_range * strength / (strength + defence)) * 4
            else:
                damage = (dmg_range * strength / (strength + defence)) * 2
            if self.turn == "player":
                for attribute in self.p_item_effects:
                    if attribute == 'AtkDmg 2x':
                        damage *= 2  # Doubles damage
        elif atk_type == "fire slash":
            self.element = "fire"
            dmg_range = (strength * 0.5) + (magic * 0.5) + \
                random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * strength / (strength + defence)) * 2
        elif atk_type == "quake":
            self.element = "earth"
            dmg_range = magic + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * magic / (magic + defence)) * 2.5
        elif atk_type == "fire":
            self.element = "fire"
            dmg_range = magic + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * magic / (magic + defence)) * 2
        elif atk_type == "ice":
            self.element = "water"
            dmg_range = magic + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * magic / (magic + defence)) * 2.5
        elif atk_type == "thunder":
            self.element = "light"
            dmg_range = magic + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * magic / (magic + defence)) * 2.7
        elif atk_type == "tsunami":
            self.element = "water"
            dmg_range = magic + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * magic / (magic + defence)) * 3.5
        elif atk_type == "meteor":
            self.element = "fire"
            dmg_range = magic + random.randrange(-3, 3)
            if dmg_range <= 0:
                dmg_range = 1
            damage = (dmg_range * magic / (magic + defence)) * 3.7
        if self.turn == "player":
            if self.element in self.m_weakness:
                damage *= 2     # Damage doubles if enemy is weak against that element
            elif self.element in self.m_strengths:
                damage *= 0.5     # Damage halves if enemy is strong against that element
            for effect in self.p_item_effects:
                if effect == "AtkDmg 2x" and atk_type == "attack":
                    damage *= 2
                elif effect == "FireDmg Up":
                    if self.element == "fire":
                        damage += damage * 0.5
                elif effect == "WaterDmg Up":
                    if self.element == "water":
                        damage += damage * 0.5

        return int(damage)

    def shake_screen(self):
        self.camera_x, self.camera_y = random.randrange(
            -5, 5), random.randrange(-5, 5)

    def victory(self, player):
        if not self.add_flag:
            self.f_gold = 0
            self.f_exp = 0
            self.add_flag = True
            self.checked = False
            self.level_up = False
            pygame.mixer.music.pause()
            pygame.mixer.music.load(
                'data/sounds&music/Victory_and_Respite.mp3')  # victory music
            pygame.mixer.music.play()
        # making a transparent dark surface
        dark_surf = pygame.Surface(self.surface.get_size(), 32)
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        self.surface.blit(dark_surf, (0, 0))
        gold_txt = self.ui_font.render(
            'Gold:+%d' % self.f_gold, True, (255, 255, 0))
        exp_txt = self.ui_font.render(
            'Exp:+%d' % self.f_exp, True, (244, 240, 66))
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(self.vic_img, (curwidth / 3, curheight / 5))
        self.surface.blit(gold_txt, (curwidth / 3 + 100, curheight / 5 + 100))
        self.surface.blit(exp_txt, (curwidth / 3 + 100, curheight / 5 + 125))
        if self.f_gold < self.m_gold:
            if self.f_gold % 5 == 0:
                self.f_gold += 5
            elif self.f_gold % 2 == 0:
                self.f_gold += 2
            else:
                self.f_gold += 1
        if self.f_exp < self.m_exp:
            if self.f_exp % 5 == 0:
                self.f_exp += 5
            elif self.f_exp % 2 == 0:
                self.f_exp += 2
            else:
                self.f_exp += 1
        if self.f_exp == self.m_exp and self.f_gold == self.m_gold and not self.checked:
            self.check_level = True
            self.checked = True
        if self.check_level:
            self.cur_level = player.level
            self.update_player_details(player)
            self.check_level = False
            if self.level_up:
                self.level_up_sound.play()
        if self.level_up:
            lvl_txt = self.ui_font.render('Gained {} level(s)!'.format(
                player.level - self.cur_level), True, (255, 255, 0))
            hp_txt = self.ui_font.render('+{} HP'.format((player.level - self.cur_level) * 25),
                                         True, (255, 255, 0))
            mp_txt = self.ui_font.render('+{} MP'.format((player.level - self.cur_level) * 10),
                                         True, (255, 255, 0))
            stat_txt = self.ui_font.render('+{} Stat points'.format((player.level - self.cur_level) * 3),
                                           True, (255, 255, 0))
            self.surface.blit(lvl_txt, (curwidth / 3 + 100, curheight / 5 + 150))
            self.surface.blit(hp_txt, (curwidth / 3 + 100, curheight / 5 + 175))
            self.surface.blit(mp_txt, (curwidth / 3 + 100, curheight / 5 + 200))
            self.surface.blit(stat_txt, (curwidth / 3 + 100, curheight / 5 + 225))

    def defeat(self):
        if not self.add_flag:
            pygame.mixer.music.pause()
            pygame.mixer.music.load(
                'data/sounds&music/Gameover2.ogg')  # defeat music
            pygame.mixer.music.play()
            self.add_flag = True
        # making a transparent dark surface
        dark_surf = pygame.Surface(self.surface.get_size(), 32)
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        self.surface.blit(dark_surf, (0, 0))
        defeat = self.def_font.render(
            'Defeat!', True, (255, 0, 0)).convert_alpha()
        cont = self.ui_font.render(
            'Your journey isn\'t over yet! Move onward!', True, (255, 255, 0)).convert_alpha()
        curwidth, curheight = self.surface.get_size()
        self.surface.blit(defeat, (curwidth / 3, curheight / 5))
        self.surface.blit(cont, (curwidth / 3, curheight / 5 + 100))

    def set_instance(self, player_data):
        """Resets/sets the instance"""
        self.reset_cam()
        self.game_state = ""
        self.ui_state = "main"
        self.turn = "player"
        self.get_player_details(player_data)
        self.p_status = []
        self.sequence_flag = False
        self.sequence_done = False
        self.player_dmg_flag = False
        self.player_flag = True
        self.element = "none"
        self.player_sprites_burst.play()
        self.turn_count = 0
        self.healthbar_flag = False
        self.victory_flag = False
        if player_data.pclass == "warrior":
            self.player_sprites = pyganim.PygAnimation(
                [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        elif player_data.pclass == "mage":
            self.player_sprites = pyganim.PygAnimation(
                [("data/sprites/midle1.png", 0.3), ("data/sprites/midle2.png", 0.3), ("data/sprites/midle3.png", 0.3)])
        self.player_sprites.play()

    def check_victory(self):
        """Checks if player won the battle or not"""
        if self.victory_flag:
            self.victory_flag = False
            return True
        else:
            return False

    def battle(self, monster_name, player_data, set_music=0):
        #  Main loop, starts the battle
        alpha = self.font.render(self.alphatext, False, (255, 255, 0))
        self.battling = True
        self.monster_flag = True
        self.draw_menu = True
        self.add_flag = False
        self.get_monster_details(monster_name)
        self.get_player_details(player_data)
        self.play_sound('encounter')
        self.set_instance(player_data)
        fadein(self.surface, 255)
        if set_music == 0:
            pygame.mixer_music.load("data/sounds&music/03_Endless_Battle.ogg")
            pygame.mixer_music.set_volume(self.vol)
            pygame.mixer_music.play()
        elif set_music == 1:
            pygame.mixer_music.load("data/sounds&music/boss_music.mp3")
            pygame.mixer_music.set_volume(self.vol)
            pygame.mixer_music.play()
        elif set_music == 2:
            pygame.mixer_music.load("data/sounds&music/Dungeon2.ogg")
            pygame.mixer_music.set_volume(self.vol)
            pygame.mixer_music.play()
        elif set_music == 3:
            pygame.mixer_music.load("data/sounds&music/2000_Thief.ogg")
            pygame.mixer_music.set_volume(self.vol)
            pygame.mixer_music.play()
        else:
            pygame.mixer_music.load("data/sounds&music/03_Endless_Battle.ogg")
            pygame.mixer_music.set_volume(self.vol)
            pygame.mixer_music.play()
        pygame.mixer_music.set_endevent(pygame.constants.USEREVENT)
        self.player_pos = 1200  # make the player 'move'
        self.window_pos = 1400
        self.monster_pos = -1600
        while self.battling:
            self.draw_sprites()
            if self.draw_menu:  # Handles drawing the Ui and checking for input
                self.draw_ui()
                self.draw_cursor()
            if self.shake:  # Shakes the pygame.display.get_surface() when set to True
                self.shake_screen()
            if not self.shake:  # To reset the pygame.display.get_surface() back to its initial position
                self.camera_x, self.camera_y = 0, 0
            if self.focus:
                self.focus_cam(self.focus_target)
            if self.move_flag:
                self.move_to(self.move_target, self.target_pos)
            self.draw_alertbox()
            if self.player_dmg_flag:
                self.surface.blit(self.dmg_txt, (self.player_pos, 270))
                if self.crit_chance == 10:
                    self.surface.blit(self.crit_text, (self.player_pos, 240))
            if self.healthbar_flag:
                self.surface.blit(self.dmg_txt, (self.monster_pos, self.monster_y - 40))
                if self.crit_chance == 10:
                    self.surface.blit(self.crit_text,
                              (self.monster_pos, self.monster_y - 70))
                if self.element in self.m_weakness:
                    self.surface.blit(self.weak_text,
                              (self.monster_pos, self.monster_y - 70))
                elif self.element in self.m_strengths:
                    self.surface.blit(self.strong_text,
                              (self.monster_pos, self.monster_y - 70))
                self.draw_healthbar(self.m_cur_health)
            self.update_status_effects()
            self.play_sequence(self.sequence_to_play, self.sequence_target)
            self.check_state(player_data)  # To check the current game state
            self.check_inputs()
            self.surface.blit(alpha, (0, 0))
            pygame.display.get_surface().blit(self.surface, (self.camera_x, self.camera_y))
            pygame.display.update()
            self.clock.tick(60)
            fps = "FPS:%d" % self.clock.get_fps()
            pygame.display.set_caption(fps)


drawui = True  # Flag to signify whether to draw the ui or not,


# used to hide ui during dialogue or any other scenes(the main UI during which the player has control outside of battle)


