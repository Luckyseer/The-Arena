# Alpha V2.4
from __future__ import print_function  # For compatibility with python 2.x
import pickle
import random
from math import floor
import pygame
from data import pyganim
from data import gameui
from data import splashscreen
import json
from pygame.locals import *


icon = pygame.image.load("data/sprites/Icon2.png")
pygame.display.set_icon(icon)
alphatext = "Alpha v4.1 - Story and the Town"
try:
    with open('data/items.json', 'r') as items:
        item_data = json.load(items)
        weapons = item_data['weapons']
    with open('data/monsters.json', 'r') as monsters:
        monster_data = json.load(monsters)
    with open('data/soundeffects.json', 'r') as sounds:
        sound_effects = json.load(sounds)
    with open('data/animations.json', 'r') as anims:
        animations = json.load(anims)
    with open('data/skills.json', 'r') as skills:
        skills = json.load(skills)
    with open('data/sequences.json', 'r') as sequences:
        sequences = json.load(sequences)
    with open('data/dialogue.json', 'r') as dialogue:
        dialogues = json.load(dialogue)
except EOFError or IOError:
    print('Could not load item/monster/sound data, Make sure they are in the folder with the game')
    raise FileNotFoundError


class Player:
    """Hold all the player information"""

    def __init__(self, item_data=item_data, name='Zen', health=100, mana=50, strength=10, magic=20, defence=10, luck=2):
        self.name = name
        self.hp = health
        self.curhp = self.hp
        self.mp = mana
        self.curmp = self.mp
        self.cur_weapon = 0  # set the id of the item
        self.cur_armour = 0  # NOTE TO SELF: DON'T FORGET TO CHANGE DEFAULT ITEMS BACK!!
        self.cur_accessory = 0
        self.stre = strength  # Player's base stats
        self.defe = defence
        self.mag = magic
        self.luck = luck
        self.stat_points = 0
        self.expreq = 0
        # Player's stats from equipment
        self.add_stre = item_data['weapons'][self.cur_weapon]['atk'] + item_data['armours'][self.cur_armour]['atk'] + \
            item_data['accessories'][self.cur_accessory]['atk']
        self.add_defe = item_data['weapons'][self.cur_weapon]['def'] + item_data['armours'][self.cur_armour]['def'] + \
            item_data['accessories'][self.cur_accessory]['def']
        self.add_mag = item_data['weapons'][self.cur_weapon]['mag'] + item_data['armours'][self.cur_armour]['mag'] + \
            item_data['accessories'][self.cur_accessory]['mag']
        self.add_luck = luck
        self.progress = 1  # progress in game
        self.gold = 1500000
        self.level = 1
        self.hours = 6  # in-game clock values
        self.minutes = 0  # ^
        self.exp = 0
        self.inventory = []
        self.wep_owned = []  # Used to store ids of currently owned weapons
        self.arm_owned = []
        self.acc_owned = []
        self.pclass = 'mage'
        self.fkills = 0  # Kills in floor
        self.tkills = 0  # Total Kills
        self.scene = 'menu'
        # Flag to check if player visited town or not.
        self.town_first_flag = False
        # Flag for whether the player paid the girl during the town scene
        self.paid_girl_flag = False

    def xp_till_levelup(self, currentlevel):  # Experience needed to level up
        self.expreq = floor((currentlevel ** 4) / 5)
        return self.expreq

    def check_levelup(self):  # Check if player has leveled up
        self.xp_till_levelup(self.level)
        print(f'Exp:{self.exp}, to_lvl:{self.xp_till_levelup(self.level)}')
        if self.exp >= self.expreq:
            return True
        else:
            return False

    def update_stats(self):
        self.add_stre = item_data['weapons'][self.cur_weapon]['atk'] + item_data['armours'][self.cur_armour]['atk'] + \
            item_data['accessories'][self.cur_accessory]['atk']
        self.add_defe = item_data['weapons'][self.cur_weapon]['def'] + item_data['armours'][self.cur_armour]['def'] + \
            item_data['accessories'][self.cur_accessory]['def']
        self.add_mag = item_data['weapons'][self.cur_weapon]['mag'] + item_data['armours'][self.cur_armour]['mag'] + \
            item_data['accessories'][self.cur_accessory]['mag']

    def set_player_stats(self, **kwargs):
        """For debug purposes"""
        for stat, value in kwargs.items():
            if stat == "strength" or stat == "stre":
                self.stre = value
            elif stat == "defence" or stat == "defe":
                self.defe = value
            elif stat == "magic" or stat == "mag":
                self.mag = value
            elif stat == "luck" or stat == "luk":
                self.luck = value
            elif stat == "health":
                self.hp = self.curhp = value
            elif stat == "mana":
                self.mp = self.curmp = value
            elif stat == "level":
                self.level = value


if __name__ == '__main__':
    pygame.init()
    screen_width = 1280
    screen_height = 720
    is_fullscreen = False
    if not is_fullscreen:
        screen = pygame.display.set_mode([screen_width, screen_height])
    else:
        screen = pygame.display.set_mode(
            [screen_width, screen_height], pygame.FULLSCREEN)

    # #Note to self: remove debug lines after done# #

    clock = pygame.time.Clock()
    pygame.display.set_caption('The Arena')
    done = False


def posfinder():  # Used to find position of cursor
    posx, posy = pygame.mouse.get_pos()
    print(posx, posy)


class Timer:
    """The Timer class, used to time things in-game."""

    def __init__(self):
        self.start = int(pygame.time.get_ticks())
        self.seconds = 0

    def timing(self, mode=0):
        # Set mode = 0 to return the time in seconds,set mode = 1 to return the time in milliseconds.
        if mode == 0:
            # How many seconds passed
            self.seconds = int((pygame.time.get_ticks() - self.start) / 1000)
        elif mode == 1:
            # How many milliseconds passed
            self.seconds = (pygame.time.get_ticks() - self.start) / 1000
        return self.seconds

    def reset(self):
        self.start = int(pygame.time.get_ticks())

    def dothing(self, time):
        seconds = self.timing()
        if seconds >= time:
            print("Doing thing")  # debug
            return True


def fadein(rgb, time=0.0001, fadetimer=Timer()):  # fadein effect
    global screen
    fade_done = False
    col = 0
    while True:
        while col < 256:
            if fadetimer.timing(1) >= time:
                r = col
                g = col
                b = col
                screen.fill([r, g, b])
                pygame.display.flip()
                col += 1
                fadetimer.reset()
        fade_done = True
        if fade_done:
            break
    return fade_done


def fadeout(surface, time=0.000001, fadetimer=Timer(), fade_in=False, optional_bg=""):  # fadeout effect
    global screen
    if optional_bg != "":
        post_fade_bg = optional_bg   # Image to show on screen when it fades back in
    fade_done = False
    alpha = 255
    while True:
        while alpha >= 0 and not fade_done:
            if fadetimer.timing(1) >= time:
                surface.set_alpha(alpha)
                screen.fill([0, 0, 0])
                screen.blit(surface, (0, 0))
                pygame.display.flip()
                alpha -= 3
                fadetimer.reset()
        fade_done = True
        if fade_done:
            if fade_in:
                while alpha < 255:
                    if fadetimer.timing(1) >= time:
                        if optional_bg != "":
                            surface.blit(post_fade_bg, (0, 0))
                        surface.set_alpha(alpha)
                        screen.blit(surface, (0, 0))
                        pygame.display.flip()
                        alpha += 3
                        fadetimer.reset()
                if alpha >= 255:
                    fade_in = False
                    break
            else:
                surface.set_alpha(255)
                break
    return fade_done


class SideBattle:
    """ The sidebattle class, which provides us with the main gameplay(the battle system)
        Needs some work, could be a lot more efficient.
        Currently, needs some work on the aesthetics side. """

    # The stats for the monster are by default for the weakest enemy 'rat', remember to change the stats as needed.
    def __init__(self, mondata, pclass, castanim, bg, bgm, phealth=100, pmana=50, pstr=10, pstrmod=10, pdef=10,
                 pmag=20, pluck=2):
        self.mondata = mondata
        self.players = [1, pyganim.PygAnimation(castanim)]
        self.pname = 'Zen'
        self.plevel = 5
        self.xptolevel = 100
        self.monsters = ''
        self.inventory = {'Potion': 1, 'Mana Potion': 1}
        self.mhurt = pyganim.PygAnimation(
            [("data/sprites/mhurt1.png", 0.3), ("data/sprites/mhurt2.png", 0.3), ("data/sprites/mhurt3.png", 0.3)])
        self.staticon1 = pygame.image.load(
            "data/sprites/attack+.png").convert_alpha()
        self.pshadow = pygame.image.load(
            "data/sprites/Shadow1.png").convert_alpha()
        self.encountersound = pygame.mixer.Sound(
            'data/sounds&music/Battle2.ogg')
        self.cursorsound = pygame.mixer.Sound('data/sounds&music/Cursor1.ogg')
        self.cursorsound.set_volume(0.05)
        self.buzzer = pygame.mixer.Sound('data/sounds&music/Buzzer1.ogg')
        self.bg = pygame.image.load(bg).convert_alpha()
        self.players[1].convert_alpha()
        self.turn = 1
        self.burstanim = pyganim.PygAnimation(
            [("data/sprites/burst1.png", 0.3), ("data/sprites/burst2.png", 0.3), ("data/sprites/burst3.png", 0.3)])
        self.castanim = pyganim.PygAnimation(
            [("data/sprites/cast1.png", 0.1), ("data/sprites/cast2.png", 0.1), ("data/sprites/cast3.png", 0.1),
             ("data/sprites/cast4.png", 0.1), ("data/sprites/cast5.png", 0.5)], False)
        self.coinanim = pyganim.PygAnimation(
            [("data/sprites/coin1.png", 0.1), ("data/sprites/coin2.png", 0.1), ("data/sprites/coin3.png", 0.1),
             ("data/sprites/coin4.png", 0.1), ("data/sprites/coin5.png",
                                               0.1), ("data/sprites/coin6.png", 0.1),
             ("data/sprites/coin7.png", 0.1), ("data/sprites/coin8.png", 0.1), ("data/sprites/coin9.png", 0.1)])
        self.fireanim = pyganim.PygAnimation(
            [("data/sprites/Fire1.png", 0.1), ("data/sprites/Fire2.png", 0.1), ("data/sprites/Fire3.png", 0.1),
             ("data/sprites/Fire4.png", 0.1), ("data/sprites/Fire5.png",
                                               0.1), ("data/sprites/Fire6.png", 0.1),
             ("data/sprites/Fire7.png", 0.1), ("data/sprites/Fire8.png", 0.1)], False)
        self.iceanim = pyganim.PygAnimation(
            [("data/sprites/Ice1.png", 0.09), ("data/sprites/Ice2.png", 0.09), ("data/sprites/Ice3.png", 0.09),
             ("data/sprites/Ice4.png", 0.09), ("data/sprites/Ice5.png",
                                               0.09), ("data/sprites/Ice6.png", 0.09),
             ("data/sprites/Ice7.png", 0.09), ("data/sprites/Ice8.png",
                                               0.09), ("data/sprites/Ice9.png", 0.09),
             ("data/sprites/Ice10.png", 0.09), ("data/sprites/Ice11.png",
                                                0.09), ("data/sprites/Ice12.png", 0.09),
             ("data/sprites/Ice13.png", 0.09), ("data/sprites/Ice14.png",
                                                0.09), ("data/sprites/Ice15.png", 0.09),
             ("data/sprites/Ice16.png", 0.09), ("data/sprites/Ice17.png", 0.09), ("data/sprites/Ice18.png", 0.1)], False)
        self.deathanim = pyganim.PygAnimation(
            [("data/sprites/Death1.png", 0.1), ("data/sprites/Death2.png", 0.1), ("data/sprites/Death3.png", 0.1),
             ("data/sprites/Death4.png", 0.1), ("data/sprites/Death5.png",
                                                0.1), ("data/sprites/Death6.png", 0.1),
             ("data/sprites/Death7.png", 0.1), ("data/sprites/Death8.png",
                                                0.1), ("data/sprites/Death9.png", 0.1),
             ("data/sprites/Death10.png", 0.1), ("data/sprites/Death11.png", 0.1), ("data/sprites/Death12.png", 0.1)], False)
        self.cureanim = pyganim.PygAnimation(
            [("data/sprites/Cure1.png", 0.1), ("data/sprites/Cure2.png", 0.1), ("data/sprites/Cure3.png", 0.1),
             ("data/sprites/Cure4.png", 0.1), ("data/sprites/Cure5.png",
                                               0.1), ("data/sprites/Cure6.png", 0.1),
             ("data/sprites/Cure7.png", 0.1), ("data/sprites/Cure8.png",
                                               0.1), ("data/sprites/Cure9.png", 0.1),
             ("data/sprites/Cure10.png", 0.1), ("data/sprites/Cure11.png",
                                                0.1), ("data/sprites/Cure12.png", 0.1),
             ("data/sprites/Cure13.png", 0.1), ("data/sprites/Cure14.png", 0.1), ("data/sprites/Cure15.png", 0.1)], False)
        self.curesound = pygame.mixer.Sound('data/sounds&music/Item3.ogg')
        self.icesound = pygame.mixer.Sound('data/sounds&music/Ice4.ogg')
        self.deathmagsound = pygame.mixer.Sound(
            'data/sounds&music/Darkness5.ogg')
        self.firesound = pygame.mixer.Sound('data/sounds&music/Fire2.ogg')
        self.watersound1 = pygame.mixer.Sound('data/sounds&music/Water5.ogg')
        self.watersound2 = pygame.mixer.Sound('data/sounds&music/Water1.ogg')
        self.levelupsound = pygame.mixer.Sound('data/sounds&music/levelup.wav')
        self.coinanim.convert_alpha()
        self.castsound = pygame.mixer.Sound('data/sounds&music/Magic4.ogg')
        self.attacksound = pygame.mixer.Sound('data/sounds&music/Slash1.ogg')
        self.thunderanim = pyganim.PygAnimation(
            [("data/sprites/Thunder1.png", 0.2), ("data/sprites/Thunder2.png", 0.1), ("data/sprites/Thunder3.png", 0.1),
             ("data/sprites/Thunder4.png", 0.1), ("data/sprites/Thunder5.png", 0.1)], False)
        self.thunderanim.convert_alpha()
        self.wateranim = pyganim.PygAnimation(
            [("data/sprites/Water1.png", 0.1), ("data/sprites/Water2.png", 0.1), ("data/sprites/Water3.png", 0.1),
             ("data/sprites/Water4.png", 0.1), ("data/sprites/Water5.png",
                                                0.1), ("data/sprites/Water6.png", 0.1),
             ("data/sprites/Water7.png", 0.1), ("data/sprites/Water8.png",
                                                0.1), ("data/sprites/Water9.png", 0.1),
             ("data/sprites/Water10.png", 0.1), ("data/sprites/Water11.png",
                                                 0.1), ("data/sprites/Water12.png", 0.1),
             ("data/sprites/Water13.png", 0.1), ("data/sprites/Water14.png",
                                                 0.1), ("data/sprites/Water15.png", 0.1),
             ("data/sprites/Water16.png", 0.1), ("data/sprites/Water17.png", 0.1), ("data/sprites/Water18.png", 0.1)], False)
        self.thundersound = pygame.mixer.Sound(
            'data/sounds&music/Thunder9.ogg')
        self.deathsprite = pygame.image.load(
            "data/sprites/death.png").convert_alpha()
        self.attacksound2 = pygame.mixer.Sound('data/sounds&music/Slash2.ogg')
        self.deadsound = pygame.mixer.Sound('data/sounds&music/Collapse1.ogg')
        self.skillsound = pygame.mixer.Sound('data/sounds&music/Skill1.ogg')
        self.attack = 'attack'
        self.state = 'player'
        self.enemymovelist = ['attack']
        self.phealth = phealth  # p-player m-monster
        self.curphealth = phealth
        self.pmana = pmana
        self.curpmana = self.pmana
        self.pstr = pstr
        self.slashanim = pyganim.PygAnimation(
            [["data/sprites/Slash1.png", 0.1], ("data/sprites/Slash2.png", 0.1), ("data/sprites/Slash3.png", 0.1),
             ("data/sprites/Slash4.png", 0.1), ("data/sprites/Slash5.png", 0.1)], False)
        self.slashanim.convert_alpha()
        self.clawanim = pyganim.PygAnimation(
            [("data/sprites/Claw1.png", 0.1), ("data/sprites/Claw2.png", 0.1), ("data/sprites/Claw3.png", 0.1),
             ("data/sprites/Claw4.png", 0.1), ("data/sprites/Claw5.png", 0.1)], False)
        self.clawanim.convert_alpha()
        self.xpanim = pyganim.PygAnimation(
            [("data/sprites/xp1.png", 0.1), ("data/sprites/xp2.png", 0.1), ("data/sprites/xp3.png", 0.1), ("data/sprites/xp4.png", 0.1),
             ("data/sprites/xp5.png", 0.1), ("data/sprites/xp6.png",
                                             0.1), ("data/sprites/xp7.png", 0.1), ("data/sprites/xp8.png", 0.1),
             ("data/sprites/xp9.png", 0.1)])
        self.xpanim.convert_alpha()
        self.specialanim = pyganim.PygAnimation(
            [("data/sprites/Special1.png", 0.1), ("data/sprites/Special2.png", 0.1), ("data/sprites/Special3.png", 0.1),
             ("data/sprites/Special4.png", 0.1), ("data/sprites/Special5.png",
                                                  0.1), ("data/sprites/Special6.png", 0.1),
             ("data/sprites/Special7.png", 0.1), ("data/sprites/Special8.png",
                                                  0.1), ("data/sprites/Special9.png", 0.1),
             ("data/sprites/Special10.png", 0.1), ("data/sprites/Special11.png",
                                                   0.1), ("data/sprites/Special12.png", 0.1),
             ("data/sprites/Special13.png", 0.1), ("data/sprites/Special14.png",
                                                   0.1), ("data/sprites/Special15.png", 0.1),
             ("data/sprites/Special16.png", 0.1), ("data/sprites/Special17.png",
                                                   0.1), ("data/sprites/Special18.png", 0.1),
             ("data/sprites/Special19.png", 0.1), ("data/sprites/Special20.png", 0.1), ], False)
        self.specialanim.convert_alpha()
        self.enemyattacking = False
        self.bgm = bgm
        self.pclass = pclass
        self.pstrmod = pstrmod
        self.pdef = pdef
        self.pmag = pmag
        self.pluck = pluck
        self.mhealth = 1
        self.mmaxhealth = self.mhealth
        self.mstr = 1
        self.mdef = 1
        self.mmag = 1
        self.pstatus = 'normal'
        self.gold = 1
        self.crit = 0
        self.exp = 1
        self.magic = ['Fire', 'Ice', 'Cure', 'Death', 'Tsunami']
        self.skilllist = ['Burst']
        self.cursorpos = 0
        self.txtcolor = (21, 57, 114)
        self.gotskills = False
        self.gotmagic = False
        self.gotitems = False
        self.battleflow = Timer()
        self.ui1 = pygame.image.load(
            "data/backgrounds/rpgtxt.png").convert_alpha()
        self.ui2 = pygame.image.load(
            "data/backgrounds/rpgtxt.png").convert_alpha()
        self.cursor = pygame.image.load(
            "data/sprites/Cursor.png").convert_alpha()
        self.cursormax = 2
        self.uitext = pygame.font.Font(
            "data/fonts/runescape_uf.ttf", 30)  # Default font for Ui
        self.uitext2 = pygame.font.Font(
            "data/fonts/Vecna.otf", 30)  # font for damage
        self.burstdesc = self.uitext.render('Greatly strengthens next attack for 1 turn. MP COST:15', False,
                                            (37, 61, 36))
        self.firedesc = self.uitext.render(
            'Deal small Fire damage to the enemy. MP COST:5', False, (37, 61, 36))
        self.icedesc = self.uitext.render(
            'Deal small Ice damage to the enemy. MP COST:10', False, (37, 61, 36))
        self.curedesc = self.uitext.render(
            'Restores a small amount of health. MP COST:15', False, (37, 61, 36))
        self.deathdesc = self.uitext.render(
            'Invokes death upon your foe. Chance of instantly killing your enemy. MP COST:30', False, (37, 61, 36))
        self.tsunamidesc = self.uitext.render(
            'Creates a devastating flood and deals massive Water damage to enemies. MP COST:50', False, (37, 61, 36))
        self.potiondesc = self.uitext.render(
            'Heals 50 Health', False, (37, 61, 36))
        self.atk = self.uitext.render(
            'Attack', False, self.txtcolor).convert_alpha()
        self.mag = self.uitext.render(
            'Magic', False, self.txtcolor).convert_alpha()
        self.ski = self.uitext.render(
            'Skill', False, self.txtcolor).convert_alpha()
        self.item = self.uitext.render(
            'Item', False, self.txtcolor).convert_alpha()
        self.cancel = self.uitext.render(
            'Cancel', False, self.txtcolor).convert_alpha()
        self.crittxt = self.uitext2.render(
            'Critical!', False, (200, 0, 0)).convert_alpha()
        self.nametext = self.uitext.render(
            self.pname, False, (61, 61, 58)).convert_alpha()
        self.hptxt = self.uitext.render(
            'HP:', True, (255, 21, 45)).convert_alpha()
        self.mptxt = self.uitext.render(
            'MP:', True, (29, 21, 255)).convert_alpha()
        self.notlearnedtxt = self.uitext.render(
            'Not learned yet!', True, (255, 21, 45)).convert_alpha()
        self.victoryflag = False
        self.defeatflag = False
        self.bgtxt = self.uitext.render(
            '', False, self.txtcolor).convert_alpha()  # Action bg txt
        self.bgflag = False  # action bg flag
        self.actionbg = pygame.transform.scale(self.ui1, (300, 50))
        self.vicimg = pygame.image.load(
            "data/sprites/victory.png").convert_alpha()
        self.mdeathresist = False  # Check if monster resists the 'death' spell or not
        self.extraheight = 0  # Extra height for position of monster image if needed
        self.hpbarEmpty = pygame.image.load(
            "data/sprites/hpbar1.png").convert_alpha()
        self.hpbarFull = pygame.image.load(
            "data/sprites/hpbar2.png").convert_alpha()

        # 'Virtual Health' of monster, for the displaying of hp on the hp bar.
        self.virtualMonsterHealth = self.mhealth
        self.post_victory = False

    def getitems(self):
        self.itemtxtlist = []
        self.itemlist = []
        if not self.gotitems:
            for item in self.inventory:
                if self.inventory[item] > 0:
                    txt = self.uitext.render(
                        str(item) + '   x' + str(self.inventory[item]), False, self.txtcolor)
                    self.itemtxtlist.append(txt)
                    self.itemlist.append(item)
            self.gotitems = True

    def getskills(self):
        if not self.gotskills:
            self.skitxt = self.uitext.render(
                self.skilllist[0], False, self.txtcolor)
            self.gotskills = True

    def getmagic(self):
        if not self.gotmagic:
            if self.plevel >= 5:
                self.magtxt1 = self.uitext.render(
                    self.magic[0], False, self.txtcolor)
            else:
                self.magtxt1 = self.uitext.render(
                    self.magic[0], False, (105, 109, 114))
            if self.plevel >= 8:
                self.magtxt2 = self.uitext.render(
                    self.magic[1], False, self.txtcolor)
            else:
                self.magtxt2 = self.uitext.render(
                    self.magic[1], False, (105, 109, 114))
            if self.plevel >= 12:
                self.magtxt3 = self.uitext.render(
                    self.magic[2], False, self.txtcolor)
            else:
                self.magtxt3 = self.uitext.render(
                    self.magic[2], False, (105, 109, 114))
            if self.plevel >= 18:
                self.magtxt4 = self.uitext.render(
                    self.magic[3], False, self.txtcolor)
            else:
                self.magtxt4 = self.uitext.render(
                    self.magic[3], False, (105, 109, 114))
            if self.plevel >= 20:
                self.magtxt5 = self.uitext.render(
                    self.magic[4], False, self.txtcolor)
            else:
                self.magtxt5 = self.uitext.render(
                    self.magic[4], False, (105, 109, 114))
            self.gotmagic = True

    def calcdamage(self, dmgtype='normal'):
        # calculates player damage during players turn and enemies damage during the enemies turn.
        if dmgtype == 'fire':
            damage = self.pmag * (100 / (100 + self.mdef)
                                  ) - random.randrange(0, 10)
        if dmgtype == 'ice':
            damage = self.pmag * (100 / (100 + self.mdef)
                                  ) - random.randrange(0, 10)
        if dmgtype == 'water':
            damage = (self.pmag * 3) * (100 / (100 + self.mdef)) - \
                random.randrange(0, 10)
        if dmgtype == 'death':
            if self.mdeathresist:
                return 'Resist!'
            else:
                deathluck = random.randrange(1, 6)  # 1 in 5 chance of success
                print('Deathluck:', deathluck)
                if deathluck == 5:
                    damage = 99999
                else:
                    return 'Failed!'
        if dmgtype == 'cure':  # Not really damage but eh
            damage = ((self.phealth * 10) / 35) - random.randrange(0, 6)
        elif self.state == 'attack':
            if self.attack == 'attack':

                self.crit = random.randrange(self.pluck,
                                             11)  # higher probability with higher luck,will always crit with 10 luck.
                if self.pluck >= 10:
                    self.crit = 10
                print(self.crit)
                if self.pstatus == 'burst':  # Warrior burst skill takes priority over a crit
                    damage = (self.pstr * (100 / (100 + self.mdef))
                              ) * 5 - random.randrange(0, 10)
                elif self.crit == 10:
                    damage = (self.pstr * (100 / (100 + self.mdef))
                              ) * 4 - random.randrange(0, 10)
                else:
                    damage = (self.pstr * (100 / (100 + self.mdef))
                              ) * 2 - random.randrange(0, 10)
        elif self.state == 'enemyattack':
            if self.attack == 'attack':
                damage = self.mstr * \
                    (100 / (100 + self.pdef)) - random.randrange(0, 10)
            if dmgtype == 'thunder':  # temp make sure to change
                damage = self.mmag * \
                    (100 / (100 + self.pdef)) - random.randrange(0, 10)
        print(self.state)
        if damage < 0:
            damage = 0
        elif damage > 99999:
            damage = 99999
        return int(damage)

    def statuswindow(self):  # The main UI during the battle. Needs some work
        self.nametext = self.uitext.render(
            self.pname, False, (61, 61, 58)).convert_alpha()

        curhealth = self.uitext.render(
            str(self.curphealth) + '/' + str(self.phealth), False, (114, 21, 45))

        curmana = self.uitext.render(
            str(self.curpmana) + '/' + str(self.pmana), False, (29, 21, 114))

        surf.blit(pygame.transform.scale(self.ui1, (curwidth, 300)), (0, 430))
        surf.blit(self.nametext, (332, 474))
        surf.blit(self.hptxt, (463, 474))
        surf.blit(self.mptxt, (675, 474))
        surf.blit(curhealth, (503, 474))
        surf.blit(curmana, (715, 474))
        if self.state == 'player':
            surf.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            surf.blit(self.atk, (38, 474))
            surf.blit(self.item, (38, 534))
            if self.pclass == 'mage':
                surf.blit(self.mag, (38, 504))
            if self.pclass == 'warrior':
                surf.blit(self.ski, (38, 504))

            if self.cursorpos == 0:
                surf.blit(self.cursor, (6, 474))
            elif self.cursorpos == 1:
                surf.blit(self.cursor, (6, 504))
            elif self.cursorpos == 2:
                surf.blit(self.cursor, (6, 534))
        if self.state == 'skill':
            self.getskills()
            surf.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            surf.blit(self.skitxt, (38, 464))
            surf.blit(self.cancel, (38, 494))
            if self.cursorpos == 0:  # burst
                surf.blit(self.cursor, (6, 464))
                surf.blit(self.burstdesc, (328, 577))
            elif self.cursorpos == 1:  # cancel
                surf.blit(self.cursor, (6, 494))

        if self.state == 'magic':
            self.getmagic()
            surf.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            surf.blit(self.magtxt1, (38, 464))
            surf.blit(self.magtxt2, (38, 494))
            surf.blit(self.magtxt3, (38, 524))
            surf.blit(self.magtxt4, (38, 554))
            surf.blit(self.magtxt5, (38, 584))
            surf.blit(self.cancel, (38, 614))
            if self.cursorpos == 0:  # fire
                surf.blit(self.cursor, (6, 464))
                surf.blit(self.firedesc, (328, 577))
                if self.plevel < 5:
                    surf.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 1:  # ice
                surf.blit(self.cursor, (6, 494))
                surf.blit(self.icedesc, (328, 577))
                if self.plevel < 8:
                    surf.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 2:  # cure
                surf.blit(self.cursor, (6, 524))
                surf.blit(self.curedesc, (328, 577))
                if self.plevel < 12:
                    surf.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 3:  # death
                surf.blit(self.cursor, (6, 554))
                surf.blit(self.deathdesc, (328, 577))
                if self.plevel < 18:
                    surf.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 4:  # tsunami
                surf.blit(self.cursor, (6, 584))
                surf.blit(self.tsunamidesc, (328, 577))
                if self.plevel < 20:
                    surf.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 5:  # cancel
                surf.blit(self.cursor, (6, 614))
        if self.state == 'item':
            self.getitems()
            surf.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            surf.blit(self.itemtxtlist[0], (38, 464))
            surf.blit(self.cancel, (38, 494))
            if self.cursorpos == 0:
                surf.blit(self.cursor, (6, 464))
                surf.blit(self.potiondesc, (328, 577))
            elif self.cursorpos == 1:
                surf.blit(self.cursor, (6, 494))

        if self.pstatus == 'burst':
            surf.blit(self.staticon1, (800, 474))
        if self.bgflag:
            surf.blit(self.actionbg, (495, 73))
            surf.blit(self.bgtxt, (604, 83))

    def healthbar(self, animpos=0):  # Enemy health bar
        healthpercent = (self.virtualMonsterHealth / self.mmaxhealth) * 100
        if healthpercent < 0:
            healthpercent = 0.1
        surf.blit(pygame.transform.scale(self.hpbarEmpty, (260, 18)),
                  (self.monpos[0], self.monpos[1] + 100 - animpos))
        surf.blit(pygame.transform.scale(self.hpbarFull, (int(246 * (healthpercent / 100)), 18)),
                  (self.monpos[0] + 7, self.monpos[1] + 1 + 100 - animpos))

    def skillanim(self):  # Skill logic and animation queues
        if self.state == 'burst':  # burst skill start
            self.specialanim.play()
            self.skillsound.play()
            self.battleflow.reset()
            self.state = 'burstanim'
            self.bgflag = True
            self.bgtxt = self.uitext.render('Burst', False, self.txtcolor)

        if self.battleflow.timing() == 3 and self.state == 'burstanim':
            self.bgflag = False
            self.pstatus = 'burst'
            self.players[0].stop()
            self.burstanim.play()
            self.state = 'enemy'
            self.curpmana -= 15
            self.enemyattacking = True
            self.currentturn = self.turn
            self.battleflow.reset()
        if self.pstatus == 'burst':
            if self.turn - self.currentturn == 2:
                self.pstatus = 'normal'
                self.burstanim.stop()
                self.players[0].play()  # burst skill end
        if self.state == 'fire':  # Fire magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus = 'firecast'
            self.state = 'enemy'
            self.enemyattacking = True
        if self.state == 'ice':  # Ice magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus = 'icecast'
            self.state = 'enemy'
            self.enemyattacking = True
        if self.state == 'water':  # Water magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus = 'watercast'
            self.state = 'enemy'
            self.enemyattacking = True
        if self.state == 'death':  # Death magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus = 'deathcast'
            self.state = 'enemy'
            self.enemyattacking = True
        if self.state == 'cure':  # Cure magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus = 'curecast'
            self.state = 'enemy'
            self.enemyattacking = True

    # raises the defeat flag,ends the match when set to true and sends player back to main menu.
    def defeat(self):
        timer = Timer()
        pygame.mixer.music.pause()
        pygame.mixer.music.load('data/sounds&music/Gameover2.ogg')
        pygame.mixer.music.play()
        dark = pygame.Surface(surf.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark, (0, 0))

        deftxt = pygame.font.Font("data/fonts/Daisy_Roots.otf", 70)
        defeat = deftxt.render('Defeat!', True, (255, 0, 0)).convert_alpha()
        cont = self.uitext.render(
            'Your journey isn\'t over yet! Move onward!', True, (255, 255, 0)).convert_alpha()
        surf.blit(defeat, ((curwidth / 3) - 30, curheight / 5))
        cFlag = False  # continue flag
        while self.defeatflag:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RCTRL:
                        self.defeatflag = False
                        self.battling = False
                        pygame.mixer.music.load('data/sounds&music/Theme2.ogg')
                        self.mhealth = self.mmaxhealth  # reseting instance
                        self.state = 'player'
                        self.virtualMonsterHealth = self.mmaxhealth
                        pygame.mixer.music.play()
                        global scene, battle_choice, post_battle, drawui, controlui
                        scene = 'menu'
                        battle_choice = False
                        post_battle = False
                        drawui = True
                        controlui = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posfinder()
            if not cFlag:
                if timer.dothing(2):
                    surf.blit(cont, (407, 253))

                    cFlag = True

            screen.blit(surf, (0, 0))
            clock.tick(60)
            pygame.display.update()

    # raises the victory flag,ends the match when set to true.
    def victory(self):
        timer = Timer()
        pygame.mixer.music.pause()
        pygame.mixer.music.load('data/sounds&music/Victory_and_Respite.mp3')
        pygame.mixer.music.play()
        dark = pygame.Surface(surf.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark, (0, 0))
        surf.blit(self.vicimg, (curwidth / 3, curheight / 5))
        gold = self.uitext.render('Gold:+%d' % self.gold, True, (255, 255, 0))
        exp = self.uitext.render('Exp:+%d' % self.exp, True, (244, 240, 66))
        lvlup = self.uitext.render('Level Up!', True, (120, 240, 66))
        statup = self.uitext.render('All stats up!', True, (110, 255, 66))
        gFlag = False
        eFlag = False
        lFlag = False
        while self.victoryflag:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if (
                            event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_RCTRL) and lFlag:
                        self.victoryflag = False
                        self.post_victory = True
                        self.battling = False
                        pygame.mixer.music.load(
                            'data/sounds&music/Infinite_Arena.mp3')
                        pygame.mixer.music.play()
                        self.mhealth = self.mmaxhealth  # reseting instance
                        self.virtualMonsterHealth = self.mmaxhealth
                        self.state = 'player'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posfinder()
            if not gFlag:
                if timer.dothing(1):
                    surf.blit(gold, (427, 253))
                    self.coinanim.play()
                    gFlag = True
            if not eFlag:
                if timer.dothing(2):
                    surf.blit(exp, (427, 287))
                    self.xpanim.play()
                    eFlag = True
            if not lFlag:
                if timer.dothing(6):
                    if (self.exp >= self.xptolevel) and (eFlag and gFlag):
                        self.levelupsound.play()
                        surf.blit(lvlup, (427, 321))
                        surf.blit(statup, (427, 354))
                    lFlag = True

            self.coinanim.blit(surf, (397, 253))
            self.xpanim.blit(surf, (397, 287))
            screen.blit(surf, (0, 0))
            clock.tick(60)
            pygame.display.update()

    # Method to get the players current stats and other details.
    def getplayerdetails(self, player=Player()):
        self.plevel = player.level
        self.pname = player.name
        self.phealth = player.hp
        self.pmana = player.mp
        self.curphealth = player.curhp
        self.curpmana = player.curmp
        self.pstr = player.stre + player.add_stre
        self.pdef = player.defe + player.add_defe
        self.pmag = player.mag + player.add_mag
        self.pclass = player.pclass
        self.pluck = player.luck

    def set_monster(self, monster_name):  # Initialise the monster
        self.mhealth = self.mondata[monster_name]['health']
        self.mmaxhealth = self.mhealth
        self.virtualMonsterHealth = self.mhealth
        self.monsters = pygame.image.load(
            self.mondata[monster_name]['sprites']).convert_alpha()
        self.mstr = self.mondata[monster_name]['str']
        self.mdef = self.mondata[monster_name]['def']
        self.mmag = self.mondata[monster_name]['mag']
        self.gold = self.mondata[monster_name]['gold']
        self.exp = self.mondata[monster_name]['exp']
        self.enemymovelist = self.mondata[monster_name]['move_list']

    def battle(self, monstername, offset=0, resist_death=False,
               bgm='data/sounds&music/yousayrun.mp3'):  # The main battle scene
        self.extraheight = offset
        self.mdeathresist = resist_death
        self.bgm = bgm
        self.set_monster(monstername)
        if self.pclass == 'warrior':
            self.players[0] = pyganim.PygAnimation(
                [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        elif self.pclass == 'mage':
            self.players[0] = pyganim.PygAnimation(
                [("data/sprites/midle1.png", 0.3), ("data/sprites/midle2.png", 0.3), ("data/sprites/midle3.png", 0.3)])
        self.players[0].play()
        self.players[0].convert_alpha()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.bgm)
        self.encountersound.play()
        fadein(255)
        pygame.time.wait(300)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.battling = True
        win = False
        lose = False
        self.state = 'player'
        text = pygame.font.Font("data/fonts/runescape_uf.ttf", 30)
        ab = text.render(alphatext, False, (255, 255, 0))  # debug
        doneflag = False
        get = True  # monsterpos flag
        attackdone = False  # flag for attacking
        played_once = False  # deathsound flag
        attacking = False
        attacked = False
        attackedp = False
        casted = False
        cure = False  # For cure magic
        enemydead = False
        enemyskill = ''
        critted = False  # crit txt flag
        global screen
        while self.battling:
            curwidth, curheight = screen.get_size()
            surf.blit(pygame.transform.scale(
                self.bg, (curwidth, curheight)), (0, 0))

            if get:
                self.monpos = (curwidth - 1080, 200 + self.extraheight)

                get = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.battling = False
                    global done
                    done = True

                if event.type == KEYDOWN:
                    if self.state == 'player' and event.key == pygame.K_DOWN or self.state == 'player' and event.key == pygame.K_UP:
                        self.cursorsound.play()
                    if event.key == pygame.K_DOWN:
                        self.cursorpos += 1
                    if event.key == pygame.K_UP:
                        self.cursorpos -= 1
                    if self.state == 'skill' and event.key == pygame.K_DOWN or self.state == 'state' and event.key == pygame.K_UP:
                        self.cursorsound.play()
                    if event.key == pygame.K_w:
                        self.victoryflag = True
                        self.victory()
                        if self.state == 'player':
                            self.state = 'enemy'
                            print(self.state)
                        elif self.state == 'enemy':
                            self.state = 'player'
                            print(self.state)
                    if self.cursorpos == 2 and event.key == pygame.K_RETURN and self.state == 'player':  # items
                        self.state = 'item'
                        self.gotitems = False
                        self.cursorpos = 3
                    if (
                            self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state == 'player') and self.pclass == 'warrior':  # magic/skill
                        self.state = 'skill'
                        self.cursorpos = 99
                    if (
                            self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state == 'player') and self.pclass == 'mage':  # magic/skill
                        self.state = 'magic'
                        self.cursormax = 5
                        self.cursorpos = 99
                    if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state == 'player':  # attack

                        attacking = True
                    if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state == 'skill':  # burst
                        if self.curpmana >= 10:
                            self.state = 'burst'
                        else:
                            self.buzzer.play()
                    if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state == 'magic':  # Fire
                        if self.curpmana >= 5 and self.plevel >= 5:
                            self.state = 'fire'
                        else:
                            self.buzzer.play()
                    if self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state == 'magic':  # Ice
                        if self.curpmana >= 10 and self.plevel >= 8:
                            self.state = 'ice'
                        else:
                            self.buzzer.play()
                    if self.cursorpos == 2 and event.key == pygame.K_RETURN and self.state == 'magic':  # Cure
                        if self.curpmana >= 15 and self.plevel >= 12:
                            self.state = 'cure'
                        else:
                            self.buzzer.play()
                    if self.cursorpos == 3 and event.key == pygame.K_RETURN and self.state == 'magic':  # Death
                        if self.curpmana >= 30 and self.plevel >= 18:
                            self.state = 'death'
                        else:
                            self.buzzer.play()
                    if self.cursorpos == 4 and event.key == pygame.K_RETURN and self.state == 'magic':  # Tsunami
                        if self.curpmana >= 50 and self.plevel >= 20:
                            self.state = 'water'
                        else:
                            self.buzzer.play()
                    if self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state == 'skill':  # Cancel
                        self.state = 'player'
                    if self.cursorpos == 5 and event.key == pygame.K_RETURN and self.state == 'magic':  # Cancel
                        self.state = 'player'

                    if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state == 'item':  # item1
                        print(self.itemlist)
                        self.inventory[self.itemlist[0]] += 1
                        print(self.inventory[self.itemlist[0]])
                    if self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state == 'item':  # Cancel
                        self.state = 'player'
                        self.cursorpos = 2

                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.load(self.bgm)
                    pygame.mixer.music.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posfinder()  # debug

            if self.cursorpos < 0:
                self.cursorpos = self.cursormax
            if self.cursorpos > self.cursormax:
                self.cursorpos = 0
            # Battle blits below This line#
            self.skillanim()
            surf.blit(self.pshadow, [curwidth - 320, 305])
            self.players[0].blit(surf, [curwidth - 331, 280])
            self.players[1].blit(surf, [curwidth - 331, 280])
            self.burstanim.blit(surf, [curwidth - 331, 280])
            self.cureanim.blit(surf, [curwidth - 391, 240])
            if not enemydead:
                surf.blit(self.monsters, self.monpos)

            # battleflow timer - controls flow of battle(animations,timing,etc.)
            self.battleflow.timing()
            self.mhurt.blit(surf, [curwidth - 331, 280])
            self.slashanim.blit(surf, self.monpos)
            self.clawanim.blit(surf, [curwidth - 381, 255])
            self.specialanim.blit(surf, [curwidth - 381, 255])
            self.thunderanim.blit(surf, [curwidth - 381, 255])
            self.castanim.blit(surf, [curwidth - 409, 200])
            self.fireanim.blit(
                surf, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.iceanim.blit(
                surf, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.deathanim.blit(
                surf, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.wateranim.blit(
                surf, (self.monpos[0], (self.monpos[1] + 100) - self.extraheight))
            self.statuswindow()
            surf.blit(ab, (0, 0))
            screen.blit(surf, [0, 0])

            # Battle blits above this line#
            if self.pstatus == 'firecast' and self.state == 'firecasting':  # fire
                self.bgtxt = self.uitext.render('Fire', False, self.txtcolor)
                self.bgflag = True
                self.castsound.play()
                self.castanim.play()
                self.state = 'fireanim'
                dmg = self.calcdamage('fire')
                self.virtualMonsterHealth -= dmg
                dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))

            if self.battleflow.timing() == 2 and self.state == 'fireanim':
                self.bgflag = False
                self.pstatus = 'normal'

                self.fireanim.play()
                self.firesound.play()
                self.state = 'animdone'
                self.curpmana -= 5
                casted = True

            if self.pstatus == 'icecast' and self.state == 'icecasting':  # ice
                self.bgtxt = self.uitext.render('Ice', False, self.txtcolor)
                self.bgflag = True
                self.castsound.play()
                self.castanim.play()
                self.state = 'iceanim'
                dmg = self.calcdamage('ice')
                self.virtualMonsterHealth -= dmg
                dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))

            if self.battleflow.timing() == 2 and self.state == 'iceanim':
                self.bgflag = False
                self.pstatus = 'normal'

                self.iceanim.play()
                self.icesound.play()
                self.state = 'animdone'
                self.curpmana -= 10
                casted = True
            if self.pstatus == 'watercast' and self.state == 'watercasting':  # Tsunami
                self.bgtxt = self.uitext.render(
                    'Tsunami', False, self.txtcolor)
                self.bgflag = True
                self.castsound.play()
                self.castanim.play()
                self.state = 'wateranim'
                dmg = self.calcdamage('water')
                self.virtualMonsterHealth -= dmg
                dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))

            if self.battleflow.timing() == 2 and self.state == 'wateranim':
                self.bgflag = False
                self.pstatus = 'normal'

                self.wateranim.play()
                self.watersound1.play()
                self.watersound2.play()
                self.state = 'animdone'
                self.curpmana -= 50
                casted = True
            # Death(magic)
            if self.pstatus == 'deathcast' and self.state == 'deathcasting':
                self.bgtxt = self.uitext.render('Death', False, self.txtcolor)
                self.bgflag = True
                self.castsound.play()
                self.castanim.play()
                self.state = 'deathanim'
                dmg = self.calcdamage('death')
                if type(dmg) == int:  # Only subtract from virtual health if death is successful
                    self.virtualMonsterHealth -= dmg
                dmgtxt = self.uitext2.render(str(dmg), True, (119, 17, 38))
                casted = False
            if self.battleflow.timing() == 2 and self.state == 'deathanim':
                self.bgflag = False
                self.pstatus = 'normal'

                self.deathanim.play()
                self.deathmagsound.play()
                self.state = 'animdone'
                self.curpmana -= 30
                casted = True
                death = True
            if self.pstatus == 'curecast' and self.state == 'curecasting':  # Cure
                self.bgtxt = self.uitext.render('Cure', False, self.txtcolor)
                self.bgflag = True
                self.castsound.play()
                self.castanim.play()
                self.state = 'cureanim'
                dmg = self.calcdamage('cure')
                dmgtxt = self.uitext2.render(str(dmg), True, (55, 181, 27))
                cure = False
            if self.battleflow.timing() == 2 and self.state == 'cureanim':
                self.bgflag = False
                self.pstatus = 'normal'

                self.cureanim.play()
                self.curesound.play()
                self.state = 'animdone'
                self.curpmana -= 15
                cure = True

            if casted:
                self.healthbar(hpbarpos)  # shows health bar after cast
                # damage text after spell cast
                surf.blit(
                    dmgtxt, (self.monpos[0] + 100, self.monpos[1] - dmgtxtpos))
                screen.blit(surf, (0, 0))

            if cure:
                surf.blit(dmgtxt, [curwidth - 331, 240])
                screen.blit(surf, (0, 0))
            if self.battleflow.timing() == 5 and self.state == 'animdone':
                self.players[1].stop()
                self.players[0].play()
                casted = False
                if type(dmg) == int and not cure:
                    self.mhealth -= dmg
                if cure:
                    self.curphealth += dmg
                    cure = False
                self.battleflow.reset()
                self.state = 'player'
            if attacking:  # Attack state
                if self.state == 'player':
                    dmgtxtpos = 0  # Text 'Animation'
                    hpbarpos = 0  # Hp bar 'Animation'
                    attackedp = False
                    print(attackedp, self.crit, self.pstatus)
                    self.state = 'attack'
                    dmg = self.calcdamage()
                    self.virtualMonsterHealth -= dmg
                    self.battleflow.reset()

                if self.battleflow.timing() == 1 and attackdone == False:
                    if (attackedp == False and self.crit == 10) and self.pstatus != 'burst':
                        self.slashanim.play()
                        self.attacksound.play()
                        dmgtxt = self.uitext2.render(
                            str(dmg), True, (255, 255, 255))
                        critted = True
                        screen.blit(surf, (0, 0))
                        attackedp = True
                        print(critted)

                    if (attackedp == False and self.crit != 10) or (attackedp == False and self.pstatus == 'burst'):
                        self.slashanim.play()
                        self.attacksound.play()
                        dmgtxt = self.uitext2.render(
                            str(dmg), True, (255, 255, 255))
                        attackedp = True
                    if dmgtxtpos < 35:
                        dmgtxtpos += 5
                    if hpbarpos < 100:
                        hpbarpos += 10
                    surf.blit(
                        dmgtxt, (self.monpos[0] + 100, self.monpos[1] - dmgtxtpos))
                    self.healthbar(hpbarpos)
                    screen.blit(surf, (0, 0))

                if critted:
                    surf.blit(self.crittxt,
                              (self.monpos[0] + 100, self.monpos[1] - 70))
                    screen.blit(surf, (0, 0))

                if self.battleflow.timing() == 2 and attackdone == False:
                    print('done:player')  # debug
                    dmgtxtpos = 60
                    attackdone = True
                    critted = False
                    self.battleflow.reset()
                if self.battleflow.timing() == 2 and attackdone == True:
                    self.mhealth -= dmg
                    attacking = False

                    attackdone = False
                    if self.mhealth <= 0:
                        self.state = 'victory'
                    else:
                        self.state = 'enemy'
                        attackedp = False
                        self.enemyattacking = True

            if self.enemyattacking:
                if self.state == 'enemy':
                    move = random.randrange(0, len(self.enemymovelist))
                    if self.enemymovelist[move] == 'attack':
                        attacked = False
                    # enemy casting thunder
                    elif self.enemymovelist[move] == 'thunder':
                        attacked = True
                        enemyskill = 'thunder'
                        self.bgtxt = self.uitext.render(
                            'Thunder', False, self.txtcolor)
                        self.bgflag = True

                self.state = 'enemyattack'
                if self.battleflow.timing() == 2 and attackdone == False:
                    if not attacked:
                        self.clawanim.play()
                        self.attacksound2.play()
                        dmg = self.calcdamage()
                        dmgtxt = self.uitext2.render(
                            str(dmg), True, (255, 255, 255))
                        attacked = True

                    if enemyskill == 'thunder':
                        self.thunderanim.play()
                        self.thundersound.play()
                        dmg = self.calcdamage('thunder')
                        dmgtxt = self.uitext2.render(
                            str(dmg), True, (255, 255, 255))
                        enemyskill = ''
                    surf.blit(dmgtxt, [curwidth - 331, 280])
                    screen.blit(surf, (0, 0))
                if self.battleflow.timing() == 4 and attackdone == False:
                    print('done:enemy')  # debug
                    self.bgflag = False
                    attackdone = True
                    self.battleflow.reset()
                if self.battleflow.timing() == 1 and attackdone == True:
                    self.curphealth -= dmg
                    attackdone = False
                    self.enemyattacking = False
                    self.turn += 1
                    if self.pstatus == 'firecast':
                        self.state = 'firecasting'
                        self.battleflow.reset()

                    elif self.pstatus == 'icecast':
                        self.state = 'icecasting'
                        self.battleflow.reset()
                    elif self.pstatus == 'watercast':
                        self.state = 'watercasting'
                        self.battleflow.reset()
                    elif self.pstatus == 'deathcast':
                        self.state = 'deathcasting'
                        self.battleflow.reset()
                    elif self.pstatus == 'curecast':
                        self.state = 'curecasting'
                        self.battleflow.reset()
                    else:
                        self.state = 'player'

            if self.mhealth <= 0:
                if not played_once:
                    self.deadsound.play()
                    enemydead = True
                    self.battleflow.reset()
                    played_once = True
                self.state = 'victory'
                win = True
            if self.battleflow.timing() == 3 and win == True:
                self.victoryflag = True
                self.victory()
            if self.curphealth <= 0:
                self.state = 'defeat'
                self.curphealth = 0
                self.players[0].stop()
                self.burstanim.stop()
                self.players[1].stop()
                surf.blit(self.deathsprite, [curwidth - 331, 280])
                screen.blit(surf, (0, 0))
                lose = True
            if self.curphealth > self.phealth:
                self.curphealth = self.phealth
            if self.battleflow.timing() == 3 and lose == True:
                self.defeatflag = True
                self.defeat()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)

            pygame.display.update()


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
        # Rough x coordinate of player on screen (For animations)
        self.player_x = 920
        self.player_y = 270
        self.add_flag = False  # flag for the gold and exp adding up on the victory screen
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
        self.buzzer_sound = pygame.mixer.Sound(sounddata['system']['buzzer'])
        self.level_up_sound = pygame.mixer.Sound(
            'data/sounds&music/levelup.wav')
        #  State control
        self.battling = True
        self.turn = 'player'
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
            self.player_sprites.blit(surf, (600, 300))
        elif target == 'enemy':
            surf.blit(self.m_sprite, (600, 300))

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
                global done
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                posfinder()
            if event.type == pygame.constants.USEREVENT:
                pygame.mixer_music.set_volume(vol)
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
                            fadeout(surf, 0.001)
                            self.victory_flag = False

    def draw_sprites(self):
        surf.blit(self.background, (0, 0))
        if self.player_flag:
            self.player_sprites.blit(surf, (self.player_pos, 300))
            if self.player_pos > 950:
                self.player_pos -= 50
        for status in self.p_status:
            if "burst" in status[0]:
                self.player_sprites_burst.blit(surf, (self.player_pos, 300))
                self.player_flag = False
        else:
            self.player_flag = True
        if self.monster_flag:
            surf.blit(self.m_sprite, (self.monster_pos,
                      self.monster_y + self.monster_y_offset))
            self.loaded_anim.blit(surf, self.anim_pos)  # Loaded animation
            if self.monster_pos < 200:
                self.monster_pos += 50

    def play_sound(self, sound):
        self.sound_effect = pygame.mixer.Sound(self.sound_data[sound])
        global vol
        self.sound_effect.set_volume(vol)
        self.sound_effect.play()

    def play_animation(self, animation, pos=(920, 270)):
        self.loaded_anim = pyganim.PygAnimation(
            self.animation_data[animation], False)
        self.anim_pos = pos
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
            choose_move = random.randrange(0, len(self.m_move_list))
            enemy_action = self.m_move_list[choose_move]
            if enemy_action == 'attack':
                self.game_state = 'enemy_attack'
                self.global_timer.reset()
            else:
                self.sequence_to_play = enemy_action
                self.game_state = 'enemy_skill'
                self.global_timer.reset()
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
                self.game_state = ''
                self.global_timer.reset()
                self.turn_count += 1
                self.draw_menu = True
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
                self.game_state = ''
                self.draw_menu = True
                self.ui_state = 'main'
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
            surf.blit(self.death_sprite,
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
                surf.blit(self.death_sprite,
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
                        if action[0] != "end_sequence":
                            self.action_count += 1
                            self.sequence_timer.reset()
                            # Getting the time to wait for the next action
                            self.wait_time = action[len(action) - 1]
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
            surf.blit(self.cursor, (890, 475))
        if self.cursor_pos == 1:
            surf.blit(self.cursor, (890, 500))
        if self.cursor_pos == 2:
            surf.blit(self.cursor, (890, 525))
        if self.cursor_pos == 3:
            surf.blit(self.cursor, (890, 550))

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
        surf.blit(pygame.transform.scale(self.hp_bar_Empty,
                  (260, 18)), (self.monster_pos, self.monster_y))
        surf.blit(pygame.transform.scale(self.hp_bar_Full, (int(246 * (health_percent / 100)), 18)),
                  (self.monster_pos + 7, self.monster_y + 1))

    def draw_alertbox(self):
        """The alert box or the skill box that gets drawn when a skill is used."""
        if self.alert_box_flag:
            surf.blit(self.alert_box, (430, 80))
            txt = self.ui_font.render(self.alert_text, False, (55, 0, 200))
            surf.blit(txt, (500, 120))

    def draw_ui(self):
        surf.blit(self.battle_ui, (self.window_pos, 400))
        surf.blit(self.battle_ui3, (self.window_pos - 30, -10))
        if self.window_pos > 900:
            self.window_pos -= 50

        if self.window_pos <= 900:  # when the 'animation' finishes
            hp_text = self.ui_font.render(
                "HP: %d/%d" % (self.p_health, self.p_max_health), True, (230, 0, 50))
            mp_text = self.ui_font.render(
                "MP: %d/%d" % (self.p_mana, self.p_max_mana), True, (20, 0, 230))

            surf.blit(hp_text, (920, 90))  # Text for hp
            surf.blit(mp_text, (920, 110))  # Text for mp
            for index, status in enumerate(self.p_status):
                if status[0] in self.status_icons:
                    surf.blit(
                        self.status_icons[status[0]], (900 + (40 * index), 140))
            if self.ui_state == 'main':
                self.current_title = 0
                surf.blit(self.atk_txt, (945, 475))
                surf.blit(self.skill_txt, (945, 500))
                surf.blit(self.item_txt, (945, 525))
            elif self.ui_state == 'skill':    # Skill selection
                self.current_title = 2
                cur_mp_cost = self.skill_data[self.p_class][self.skill_min +
                                                            self.cursor_pos]['mp_cost']
                self.skill_desc = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['desc'], True, (200, 200, 200))
                surf.blit(self.battle_ui2, (self.initial_window_pos, 400))
                skill_text1 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min]['name'], True, (200, 200, 200))
                skill_text2 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + 1]['name'], True, (200, 200, 200))
                skill_text3 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + 2]['name'], True, (200, 200, 200))
                skill_text4 = self.ui_font.render(
                    self.skill_data[self.p_class][self.skill_min + 3]['name'], True, (200, 200, 200))
                surf.blit(skill_text1, (915, 475))
                surf.blit(skill_text2, (915, 500))
                surf.blit(skill_text3, (915, 525))
                surf.blit(skill_text4, (915, 550))
                if self.skill_min != 0:
                    surf.blit(self.cursor_up, (960, 430))
                if self.skill_min + 4 < len(self.skill_data[self.p_class]):
                    surf.blit(self.cursor_down, (960, 590))
                if self.initial_window_pos < 300:
                    self.initial_window_pos += 30
                if self.initial_window_pos == 300:
                    surf.blit(self.skill_desc, (340, 480))
                    title_text2 = self.title_font.render(
                        self.ui_text[6], True, (200, 30, 30))
                    surf.blit(title_text2, (520, 413))
                    mp_cost_txt = self.ui_font.render(
                        "Mp Cost: %d" % cur_mp_cost, True, (200, 60, 130))
                    surf.blit(mp_cost_txt, (340, 540))
                    if self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['level_req'] > self.p_level:
                        surf.blit(self.ui_font.render("Not learned!",
                                  True, (204, 55, 87)), (570, 540))
                    if self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['mp_cost'] > self.p_mana and \
                            self.skill_data[self.p_class][self.skill_min + self.cursor_pos][
                                'level_req'] <= self.p_level:
                        surf.blit(self.ui_font.render(
                            "Insufficient MP!", True, (49, 61, 224)), (340, 510))
            elif self.ui_state == 'item':
                self.current_title = 3
                surf.blit(self.battle_ui2, (self.initial_window_pos, 400))
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
                        surf.blit(self.cursor_up, (960, 430))
                    if len(self.p_inventory) >= 4:
                        if self.item_min + 4 < len(self.p_inventory):
                            surf.blit(self.cursor_down, (960, 590))
                    amount_in_inventory = self.ui_font.render("In Inventory: {}".format(
                        self.p_inventory[self.item_min + self.cursor_pos]["amount"]), True, (255, 0, 85))
                    item1 = self.ui_font.render(
                        self.p_inventory[self.item_min]["name"], True, (200, 200, 200))
                    surf.blit(item1, (915, 475))
                    if len(self.p_inventory) >= 2:
                        item2 = self.ui_font.render(
                            self.p_inventory[self.item_min + 1]["name"], True, (200, 200, 200))
                        surf.blit(item2, (915, 500))
                    if len(self.p_inventory) >= 3:
                        item3 = self.ui_font.render(
                            self.p_inventory[self.item_min + 2]["name"], True, (200, 200, 200))
                        surf.blit(item3, (915, 525))
                    if len(self.p_inventory) >= 4:
                        item3 = self.ui_font.render(
                            self.p_inventory[self.item_min + 3]["name"], True, (200, 200, 200))
                        surf.blit(item3, (915, 550))
                if self.initial_window_pos < 300:
                    self.initial_window_pos += 30
                if self.initial_window_pos == 300:
                    if len(self.p_inventory) <= 0:
                        item_desc = self.ui_font.render(
                            "No items in inventory.", True, (200, 200, 200))
                        amount_in_inventory = self.ui_font.render(
                            "", True, (200, 200, 200))
                    surf.blit(item_desc, (340, 480))
                    surf.blit(amount_in_inventory, (340, 540))
                    title_text2 = self.title_font.render(
                        self.ui_text[6], True, (200, 30, 30))
                    surf.blit(title_text2, (520, 413))
            title_text = self.title_font.render(
                self.ui_text[self.current_title], True, (200, 30, 30))  # Title for the ui
            surf.blit(title_text, (959, 412))

    def get_monster_details(self, monster_name):
        self.m_max_health = monster_data[monster_name]['health']
        self.m_cur_health = self.m_max_health
        self.virtualMonsterHealth = self.m_cur_health
        self.m_str = monster_data[monster_name]['str']
        self.m_def = monster_data[monster_name]['def']
        self.m_mag = monster_data[monster_name]['mag']
        self.m_luck = monster_data[monster_name]['luck']
        self.m_sprite = pygame.image.load(
            monster_data[monster_name]['sprites'])
        self.m_move_list = monster_data[monster_name]['move_list']
        self.m_gold = monster_data[monster_name]['gold']
        self.m_exp = monster_data[monster_name]['exp']
        self.background = pygame.transform.scale(pygame.image.load(monster_data[monster_name]['bg']).convert_alpha(),
                                                 (1280, 720))
        self.m_weakness = monster_data[monster_name]['weakness']
        self.m_strengths = monster_data[monster_name]['strengths']
        self.m_status = []
        height = self.m_sprite.get_height()
        if height > 220:
            self.monster_y_offset = -100
        else:
            self.monster_y_offset = 0

    def get_player_details(self, player_data=Player()):
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
    def update_player_details(self, player_data=Player()):
        """I don't remember the original reason that I didn't just directly update the player object.
        Well, this works  for now lol."""
        player_data.curhp = self.p_health
        player_data.curmp = self.p_mana
        player_data.gold += self.m_gold
        player_data.exp += self.m_exp
        player_data.inventory = self.p_inventory
        while player.check_levelup():
            print(player.level)
            player.level += 1
            player.hp += 25
            player.mp += 10
            player.stat_points += 3
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
        dark_surf = pygame.Surface(surf.get_size(), 32)
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark_surf, (0, 0))
        gold_txt = self.ui_font.render(
            'Gold:+%d' % self.f_gold, True, (255, 255, 0))
        exp_txt = self.ui_font.render(
            'Exp:+%d' % self.f_exp, True, (244, 240, 66))
        surf.blit(self.vic_img, (curwidth / 3, curheight / 5))
        surf.blit(gold_txt, (curwidth / 3 + 100, curheight / 5 + 100))
        surf.blit(exp_txt, (curwidth / 3 + 100, curheight / 5 + 125))
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
            surf.blit(lvl_txt, (curwidth / 3 + 100, curheight / 5 + 150))
            surf.blit(hp_txt, (curwidth / 3 + 100, curheight / 5 + 175))
            surf.blit(mp_txt, (curwidth / 3 + 100, curheight / 5 + 200))
            surf.blit(stat_txt, (curwidth / 3 + 100, curheight / 5 + 225))

    def defeat(self):
        if not self.add_flag:
            pygame.mixer.music.pause()
            pygame.mixer.music.load(
                'data/sounds&music/Gameover2.ogg')  # defeat music
            pygame.mixer.music.play()
            self.add_flag = True
        # making a transparent dark surface
        dark_surf = pygame.Surface(surf.get_size(), 32)
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark_surf, (0, 0))
        defeat = self.def_font.render(
            'Defeat!', True, (255, 0, 0)).convert_alpha()
        cont = self.ui_font.render(
            'Your journey isn\'t over yet! Move onward!', True, (255, 255, 0)).convert_alpha()
        surf.blit(defeat, (curwidth / 3, curheight / 5))
        surf.blit(cont, (curwidth / 3, curheight / 5 + 100))

    def set_instance(self, player_data=Player()):
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

    def battle(self, monster_name, player_data=Player(), set_music=0):
        #  Main loop, starts the battle
        alpha = text.render(alphatext, False, (255, 255, 0))
        self.battling = True
        self.monster_flag = True
        self.draw_menu = True
        self.add_flag = False
        self.get_monster_details(monster_name)
        self.get_player_details(player_data)
        self.play_sound('encounter')
        self.set_instance(player_data)
        fadein(255)
        if set_music == 0:
            pygame.mixer_music.load("data/sounds&music/03_Endless_Battle.ogg")
            pygame.mixer_music.set_volume(vol)
            pygame.mixer_music.play()
        elif set_music == 1:
            pygame.mixer_music.load("data/sounds&music/boss_music.mp3")
            pygame.mixer_music.set_volume(vol)
            pygame.mixer_music.play()
        elif set_music == 2:
            pygame.mixer_music.load("data/sounds&music/Dungeon2.ogg")
            pygame.mixer_music.set_volume(vol)
            pygame.mixer_music.play()
        elif set_music == 3:
            pygame.mixer_music.load("data/sounds&music/2000_Thief.ogg")
            pygame.mixer_music.set_volume(vol)
            pygame.mixer_music.play()
        else:
            pygame.mixer_music.load("data/sounds&music/03_Endless_Battle.ogg")
            pygame.mixer_music.set_volume(vol)
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
            if self.shake:  # Shakes the screen when set to True
                self.shake_screen()
            if not self.shake:  # To reset the screen back to its initial position
                self.camera_x, self.camera_y = 0, 0
            if self.focus:
                self.focus_cam(self.focus_target)
            if self.move_flag:
                self.move_to(self.move_target, self.target_pos)
            self.draw_alertbox()
            if self.player_dmg_flag:
                surf.blit(self.dmg_txt, (self.player_pos, 270))
                if self.crit_chance == 10:
                    surf.blit(self.crit_text, (self.player_pos, 240))
            if self.healthbar_flag:
                surf.blit(self.dmg_txt, (self.monster_pos, self.monster_y - 40))
                if self.crit_chance == 10:
                    surf.blit(self.crit_text,
                              (self.monster_pos, self.monster_y - 70))
                if self.element in self.m_weakness:
                    surf.blit(self.weak_text,
                              (self.monster_pos, self.monster_y - 70))
                elif self.element in self.m_strengths:
                    surf.blit(self.strong_text,
                              (self.monster_pos, self.monster_y - 70))
                self.draw_healthbar(self.m_cur_health)
            self.update_status_effects()
            self.play_sequence(self.sequence_to_play, self.sequence_target)
            self.check_state(player_data)  # To check the current game state
            self.check_inputs()
            surf.blit(alpha, (0, 0))
            screen.blit(surf, (self.camera_x, self.camera_y))
            pygame.display.update()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)


drawui = True  # Flag to signify whether to draw the ui or not,


# used to hide ui during dialogue or any other scenes(the main UI during which the player has control outside of battle)


class MainUi:
    """The Main UI of the game(outside of battle.)"""

    def __init__(self):
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

    def arena(self, floor=1):  # Main ui in the arena
        surf.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))
        surf.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 48))
        surf.blit(pygame.transform.scale(self.bg, (300, 300)), (905, 430))
        surf.blit(self.talktxt, (946, 496))
        surf.blit(self.battxt, (946, 526))
        surf.blit(self.stattxt, (946, 556))
        surf.blit(self.shoptxt, (946, 586))
        surf.blit(self.inntxt, (946, 616))
        surf.blit(self.systxt, (946, 646))
        self.cur = self.uitext.render(
            'Floor:  %d' % floor, False, self.txtcolor)  # Current floor
        surf.blit(self.cur, (27, 61))
        if self.cursorpos == 0:
            surf.blit(self.cursor, (916, 496))
            surf.blit(self.talkdesc, (112, 490))
        if self.cursorpos == 1:
            surf.blit(self.cursor, (916, 526))
            surf.blit(self.batdesc, (112, 490))
        if self.cursorpos == 2:
            surf.blit(self.cursor, (916, 556))
            surf.blit(self.statdesc, (112, 490))
        if self.cursorpos == 3:
            surf.blit(self.cursor, (916, 586))
            surf.blit(self.shopdesc, (112, 490))
        if self.cursorpos == 4:
            surf.blit(self.cursor, (916, 616))
            surf.blit(self.inndesc, (112, 490))
        if self.cursorpos == 5:
            surf.blit(self.cursor, (916, 646))
            surf.blit(self.sysdesc, (112, 490))

    def clock(self, hours, minutes):  # draw ui for the clock
        if minutes == 0:
            minutes = '00'  # Double zeros because that's how clocks work
        timetxt = str(hours) + ':' + str(minutes)
        self.time = self.uitext.render(timetxt, False, self.txtcolor)
        surf.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 81))
        surf.blit(self.time, (27, 94))
        if hours >= 6 and hours < 14:  # Day
            surf.blit(pygame.transform.scale(self.sunIcon, (40, 30)), (90, 93))
        if hours >= 14 and hours < 20:  # Afternoon
            surf.blit(pygame.transform.scale(self.eveIcon, (20, 30)), (90, 93))
        if hours >= 20 or hours < 6:  # Night
            surf.blit(pygame.transform.scale(
                self.moonIcon, (35, 25)), (90, 97))

    def talk(self, val):
        global drawui
        drawui = False
        self.Talk = val
        if not self.talked:
            if player.progress == 1:
                self.cur_dialogue = [[]]  # These are converted from the old textbox, so for compatibility
                if self.Talk == 0:
                    self.txtbox.draw_textbox([["data/sprites/oldman.png", 'Old Man',
                                             'I heard the monsters on the first floor are quite weak. You mustn\'t underestimate them However!\nConsider Equipping yourself with new equipment from the Shop.',
                                               ]], surf, (0, 400))
                elif self.Talk == 1:

                    self.txtbox.draw_textbox(
                        [["data/sprites/boy.png", 'Boy', 'Wow mister, you\'re going to fight in the Arena? So cool!']], surf, (0, 400))

                elif self.Talk == 2:

                    self.txtbox.draw_textbox([["data/sprites/youngman.png", 'Young Man',
                                             'In the 50 years that the Arena has been open, there has been only one winner. It was the legendary Hero known as Zen. That was 2 years ago though, nobody has seen him since.']], surf, (0, 400))
                elif self.Talk == 3:
                    self.txtbox.draw_textbox([["data/sprites/mysteryman.png", 'Stranger',
                                             'You...\nNevermind. Good luck in the Arena, I\'ll be keeping an eye on you.']], surf, (0, 400))
            elif player.progress == 2:
                if self.Talk == 0:
                    self.cur_dialogue = dialogues["floor2_oldman"]
                    self.txtbox.draw_textbox(self.cur_dialogue, surf, (0, 400))
                elif self.Talk == 1:
                    self.cur_dialogue = dialogues["floor2_boy"]
                    self.txtbox.draw_textbox(self.cur_dialogue, surf, (0, 400))
                elif self.Talk == 2:
                    if player.pclass == "mage":
                        self.cur_dialogue = dialogues["floor2_youngman_m"]
                    else:
                        self.cur_dialogue = dialogues["floor2_youngman_w"]
                    self.txtbox.draw_textbox(self.cur_dialogue, surf, (0, 400))
                elif self.Talk == 3:
                    self.cur_dialogue = dialogues["floor2_noble"]
                    self.txtbox.draw_textbox(self.cur_dialogue, surf, (0, 400))


    def status(self, player, item_data=item_data):
        surf.blit(self.status_bg, (53, 30))
        nametxt = self.uitext.render(
            'Name: ' + player.name, False, self.txtcolor)
        surf.blit(nametxt, (169, 207))
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
        surf.blit(stat_points, (430, 247))
        surf.blit(strtxt, (169, 247))
        surf.blit(strtxt2, (299, 247))
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
        surf.blit(deftxt, (169, 287))
        surf.blit(deftxt2, (299, 287))
        lucktxt = self.uitext.render(
            'LUCK: %d' % player.luck, False, self.txtcolor)
        surf.blit(lucktxt, (169, 367))
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
        surf.blit(magtxt, (169, 327))
        surf.blit(magtxt2, (299, 327))
        lvltxt = self.uitext.render('Level: %d' %
                                    player.level, False, self.txtcolor2)
        surf.blit(lvltxt, (607, 396))
        xp_txt = self.uitext2.render('Exp till next level: {}'.format(
            player.xp_till_levelup(player.level) - player.exp), False, self.txtcolor2)
        surf.blit(xp_txt, (607, 426))
        surf.blit(self.face, (679, 207))
        classtxt = self.uitext.render(
            player.pclass.capitalize(), False, self.txtcolor)
        surf.blit(classtxt, (697, 366))
        surf.blit(self.statustxt, (417, 141))
        weptxt = self.uitext2.render(
            'WEAPON: ' + item_data['weapons'][player.cur_weapon]['name'], False, self.txtcolor2)
        armtxt = self.uitext2.render(
            'ARMOR: ' + item_data['armours'][player.cur_armour]['name'], False, self.txtcolor2)
        acctxt = self.uitext2.render('ACCESSORY: ' + item_data['accessories'][player.cur_accessory]['name'], False,
                                     self.txtcolor2)
        surf.blit(self.wepicon, (169, 407))
        surf.blit(weptxt, (209, 407))
        surf.blit(self.armicon, (169, 447))
        surf.blit(armtxt, (209, 447))
        surf.blit(self.accicon, (169, 487))
        surf.blit(acctxt, (209, 487))
        floorktxt = self.uitext.render(
            'Enemies killed on this floor: %d' % player.fkills, False, self.txtcolor3)
        totktxt = self.uitext.render(
            'Total enemies killed: %d' % player.tkills, False, self.txtcolor3)
        surf.blit(floorktxt, (169, 527))
        surf.blit(totktxt, (168, 567))
        self.status_menu(player)
        self.txtbox.popup_message(self.popup_message, surf)

    def change_equipment(self, player=Player(), item_data=item_data):
        surf.blit(self.equip_menu_bg, (self.window_x, 45))
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
                        for weapon in item_data['weapons']:
                            if weapon['id'] == player.wep_owned[i]:
                                surf.blit(self.uitext.render(
                                    weapon['name'], False, self.txtcolor), (980, 110 + 55 * (i - self.min_pos)))
                self.cur_id = player.wep_owned[self.min_pos +
                                               self.equip_cursor2_pos]
                if self.min_pos != 0:
                    surf.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    surf.blit(self.cursor_down, (1085, 360))

            else:
                no_item = True
                self.item_desc = ''
                surf.blit(self.uitext.render("No weapons owned",
                          False, self.txtcolor), (980, 110))
        elif self.equip_cursor1_pos == 1:
            self.max_pos = len(player.arm_owned)
            if len(player.arm_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        for armour in item_data['armours']:
                            if armour['id'] == player.arm_owned[i]:
                                surf.blit(self.uitext.render(
                                    armour['name'], False, self.txtcolor), (980, 110 + 55 * (i - self.min_pos)))
                self.cur_id = player.arm_owned[self.min_pos +
                                               self.equip_cursor2_pos]
                if self.min_pos != 0:
                    surf.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    surf.blit(self.cursor_down, (1085, 360))
            else:
                no_item = True
                surf.blit(self.uitext.render("No armours owned",
                          False, self.txtcolor), (980, 110))
        elif self.equip_cursor1_pos == 2:
            self.max_pos = len(player.acc_owned)
            if len(player.acc_owned) > 0:
                no_item = False
                for i in range(self.min_pos, self.max_pos):
                    if i <= self.min_pos + 4:
                        for acc in item_data['accessories']:
                            if acc['id'] == player.acc_owned[i]:
                                surf.blit(self.uitext.render(
                                    acc['name'], False, self.txtcolor), (980, 110 + 55 * (i - self.min_pos)))
                self.cur_id = player.acc_owned[self.min_pos +
                                               self.equip_cursor2_pos]
                if self.min_pos != 0:
                    surf.blit(self.cursor_up, (1085, 80))
                elif self.min_pos + 5 < self.max_pos:
                    surf.blit(self.cursor_down, (1085, 360))
            else:
                no_item = True
                self.item_desc = ''
                surf.blit(self.uitext.render("No accessories owned",
                          False, self.txtcolor), (980, 110))
        if self.equip_flag2:
            if self.equip_cursor2_pos == 0:
                surf.blit(self.cursor, (940, 110))
            elif self.equip_cursor2_pos == 1:
                surf.blit(self.cursor, (940, 170))
            elif self.equip_cursor2_pos == 2:
                surf.blit(self.cursor, (940, 225))
            elif self.equip_cursor2_pos == 3:
                surf.blit(self.cursor, (940, 280))
            elif self.equip_cursor2_pos == 4:
                surf.blit(self.cursor, (940, 335))
            if self.equip_cursor1_pos == 0:
                cur_desc = item_data["weapons"]
            elif self.equip_cursor1_pos == 1:
                cur_desc = item_data["armours"]
            elif self.equip_cursor1_pos == 2:
                cur_desc = item_data["accessories"]
            if not no_item:
                self.item_desc = self.uitext2.render(
                    cur_desc[self.cur_id]["description"], False, self.txtcolor2)
                hover_item_str = self.uitext2.render(
                    "STR:" + str(cur_desc[self.cur_id]["atk"]), False, self.txtcolor2)
                hover_item_def = self.uitext2.render(
                    "DEF:" + str(cur_desc[self.cur_id]["def"]), False, self.txtcolor2)
                hover_item_mag = self.uitext2.render(
                    "MAG:" + str(cur_desc[self.cur_id]["mag"]), False, self.txtcolor2)
                surf.blit(self.item_desc, (120, 620))
                surf.blit(hover_item_str, (605, 500))
                surf.blit(hover_item_def, (605, 540))
                surf.blit(hover_item_mag, (605, 580))

    def stat_point_alloc(self, player=Player()):
        if self.stat_cursor_pos == 0:
            surf.blit(self.cursor, (255, 250))
            surf.blit(self.cursor_left, (135, 247))
        elif self.stat_cursor_pos == 1:
            surf.blit(self.cursor, (255, 290))
            surf.blit(self.cursor_left, (135, 287))
        elif self.stat_cursor_pos == 2:
            surf.blit(self.cursor, (265, 330))
            surf.blit(self.cursor_left, (135, 327))
        if self.stat_cursor_pos > 2:
            self.stat_cursor_pos = 0
        elif self.stat_cursor_pos < 0:
            self.stat_cursor_pos = 2
        if self.confirm:
            self.txtbox.confirm_box('Confirm Changes?', surf)

    def status_menu(self, player=Player()):
        surf.blit(self.status_menu_bg, (955, 405))
        surf.blit(self.equip_txt, (990, 465))
        surf.blit(self.stats_txt, (990, 505))
        surf.blit(self.back_txt, (990, 545))
        if self.status_cur_pos == 0:
            surf.blit(self.cursor, (950, 465))
        elif self.status_cur_pos == 1:
            surf.blit(self.cursor, (950, 505))
        elif self.status_cur_pos == 2:
            surf.blit(self.cursor, (950, 545))
        if self.equip_flag1:
            if self.equip_cursor1_pos == 0:
                surf.blit(self.cursor, (140, 410))
            elif self.equip_cursor1_pos == 1:
                surf.blit(self.cursor, (140, 450))
            elif self.equip_cursor1_pos == 2:
                surf.blit(self.cursor, (140, 490))
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

    def handle_status_inputs(self, player=Player()):
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
        surf.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 2.7), int(curheight / 3))), (470, 200))
        surf.blit(self.sysopt1, (528, 259))
        surf.blit(self.sysopt2, (528, 299))
        surf.blit(self.sysopt3, (528, 339))
        if self.syscursorpos == 0:
            surf.blit(self.cursor, (498, 259))
        if self.syscursorpos == 1:
            surf.blit(self.cursor, (498, 299))
        if self.syscursorpos == 2:
            surf.blit(self.cursor, (498, 339))
        if self.syscursorpos > 2:
            self.syscursorpos = 0
        if self.syscursorpos < 0:
            self.syscursorpos = 2

    def battle_choice(self, monkill):
        if self.battalk:
            montokill = 5 - monkill
            if monkill < 5:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'You have %d monter(s) left to kill. You\'re almost there!' % montokill]], surf, (0, 400))
            if monkill >= 5:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'You can challenge the floor boss! Are you prepared for it?']], surf, (0, 400))

        if not self.battalk:
            if monkill >= 5:
                self.batopt2 = self.uitext.render(
                    'Challenge the floor boss', False, self.txtcolor)
            elif monkill < 5:
                self.batopt2 = self.uitext.render(
                    'Challenge the floor boss', False, (105, 109, 114))
            surf.blit(pygame.transform.scale(
                self.bg, (int(curwidth / 2.7), int(curheight / 3))), (470, 200))
            surf.blit(self.batopt1, (528, 259))
            surf.blit(self.batopt2, (528, 299))
            surf.blit(self.sysopt3, (528, 339))
            if self.batcursorpos == 0:
                surf.blit(self.cursor, (498, 259))
            if self.batcursorpos == 1:
                surf.blit(self.cursor, (498, 299))
            if self.batcursorpos == 2:
                surf.blit(self.cursor, (498, 339))
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
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                   'That was a good battle! If you\'re injured make sure to rest up at the inn.'
                                     ]], surf, (0, 400))
        elif self.pbtalk == 1 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                   'Good job! Make sure to use the gold from your battle to buy equipment from our Shop!']], surf, (0, 400))
        elif self.pbtalk == 2 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                   'Nice work! You\'re pretty skilled, are you sure you haven\'t done this before?'
                                     ]], surf, (0, 400))
        elif self.pbtalk == 3 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     'Good work out there! I overheard some strange people talking about you. Something about.. A debt?']], surf, (0, 400))
        if self.pbtalk == 0 and progress == 2:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "Good work! Maybe I should bet some money on you next time, huh? *laughs*"
                                     ]], surf, (0, 400))
        elif self.pbtalk == 1 and progress == 2:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "... Oh you're already done? Good job, sorry about that I was a bit lost in my own thoughts!"]], surf, (0, 400))
        elif self.pbtalk == 2 and progress == 2:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "Great job! How'd you get so strong? What's your secret?"
                                     ]], surf, (0, 400))
        elif self.pbtalk == 3 and progress == 2:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                     "If you would like to get stronger, don't forget to buy new equipment! Or just keep killing these monsters for experience!"]], surf, (0, 400))

    def draw_inn(self, gold):
        surf.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        surf.blit(pygame.transform.scale(
            self.bg, (170, 50)), (10, 48))  # Gold box
        surf.blit(pygame.transform.scale(self.bg, (300, 300)),
                  (905, 430))  # Actions box
        surf.blit(self.talktxt, (946, 496))
        surf.blit(self.sleeptxt, (946, 526))
        surf.blit(self.backtxt, (946, 556))
        # Current gold with the player
        self.cur = self.uitext2.render(
            'Gold:  %d' % gold, False, self.txtcolor)
        self.coinAnim.blit(surf, (22, 62))  # Gold icon
        surf.blit(self.cur, (47, 62))
        if self.cursorpos == 0:
            surf.blit(self.cursor, (916, 496))
            surf.blit(self.talkdesc2, (112, 490))
        if self.cursorpos == 1:
            surf.blit(self.cursor, (916, 526))
            surf.blit(self.sleepdesc, (112, 490))
        if self.cursorpos == 2:
            surf.blit(self.cursor, (916, 556))
            surf.blit(self.backdesc, (112, 490))

    def draw_town(self, player):
        surf.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        surf.blit(pygame.transform.scale(
            self.bg, (170, 50)), (10, 29))  # Gold box
        surf.blit(pygame.transform.scale(self.bg, (300, 300)),
                  (905, 430))  # Actions box
        surf.blit(self.talktxt, (946, 496))
        surf.blit(self.inntxt, (946, 526))
        surf.blit(self.slumstxt, (946, 556))
        surf.blit(self.backtxt, (946, 586))
        # Current gold with the player
        gold = self.uitext2.render('Gold:  %d' %
                                   player.gold, False, self.txtcolor)
        self.coinAnim.blit(surf, (22, 45))  # Gold icon
        surf.blit(gold, (47, 45))
        if self.cursorpos == 0:
            surf.blit(self.cursor, (916, 496))
            surf.blit(self.talkdesc3, (112, 490))
        elif self.cursorpos == 1:
            surf.blit(self.cursor, (916, 526))
            surf.blit(self.inndesc, (112, 490))
        elif self.cursorpos == 2:
            surf.blit(self.cursor, (916, 556))
            surf.blit(self.slumsdesc, (112, 490))
        elif self.cursorpos == 3:
            surf.blit(self.cursor, (916, 586))
            surf.blit(self.backdesc, (112, 490))
        elif self.cursorpos > 3:
            self.cursorpos = 0
        elif self.cursorpos < 0:
            self.cursorpos = 3
        self.clock(player.hours, player.minutes)

    def draw_casino(self, player):  # Draws the casino UI
        surf.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        surf.blit(pygame.transform.scale(
            self.bg, (170, 50)), (10, 29))  # Gold box
        surf.blit(pygame.transform.scale(self.bg, (300, 300)),
                  (905, 430))  # Actions box
        surf.blit(self.talktxt, (946, 496))
        surf.blit(self.sleeptxt, (946, 526))
        surf.blit(self.casino_text, (946, 556))
        surf.blit(self.backtxt, (946, 586))
        # Current gold with the player
        gold = self.uitext2.render('Gold:  %d' %
                                   player.gold, False, self.txtcolor)
        self.coinAnim.blit(surf, (22, 45))  # Gold icon
        surf.blit(gold, (47, 45))
        if self.cursorpos == 0:
            surf.blit(self.cursor, (916, 496))
            surf.blit(self.talkdesc3, (112, 490))
        elif self.cursorpos == 1:
            surf.blit(self.cursor, (916, 526))
            surf.blit(self.inndesc, (112, 490))
        elif self.cursorpos == 2:
            surf.blit(self.cursor, (916, 556))
            surf.blit(self.casino_desc, (112, 490))
        elif self.cursorpos == 3:
            surf.blit(self.cursor, (916, 586))
            surf.blit(self.backdesc, (112, 490))
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
            [("data/sprites/alert1.png", 0.4), ("data/sprites/alert2.png", 0.4)])
        self.alertAnim.scale([35, 35])
        self.alertAnim.play()

    def drawUi(self, no=1, opt1='1', opt2='2', opt3='3', opt4='4', opt5='5',
               opt6='6'):  # Select option among 6 or fewer choices,where no is the number of choices
        surf.blit(pygame.transform.scale(
            self.bg, (int(curwidth / 1.5), 300)), (0, 430))
        Option1 = self.uitext.render(opt1, False, self.txtcolor)
        Option2 = self.uitext.render(opt2, False, self.txtcolor)
        Option3 = self.uitext.render(opt3, False, self.txtcolor)
        Option4 = self.uitext.render(opt4, False, self.txtcolor)
        Option5 = self.uitext.render(opt5, False, self.txtcolor)
        Option6 = self.uitext.render(opt6, False, self.txtcolor)
        backTxt = self.uitext.render('Back', False, self.txtcolor)
        surf.blit(Option1, (80, 490))  # Row 1
        if self.alert1:  # If the option is new/updated show alert.
            self.alertAnim.blit(surf, (80 + Option1.get_width(), 490))
        if no >= 2:
            surf.blit(Option2, (280, 490))
            if self.alert2:
                self.alertAnim.blit(surf, (280 + Option2.get_width(), 490))
            if no >= 3:
                surf.blit(Option3, (480, 490))
                if self.alert3:
                    self.alertAnim.blit(surf, (480 + Option3.get_width(), 490))
                if no >= 4:
                    surf.blit(Option4, (80, 590))  # Row 2
                    if self.alert4:
                        self.alertAnim.blit(
                            surf, (80 + Option4.get_width(), 590))
                    if no >= 5:
                        surf.blit(Option5, (280, 590))
                        if self.alert5:
                            self.alertAnim.blit(
                                surf, (280 + Option5.get_width(), 590))
                        if no >= 6:
                            surf.blit(Option6, (480, 590))
                            if self.alert6:
                                self.alertAnim.blit(
                                    surf, (480 + Option6.get_width(), 590))
        surf.blit(backTxt, (680, 590))  # Exit
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
            surf.blit(self.cursor, (50, 490))
        if self.rowpos == 0 and self.colpos == 1:  # Option 2
            surf.blit(self.cursor, (250, 490))
        if self.rowpos == 0 and self.colpos == 2:  # Option 3
            surf.blit(self.cursor, (450, 490))
        if self.rowpos == 1 and self.colpos == 0:  # Option 4
            surf.blit(self.cursor, (50, 590))
        if self.rowpos == 1 and self.colpos == 1:  # Option 5
            surf.blit(self.cursor, (250, 590))
        if self.rowpos == 1 and self.colpos == 2:  # Option 6
            surf.blit(self.cursor, (450, 590))
        if self.rowpos == 1 and self.colpos == 3:  # Back
            surf.blit(self.cursor, (650, 590))

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
        self.weapons_list = item_data['weapons']
        self.armour_list = item_data['armours']
        self.acc_list = item_data['accessories']
        self.consume_list = item_data['consumables']
        self.player_data = Player()
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
            surf.blit(item_desc, (120, 660))
            if self.min_pos != 0:
                surf.blit(self.cursor_up, (212, 303))
            if self.min_pos + 5 != self.max_pos:
                # Downward facing arrow to show that more items are available
                surf.blit(self.cursor_down, (212, 623))
        else:
            if not self.status_anim:
                self.box_pos = 2000
                self.status_anim = True
            if self.status_anim:
                if self.box_pos > 950:
                    self.box_pos -= 50

            surf.blit(self.status_bg, (self.box_pos, 222))
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
                    surf.blit(str_diftxt, (1120, 300))
                else:
                    str_diftxt = self.uitext.render(
                        '(' + str(str_dif) + ')', False, self.red_rgb)
                    surf.blit(str_diftxt, (1120, 300))
                if def_dif >= 0:
                    def_diftxt = self.uitext.render(
                        '(+' + str(def_dif) + ')', False, self.green_rgb)
                    surf.blit(def_diftxt, (1120, 370))
                else:
                    def_diftxt = self.uitext.render(
                        '(' + str(def_dif) + ')', False, self.red_rgb)
                    surf.blit(def_diftxt, (1120, 370))
                if mag_dif >= 0:
                    mag_diftxt = self.uitext.render(
                        '(+' + str(mag_dif) + ')', False, self.green_rgb)
                    surf.blit(mag_diftxt, (1120, 440))
                else:
                    mag_diftxt = self.uitext.render(
                        '(' + str(mag_dif) + ')', False, self.red_rgb)
                    surf.blit(mag_diftxt, (1120, 440))
                if self.min_pos + 5 != self.max_pos:
                    # Downward facing arrow to show that more items are available
                    surf.blit(self.cursor_down, (212, 623))
                if self.min_pos != 0:
                    surf.blit(self.cursor_up, (212, 303))
                surf.blit(item_desc, (120, 660))
                surf.blit(str_txt, (1000, 300))
                surf.blit(def_txt, (1000, 370))
                surf.blit(mag_txt, (1000, 440))
                surf.blit(luk_txt, (1000, 510))

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

    def draw_shop(self, shop_name='', player_data=Player()):
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
                                     'Welcome to the Arena shop! How can I help you?']], surf, (0, 400))
        if not self.shopkeep:
            surf.blit(self.shopbg, (53, 30))
            surf.blit(shop_title, (360, 57))
            surf.blit(self.uitext.render(
                self.shoptxt[0], False, self.txtcolor3), (shop_text_pos, 150))
            surf.blit(self.uitext.render(
                self.shoptxt[1], False, self.txtcolor3), (shop_text_pos + 150, 150))
            surf.blit(self.uitext.render(
                self.shoptxt[2], False, self.txtcolor3), (shop_text_pos + 300, 150))
            surf.blit(self.uitext.render(
                self.shoptxt[3], False, self.txtcolor3), (shop_text_pos + 510, 150))
            surf.blit(self.uitext2.render(
                self.shoptxt2[0], False, (186, 31, 34)), (161, 290))
            surf.blit(self.uitext2.render(
                self.shoptxt2[1], True, (186, 31, 34)), (449, 290))
            surf.blit(pygame.transform.scale(self.bg, (170, 50)),
                      (925, 42))  # Gold box 10,48
            self.cur = self.uitext2.render('Gold:  %d' % player_data.gold, False,
                                           self.txtcolor)  # Current gold with the player
            self.coinAnim.blit(surf, (937, 56))  # Gold icon
            surf.blit(self.cur, (962, 56))
            if self.shop_page == 0:
                self.max_pos = len(self.weapons_list)
                if self.min_pos in player_data.wep_owned or self.min_pos == self.player_data.cur_weapon:
                    item1 = self.uitext.render(
                        wepnamelist[self.min_pos], False, (86, 91, 99))
                    cost1 = self.uitext.render(
                        wepcostlist[self.min_pos], False, (86, 91, 99))
                    surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
                            "Owned", False, (186, 31, 34)), (600, 579))
                    else:
                        item5 = self.uitext.render(
                            wepnamelist[self.min_pos + 4], False, self.txtcolor3)
                        cost5 = self.uitext.render(
                            wepcostlist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 1:
                self.max_pos = len(self.armour_list)
                if self.min_pos in player_data.arm_owned or self.min_pos == self.player_data.cur_armour:
                    item1 = self.uitext.render(
                        armnamelist[self.min_pos], False, (86, 91, 99))
                    cost1 = self.uitext.render(
                        armcostlist[self.min_pos], False, (86, 91, 99))
                    surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
                            "Owned", False, (186, 31, 34)), (600, 579))
                    else:
                        item5 = self.uitext.render(
                            armnamelist[self.min_pos + 4], False, self.txtcolor3)
                        cost5 = self.uitext.render(
                            armcostlist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 2:
                self.max_pos = len(self.acc_list)
                if self.min_pos in player_data.acc_owned or self.min_pos == self.player_data.cur_accessory:
                    item1 = self.uitext.render(
                        accnamelist[self.min_pos], False, (86, 91, 99))
                    cost1 = self.uitext.render(
                        acccostlist[self.min_pos], False, (86, 91, 99))
                    surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
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
                        surf.blit(self.uitext2.render(
                            "Owned", False, (186, 31, 34)), (600, 579))
                    else:
                        item5 = self.uitext.render(
                            accnamelist[self.min_pos + 4], False, self.txtcolor3)
                        cost5 = self.uitext.render(
                            acccostlist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 3:
                surf.blit(self.uitext2.render("In Inventory",
                          False, (186, 31, 34)), (590, 290))
                self.max_pos = len(self.consume_list)
                item1 = self.uitext.render(
                    connamelist[self.min_pos], False, self.txtcolor3)
                cost1 = self.uitext.render(
                    concostlist[self.min_pos], False, self.txtcolor3)
                for i in range(self.min_pos, self.max_pos):
                    for item in self.player_data.inventory:
                        if item["name"] == connamelist[i] and i <= self.min_pos + 4:
                            surf.blit(self.uitext2.render(
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

            surf.blit(item1, (161, 339))
            surf.blit(cost1, (449, 339))

            if self.max_pos >= 2:
                surf.blit(item2, (161, 399))
                surf.blit(cost2, (449, 399))

            if self.max_pos >= 3:
                surf.blit(item3, (161, 459))
                surf.blit(cost3, (449, 459))

            if self.max_pos >= 4:
                surf.blit(item4, (161, 519))
                surf.blit(cost4, (449, 519))

            if self.max_pos >= 5:
                surf.blit(item5, (161, 579))
                surf.blit(cost5, (449, 579))

            if self.shop_selection_flag:  # while using cursor 1
                self.min_pos = 0
                self.shop_cursor_pos2 = 0
                self.status_anim = False
                if self.shop_cursor_pos1 == 0:
                    surf.blit(self.cursor, (shop_text_pos - 35, 150))
                    self.shop_page = 0
                    self.current_list = self.weapons_list
                if self.shop_cursor_pos1 == 1:
                    surf.blit(self.cursor, (shop_text_pos + 150 - 35, 150))
                    self.shop_page = 1
                    self.current_list = self.armour_list
                if self.shop_cursor_pos1 == 2:
                    surf.blit(self.cursor, (shop_text_pos + 300 - 35, 150))
                    self.shop_page = 2
                    self.current_list = self.acc_list
                if self.shop_cursor_pos1 == 3:
                    surf.blit(self.cursor, (shop_text_pos + 510 - 35, 150))
                    self.shop_page = 3
                    self.current_list = self.consume_list
                if self.shop_cursor_pos1 > 3:
                    self.shop_cursor_pos1 = 0
                elif self.shop_cursor_pos1 < 0:
                    self.shop_cursor_pos1 = 3
            if not self.shop_selection_flag:  # while using cursor 2
                if self.shop_cursor_pos2 == 0:
                    surf.blit(self.cursor, (120, 339))
                elif self.shop_cursor_pos2 == 1:
                    surf.blit(self.cursor, (120, 399))
                elif self.shop_cursor_pos2 == 2:
                    surf.blit(self.cursor, (120, 459))
                elif self.shop_cursor_pos2 == 3:
                    surf.blit(self.cursor, (120, 519))
                elif self.shop_cursor_pos2 == 4:
                    surf.blit(self.cursor, (120, 579))
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
            self.txtbox.popup_message(self.popup_message, surf)


class GameEvents(MainUi):
    """Class for all special events in the game."""

    def __init__(self):
        MainUi.__init__(self)
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
        self.option_selector = SelectOptions()
        self.town_talk1 = False  # Flag for drawing options menu for the 'Talk' Screen
        self.text_box = gameui.TextBox()
        self.ui_text = gameui.UiText()
        self.ui_text.main_font_colour = (255, 255, 255)
        self.casino_state = ''  # Current state of the casino

    def town_first_visit(self, player_data):
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Bustling_Streets.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        global surf
        global screen
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
            curwidth, curheight = screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    global done
                    done = True
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

            surf.blit(pygame.transform.scale(
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
                                         '''The town that the Arena is situated in gets very lively this time of the year as this is when most of the challengers arrive.''']], surf)
            elif self.townDialogue == 2:
                self.txtbox.draw_textbox([['', '',
                                         """You\'ve been here before but never really got the chance to look around, so the sights of this place are still very unfamiliar to you."""]], surf
                                         )
            elif self.townDialogue == 3:
                self.txtbox.draw_textbox([['', '',
                                         'Even if you had been familiar with this place in the past, It would still have been difficult finding your way through this place as the town has changed dramatically over the course of a few years.']], surf)
            elif self.townDialogue == 4:
                self.txtbox.draw_textbox([['', '',
                                         '''This is mostly due to the overwhelming popularity of the arena which has brought visitors from all over the country to this one location. This has let the town flourish and expand at a very quick pace, with new buildings and stores being built seemingly everyday.''']], surf
                                         )
            elif self.townDialogue == 5:
                self.txtbox.draw_textbox([['', '',
                                         '''The presence and influence of the arena played a major role in the growth of the town, so much so that the people of the town decided to change it\'s old name and give it a new more fitting name, \"Arena Town\".''']], surf
                                         )
            elif self.townDialogue == 6:
                runningsound.play()
                self.timekeep.reset()
                self.townDialogue += 1
                self.dialoguecontrol = False
            elif self.townDialogue == 7 and timedflag1:
                self.dialoguecontrol = True
                self.txtbox.draw_textbox([['', '',
                                         'You see a young girl running towards your direction.']], surf
                                         )
            elif self.townDialogue == 8:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'Oh no, I\'m so late, Grandpa\'s gonna get so mad!']], surf
                                         )
                timedflag1 = False

            elif self.townDialogue == 9:
                self.thudSound.play()
                self.townDialogue += 1
                self.dialoguecontrol = False
                self.timekeep.reset()
            elif self.townDialogue == 10 and timedflag1:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'Ouch!']], surf
                                         )
                self.dialoguecontrol = True
            elif self.townDialogue == 11:
                self.txtbox.draw_textbox([['', '',
                                         'The girl crashes into you at full speed and topples over onto the gravel road.']], surf
                                         )
            elif self.townDialogue == 12:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'Hey, watch where you\'re going!']], surf
                                         )

            elif self.townDialogue == 13:
                self.txtbox.draw_textbox([['', '',
                                         'The girl gets up and brushes off her skirt.']], surf
                                         )
            elif self.townDialogue == 14:
                self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                         'There\'s a tear in my new dress! What are you going to do about this?']], surf
                                         )
                choice_select = True
                self.txtbox.choice_flag = True
            elif self.townDialogue == 15:
                self.txtbox.draw_textbox([['', '',
                                         'What do you do?']], surf
                                         )
                self.txtbox.select_choice(
                    ['Offer to pay her money', 'Ignore her and walk away'], surf)
                self.dialoguecontrol = False
            elif dialogue_choice == 0 and self.townDialogue >= 16:  # Pay money dialogue tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                             'Oh you\'re willing to pay? I\'m going to need atleast 150 gold for the dress.']], surf
                                             )
                    choice_select = True
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox([['', '',
                                             'Pay 150 gold?']], surf
                                             )
                    self.txtbox.select_choice(['Pay her', 'Don\'t Pay'], surf)
                    self.dialoguecontrol = False
                elif self.townDialogue >= 18 and dialogue_choice2 == 0:  # Pay her
                    if player_data.gold < 150 and not paid_girl:  # if player doesn't have enough gold
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'Hey you don\'t even have enough gold to pay me!']]), surf
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'Don\'t waste my time if you don\'t have any money!']]), surf
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
                                                     'Well, I guess this will have to do.']], surf)
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                     'You better be careful next time! Be grateful that I let you off easily!']], surf)
                        elif self.townDialogue == 20:
                            self.txtbox.draw_textbox([['', '',
                                                     '''The girl walks away after glaring at you in the eye. You could have sworn you saw a smile for a second.''']], surf)
                        elif self.townDialogue == 21:
                            self.txtbox.draw_textbox([['', '',
                                                     'The girl disappears into the crowd.']], surf)

                elif self.townDialogue >= 18 and dialogue_choice2 == 1:  # Don't pay her
                    if self.townDialogue == 18:
                        self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                 '...You\'re not going to pay?']], surf)
                    if self.townDialogue == 19:
                        self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                 'Tch.. he didn\'t fall for it']], surf)
                    elif self.townDialogue == 20:
                        self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                                 'Well don\'t waste my time then, get out of my way!']], surf)
                    elif self.townDialogue == 21:
                        self.txtbox.draw_textbox([['', '',
                                                 'The girl storms off and disappears into the crowd.']], surf)
            elif dialogue_choice == 1 and self.townDialogue >= 16:  # ignore girl tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                             '....']], surf
                                             )
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox([["data/sprites/girl.png", '???',
                                             'Don\'t just ignore me!']], surf)
                elif self.townDialogue == 18:
                    self.txtbox.draw_textbox([['', '',
                                             '''You continue ignoring the girl while she makes a commotion in the middle of the street and proceed to the Town.''']], surf)
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
            screen.blit(surf, (0, 0))
            self.timekeep.timing()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def firstfloor_boss(self, name='Zen'):
        # Cutscene when challenging the first_floor boss
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Dungeon3.ogg')
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
            curwidth, curheight = screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    global done
                    done = True
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

            surf.blit(self.arena_bg, (0, 0))
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
                                         'Ladies and gentlemen!']], surf
                                         )

            elif self.arenaDialogue == 2:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'It seems like it\'s been ages since we\'ve had a challenger strong enough to finally get to this point!']], surf
                                         )
            elif self.arenaDialogue == 3:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'But we finally have him here, someone who is both brave and foolish enough to step up and fight his way through some of the most powerful monsters, to be able to stand before you at this very moment and face against what many would consider suicide! ']], surf
                                         )
            elif self.arenaDialogue == 4:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'Please put your hands together for.. ' + name + '!']], surf
                                         )
                applause_flag2 = True
            elif self.arenaDialogue == 5:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'And his opponent.. A beast that has destroyed the dreams of many young adventurers, said to be the \'Gatekeeper\' of the Arena.']], surf
                                         )
            elif self.arenaDialogue == 6:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'Introducing.. Tho\'k!']], surf
                                         )
                boss_roar = True

            elif self.arenaDialogue == 7:
                self.txtbox.draw_textbox([["data/sprites/Boss1.png", 'Tho\'k',
                                         'RAAAAAAAAAAAAAAAAAARRGGHHHHHH!!!!!']], surf
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
                                         'Now, the time has come. ' + name + ', I assume you are ready?']], surf
                                         )
                self.txtbox.select_choice(['Yes, I am ready.',
                                          'I don\'t think I am.'], surf)
                self.dialoguecontrol = False
                choice_select = True
                self.txtbox.choice_flag = True
            elif self.arenaDialogue == 9:
                if dialogue_choice == 0:
                    self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                             'Good! That\'s what I expected from you!']], surf
                                             )
                elif dialogue_choice == 1:
                    self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                             'Well unfortunately it\'s too late to turn back now!']], surf
                                             )
            elif self.arenaDialogue == 10:
                self.txtbox.draw_textbox([["data/sprites/host_face.png", 'Chance',
                                         'It is time! Fight!']], surf
                                         )
            elif self.arenaDialogue == 11:
                event_done = True
            screen.blit(surf, (0, 0))
            self.timekeep.timing()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def first_floor_victory(self, dialogues):
        # Cutscene after beating the first_floor boss
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
        global surf
        global screen
        pygame.mixer_music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        pygame.mixer_music.play()
        state = 0
        cur_song = 'data/sounds&music/Infinite_Arena.mp3'
        draw_tb = False
        cur_dialogue = dialogues["first_floor_victory1"]
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
                    pygame.mixer_music.load(cur_song)
                    pygame.mixer_music.set_volume(vol)
                    pygame.mixer_music.play()
                    pygame.mixer_music.set_endevent(pygame.constants.USEREVENT)
                if event.type == pygame.QUIT:
                    global done
                    done = True
                    event_done = True
                    pygame.quit()
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
                    fadeout(surf, 0.01, fade_in=True,
                            optional_bg=self.arena_bg)
                    state += 1
                    self.timekeep.reset()
            elif state == 3:
                if self.timekeep.timing() > 1:
                    cur_dialogue = dialogues['first_floor_victory2']
                    self.dialoguecontrol = True
                    draw_tb = True
            elif state == 4:
                pygame.mixer_music.fadeout(200)
                fadeout(surf, 0.01, fade_in=True,
                        optional_bg=self.arena_bg_night)
                pygame.mixer_music.load("data/sounds&music/Dungeon 2.ogg")
                pygame.mixer_music.set_volume(vol)
                cur_song = "data/sounds&music/Dungeon 2.ogg"
                pygame.mixer_music.set_endevent(USEREVENT)
                pygame.mixer_music.play()
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
                    pygame.mixer_music.fadeout(200)
                    fadeout(surf)
                    event_done = True
            if state < 5:
                surf.blit(self.arena_bg, (0, 0))
            else:
                surf.blit(self.arena_bg_night, (0, 0))
            if draw_tb:
                self.txtbox.draw_textbox(cur_dialogue, surf)
            clock.tick(60)
            screen.blit(surf, (0, 0))
            pygame.display.set_caption("FPS:{}".format(int(clock.get_fps())))
            pygame.display.flip()

    def intro_scene(self, intro_dialogue):
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Church.mp3')
        door_sound = pygame.mixer.Sound('data/sounds&music/Door1.ogg')
        door_sound.set_volume(0.05)
        gate_sound = pygame.mixer.Sound('data/sounds&music/Door4.ogg')
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
        text = ''
        dialogue = 'intro1'
        while not event_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    global done
                    done = True
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
                surf.fill((0, 0, 0, 255))
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
                pygame.mixer_music.set_volume(vol)
                pygame.mixer_music.play()
                self.timekeep.reset()
            elif intro_level == 25:
                surf.blit(self.arena_bg, (0, 0))
                if self.timekeep.timing(1) > 2:
                    draw_tb = True
            elif intro_level == 26:
                event_done = True
            self.ui_text.draw_text((text_x, text_y), text, False, text_surf)
            surf.blit(text_surf, (0, 0))
            if draw_tb:
                self.text_box.draw_textbox(
                    intro_dialogue[dialogue], surf, (0, 400))
            screen.blit(surf, (0, 0))
            clock.tick(60)
            pygame.display.set_caption("FPS:{}".format(int(clock.get_fps())))
            pygame.display.flip()

    def town(self, player_data):
        ''' The town and all the locations present in it. '''
        if not player_data.town_first_flag:
            self.town_first_visit(player_data)
        event_done = False
        global surf
        global screen
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
                    global done
                    done = True
                if event.type == pygame.KEYDOWN:
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
                    if event.key == pygame.K_RETURN:
                        if self.cursorpos == 0:  # Talk option
                            if self.town_location == 0:  # In main town square
                                self.town_talk1 = True
                                town_ui = False
                    if event.key == pygame.K_RCTRL:
                        if self.town_talk1:
                            self.town_talk1 = False
                            town_ui = True
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()
            if self.town_location == 0:
                if self.game_clock.time_state == 'Morning':
                    surf.blit(self.town_bg_day, (0, 0))
                elif self.game_clock.time_state == 'Noon':
                    surf.blit(self.town_bg_eve, (0, 0))
                else:
                    surf.blit(self.town_bg_ngt, (0, 0))
                if town_ui:
                    self.draw_town(player_data)
                if self.town_talk1:
                    self.option_selector.drawUi(
                        3, 'Citizen', 'Rich Lady', 'Fan boy')
                screen.blit(surf, (0, 0))
            self.game_clock.pass_time(player_data, area_music)
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
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
                    global done
                    done = True
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
                            self.casino_state = 'casino'
                            casino_ui = False
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()
            surf.blit(self.inn_bg, (0, 0))
            if casino_ui:
                self.draw_casino(player_data)
            if self.casino_state == 'casino':
                pass
            surf.blit(ab, (0, 0))
            screen.blit(surf, (0, 0))
            self.game_clock.pass_time(player_data, area_music)
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.flip()
    

class GameClock:

    def __init__(self):
        self.clockTime = Timer()
        self.curTime = 0
        self.bellflag = False
        self.fadeoutflag = False
        # Music to be played in the area
        self.area_music = 'data/sounds&music/Infinite_Arena.mp3'
        # Bell sound during nighttime
        self.bell = pygame.mixer.Sound('data/sounds&music/Bell1.ogg')
        self.bell.set_volume(0.05)
        self.rooster = pygame.mixer.Sound(
            'data/sounds&music/Roost.ogg')  # Morning sound
        self.rooster.set_volume(0.05)
        self.paused = False
        self.time_state = "Morning"  # The time of day

    def toggle_clock(self):     # Pauses/Unpauses the flow of ingame time
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def reset(self):
        self.clockTime.reset()

    def pass_time(self, player_details, area_music='data/sounds&music/Infinite_Arena.mp3'):
        player = player_details
        self.area_music = area_music
        self.curTime = self.clockTime.timing()  # Current time
        if not self.paused:     # If clock is not paused
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
            surf.blit(pygame.transform.scale(
                arena_bg1, (curwidth, curheight)), (0, 0))

        if player.hours >= 14 and player.hours < 20:  # Afternoon
            self.time_state = "Noon"
            surf.blit(pygame.transform.scale(
                arena_bg2, (curwidth, curheight)), (0, 0))

        if player.hours >= 20 or player.hours < 6:  # Night
            self.time_state = "Night"
            surf.blit(pygame.transform.scale(
                arena_bg3, (curwidth, curheight)), (0, 0))

        if (player.hours == 19 and player.minutes == 30) and (not self.bellflag):   # Music fading out
            if not self.fadeoutflag:
                pygame.mixer.music.fadeout(6000)  # 8 seconds
                self.fadeoutflag = True

        # Playing bell sound when it becomes night
        if (player.hours >= 20 or player.hours < 6) and (not self.bellflag):
            self.bell.play()
            Currentmusic = 'data/sounds&music/night.mp3'
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


if __name__ == "__main__":
    player = Player(item_data=item_data)
    eventManager = GameEvents()
    warrior = pyganim.PygAnimation(
        [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])

    mage = pyganim.PygAnimation([("data/sprites/midle1.png", 0.3),
                                ("data/sprites/midle2.png", 0.3), ("data/sprites/midle3.png", 0.3)])

    castanim = [("data/sprites/b1.png", 0.3),
                ("data/sprites/b2.png", 0.3), ("data/sprites/b3.png", 0.3)]
    old_battler = SideBattle(monster_data, 'mage', castanim, "data/backgrounds/Ruins2.png",
                             'data/sounds&music/yousayrun2.mp3')

    floor_talk = SelectOptions()  # Choices for 'Talk' in floor 1
    arena_shop = Shop(item_data)
    #####

    randbattle = 0
    timepassed = False  # Flag to check if the time passed or6 not
    newgtxtbox = 0
    pygame.mixer.music.load('data/sounds&music/Theme2.ogg')
    pygame.mixer.music.play()
    vol = 0.05
    surf = pygame.Surface((1366, 768))
    pygame.mixer.music.set_volume(vol)
    # I deeply apologize for the code below(and above)
    talked = False  # Ui flags
    options = False
    status = False
    shop = False
    system = False
    talking = False
    battle_choice = False
    post_battle = False  # After battle shenanigans
    controlui = True  # Flag to check if player can control ui
    talkval = 0
    text = pygame.font.Font("data/fonts/runescape_uf.ttf", 30)
    seltext = pygame.font.Font("data/fonts/runescape_uf.ttf", 40)
    secretbattle = SideBattle(monster_data, 'warrior', castanim, "data/backgrounds/LavaCave.png",
                              'data/sounds&music/Battle3.ogg', phealth=1000, pmana=100, pstr=1000, pstrmod=14, pdef=100,
                              pmag=2000, pluck=9)
    secretbattle.plevel = 50
    debugbattle = SideBattle(monster_data, 'mage', castanim, "data/backgrounds/DemonicWorld.png",
                             'data/sounds&music/Dungeon2.ogg', phealth=10000, pmana=1000, pstr=1000, pstrmod=14, pdef=100,
                             pmag=2000, pluck=9)
    debugbattle.plevel = 50
    healsound = pygame.mixer.Sound('data/sounds&music/Recovery.ogg')
    healsound.set_volume(0.05)
    mage.play()
    warrior.play()
    menutext = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40)
    ab = text.render(alphatext, False, (255, 255, 0))  # debug
    sel1 = seltext.render('Enter your name:', False, (255, 255, 0))
    sel2 = seltext.render('Press RCTRL to continue..', False, (255, 255, 0))
    MageDesc = seltext.render(
        'Mages are proficient at magic but weak physically.', False, (178, 57, 63))
    WarDesc = seltext.render(
        'Warriors specialize in physical attacks and buffs.', False, (178, 57, 63))
    clockTime = GameClock()  # Clock for the day/night system
    sel3 = seltext.render('Select your class:', False, secretbattle.txtcolor)
    sel4 = text.render('Mage', False, secretbattle.txtcolor)
    sel5 = text.render('Warrior', False, secretbattle.txtcolor)
    loadgamecolor = (255, 255, 0)
    nosavefile = True  # Check if a savefile is already present or not
    load_flag = False
    if not load_flag:
        try:
            rfile = open('savegame.dat', 'rb')
            rfile.close()
            loadgamecolor = (255, 255, 0)
            nosavefile = False
            load_flag = True
        except:
            loadgamecolor = (105, 109, 114)
            nosavefile = True
            load_flag = True
    newgame = menutext.render(
        'New Game', True, (255, 255, 0))  # Things for main menu
    loadgame = menutext.render('Load Game', True, loadgamecolor)
    quitgame = menutext.render('Quit Game', True, (255, 255, 0))
    namelist = ['']
    curwidth, curheight = screen.get_size()
    menubg1 = pygame.transform.scale(pygame.image.load("data/backgrounds/bg2.jpg").convert_alpha(), (curwidth, curheight))
    arena_bg1 = pygame.image.load(
        "data/backgrounds/arenaDay.png").convert_alpha()  # day time arena
    arena_bg2 = pygame.image.load(
        "data/backgrounds/arenaEvening.png").convert_alpha()
    arena_bg3 = pygame.image.load(
        "data/backgrounds/arenaNight.png").convert_alpha()
    inn_bg = pygame.image.load("data/backgrounds/inn.png").convert_alpha()
    logo = pygame.image.load(
        "data/backgrounds/logo3.png").convert_alpha()  # Main menu logo
    cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
    # New game screen background
    newgbg = pygame.image.load("data/backgrounds/Meadow.png").convert_alpha()
    loadsound = pygame.mixer.Sound('data/sounds&music/Load.ogg')
    loadsound.set_volume(0.05)
    cursorpos = 0
    Textbox = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
    scene = 'splash'
    popup_message = ""
    Currentmusic = 'data/sounds&music/Infinite_Arena.mp3'
    ui = MainUi()
    splash_screen = splashscreen.Splash(screen)
    splash_screen.toggle_splash()
    shh = []
    battler = NewBattle(monster_data, item_data, sound_effects,
                        animations, skills, sequences)  # New battle tester
    bellflag = False  # Flag for bell sound to play during time change
    txtbox = gameui.TextBox()
    timer = Timer()
    fadeoutflag = False  # Flag for music to fade out

    while not done:
        # main

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # All the required controls
                posfinder()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and scene == 'menu':
                    shh.append('b')

                    print(shh)
                if event.key == pygame.K_o and scene == 'menu':
                    shh.append('o')
                    print(shh)
                if event.key == pygame.K_s and scene == 'menu':
                    shh.append('s')
                    print(shh)
                if event.key == pygame.K_t and scene == 'menu':
                    shh.append('t')
                    print(shh)
                if event.key == pygame.K_e and scene == 'menu':
                    shh.append('e')
                    print(shh)
                if event.key == pygame.K_w and scene == 'menu':
                    shh.append('w')
                    print(shh)
                if event.key == pygame.K_n and scene == 'menu':
                    shh.append('n')
                    print(shh)
                if event.key == pygame.K_m and scene == 'menu':
                    shh.append('m')
                    print(shh)
                if event.key == pygame.K_v and scene == 'menu':
                    shh.append('v')
                    print(shh)
                if event.key == pygame.K_BACKSPACE and scene == 'menu':
                    if shh != []:
                        shh.pop(0)
                    print(shh)
                if event.key == pygame.K_RETURN and cursorpos == 0 and scene == 'menu':  # newgame
                    pygame.mixer.music.stop()
                    loadsound.play()
                    fadeout(surf)
                    pygame.time.wait(1000)
                    pygame.mixer.music.load('data/sounds&music/Castle1.ogg')
                    pygame.mixer.music.play()
                    load_flag = False
                    scene = 'new_game'

                if (event.key == pygame.K_RETURN and cursorpos == 1 and scene == 'menu') and not nosavefile:  # load
                    try:
                        player = Player(item_data=item_data)
                        rfile = open('savegame.dat', 'rb+')
                        pygame.mixer.music.stop()
                        loadsound.play()
                        player = pickle.load(rfile)
                        rfile.close()
                        fadein(255)
                        scene = 'arena'
                        load_flag = False
                        ui.cursorpos = 9
                        pygame.mixer.music.load(
                            'data/sounds&music/Infinite_Arena.mp3')
                        pygame.mixer.music.play()
                    except FileNotFoundError:
                        print("Could not open")
                        popup_message = "Could not open save file!"
                        txtbox.toggle_popup_flag()

                if event.key == pygame.K_RETURN and cursorpos == 2 and scene == 'menu':  # quit
                    done = True
                if event.key == pygame.K_UP and scene == 'menu':
                    secretbattle.cursorsound.play()
                    cursorpos -= 1
                if event.key == pygame.K_DOWN and scene == 'menu':
                    cursorpos += 1
                    secretbattle.cursorsound.play()

                # Keyboard entry for name.
                if event.key == pygame.K_q and scene == 'new_game':
                    namelist.append('q')
                if event.key == pygame.K_w and scene == 'new_game':
                    namelist.append('w')
                if event.key == pygame.K_e and scene == 'new_game':
                    namelist.append('e')
                if event.key == pygame.K_r and scene == 'new_game':
                    namelist.append('r')
                if event.key == pygame.K_t and scene == 'new_game':
                    namelist.append('t')
                if event.key == pygame.K_y and scene == 'new_game':
                    namelist.append('y')
                if event.key == pygame.K_u and scene == 'new_game':
                    namelist.append('u')
                if event.key == pygame.K_i and scene == 'new_game':
                    namelist.append('i')
                if event.key == pygame.K_o and scene == 'new_game':
                    namelist.append('o')
                if event.key == pygame.K_p and scene == 'new_game':
                    namelist.append('p')
                if event.key == pygame.K_a and scene == 'new_game':
                    namelist.append('a')
                if event.key == pygame.K_s and scene == 'new_game':
                    namelist.append('s')
                if event.key == pygame.K_d and scene == 'new_game':
                    namelist.append('d')
                if event.key == pygame.K_f and scene == 'new_game':
                    namelist.append('f')
                if event.key == pygame.K_g and scene == 'new_game':
                    namelist.append('g')
                if event.key == pygame.K_h and scene == 'new_game':
                    namelist.append('h')
                if event.key == pygame.K_j and scene == 'new_game':
                    namelist.append('j')
                if event.key == pygame.K_k and scene == 'new_game':
                    namelist.append('k')
                if event.key == pygame.K_l and scene == 'new_game':
                    namelist.append('l')
                if event.key == pygame.K_z and scene == 'new_game':
                    namelist.append('z')
                if event.key == pygame.K_x and scene == 'new_game':
                    namelist.append('x')
                if event.key == pygame.K_c and scene == 'new_game':
                    namelist.append('c')
                if event.key == pygame.K_v and scene == 'new_game':
                    namelist.append('v')
                if event.key == pygame.K_b and scene == 'new_game':
                    namelist.append('b')
                if event.key == pygame.K_n and scene == 'new_game':
                    namelist.append('n')
                if event.key == pygame.K_m and scene == 'new_game':
                    namelist.append('m')
                if event.key == pygame.K_BACKSPACE and scene == 'new_game':
                    if len(namelist) > 0:
                        namelist.pop()
                if (event.key == pygame.K_RCTRL and scene == 'new_game') and len(namelist) > 1:
                    scene = "new_game2"
                    name = "".join(namelist).capitalize()
                    player.name = name
                if event.key == pygame.K_LEFT and scene == 'new_game2':
                    cursorpos -= 1
                if event.key == pygame.K_RIGHT and scene == 'new_game2':
                    cursorpos += 1
                if event.key == pygame.K_RETURN and scene == 'new_game2' and cursorpos == 0:
                    player = Player(item_data=item_data)
                    player.name = name.capitalize()
                    player.pclass = 'mage'
                    rfile = open('savegame.dat', 'wb+')
                    scene = 'new_game3'
                    pygame.mixer.music.stop()
                    try:
                        pickle.dump(player, rfile)
                        rfile.close()
                    except:
                        print("Could not create save file.")
                        pass
                    timer.reset()
                if event.key == pygame.K_RETURN and scene == 'new_game2' and cursorpos == 1:
                    player = Player(item_data=item_data)
                    player.name = name.capitalize()
                    player.pclass = 'warrior'
                    rfile = open('savegame.dat', 'wb+')
                    scene = 'new_game3'
                    pygame.mixer.music.stop()
                    try:
                        pickle.dump(player, rfile)
                        rfile.close()
                    except EOFError:
                        print("Could not create save file.")
                        pass
                    timer.reset()
                if event.key == pygame.K_RCTRL and (
                        scene == 'new_game3' or scene == 'new_game4') or scene == 'credits':
                    newgtxtbox += 1
                if (event.key == pygame.K_DOWN and (scene == 'arena' or scene == 'inn')) and controlui:
                    ui.cursorsound.play()
                    ui.cursorpos += 1

                if (event.key == pygame.K_UP and (scene == 'arena' or scene == 'inn')) and controlui:
                    ui.cursorsound.play()
                    ui.cursorpos -= 1
                if (event.key == pygame.K_DOWN and scene == 'arena') and system:
                    ui.cursorsound.play()
                    ui.syscursorpos += 1
                if (event.key == pygame.K_UP and scene == 'arena') and system:
                    ui.cursorsound.play()
                    ui.syscursorpos -= 1
                if (event.key == pygame.K_DOWN and scene == 'arena') and battle_choice:
                    ui.cursorsound.play()
                    ui.batcursorpos += 1
                if (event.key == pygame.K_UP and scene == 'arena') and battle_choice:
                    ui.cursorsound.play()
                    ui.batcursorpos -= 1
                if (event.key == pygame.K_RETURN and ui.cursorpos == 0) and scene == 'arena' and controlui:  # Talk option
                    options = True
                    drawUi = False
                    controlui = False
                    # So that it doesn't automatically pick the first option(input is annoying on pygame)
                    event.key = 1

                if (event.key == pygame.K_RCTRL and options) or (event.key == pygame.K_RCTRL and talking):
                    if ui.txtbox.progress_dialogue(ui.cur_dialogue):
                        drawui = True
                        controlui = True
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
                        drawui = True
                        controlui = True
                        ui.talked = False
                        options = False
                        talking = False

                if (event.key == pygame.K_RETURN and ui.cursorpos == 1) and scene == 'arena' and controlui:  # Battle option
                    drawui = False
                    controlui = False
                    battle_choice = True
                    ui.txtbox.reset()
                    ui.battalk = True
                    ui.batcursorpos = 4

                if (event.key == pygame.K_RETURN and ui.cursorpos == 2) and scene == 'arena' and controlui:  # Status option
                    drawui = False
                    controlui = False
                    status = True
                    event.key = ""
                if status:
                    if event.key == pygame.K_RCTRL and (not ui.equip_flag1 and not ui.equip_flag2 and not ui.stat_flag):
                        drawui = True
                        controlui = True
                        status = False
                    elif event.key == pygame.K_RETURN and ui.status_cur_pos == 2:
                        drawui = True
                        controlui = True
                        status = False
                    ui.handle_status_inputs(player)
                if (event.key == pygame.K_RETURN and ui.cursorpos == 3) and scene == 'arena' and controlui:  # Shop option
                    drawui = False
                    controlui = False
                    arena_shop.txtbox.reset()
                    shop = True
                if (event.key == pygame.K_RCTRL and shop) and arena_shop.shopkeep:
                    if arena_shop.txtbox.progress_dialogue([[]]):
                        arena_shop.shopkeep = False
                        event.key = 0  # to stop pygame from being dumb
                if (event.key == pygame.K_RCTRL and shop) and not arena_shop.shopkeep:
                    if arena_shop.shop_selection_flag:
                        drawui = True
                        controlui = True
                        shop = False
                        arena_shop.shopkeep = True
                    else:
                        arena_shop.shop_selection_flag = True
                if (event.key == pygame.K_RETURN and shop) and not arena_shop.shopkeep and arena_shop.shop_selection_flag:
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
                if (event.key == pygame.K_RETURN and shop) and not arena_shop.shop_selection_flag:
                    if arena_shop.buy_item(arena_shop.min_pos + arena_shop.shop_cursor_pos2):
                        # Buying item from shop
                        player.gold -= arena_shop.current_list[arena_shop.min_pos +
                                                               arena_shop.shop_cursor_pos2]['cost']
                        if arena_shop.current_list == arena_shop.weapons_list:
                            player.wep_owned.append(
                                arena_shop.min_pos + arena_shop.shop_cursor_pos2)
                        elif arena_shop.current_list == arena_shop.armour_list:
                            player.arm_owned.append(
                                arena_shop.min_pos + arena_shop.shop_cursor_pos2)
                        elif arena_shop.current_list == arena_shop.acc_list:
                            player.acc_owned.append(
                                arena_shop.min_pos + arena_shop.shop_cursor_pos2)
                        elif arena_shop.current_list == arena_shop.consume_list:
                            for consumable in arena_shop.consume_list:
                                if consumable["id"] == arena_shop.min_pos + arena_shop.shop_cursor_pos2:
                                    if len(player.inventory) > 0:
                                        item_in_inventory = False
                                        for item in player.inventory:
                                            if item["name"] == consumable["name"]:
                                                item["amount"] += 1
                                                item_in_inventory = True
                                        if not item_in_inventory:
                                            player.inventory.append(
                                                {"name": consumable["name"], "amount": 1})
                                    else:
                                        player.inventory.append(
                                            {"name": consumable["name"], "amount": 1})
                        player.update_stats()

                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 4) and scene == 'arena' and controlui:  # Inn option
                    pygame.mixer.music.pause()
                    fadein(255)
                    pygame.mixer.music.load('data/sounds&music/Town2.ogg')
                    pygame.mixer.music.play()
                    scene = 'inn'
                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 5) and scene == 'arena' and controlui:  # System option
                    drawui = False
                    controlui = False
                    system = True
                    ui.syscursorpos = 4
                if (event.key == pygame.K_RETURN and ui.cursorpos == 1) and scene == 'inn' and controlui:
                    if player.gold >= 20:  # rest
                        player.curhp = player.hp
                        player.curmp = player.mp
                        player.hours = 6  # Set time to 6:00 after resting at inn
                        player.minutes = 0
                        healsound.play()
                        fadein(255)
                        player.gold -= 20
                if (event.key == pygame.K_RETURN and ui.cursorpos == 2) and scene == 'inn' and controlui:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(
                        'data/sounds&music/Infinite_Arena.mp3')
                    fadein(255)
                    pygame.mixer.music.play()
                    scene = 'arena'
                if (event.key == pygame.K_RETURN and ui.syscursorpos == 0) and system:
                    try:
                        rfile = open('savegame.dat', 'wb+')
                        pickle.dump(player, rfile)
                        ui.savesound.play()
                        drawui = True
                        controlui = True
                        system = False
                        rfile.close()
                    except:
                        print("Could not create save file")
                if (event.key == pygame.K_RETURN and ui.syscursorpos == 1) and system:
                    done = True
                if (event.key == pygame.K_RETURN and ui.syscursorpos == 2) and system:
                    drawui = True
                    controlui = True
                    system = False

                if event.key == pygame.K_RCTRL and system:
                    drawui = True
                    controlui = True
                    system = False
                if (event.key == pygame.K_RETURN and ui.batcursorpos == 0) and battle_choice:
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
                        battle_choice = False
                        post_battle = True
                        pygame.mixer.music.load(
                            'data/sounds&music/Infinite_Arena.mp3')
                        pygame.mixer.music.play()
                    else:
                        scene = 'menu'
                        pygame.mixer_music.load('data/sounds&music/Theme2.ogg')
                        pygame.mixer_music.set_volume(0.1)
                        pygame.mixer_music.play()
                        battle_choice = False
                        post_battle = False
                        drawui = True
                        controlui = True
                        ui.pb_dialogue = False
                if (event.key == pygame.K_RETURN and ui.batcursorpos == 1) and battle_choice:
                    if player.fkills >= 5 and player.progress == 1:
                        fadein(255)
                        eventManager.firstfloor_boss(player.name)
                        battler.battle('floor_boss1', player, set_music=1)
                        if battler.check_victory():
                            eventManager.first_floor_victory(dialogues)
                            player.progress += 1
                            player.fkills = 0
                            battle_choice = False
                            post_battle = False
                            drawui = True
                            controlui = True
                            ui.pb_dialogue = False
                            scene = 'arena'
                            player.hours = 6
                            player.minutes = 0
                            pygame.mixer.music.load(
                                'data/sounds&music/Infinite_Arena.mp3')
                            pygame.mixer.music.play()
                        else:
                            scene = 'menu'
                            pygame.mixer_music.load(
                                'data/sounds&music/Theme2.ogg')
                            pygame.mixer_music.set_volume(0.1)
                            pygame.mixer_music.play()
                            battle_choice = False
                            post_battle = False
                            drawui = True
                            controlui = True
                            ui.pb_dialogue = False
                    else:
                        secretbattle.buzzer.play()
                if (event.key == pygame.K_RETURN and ui.batcursorpos == 2) and battle_choice:
                    drawui = True
                    controlui = True
                    battle_choice = False
                if (event.key == pygame.K_RCTRL and battle_choice) and ui.battalk:
                    if ui.txtbox.progress_dialogue([[]]):
                        ui.battalk = False
                if event.key == pygame.K_RCTRL and post_battle:
                    ui.pb_dialogue = False
                    post_battle = False
                    drawui = True
                    controlui = True

            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.load(Currentmusic)
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

        name = "".join(namelist)
        if scene == 'splash':
            splash_screen.draw_splash(screen, event)
            fadeout(surf, fade_in=True, optional_bg=menubg1)
            scene = 'menu'
        elif scene == 'menu':  # Main menu of the game(What you see on start-up)
            surf.blit(menubg1, (0, 0))
            surf.blit(logo, (curwidth - 1100, curheight - 600))
            surf.blit(pygame.transform.scale(Textbox, (250, 180)), (450, 368))
            surf.blit(newgame, (474, 391))
            surf.blit(loadgame, (474, 431))
            surf.blit(quitgame, (474, 471))
            if shh == ['b', 'o', 's', 's'] and scene == 'menu':
                shh = []
                secretbattle.battle('secret_battle1', -10,
                                    False, bgm='data/sounds&music/Battle3.ogg')
            if shh == ['t', 'e', 's', 't'] and scene == 'menu':
                shh = []
                Zen = Player()
                Zen.set_player_stats(stre=1000, mag=2000,
                                     health=10000, mana=1000, luck=9, level=90)
                battler.battle("debug_fight", Zen, set_music=2)
            if shh == ['m', 'o', 'v', 'e'] and scene == 'menu':
                shh = []
                Zen = Player()
                Zen.set_player_stats(stre=1000, mag=2000,
                                     health=10000, mana=1000, luck=9, level=90)
                battler.battle("move_tester", Zen, set_music=3)
            if shh == ['t', 'o', 'w', 'n'] and scene == 'menu':
                shh = []
                fadeout(surf)
                eventManager.town_first_visit(player)
                fadeout(surf)
                pygame.mixer_music.load(Currentmusic)
                pygame.mixer_music.play()
            if shh == ['t', 'e', 't'] and scene == 'menu':
                player.set_player_stats(level=20, health=1000, mana=1000)
                battler.battle('rat', player)
                shh = []
            if shh == ['t', 'o', 't'] and scene == 'menu':
                player.town_first_flag = False
                eventManager.town(player)
                shh = []
            if shh == ['t', 's', 't'] and scene == 'menu':
                eventManager.intro_scene(dialogues)
                shh = []
            if shh == ['t', 'o', 's'] and scene == 'menu':
                eventManager.casino(player)
                shh = []
            if cursorpos == 0:
                surf.blit(cursor, (434, 400))
            elif cursorpos == 1:
                surf.blit(cursor, (434, 443))
            elif cursorpos == 2:
                surf.blit(cursor, (434, 483))
            if cursorpos < 0:
                cursorpos = 2
            if cursorpos > 2:
                cursorpos = 0
        elif scene == 'new_game':
            surf.blit(pygame.transform.scale(
                newgbg, (curwidth, curheight)), (0, 0))
            sel1 = seltext.render(
                'Enter your name:' + name.capitalize(), False, secretbattle.txtcolor)
            if len(namelist) > 11:
                del namelist[len(namelist) - 1]
                secretbattle.buzzer.play()
            surf.blit(sel2, (500, 500))
            surf.blit(sel1, (300, 300))
            cursorpos = 0
        elif scene == 'new_game2':
            surf.blit(pygame.transform.scale(
                newgbg, (curwidth, curheight)), (0, 0))
            surf.blit(sel3, (300, 300))
            surf.blit(sel4, (300, 375))
            surf.blit(sel5, (778, 375))
            warrior.blit(surf, (778, 429))
            mage.blit(surf, (300, 435))
            if cursorpos == 0:
                statstxt = seltext.render(
                    'STR:%d MAG:%d DEF:%d LUCK:%d' % (
                        player.stre, player.mag, player.defe, player.luck), False,
                    (10, 33, 147))
                surf.blit(cursor, (260, 375))
                surf.blit(MageDesc, (260, 45))
                surf.blit(statstxt, (260, 95))
                player.stre = 10
                player.mag = 25
                player.defe = 15

            elif cursorpos == 1:
                statstxt = seltext.render(
                    'STR:%d MAG:%d DEF:%d LUCK:%d' % (
                        player.stre, player.mag, player.defe, player.luck), False,
                    (10, 33, 147))
                surf.blit(cursor, (738, 375))
                surf.blit(WarDesc, (260, 45))
                surf.blit(statstxt, (260, 95))
                player.stre = 20
                player.mag = 10
                player.defe = 20
            if cursorpos < 0:
                cursorpos = 1
            elif cursorpos > 1:
                cursorpos = 0
        elif scene == 'new_game3':
            fadeout(surf, 0.01)
            eventManager = GameEvents()
            eventManager.intro_scene(dialogues)
            scene = 'arena'
        elif scene == 'arena':
            clockTime.pass_time(player)  # passage of ingame time
            if clockTime.time_state == 'Morning':
                surf.blit(pygame.transform.scale(
                    arena_bg1, (curwidth, curheight)), (0, 0))  # day bg
            elif clockTime.time_state == 'Noon':
                surf.blit(pygame.transform.scale(
                    arena_bg2, (curwidth, curheight)), (0, 0))  # Noon bg
            else:
                surf.blit(pygame.transform.scale(
                    arena_bg3, (curwidth, curheight)), (0, 0))  # Night bg

            if drawui:
                ui.clock(player.hours, player.minutes)
                ui.arena(player.progress)
                if ui.cursorpos > 5:
                    ui.cursorpos = 0
                if ui.cursorpos < 0:
                    ui.cursorpos = 5
            if talking:
                ui.talk(talkval)
            if options:
                if player.progress == 1:
                    floor_talk.drawUi(4, 'Old Man', 'Boy', 'Villager', 'Stranger')
                elif player.progress == 2:
                    floor_talk.drawUi(4, 'Old Man', 'Boy', 'Villager', 'Pompous Noble')
            if status:
                ui.status(player, item_data)
            if shop:
                arena_shop.draw_shop('Arena Shop', player)
            if system:
                ui.system()
            if battle_choice:
                ui.battle_choice(player.fkills)
            if post_battle:
                ui.post_battle(player.progress)
        elif scene == 'inn':
            surf.blit(pygame.transform.scale(
                inn_bg, (curwidth, curheight)), (0, 0))
            if drawui:
                ui.draw_inn(player.gold)
            if ui.cursorpos > 2:
                ui.cursorpos = 0
            if ui.cursorpos < 0:
                ui.cursorpos = 2
        elif scene == 'credits':
            surf.fill((0, 0, 0))
            if newgtxtbox == 1:
                txtbox.draw_textbox(
                    "data/sprites/host_face.png", 'Chance', 'Hey congrats you beat the demo!')
            if newgtxtbox == 2:
                txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                    'There is more to come but ill save that for another time.')
            if newgtxtbox == 3:
                txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                    'This was a project made by Hameel and Nihal!')
            if newgtxtbox == 4:
                txtbox.draw_textbox(
                    "data/sprites/host_face.png", 'Chance', 'Stay tuned for the final project!')

            if newgtxtbox > 4:
                scene = 'menu'
        timer.timing()
        surf.blit(ab, (0, 0))
        txtbox.popup_message(popup_message, surf)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)
        fps = "FPS:%d" % clock.get_fps()
        pygame.display.set_caption(fps)
    pygame.quit()
