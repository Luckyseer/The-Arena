# Alpha V2.4
from __future__ import print_function  # For compatibility with python 2.x
import pickle
import random
from math import floor
import pygame
import pyganim
import json
from pygame.locals import *

icon = pygame.image.load("data/sprites/icon2.png")
pygame.display.set_icon(icon)
alphatext = "Alpha v3.0 - New Battle System"
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
        self.cur_weapon = 4  # set the id of the item
        self.cur_armour = 5  # NOTE TO SELF: DON'T FORGET TO CHANGE DEFAULT ITEMS BACK!!
        self.cur_accessory = 5
        self.stre = strength  # Player's base stats
        self.defe = defence
        self.mag = magic
        self.luck = luck
        # Player's stats from equipment
        self.add_stre = item_data['weapons'][self.cur_weapon]['atk'] + item_data['armours'][self.cur_armour]['atk'] + \
                        item_data['accessories'][self.cur_accessory]['atk']
        self.add_defe = item_data['weapons'][self.cur_weapon]['def'] + item_data['armours'][self.cur_armour]['def'] + \
                        item_data['accessories'][self.cur_accessory]['def']
        self.add_mag = item_data['weapons'][self.cur_weapon]['mag'] + item_data['armours'][self.cur_armour]['mag'] + \
                       item_data['accessories'][self.cur_accessory]['mag']
        self.add_luck = luck
        self.progress = 1  # progress in game
        self.gold = 150
        self.level = 15
        self.hours = 6  # in-game clock values
        self.minutes = 0  # ^
        self.exp = 0
        self.inventory = {'Potion': 1,  # Heals 200 HP
                          'Bread': 0,  # Heals 50 HP
                          'Steak': 0,  # Heals 120 HP
                          'Meat Stew': 0,  # Heals 250 HP
                          'Roasted Beef': 0,  # Heals 500 HP
                          'Elixir': 0,  # Fully heals HP and MP
                          'Mana Potion': 0,  # Restores 100 MP
                          'Water': 0,  # Restores 20MP
                          'Orange Juice': 0,  # Restores 50MP
                          'Orc Tears': 0,  # Restores 150MP
                          'Dragon\'s Breath': 0,  # Restores 250MP
                          }
        self.pclass = 'warrior'
        self.fkills = 0  # Kills in floor
        self.tkills = 0  # Total Kills
        self.scene = 'menu'
        self.town_first_flag = True  # Flag to check if player visited town or not.
        self.paid_girl_flag = False  # Flag for whether the player paid the girl during the town scene

    def xp_till_levelup(self, currentlevel):  # Experience needed to level up

        self.expreq = floor((currentlevel ** 4) / 5)
        return self.expreq

    def check_levelup(self):  # Check if player has leveled up
        self.xp_till_levelup(self.level)
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


if  __name__ == '__main__':
    pygame.init()

    isfullscreen = True
    screen_width = 1280
    screen_height = 720
    # #Note to self: remove debug lines after done# #

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([screen_width, screen_height])
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


def fadeout(surface, time=0.000001, fadetimer=Timer()):  # fadeout effect
    global screen
    fade_done = False
    alpha = 255
    while True:
        while alpha >= 0:
            if fadetimer.timing(1) >= time:
                surface.set_alpha(alpha)
                screen.fill([0, 0, 0])
                screen.blit(surface, (0, 0))
                pygame.display.flip()
                alpha -= 3
                fadetimer.reset()
        fade_done = True
        if fade_done:
            surface.set_alpha(255)
            break
    return fade_done


class SideBattle:
    """ The sidebattle class, which provides us with the main gameplay(the battle system)
        Needs some work, could be a lot more efficient.
        Currently needs some work on the aesthetics side. """

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
        self.staticon1 = pygame.image.load("data/sprites/attack+.png").convert_alpha()
        self.pshadow = pygame.image.load("data/sprites/Shadow1.png").convert_alpha()
        self.encountersound = pygame.mixer.Sound('data/sounds&music/Battle2.ogg')
        self.cursorsound = pygame.mixer.Sound('data/sounds&music/Cursor1.ogg')
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
             ("data/sprites/coin4.png", 0.1), ("data/sprites/coin5.png", 0.1), ("data/sprites/coin6.png", 0.1),
             ("data/sprites/coin7.png", 0.1), ("data/sprites/coin8.png", 0.1), ("data/sprites/coin9.png", 0.1)])
        self.fireanim = pyganim.PygAnimation(
            [("data/sprites/Fire1.png", 0.1), ("data/sprites/Fire2.png", 0.1), ("data/sprites/Fire3.png", 0.1),
             ("data/sprites/Fire4.png", 0.1), ("data/sprites/Fire5.png", 0.1), ("data/sprites/Fire6.png", 0.1),
             ("data/sprites/Fire7.png", 0.1), ("data/sprites/Fire8.png", 0.1)], False)
        self.iceanim = pyganim.PygAnimation(
            [("data/sprites/Ice1.png", 0.09), ("data/sprites/Ice2.png", 0.09), ("data/sprites/Ice3.png", 0.09),
             ("data/sprites/Ice4.png", 0.09), ("data/sprites/Ice5.png", 0.09), ("data/sprites/Ice6.png", 0.09),
             ("data/sprites/Ice7.png", 0.09), ("data/sprites/Ice8.png", 0.09), ("data/sprites/Ice9.png", 0.09),
             ("data/sprites/Ice10.png", 0.09), ("data/sprites/Ice11.png", 0.09), ("data/sprites/Ice12.png", 0.09),
             ("data/sprites/Ice13.png", 0.09), ("data/sprites/Ice14.png", 0.09), ("data/sprites/Ice15.png", 0.09),
             ("data/sprites/Ice16.png", 0.09), ("data/sprites/Ice17.png", 0.09), ("data/sprites/Ice18.png", 0.1)], False)
        self.deathanim = pyganim.PygAnimation(
            [("data/sprites/Death1.png", 0.1), ("data/sprites/Death2.png", 0.1), ("data/sprites/Death3.png", 0.1),
             ("data/sprites/Death4.png", 0.1), ("data/sprites/Death5.png", 0.1), ("data/sprites/Death6.png", 0.1),
             ("data/sprites/Death7.png", 0.1), ("data/sprites/Death8.png", 0.1), ("data/sprites/Death9.png", 0.1),
             ("data/sprites/Death10.png", 0.1), ("data/sprites/Death11.png", 0.1), ("data/sprites/Death12.png", 0.1)], False)
        self.cureanim = pyganim.PygAnimation(
            [("data/sprites/Cure1.png", 0.1), ("data/sprites/Cure2.png", 0.1), ("data/sprites/Cure3.png", 0.1),
             ("data/sprites/Cure4.png", 0.1), ("data/sprites/Cure5.png", 0.1), ("data/sprites/Cure6.png", 0.1),
             ("data/sprites/Cure7.png", 0.1), ("data/sprites/Cure8.png", 0.1), ("data/sprites/Cure9.png", 0.1),
             ("data/sprites/Cure10.png", 0.1), ("data/sprites/Cure11.png", 0.1), ("data/sprites/Cure12.png", 0.1),
             ("data/sprites/Cure13.png", 0.1), ("data/sprites/Cure14.png", 0.1), ("data/sprites/Cure15.png", 0.1)], False)
        self.curesound = pygame.mixer.Sound('data/sounds&music/Item3.ogg')
        self.icesound = pygame.mixer.Sound('data/sounds&music/Ice4.ogg')
        self.deathmagsound = pygame.mixer.Sound('data/sounds&music/Darkness5.ogg')
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
             ("data/sprites/Water4.png", 0.1), ("data/sprites/Water5.png", 0.1), ("data/sprites/Water6.png", 0.1),
             ("data/sprites/Water7.png", 0.1), ("data/sprites/Water8.png", 0.1), ("data/sprites/Water9.png", 0.1),
             ("data/sprites/Water10.png", 0.1), ("data/sprites/Water11.png", 0.1), ("data/sprites/Water12.png", 0.1),
             ("data/sprites/Water13.png", 0.1), ("data/sprites/Water14.png", 0.1), ("data/sprites/Water15.png", 0.1),
             ("data/sprites/Water16.png", 0.1), ("data/sprites/Water17.png", 0.1), ("data/sprites/Water18.png", 0.1)], False)
        self.thundersound = pygame.mixer.Sound('data/sounds&music/Thunder9.ogg')
        self.deathsprite = pygame.image.load("data/sprites/death.png").convert_alpha()
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
             ("data/sprites/xp5.png", 0.1), ("data/sprites/xp6.png", 0.1), ("data/sprites/xp7.png", 0.1), ("data/sprites/xp8.png", 0.1),
             ("data/sprites/xp9.png", 0.1)])
        self.xpanim.convert_alpha()
        self.specialanim = pyganim.PygAnimation(
            [("data/sprites/Special1.png", 0.1), ("data/sprites/Special2.png", 0.1), ("data/sprites/Special3.png", 0.1),
             ("data/sprites/Special4.png", 0.1), ("data/sprites/Special5.png", 0.1), ("data/sprites/Special6.png", 0.1),
             ("data/sprites/Special7.png", 0.1), ("data/sprites/Special8.png", 0.1), ("data/sprites/Special9.png", 0.1),
             ("data/sprites/Special10.png", 0.1), ("data/sprites/Special11.png", 0.1), ("data/sprites/Special12.png", 0.1),
             ("data/sprites/Special13.png", 0.1), ("data/sprites/Special14.png", 0.1), ("data/sprites/Special15.png", 0.1),
             ("data/sprites/Special16.png", 0.1), ("data/sprites/Special17.png", 0.1), ("data/sprites/Special18.png", 0.1),
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
        self.ui1 = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
        self.ui2 = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
        self.cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.cursormax = 2
        self.uitext = pygame.font.Font("data/fonts/runescape_uf.ttf", 30)  # Default font for Ui
        self.uitext2 = pygame.font.Font("data/fonts/Vecna.otf", 30)  # font for damage
        self.burstdesc = self.uitext.render('Greatly strengthens next attack for 1 turn. MP COST:15', False,
                                            (37, 61, 36))
        self.firedesc = self.uitext.render('Deal small Fire damage to the enemy. MP COST:5', False, (37, 61, 36))
        self.icedesc = self.uitext.render('Deal small Ice damage to the enemy. MP COST:10', False, (37, 61, 36))
        self.curedesc = self.uitext.render('Restores a small amount of health. MP COST:15', False, (37, 61, 36))
        self.deathdesc = self.uitext.render(
            'Invokes death upon your foe. Chance of instantly killing your enemy. MP COST:30', False, (37, 61, 36))
        self.tsunamidesc = self.uitext.render(
            'Creates a devastating flood and deals massive Water damage to enemies. MP COST:50', False, (37, 61, 36))
        self.potiondesc = self.uitext.render('Heals 50 Health', False, (37, 61, 36))
        self.atk = self.uitext.render('Attack', False, self.txtcolor).convert_alpha()
        self.mag = self.uitext.render('Magic', False, self.txtcolor).convert_alpha()
        self.ski = self.uitext.render('Skill', False, self.txtcolor).convert_alpha()
        self.item = self.uitext.render('Item', False, self.txtcolor).convert_alpha()
        self.cancel = self.uitext.render('Cancel', False, self.txtcolor).convert_alpha()
        self.crittxt = self.uitext2.render('Critical!', False, (200, 0, 0)).convert_alpha()
        self.nametext = self.uitext.render(self.pname, False, (61, 61, 58)).convert_alpha()
        self.hptxt = self.uitext.render('HP:', True, (255, 21, 45)).convert_alpha()
        self.mptxt = self.uitext.render('MP:', True, (29, 21, 255)).convert_alpha()
        self.notlearnedtxt = self.uitext.render('Not learned yet!', True, (255, 21, 45)).convert_alpha()
        self.victoryflag = False
        self.defeatflag = False
        self.bgtxt = self.uitext.render('', False, self.txtcolor).convert_alpha()  # Action bg txt
        self.bgflag = False  # action bg flag
        self.actionbg = pygame.transform.scale(self.ui1, (300, 50))
        self.vicimg = pygame.image.load("data/sprites/victory.png").convert_alpha()
        self.mdeathresist = False  # Check if monster resists the 'death' spell or not
        self.extraheight = 0  # Extra height for position of monster image if needed
        self.hpbarEmpty = pygame.image.load("data/sprites/hpbar1.png").convert_alpha()
        self.hpbarFull = pygame.image.load("data/sprites/hpbar2.png").convert_alpha()

        self.virtualMonsterHealth = self.mhealth  # 'Virtual Health' of monster, for the displaying of hp on the hp bar.
        self.post_victory = False

    def getitems(self):
        self.itemtxtlist = []
        self.itemlist = []
        if not self.gotitems:
            for item in self.inventory:
                if self.inventory[item] > 0:
                    txt = self.uitext.render(str(item) + '   x' + str(self.inventory[item]), False, self.txtcolor)
                    self.itemtxtlist.append(txt)
                    self.itemlist.append(item)
            self.gotitems = True

    def getskills(self):
        if not self.gotskills:
            self.skitxt = self.uitext.render(self.skilllist[0], False, self.txtcolor)
            self.gotskills = True

    def getmagic(self):
        if not self.gotmagic:
            if self.plevel >= 5:
                self.magtxt1 = self.uitext.render(self.magic[0], False, self.txtcolor)
            else:
                self.magtxt1 = self.uitext.render(self.magic[0], False, (105, 109, 114))
            if self.plevel >= 8:
                self.magtxt2 = self.uitext.render(self.magic[1], False, self.txtcolor)
            else:
                self.magtxt2 = self.uitext.render(self.magic[1], False, (105, 109, 114))
            if self.plevel >= 12:
                self.magtxt3 = self.uitext.render(self.magic[2], False, self.txtcolor)
            else:
                self.magtxt3 = self.uitext.render(self.magic[2], False, (105, 109, 114))
            if self.plevel >= 18:
                self.magtxt4 = self.uitext.render(self.magic[3], False, self.txtcolor)
            else:
                self.magtxt4 = self.uitext.render(self.magic[3], False, (105, 109, 114))
            if self.plevel >= 20:
                self.magtxt5 = self.uitext.render(self.magic[4], False, self.txtcolor)
            else:
                self.magtxt5 = self.uitext.render(self.magic[4], False, (105, 109, 114))
            self.gotmagic = True

    def calcdamage(self, dmgtype='normal'):
        # calculates player damage during players turn and enemies damage during the enemies turn.
        if dmgtype == 'fire':
            damage = self.pmag * (100 / (100 + self.mdef)) - random.randrange(0, 10)
        if dmgtype == 'ice':
            damage = self.pmag * (100 / (100 + self.mdef)) - random.randrange(0, 10)
        if dmgtype == 'water':
            damage = (self.pmag * 3) * (100 / (100 + self.mdef)) - random.randrange(0, 10)
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
                    damage = (self.pstr * (100 / (100 + self.mdef))) * 5 - random.randrange(0, 10)
                elif self.crit == 10:
                    damage = (self.pstr * (100 / (100 + self.mdef))) * 4 - random.randrange(0, 10)
                else:
                    damage = (self.pstr * (100 / (100 + self.mdef))) * 2 - random.randrange(0, 10)
        elif self.state == 'enemyattack':
            if self.attack == 'attack':
                damage = self.mstr * (100 / (100 + self.pdef)) - random.randrange(0, 10)
            if dmgtype == 'thunder':  # temp make sure to change
                damage = self.mmag * (100 / (100 + self.pdef)) - random.randrange(0, 10)
        print(self.state)
        if damage < 0:
            damage = 0
        elif damage > 99999:
            damage = 99999
        return int(damage)

    def statuswindow(self):  # The main UI during the battle. Needs some work
        self.nametext = self.uitext.render(self.pname, False, (61, 61, 58)).convert_alpha()

        curhealth = self.uitext.render(str(self.curphealth) + '/' + str(self.phealth), False, (114, 21, 45))

        curmana = self.uitext.render(str(self.curpmana) + '/' + str(self.pmana), False, (29, 21, 114))

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
        surf.blit(pygame.transform.scale(self.hpbarEmpty, (260, 18)), (self.monpos[0], self.monpos[1] + 100 - animpos))
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

    def defeat(self):  # raises the defeat flag,ends the match when set to true and sends player back to main menu.
        timer = Timer()
        pygame.mixer.music.pause()
        pygame.mixer.music.load('data/sounds&music/Gameover2.ogg')
        pygame.mixer.music.play()
        dark = pygame.Surface(surf.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark, (0, 0))

        deftxt = pygame.font.Font("data/fonts/Daisy_Roots.otf", 70)
        defeat = deftxt.render('Defeat!', True, (255, 0, 0)).convert_alpha()
        cont = self.uitext.render('Your journey isn\'t over yet! Move onward!', True, (255, 255, 0)).convert_alpha()
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

    def victory(self):  # raises the victory flag,ends the match when set to true.
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
                        pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
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

    def getplayerdetails(self, player=Player()):  # Method to get the players current stats and other details.
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
        self.monsters = pygame.image.load(self.mondata[monster_name]['sprites']).convert_alpha()
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
            surf.blit(pygame.transform.scale(self.bg, (curwidth, curheight)), (0, 0))

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
                if event.type == VIDEORESIZE:
                    screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    surf.blit(pygame.transform.scale(surf, (curwidth, curheight)), (0, 0))
                    self.monpos = (curwidth - 1080, 270)
                    if curwidth - 1080 <= 0:
                        self.monpos = (0, 270)
                    pygame.display.flip()
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

            self.battleflow.timing()  # battleflow timer - controls flow of battle(animations,timing,etc.)
            self.mhurt.blit(surf, [curwidth - 331, 280])
            self.slashanim.blit(surf, self.monpos)
            self.clawanim.blit(surf, [curwidth - 381, 255])
            self.specialanim.blit(surf, [curwidth - 381, 255])
            self.thunderanim.blit(surf, [curwidth - 381, 255])
            self.castanim.blit(surf, [curwidth - 409, 200])
            self.fireanim.blit(surf, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.iceanim.blit(surf, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.deathanim.blit(surf, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.wateranim.blit(surf, (self.monpos[0], (self.monpos[1] + 100) - self.extraheight))
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
                self.bgtxt = self.uitext.render('Tsunami', False, self.txtcolor)
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
            if self.pstatus == 'deathcast' and self.state == 'deathcasting':  # Death(magic)
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
                surf.blit(dmgtxt, (self.monpos[0] + 100, self.monpos[1] - dmgtxtpos))  # damage text after spell cast
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
                        dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))
                        critted = True
                        screen.blit(surf, (0, 0))
                        attackedp = True
                        print(critted)

                    if (attackedp == False and self.crit != 10) or (attackedp == False and self.pstatus == 'burst'):
                        self.slashanim.play()
                        self.attacksound.play()
                        dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))
                        attackedp = True
                    if dmgtxtpos < 35:
                        dmgtxtpos += 5
                    if hpbarpos < 100:
                        hpbarpos += 10
                    surf.blit(dmgtxt, (self.monpos[0] + 100, self.monpos[1] - dmgtxtpos))
                    self.healthbar(hpbarpos)
                    screen.blit(surf, (0, 0))

                if critted:
                    surf.blit(self.crittxt, (self.monpos[0] + 100, self.monpos[1] - 70))
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
                    elif self.enemymovelist[move] == 'thunder':  # enemy casting thunder
                        attacked = True
                        enemyskill = 'thunder'
                        self.bgtxt = self.uitext.render('Thunder', False, self.txtcolor)
                        self.bgflag = True

                self.state = 'enemyattack'
                if self.battleflow.timing() == 2 and attackdone == False:
                    if not attacked:
                        self.clawanim.play()
                        self.attacksound2.play()
                        dmg = self.calcdamage()
                        dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))
                        attacked = True

                    if enemyskill == 'thunder':
                        self.thunderanim.play()
                        self.thundersound.play()
                        dmg = self.calcdamage('thunder')
                        dmgtxt = self.uitext2.render(str(dmg), True, (255, 255, 255))
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
                    self.battleflow.reset
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
    """The new battle system written from the ground up. About time."""

    def __init__(self, monsterdata, itemdata, sounddata, animationdata, skilldata):
        #  Data
        self.monster_data = monsterdata
        self.consumable_data = itemdata['consumables']
        self.weapon_data = itemdata['weapons']
        self.sound_data = sounddata['battle']
        self.animation_data = animationdata
        self.skill_data = skilldata
        self.warrior_skills = skilldata['warrior']
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
        self.f_gold = 0
        self.f_exp = 0
        self.m_gold = 0
        self.m_move_list = []
        self.m_status = []
        self.m_weakness = []
        #  Ui elements and etc.
        self.draw_menu = True
        self.ui_bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
        self.ui_font = pygame.font.Font("data/fonts/alagard.ttf", 25)
        self.title_font = pygame.font.Font("data/fonts/Daisy_Roots.otf", 25)
        self.dmg_font = pygame.font.Font("data/fonts/Vecna.otf", 30)
        self.ui_text = ["Menu", "Attack", "Skill", "Item", "HP:", "MP:", "Info", "MP Cost:", "Level required:"]
        self.atk_txt = self.ui_font.render(self.ui_text[1], True, (200, 200, 200))
        self.skill_txt = self.ui_font.render(self.ui_text[2], True, (200, 200, 200))
        self.item_txt = self.ui_font.render(self.ui_text[3], True, (200, 200, 200))
        self.lvl_up_txt = self.ui_font.render('Level Up!', True, (120, 240, 66))
        self.stat_up_txt = self.ui_font.render('All stats up!', True, (110, 255, 66))
        self.player_x = 920  # Rough x coordinate of player on screen (For animations)
        self.player_y = 270
        self.add_flag = False  # flag for the gold and exp adding up on the victory screen
        self.dmg_txt = '0'
        self.cursor = pygame.image.load("data/sprites/Cursor.png")
        self.vic_img = pygame.image.load("data/sprites/victory.png").convert_alpha()
        self.def_font = pygame.font.Font("data/fonts/Daisy_Roots.otf", 70)
        self.current_title = 0
        #  Sound effects
        self.sound_effect = ''
        self.cursor_sound = pygame.mixer.Sound(sounddata['system']['cursor'])
        self.buzzer_sound = pygame.mixer.Sound(sounddata['system']['buzzer'])
        #  State control
        self.battling = True
        self.turn = 'player'
        self.game_state = 'player'
        self.ui_state = 'main'
        self.ui_flag = True
        self.player_flag = True
        self.monster_flag = True
        self.focus = False
        self.focus_target = 'player'
        self.cursor_pos = 0
        self.cursor_max = 3
        self.hover_skill = 0  # What skill is currently being hovered by the cursor.
        self.global_timer = Timer()
        self.camera_x = 0
        self.camera_y = 0
        #  Temp stuff remove later
        self.crit_chance = 1
        self.loaded_anim = pyganim.PygAnimation(
            [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        self.anim_pos = [300, 300]
        # Loaded animation for the animation function
        self.player_sprites = pyganim.PygAnimation(
            [("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])
        self.player_sprites.play()
        self.death_sprite = pygame.image.load("data/sprites/death.png").convert_alpha()  # player death sprite
        self.player_pos = 1200
        self.window_pos = 1400
        self.initial_window_pos = 0  # For the description window
        self.monster_pos = -1600
        self.shake = False
        #  images to load
        self.battle_ui = pygame.transform.scale(pygame.image.load("data/backgrounds/battle_menu.png").convert_alpha(),
                                                (175, 200))
        self.battle_ui2 = pygame.transform.scale(pygame.image.load("data/backgrounds/battle_menu.png").convert_alpha(),
                                                (500, 200))
        self.battle_ui3 = pygame.transform.scale(pygame.image.load("data/backgrounds/UiElement.png").convert_alpha(),
                                                 (400, 400))# player info ui
        self.title_bar = pygame.image.load("data/backgrounds/titlebar.png").convert_alpha()
        self.background = ""
        self.hp_bar_Empty = pygame.image.load("data/sprites/hpbar1.png").convert_alpha()
        self.hp_bar_Full = pygame.image.load("data/sprites/hpbar2.png").convert_alpha()
        self.virtualMonsterHealth = self.m_cur_health
        self.skill_min = 0  # The minimum value for the top position of the skill selection window
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
                                    self.skill_min = len(self.skill_data[self.p_class]) - 4
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
                        elif self.ui_state == 'skill':
                            if self.cursor_pos == 0:
                                pass
                    if event.key == pygame.K_RCTRL:
                        if self.ui_state == 'skill':
                            self.ui_state = 'main'
                            self.cursor_pos = 0

                if self.game_state == 'victory' or self.game_state == 'defeat_done':
                    if event.key == pygame.K_RETURN or event.key == pygame.K_RCTRL:
                        if self.game_state == 'victory':
                            if self.f_exp != self.m_exp or self.f_gold != self.m_gold:
                                self.f_exp = self.m_exp
                                self.f_gold = self.m_gold
                            elif self.f_exp == self.m_exp:
                                self.battling = False
                        else:
                            self.battling = False
                            fadeout(surf, 0.001)

    def draw_sprites(self):
        surf.blit(self.background, (0, 0))
        if self.player_flag:
            self.player_sprites.blit(surf, (self.player_pos, 300))
            if self.player_pos > 950:
                self.player_pos -= 50
        if self.monster_flag:
            surf.blit(self.m_sprite, (self.monster_pos, 300))
            self.loaded_anim.blit(surf, self.anim_pos)  # Loaded animation
            if self.monster_pos < 200:
                self.monster_pos += 50

    def play_sound(self, sound):
        self.sound_effect = pygame.mixer.Sound(self.sound_data[sound])
        self.sound_effect.play()

    def play_animation(self, animation, pos=(920, 270)):
        self.loaded_anim = pyganim.PygAnimation(self.animation_data[animation], False)
        self.anim_pos = pos
        self.loaded_anim.play()

    def check_state(self):
        """Keeps track of the game state"""
        if self.game_state == 'player_attack':  # Player regular attack
            player_attacking = False
            if self.global_timer.timing(1) >= 0.4 and not player_attacking:
                self.play_animation('slash', (self.monster_pos, 300))
                self.play_sound('slash')
                dmg = self.calc_damage(self.turn, 'attack')
                self.dmg_txt = self.dmg_font.render(str(dmg), True, (200, 200, 200))
                self.m_cur_health -= dmg
                player_attacking = True
                self.game_state = 'player_attack_done'
                self.global_timer.reset()
        if self.game_state == 'player_attack_done':  # Player regular attack is done
            surf.blit(self.dmg_txt, (self.monster_pos, 270))
            self.draw_healthbar(self.m_cur_health)
            if self.global_timer.timing(1) >= 1.5 and self.virtualMonsterHealth == self.m_cur_health:
                self.turn = 'enemy'
                self.game_state = 'enemy_turn'
                self.global_timer.reset()
        if self.game_state == 'enemy_turn' and self.m_cur_health > 0:  # Enemy turn begins
            choose_move = random.randrange(0, len(self.m_move_list))
            enemy_action = self.m_move_list[choose_move]
            if enemy_action == 'attack':
                self.game_state = 'enemy_attack'
                self.global_timer.reset()
        if self.game_state == 'enemy_attack':  # Enemy regular attack
            enemy_attacking = False
            if self.global_timer.timing(1) >= 0.4 and not enemy_attacking:
                self.play_animation('claw', (self.player_pos, 300))
                self.play_sound('slash2')
                dmg = self.calc_damage(self.turn, 'attack')
                self.dmg_txt = self.dmg_font.render(str(dmg), True, (200, 200, 200))
                self.p_health -= dmg
                enemy_attacking = True
                self.game_state = 'enemy_attack_done'
                self.global_timer.reset()
        if self.game_state == 'enemy_attack_done':  # Enemy regular attack done
            surf.blit(self.dmg_txt, (self.player_pos, 270))
            if self.global_timer.timing(1) >= 1.5:
                self.turn = 'player'
                self.game_state = ''
                self.draw_menu = True
                self.ui_state = 'main'
        if self.game_state == 'enemy_death' and self.global_timer.timing(1) >= 1.5:  # Enemy dies
            self.monster_flag = False
            self.play_sound('enemy_dead')
            self.game_state = 'victory'
            self.global_timer.reset()
        if self.game_state == 'victory' and self.global_timer.timing(1) >= 1:  # Victory state
            self.victory()
        if self.game_state == 'defeat_done':
            surf.blit(self.death_sprite, (self.player_x + 20, self.player_y + 20))
            if self.global_timer.timing(1) >= 1:
                self.defeat()
        if self.p_health <= 0 and self.game_state != 'defeat_done':
            self.player_sprites.stop()
            surf.blit(self.death_sprite, (self.player_x, self.player_y))
            self.game_state = 'defeat_done'
            self.global_timer.reset()
        if 0 >= self.m_cur_health == self.virtualMonsterHealth and self.game_state != 'victory':
            if self.global_timer.timing(1) >= 1.5:
                self.game_state = 'enemy_death'
        if self.m_cur_health > self.m_max_health:
            self.m_cur_health = self.m_max_health
        if self.m_cur_health < 0:
            self.m_cur_health = 0

    def skill_anim(self, skill, target):
        """Plays the animation and sound for the skill"""
        if skill == 'burst':
            if target == 'player':
                self.play_animation('burst')
                self.play_sound('ice')  # test sound change later

    def skill_logic(self, skill, target):
        if skill == 'burst':
            self.p_status.append('burst')
            self.skill_anim('burst', target)

    def draw_cursor(self):
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
        if self.cursor_pos > self.cursor_max:
            self.cursor_pos = 0
        if self.cursor_pos < 0:
            self.cursor_pos = self.cursor_max

    def draw_healthbar(self, cur_health):  # Enemy health bar
        if cur_health > self.virtualMonsterHealth:
            self.virtualMonsterHealth += 1
        elif cur_health < self.virtualMonsterHealth:
            if self.virtualMonsterHealth % 5 == 0 and not self.virtualMonsterHealth - 5 < cur_health:
                self.virtualMonsterHealth -= 5
            else:
                self.virtualMonsterHealth -= 1
        health_percent = (self.virtualMonsterHealth / self.m_max_health) * 100
        if health_percent < 0:
            health_percent = 0.1
        surf.blit(pygame.transform.scale(self.hp_bar_Empty, (260, 18)), (self.monster_pos, 300))
        surf.blit(pygame.transform.scale(self.hp_bar_Full, (int(246 * (health_percent / 100)), 18)),
                  (self.monster_pos + 7, 301))

    def draw_ui(self):
        surf.blit(self.battle_ui, (self.window_pos, 400))
        surf.blit(self.battle_ui3, (self.window_pos - 50, -70))
        if self.window_pos > 900:
            self.window_pos -= 50
        if self.window_pos <= 900:  # when the 'animation' finishes
            hp_text = self.ui_font.render("HP: %d/%d" % (self.p_health, self.p_max_health), True, (230, 0, 50))
            mp_text = self.ui_font.render("MP: %d/%d" % (self.p_mana, self.p_max_mana), True, (20, 0, 230))

            surf.blit(hp_text, (930, 100))  # Text for hp
            surf.blit(mp_text, (930, 130))  # Text for mp
            if self.ui_state == 'main':
                self.current_title = 0
                surf.blit(self.atk_txt, (945, 475))
                surf.blit(self.skill_txt, (945, 500))
                surf.blit(self.item_txt, (945, 525))
            if self.ui_state == 'skill':    # Skill selection
                self.current_title = 2
                cur_mp_cost = self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['mp_cost']
                self.skill_desc = self.ui_font.render(self.skill_data[self.p_class][self.skill_min + self.cursor_pos]['desc'], True, (200, 200, 200))
                surf.blit(self.battle_ui2, (self.initial_window_pos, 400))
                skill_text1 = self.ui_font.render(self.skill_data[self.p_class][self.skill_min]['name'], True, (200, 200, 200))
                skill_text2 = self.ui_font.render(self.skill_data[self.p_class][self.skill_min + 1]['name'], True, (200, 200, 200))
                skill_text3 = self.ui_font.render(self.skill_data[self.p_class][self.skill_min + 2]['name'], True, (200, 200, 200))
                skill_text4 = self.ui_font.render(self.skill_data[self.p_class][self.skill_min + 3]['name'], True, (200, 200, 200))
                surf.blit(skill_text1, (915, 475))
                surf.blit(skill_text2, (915, 500))
                surf.blit(skill_text3, (915, 525))
                surf.blit(skill_text4, (915, 550))
                if self.initial_window_pos < 300:
                    self.initial_window_pos += 30
                if self.initial_window_pos == 300:
                    surf.blit(self.skill_desc, (340, 480))
                    title_text2 = self.title_font.render(self.ui_text[6], True, (200, 30, 30))
                    surf.blit(title_text2, (520, 413))
                    mp_cost_txt = self.ui_font.render("Mp Cost: %d" % cur_mp_cost, True, (200, 60, 130))
                    surf.blit(mp_cost_txt, (340, 540))
            title_text = self.title_font.render(self.ui_text[self.current_title], True, (200, 30, 30))  # Title for the ui
            surf.blit(title_text, (959, 412))

    def get_monster_details(self, monster_name):
        self.m_max_health = monster_data[monster_name]['health']
        self.m_cur_health = self.m_max_health
        self.virtualMonsterHealth = self.m_cur_health
        self.m_str = monster_data[monster_name]['str']
        self.m_def = monster_data[monster_name]['def']
        self.m_mag = monster_data[monster_name]['mag']
        self.m_sprite = pygame.image.load(monster_data[monster_name]['sprites'])
        self.m_move_list = monster_data[monster_name]['move_list']
        self.m_gold = monster_data[monster_name]['gold']
        self.m_exp = monster_data[monster_name]['exp']
        self.background = pygame.transform.scale(pygame.image.load(monster_data[monster_name]['bg']).convert_alpha(),
                                                 (1280, 720))
        self.m_weakness = monster_data[monster_name]['weakness']

    def calc_damage(self, turn, atk_type='atk'):
        # WIP CHANGE A LOT OF THINGS
        element = 'Normal'
        if turn == 'player':
            if atk_type == 'fire':
                element = 'fire'
                damage = self.p_mag * (100 / (100 + self.m_def)) - random.randrange(0, 10)
            elif atk_type == 'ice':
                damage = self.p_mag * (100 / (100 + self.m_def)) - random.randrange(0, 10)
            elif atk_type == 'water':
                damage = (self.p_mag * 3) * (100 / (100 + self.m_def)) - random.randrange(0, 10)
            elif atk_type == 'cure':  # Not really damage but eh
                damage = ((self.p_max_health * 10) / 35) - random.randrange(0, 6)
            elif atk_type == 'attack':
                self.crit_chance = random.randrange(self.p_luck, 11)  # will always crit with 10 luck.
                if self.p_luck >= 10:
                    self.crit_chance = 10
                print(self.crit_chance)
                #  if self.p_status == 'burst':  # Warrior burst skill takes priority over a crit
                #   damage = (self.pstr * (100 / (100 + self.mdef))) * 5 - random.randrange(0, 10)
                if self.crit_chance == 10:
                    damage = (self.p_str * (100 / (100 + self.m_def))) * 4 - random.randrange(0, 10)
                else:
                    damage = (self.p_str * (100 / (100 + self.m_def))) * 2 - random.randrange(0, 10)
                """elif atk_type == 'death':
                            if self.mdeathresist:
                                return 'Resist!'
                            else:
                                death_luck = random.randrange(1, 6)  # 1 in 5 chance of success
                                print('Death_luck:', death_luck)
                                if death_luck == 5:
                                    damage = 99999
                                else:
                                    return 'Failed!' """
        elif turn == 'enemy':
            if atk_type == 'attack':
                damage = self.m_str * (100 / (100 + self.p_def)) - random.randrange(0, 10)
            if atk_type == 'thunder':  # temp make sure to change
                damage = self.m_mag * (100 / (100 + self.p_def)) - random.randrange(0, 10)
        if damage < 0:
            damage = 0
        elif damage > 99999:
            damage = 99999
        if element in self.m_weakness:  # If enemy is weak to the element
            damage *= 2
        return int(damage)

    def shake_screen(self):
        self.camera_x, self.camera_y = random.randrange(-5, 5), random.randrange(-5, 5)

    def victory(self):
        if not self.add_flag:
            self.f_gold = 0
            self.f_exp = 0
            self.add_flag = True
            pygame.mixer.music.pause()
            pygame.mixer.music.load('data/sounds&music/Victory_and_Respite.mp3')  # victory music
            pygame.mixer.music.play()
        dark_surf = pygame.Surface(surf.get_size(), 32)  # making a transparent dark surface
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark_surf, (0, 0))
        gold_txt = self.ui_font.render('Gold:+%d' % self.f_gold, True, (255, 255, 0))
        exp_txt = self.ui_font.render('Exp:+%d' % self.f_exp, True, (244, 240, 66))
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

    def defeat(self):
        if not self.add_flag:
            pygame.mixer.music.pause()
            pygame.mixer.music.load('data/sounds&music/Gameover2.ogg')  # defeat music
            pygame.mixer.music.play()
            self.add_flag = True
        dark_surf = pygame.Surface(surf.get_size(), 32)  # making a transparent dark surface
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark_surf, (0, 0))
        defeat = self.def_font.render('Defeat!', True, (255, 0, 0)).convert_alpha()
        cont = self.ui_font.render('Your journey isn\'t over yet! Move onward!', True, (255, 255, 0)).convert_alpha()
        surf.blit(defeat, (curwidth / 3, curheight / 5))
        surf.blit(cont, (curwidth / 3, curheight / 5 + 100))

    def set_instance(self, player_data=Player()):
        """Resets/sets the instance"""
        self.reset_cam()
        self.game_state = ""
        self.ui_state = "main"
        self.turn = "player"
        self.p_name = player_data.name
        self.p_level = player_data.level
        self.p_max_health = player_data.hp
        self.p_health = player_data.curhp
        self.p_max_mana = player_data.mp
        self.p_mana = player_data.curmp
        self.p_str = player_data.stre
        self.p_def = player_data.defe
        self.p_mag = player_data.mag
        self.p_luck = player_data.luck
        self.p_class = player_data.pclass
        self.p_status = []

    def battle(self, monster_name, set_music=0, player_data=Player()):
        #  Main loop, starts the battle
        alpha = text.render(alphatext, False, (255, 255, 0))
        self.battling = True
        self.monster_flag = True
        self.draw_menu = True
        self.add_flag = False
        self.get_monster_details(monster_name)
        self.play_sound('encounter')
        self.set_instance(player_data)
        fadein(255)
        if set_music == 0:
            pygame.mixer_music.load("data/sounds&music/03_Endless_Battle.ogg")
            pygame.mixer_music.play()
        else:
            pygame.mixer_music.load("data/sounds&music/03_Endless_Battle.ogg")
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
            self.check_state()  # To check the current game state
            self.check_inputs()
            surf.blit(alpha, (0, 0))
            screen.blit(surf, (self.camera_x, self.camera_y))
            pygame.display.update()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)


class TextBox:
    """The textbox class, used to draw textboxes and anything related to dialogue."""

    def __init__(self, txtcolor=(21, 57, 114), convo_flag=False):
        self.bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()  # Ui background
        self.txtcolor = txtcolor  # Default font colour
        self.txtcolor2 = (23, 18, 96)
        self.uitext = pygame.font.Font("data/fonts/runescape_uf.ttf", 33)  # Default font
        self.uitext2 = pygame.font.Font("data/fonts/runescape_uf.ttf", 25)  # Choice selection font
        self.cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.ch_cursorpos = 0  # Position of cursor for choice selection
        self.dialogue_progress = 0  # Current 'Progress' of the dialogue
        self.txtbox_height = 300
        self.popup_flag = False  # Flag for popup animation
        self.popup_done = False  # Check if the popup animation is done or not
        self.convo_flag = convo_flag  # if it is a conversation(aka story part) the popup animation won't repeat

    def select_choice(self, choice1, choice2, choice3=None):  # Select a choice between 2 or 3 options
        if choice3 is not None:
            surf.blit(pygame.transform.scale(self.bg, (300, 150)),
                      (916, 276))  # Adjusting size of textbox based on whether there are 3 or 2 choices.
        else:
            surf.blit(pygame.transform.scale(self.bg, (300, 125)), (916, 276))
        ch1 = self.uitext2.render(choice1, False, self.txtcolor)
        ch2 = self.uitext2.render(choice2, False, self.txtcolor)
        surf.blit(ch1, (960, 309))
        surf.blit(ch2, (960, 339))
        if self.ch_cursorpos == 0:  # Choice 1
            surf.blit(self.cursor, (930, 309))
        if self.ch_cursorpos == 1:  # Choice 2
            surf.blit(self.cursor, (930, 339))
        if choice3 is not None:
            ch3 = self.uitext2.render(choice3, False, self.txtcolor)
            surf.blit(ch3, (960, 369))
            if self.ch_cursorpos == 2:
                surf.blit(self.cursor, (930, 369))
        if self.ch_cursorpos > 1:
            self.ch_cursorpos = 0
        elif self.ch_cursorpos < 0:
            self.ch_cursorpos = 1

    def popup_reset(self):
        self.popup_flag = False
        self.popup_done = False

    def popup(self):  # popup animation for the text box
        if not self.popup_flag:
            self.txtbox_height = 0
        self.popup_flag = True
        if self.popup_flag and self.txtbox_height < 300:
            self.txtbox_height += 50
        if self.txtbox_height >= 300:
            self.popup_done = True

    def draw_textbox(self, pic=None, name='', line1='', line2='', line3='', line4='', line5='',
                     line6='Press RCTRL to continue...'):
        surf.blit(pygame.transform.scale(self.bg, (curwidth, self.txtbox_height)), (0, 430))
        if not self.popup_done:
            self.popup()
        if self.popup_done:
            if pic is not None:
                speaker = pygame.image.load(pic).convert_alpha()
                surf.blit(speaker, (110, 490))
                nameplate = self.uitext.render(name, True, (255, 21, 45))
                surf.blit(nameplate, (131, 655))  # Where the name of the speaker goes
                picoff = 0
            elif pic is None:
                picoff = 100  # When there is no pic the text starts from the leftmost box(AKA narrator mode)
            # Different rows of text for the txtbox(could be made more elegant,pygame text rendering is pretty annoying)
            row1 = self.uitext.render(line1, False, self.txtcolor)
            surf.blit(row1, (270 - picoff, 490))
            row2 = self.uitext.render(line2, False, self.txtcolor)
            surf.blit(row2, (270 - picoff, 520))
            row3 = self.uitext.render(line3, False, self.txtcolor)
            surf.blit(row3, (270 - picoff, 550))
            row4 = self.uitext.render(line4, False, self.txtcolor)
            surf.blit(row4, (270 - picoff, 580))
            row5 = self.uitext.render(line5, False, self.txtcolor)
            surf.blit(row5, (270 - picoff, 610))
            row6 = self.uitext.render(line6, False, self.txtcolor2)
            surf.blit(row6, (270 - picoff, 640))


drawui = True  # Flag to signify whether to draw the ui or not,


# used to hide ui during dialogue or any other scenes(the main UI during which the player has control outside of battle)


class MainUi:
    """The Main UI of the game(outside of battle.)"""

    def __init__(self):
        self.bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
        self.txtcolor = (21, 57, 114)
        self.txtcolor2 = (117, 17, 67)
        self.txtcolor3 = (23, 18, 96)
        self.uitext = pygame.font.Font("data/fonts/runescape_uf.ttf", 35)
        self.uitext2 = pygame.font.Font("data/fonts/runescape_uf.ttf", 25)  # Smaller font for longer sentences
        self.cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.cursorsound = pygame.mixer.Sound('data/sounds&music/Cursor1.ogg')
        self.cursorpos = 0
        self.talktxt = self.uitext.render('Talk', False, self.txtcolor)
        self.talkdesc = self.uitext.render('Talk with people around the Arena.', False, self.txtcolor)
        self.talkdesc2 = self.uitext.render('Talk with people around the Inn.', False, self.txtcolor)
        self.talkdesc3 = self.uitext.render('Talk with people around the Town.', False, self.txtcolor)
        self.battxt = self.uitext.render('Battle', False, self.txtcolor)
        self.batdesc = self.uitext.render('Battle monsters in the Arena.', False, self.txtcolor)
        self.systxt = self.uitext.render('System', False, self.txtcolor)
        self.sysdesc = self.uitext.render('System options.', False, self.txtcolor)
        self.inntxt = self.uitext.render('Inn', False, self.txtcolor)
        self.inndesc = self.uitext.render('Go to the Inn.', False, self.txtcolor)
        self.shoptxt = self.uitext.render('Shop', False, self.txtcolor)
        self.slumstxt = self.uitext.render('Slums', False, self.txtcolor)
        self.slumsdesc = self.uitext.render('Go to the Slums.', False, self.txtcolor)
        self.shopdesc = self.uitext.render('Buy items/equipment to use in the Arena.', False, self.txtcolor)
        self.stattxt = self.uitext.render('Status', False, self.txtcolor)
        self.statdesc = self.uitext.render('Check player status/equipment', False, self.txtcolor)
        self.backtxt = self.uitext.render('Leave', False, self.txtcolor)
        self.backdesc = self.uitext.render('Return to the Arena', False, self.txtcolor)
        self.sleeptxt = self.uitext.render('Rest', False, self.txtcolor)
        self.sleepdesc = self.uitext.render('Spend the night at the Inn. (20 Gold)', False, self.txtcolor)
        self.txtbox = TextBox()
        self.statustxt = self.uitext.render('- STATUS -', True, self.txtcolor)
        self.face = pygame.image.load("data/sprites/f1.png").convert_alpha()
        self.wepicon = pygame.image.load("data/sprites/wepicon.png").convert_alpha()
        self.armicon = pygame.image.load("data/sprites/armicon.png").convert_alpha()
        self.accicon = pygame.image.load("data/sprites/accicon.png").convert_alpha()
        self.sunIcon = pygame.image.load("data/sprites/sun.png").convert_alpha()  # Icon for clock
        self.eveIcon = pygame.image.load("data/sprites/eve.png").convert_alpha()  # Icon for clock
        self.moonIcon = pygame.image.load("data/sprites/moon.png").convert_alpha()  # Icon for clock
        self.talked = False
        self.coinAnim = pyganim.PygAnimation(
            [("data/sprites/coin1.png", 0.1), ("data/sprites/coin2.png", 0.1), ("data/sprites/coin3.png", 0.1),
             ("data/sprites/coin4.png", 0.1), ("data/sprites/coin5.png", 0.1), ("data/sprites/coin6.png", 0.1),
             ("data/sprites/coin7.png", 0.1), ("data/sprites/coin8.png", 0.1), ("data/sprites/coin9.png", 0.1)])
        self.coinAnim.play()
        self.shopkeep = True
        self.loaditems = False
        self.buysound = pygame.mixer.Sound('data/sounds&music/Shop1.ogg')
        self.shoplist = {'Potion': 20, 'Iron Sword': 60, 'Iron Armour': 100}
        self.Talk = -1
        self.sysopt1 = self.uitext.render('Save Game', False, self.txtcolor)
        self.sysopt2 = self.uitext.render('Quit Game', False, self.txtcolor)
        self.sysopt3 = self.uitext.render('Cancel', False, self.txtcolor)
        self.syscursorpos = 0
        self.savesound = pygame.mixer.Sound('data/sounds&music/Save.ogg')
        self.batopt1 = self.uitext.render('Fight a regular enemy', False, self.txtcolor)
        self.battalk = True
        self.batcursorpos = False
        self.pb_dialogue = False
        self.pbtalk = 0

    def arena(self, floor=1):  # Main ui in the arena
        surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 1.5), 300)), (0, 430))
        surf.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 48))
        surf.blit(pygame.transform.scale(self.bg, (300, 300)), (905, 430))
        surf.blit(self.talktxt, (946, 496))
        surf.blit(self.battxt, (946, 526))
        surf.blit(self.stattxt, (946, 556))
        surf.blit(self.shoptxt, (946, 586))
        surf.blit(self.inntxt, (946, 616))
        surf.blit(self.systxt, (946, 646))
        self.cur = self.uitext.render('Floor:  %d' % floor, False, self.txtcolor)  # Current floor
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
            minutes = '00'  # Double zeros because thats how clocks work
        timetxt = str(hours) + ':' + str(minutes)
        self.time = self.uitext.render(timetxt, False, self.txtcolor)
        surf.blit(pygame.transform.scale(self.bg, (150, 50)), (10, 81))
        surf.blit(self.time, (27, 94))
        if hours >= 6 and hours < 14:  # Day
            surf.blit(pygame.transform.scale(self.sunIcon, (40, 30)), (90, 93))
        if hours >= 14 and hours < 20:  # Afternoon
            surf.blit(pygame.transform.scale(self.eveIcon, (20, 30)), (90, 93))
        if hours >= 20 or hours < 6:  # Night
            surf.blit(pygame.transform.scale(self.moonIcon, (35, 25)), (90, 97))

    def talk(self, val):
        global drawui
        drawui = False
        self.Talk = val
        if not self.talked:
            if self.Talk == 0 and player.progress == 1:

                self.txtbox.draw_textbox("data/sprites/oldman.png", 'Old Man',
                                         'I heard the monsters on the first floor are quite weak.',
                                         'You mustn\'t underestimate them However!',
                                         'Consider Equipping yourself with new equipment from the Shop.',
                                         line6='Press RCTRL to continue...')
            elif self.Talk == 1 and player.progress == 1:

                self.txtbox.draw_textbox("data/sprites/boy.png", 'Boy',
                                         'Wow mister, you\'re going to fight in the Arena? So cool!',
                                         line6='Press RCTRL to continue...')

            elif self.Talk == 2 and player.progress == 1:

                self.txtbox.draw_textbox("data/sprites/youngman.png", 'Young Man',
                                         'In the 50 years that the Arena has been open, there has been only one winner.',
                                         ' It was the legendary Hero known as Zen.',
                                         'That was 2 years ago though, nobody has seen him since.',
                                         line6='Press RCTRL to continue...')
            elif self.Talk == 3 and player.progress == 1:

                self.txtbox.draw_textbox("data/sprites/mysteryman.png", 'Stranger',
                                         'You...', 'Nevermind. Good luck in the Arena, I\'ll be keeping an eye on you.',
                                         line6='              Press RCTRL to continue...')
            if self.Talk > 3:
                self.Talk = -1

    def status(self, player=Player(), item_data=item_data):
        surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 1.5), curheight)), (53, 30))
        nametxt = self.uitext.render('Name: ' + player.name, False, self.txtcolor)
        surf.blit(nametxt, (169, 207))
        strtxt = self.uitext.render('STR: %d' % player.stre, False, self.txtcolor)
        strtxt2 = self.uitext.render('(+%d)' % player.add_stre, False, (0, 200, 0))
        surf.blit(strtxt, (169, 247))
        surf.blit(strtxt2, (299, 247))
        deftxt = self.uitext.render('DEF: %d' % player.defe, False, self.txtcolor)
        deftxt2 = self.uitext.render('(+%d)' % player.add_defe, False, (0, 200, 0))
        surf.blit(deftxt, (169, 287))
        surf.blit(deftxt2, (299, 287))
        lucktxt = self.uitext.render('LUCK: %d' % player.luck, False, self.txtcolor)
        surf.blit(lucktxt, (169, 327))
        magtxt = self.uitext.render('MAG: %d' % player.mag, False, self.txtcolor)
        magtxt2 = self.uitext.render('(+%d)' % player.add_mag, False, (0, 200, 0))
        surf.blit(magtxt, (169, 367))
        surf.blit(magtxt2, (299, 367))
        lvltxt = self.uitext.render('Level: %d' % player.level, False, self.txtcolor2)
        surf.blit(lvltxt, (607, 396))
        xptxt = self.uitext2.render('Exp till next level: %d' % player.xp_till_levelup(player.level), False,
                                    self.txtcolor2)
        surf.blit(xptxt, (607, 426))
        surf.blit(self.face, (679, 207))
        classtxt = self.uitext.render(player.pclass.capitalize(), False, self.txtcolor)
        surf.blit(classtxt, (697, 366))
        surf.blit(self.statustxt, (417, 141))
        weptxt = self.uitext.render('WEAPON: ' + item_data['weapons'][player.cur_weapon]['name'], False, self.txtcolor2)
        armtxt = self.uitext.render('ARMOR: ' + item_data['armours'][player.cur_armour]['name'], False, self.txtcolor2)
        acctxt = self.uitext.render('ACCESSORY: ' + item_data['accessories'][player.cur_accessory]['name'], False,
                                    self.txtcolor2)
        surf.blit(self.wepicon, (169, 407))
        surf.blit(weptxt, (209, 407))
        surf.blit(self.armicon, (169, 447))
        surf.blit(armtxt, (209, 447))
        surf.blit(self.accicon, (169, 487))
        surf.blit(acctxt, (209, 487))
        floorktxt = self.uitext.render('Enemies killed on this floor: %d' % player.fkills, False, self.txtcolor3)
        totktxt = self.uitext.render('Total enemies killed: %d' % player.tkills, False, self.txtcolor3)
        surf.blit(floorktxt, (169, 527))
        surf.blit(totktxt, (168, 567))

    def system(self):
        surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 2.7), int(curheight / 3))), (470, 200))
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
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'You have %d monter(s) left to kill. You\'re almost there!' % montokill,
                                         line6='Press RCTRL to continue...')
            if monkill >= 5:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'You can challenge the floor boss! Are you prepared for it?',
                                         line6='Press RCTRL to continue...')

        if not self.battalk:
            if monkill >= 5:
                self.batopt2 = self.uitext.render('Challenge the floor boss', False, self.txtcolor)
            elif monkill < 5:
                self.batopt2 = self.uitext.render('Challenge the floor boss', False, (105, 109, 114))
            surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 2.7), int(curheight / 3))), (470, 200))
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

    def post_battle(self, progress=1):  # where 'progress' is what point in the 'story' the player is on
        if not self.pb_dialogue:
            self.pbtalk = random.randrange(0, 4)
        if self.pbtalk == 0 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                   'That was a good battle! If you\'re injured make sure to rest up at the inn.',
                                   line6='Press RCTRL to continue...')
        elif self.pbtalk == 1 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                   'Good job! Make sure to use the gold from your battle to buy equipment from',
                                   'our Shop.', line6='Press RCTRL to continue...')
        elif self.pbtalk == 2 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                   'Nice work! You\'re pretty skilled, are you sure you haven\'t done this before?',
                                   line6='Press RCTRL to continue...')
        elif self.pbtalk == 3 and progress == 1:
            self.pb_dialogue = True
            ui.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                   'Good work out there! I overheard some strange people talking about you.',
                                   'Something about.. A debt?', line6='Press RCTRL to continue...')

    def draw_inn(self, gold):
        surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
        surf.blit(pygame.transform.scale(self.bg, (170, 50)), (10, 48))  # Gold box
        surf.blit(pygame.transform.scale(self.bg, (300, 300)), (905, 430))  # Actions box
        surf.blit(self.talktxt, (946, 496))
        surf.blit(self.sleeptxt, (946, 526))
        surf.blit(self.backtxt, (946, 556))
        self.cur = self.uitext2.render('Gold:  %d' % gold, False, self.txtcolor)  # Current gold with the player
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
            surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 1.5), 300)), (0, 430))  # Description box
            surf.blit(pygame.transform.scale(self.bg, (170, 50)), (10, 29))  # Gold box
            surf.blit(pygame.transform.scale(self.bg, (300, 300)), (905, 430))  # Actions box
            surf.blit(self.talktxt, (946, 496))
            surf.blit(self.inntxt, (946, 526))
            surf.blit(self.slumstxt, (946, 556))
            surf.blit(self.backtxt, (946, 586))
            gold = self.uitext2.render('Gold:  %d' % player.gold, False, self.txtcolor)  # Current gold with the player
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


class SelectOptions(MainUi):
    def __init__(self):
        MainUi.__init__(self)
        self.rowpos = 0  # Position of cursor in Option selection(Current row)
        self.colpos = 0  # Position of cursor in Option selection(Current column)
        self.alert1 = True  # Flag for whether that option is new/updated
        self.alert2 = True  # Flag for whether that option is new/updated
        self.alert3 = True  # Flag for whether that option is new/updated
        self.alert4 = True  # Flag for whether that option is new/updated
        self.alert5 = True  # Flag for whether that option is new/updated
        self.alert6 = True  # Flag for whether that option is new/updated
        self.alertAnim = pyganim.PygAnimation([("data/sprites/alert1.png", 0.4), ("data/sprites/alert2.png", 0.4)])
        self.alertAnim.scale([35, 35])
        self.alertAnim.play()

    def drawUi(self, no=1, opt1='1', opt2='2', opt3='3', opt4='4', opt5='5',
               opt6='6'):  # Select option among 6 or less choices,where no is the number of choices
        surf.blit(pygame.transform.scale(self.bg, (int(curwidth / 1.5), 300)), (0, 430))
        Option1 = self.uitext.render(opt1, False, self.txtcolor)
        Option2 = self.uitext.render(opt2, False, self.txtcolor)
        Option3 = self.uitext.render(opt3, False, self.txtcolor)
        Option4 = self.uitext.render(opt4, False, self.txtcolor)
        Option5 = self.uitext.render(opt5, False, self.txtcolor)
        Option6 = self.uitext.render(opt6, False, self.txtcolor)
        backTxt = self.uitext.render('Back', False, self.txtcolor)
        surf.blit(Option1, (80, 490))  # Row 1
        if self.alert1:  # If the option is new/updated show alert.
            self.alertAnim.blit(surf, (200, 490))
        if no >= 2:
            surf.blit(Option2, (280, 490))
            if self.alert2:
                self.alertAnim.blit(surf, (400, 490))
            if no >= 3:
                surf.blit(Option3, (480, 490))
                if self.alert3:
                    self.alertAnim.blit(surf, (600, 490))
                if no >= 4:
                    surf.blit(Option4, (80, 590))  # Row 2
                    if self.alert4:
                        self.alertAnim.blit(surf, (200, 590))
                    if no >= 5:
                        surf.blit(Option5, (280, 590))
                        if self.alert5:
                            self.alertAnim.blit(surf, (400, 590))
                        if no >= 6:
                            surf.blit(Option6, (480, 590))
                            if self.alert6:
                                self.alertAnim.blit(surf, (600, 590))
        surf.blit(backTxt, (680, 590))  # Exit

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
        if self.colpos > 3:
            self.colpos = 0
        if self.rowpos > 1:
            self.rowpos = 0
        if self.colpos < 0:
            self.colpos = 2
        if self.rowpos < 0:
            self.rowpos = 1
        if self.rowpos == 0:  # Goes to exit when trying to go right on the end of row 1
            if self.colpos > 2:
                self.rowpos = 1
                self.colpos = 3

    def alert_off(self, alert):  # Switch off the specified alert(from 1 - 6)
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

    def alert_on(self, alert):  # Switch on the specified alert(from 1 - 6)
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
        self.shopbg = pygame.image.load("data/backgrounds/shopbg.png").convert_alpha()
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
        self.status_bg = pygame.transform.scale(self.bg, (300, 500))
        self.status_anim = False
        self.green_rgb = (0, 200, 0)
        self.red_rgb = (200, 0, 0)
        self.box_pos = 2000
        self.current_list = []  # which set of items u are currently viewing
        self.buzzer = pygame.mixer.Sound('data/sounds&music/Buzzer1.ogg')

    def get_player_stats(self, player_data):
        self.player_data = player_data
        self.pstr = self.player_data.stre + self.player_data.add_stre
        self.pdef = self.player_data.defe + self.player_data.add_defe
        self.pmag = self.player_data.mag + self.player_data.add_mag
        self.pluck = self.player_data.luck

    def status_window(self, item, player_data):
        self.get_player_stats(player_data)
        if not self.status_anim:
            self.box_pos = 2000
            self.status_anim = True
        if self.status_anim:
            if self.box_pos > 950:
                self.box_pos -= 50

        surf.blit(self.status_bg, (self.box_pos, 222))
        if self.box_pos <= 950:
            str_txt = self.uitext.render('STR: ' + str(self.pstr), False, self.txtcolor3)
            def_txt = self.uitext.render('DEF: ' + str(self.pdef), False, self.txtcolor3)
            mag_txt = self.uitext.render('MAG: ' + str(self.pmag), False, self.txtcolor3)
            luk_txt = self.uitext.render('LUCK: ' + str(self.pluck), False, self.txtcolor3)
            if self.current_list == self.weapons_list:
                player_item = player_data.cur_weapon

            elif self.current_list == self.armour_list:
                player_item = player_data.cur_armour
            else:
                player_item = player_data.cur_accessory

            str_dif = self.pstr + item['atk'] - (self.pstr + self.current_list[player_item]['atk'])
            def_dif = self.pdef + item['def'] - (self.pdef + self.current_list[player_item]['def'])
            mag_dif = self.pmag + item['mag'] - (self.pmag + self.current_list[player_item]['mag'])
            if str_dif >= 0:
                str_diftxt = self.uitext.render('(+' + str(str_dif) + ')', False, self.green_rgb)
                surf.blit(str_diftxt, (1120, 300))
            else:
                str_diftxt = self.uitext.render('(' + str(str_dif) + ')', False, self.red_rgb)
                surf.blit(str_diftxt, (1120, 300))
            if def_dif >= 0:
                def_diftxt = self.uitext.render('(+' + str(def_dif) + ')', False, self.green_rgb)
                surf.blit(def_diftxt, (1120, 370))
            else:
                def_diftxt = self.uitext.render('(' + str(def_dif) + ')', False, self.red_rgb)
                surf.blit(def_diftxt, (1120, 370))
            if mag_dif >= 0:
                mag_diftxt = self.uitext.render('(+' + str(mag_dif) + ')', False, self.green_rgb)
                surf.blit(mag_diftxt, (1120, 440))
            else:
                mag_diftxt = self.uitext.render('(' + str(mag_dif) + ')', False, self.red_rgb)
                surf.blit(mag_diftxt, (1120, 440))

            surf.blit(str_txt, (1000, 300))
            surf.blit(def_txt, (1000, 370))
            surf.blit(mag_txt, (1000, 440))
            surf.blit(luk_txt, (1000, 510))

    def buy_item(self, item_id):
        if self.player_data.gold < self.current_list[item_id]['cost']:
            self.buzzer.play()
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
                wepstatlist.append(str([weapon['atk'], weapon['def'], weapon['mag']]))
                wepattributelist.append(weapon['attributes'])
            for armour in self.armour_list:
                armnamelist.append(armour['name'])
                armcostlist.append(str(armour['cost']))
                armstatlist.append(str([armour['atk'], armour['def'], armour['mag']]))
                armattributelist.append(armour['attributes'])
            for accessory in self.acc_list:
                accnamelist.append(accessory['name'])
                acccostlist.append(str(accessory['cost']))
                accstatlist.append(str([accessory['atk'], accessory['def'], accessory['mag']]))
                accattributelist.append(accessory['attributes'])
            for consumable in self.consume_list:
                connamelist.append(consumable['name'])
                concostlist.append(str(consumable['cost']))
                constatlist.append(str([consumable['hp'], consumable['mp']]))
            shop_title = self.title_text.render(shop_name, True, self.txtcolor2)

        if self.shopkeep:
            self.txtbox.draw_textbox("data/sprites/shopkeep.png", 'Shopkeeper',
                                     'Welcome to the Arena shop! How can I help you?',
                                     line6='              Press RCTRL to continue...')
        if not self.shopkeep:
            surf.blit(self.shopbg, (53, 30))
            surf.blit(shop_title, (360, 57))
            surf.blit(self.uitext.render(self.shoptxt[0], False, self.txtcolor3), (shop_text_pos, 150))
            surf.blit(self.uitext.render(self.shoptxt[1], False, self.txtcolor3), (shop_text_pos + 150, 150))
            surf.blit(self.uitext.render(self.shoptxt[2], False, self.txtcolor3), (shop_text_pos + 300, 150))
            surf.blit(self.uitext.render(self.shoptxt[3], False, self.txtcolor3), (shop_text_pos + 510, 150))
            surf.blit(self.uitext2.render(self.shoptxt2[0], False, (186, 31, 34)), (161, 290))
            surf.blit(self.uitext2.render(self.shoptxt2[1], True, (186, 31, 34)), (449, 290))
            surf.blit(pygame.transform.scale(self.bg, (170, 50)), (925, 42))  # Gold box 10,48
            self.cur = self.uitext2.render('Gold:  %d' % player_data.gold, False,
                                           self.txtcolor)  # Current gold with the player
            self.coinAnim.blit(surf, (937, 56))  # Gold icon
            surf.blit(self.cur, (962, 56))
            if self.shop_page == 0:
                self.max_pos = len(self.weapons_list)
                item1 = self.uitext.render(wepnamelist[self.min_pos], False, self.txtcolor3)
                cost1 = self.uitext.render(wepcostlist[self.min_pos], False, self.txtcolor3)
                stat1 = self.uitext.render(wepstatlist[self.min_pos], False, self.txtcolor3)
                attr1 = self.uitext.render(wepattributelist[self.min_pos], False, self.txtcolor3)
                if self.max_pos > 2:
                    item2 = self.uitext.render(wepnamelist[self.min_pos + 1], False, self.txtcolor3)
                    cost2 = self.uitext.render(wepcostlist[self.min_pos + 1], False, self.txtcolor3)
                    stat2 = self.uitext.render(wepstatlist[self.min_pos + 1], False, self.txtcolor3)
                    attr2 = self.uitext.render(wepattributelist[self.min_pos + 1], False, self.txtcolor3)
                if self.max_pos > 3:
                    item3 = self.uitext.render(wepnamelist[self.min_pos + 2], False, self.txtcolor3)
                    cost3 = self.uitext.render(wepcostlist[self.min_pos + 2], False, self.txtcolor3)
                    stat3 = self.uitext.render(wepstatlist[self.min_pos + 2], False, self.txtcolor3)
                    attr3 = self.uitext.render(wepattributelist[self.min_pos + 2], False, self.txtcolor3)
                if self.max_pos > 4:
                    item4 = self.uitext.render(wepnamelist[self.min_pos + 3], False, self.txtcolor3)
                    cost4 = self.uitext.render(wepcostlist[self.min_pos + 3], False, self.txtcolor3)
                    stat4 = self.uitext.render(wepstatlist[self.min_pos + 3], False, self.txtcolor3)
                    attr4 = self.uitext.render(wepattributelist[self.min_pos + 3], False, self.txtcolor3)
                if self.max_pos > 5:
                    item5 = self.uitext.render(wepnamelist[self.min_pos + 4], False, self.txtcolor3)
                    cost5 = self.uitext.render(wepcostlist[self.min_pos + 4], False, self.txtcolor3)
                    stat5 = self.uitext.render(wepstatlist[self.min_pos + 4], False, self.txtcolor3)
                    attr5 = self.uitext.render(wepattributelist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 1:
                self.max_pos = len(self.armour_list)
                item1 = self.uitext.render(armnamelist[self.min_pos], False, self.txtcolor3)
                cost1 = self.uitext.render(armcostlist[self.min_pos], False, self.txtcolor3)
                stat1 = self.uitext.render(armstatlist[self.min_pos], False, self.txtcolor3)
                attr1 = self.uitext.render(armattributelist[self.min_pos], False, self.txtcolor3)
                if self.max_pos > 2:
                    item2 = self.uitext.render(armnamelist[self.min_pos + 1], False, self.txtcolor3)
                    cost2 = self.uitext.render(armcostlist[self.min_pos + 1], False, self.txtcolor3)
                    stat2 = self.uitext.render(armstatlist[self.min_pos + 1], False, self.txtcolor3)
                    attr2 = self.uitext.render(armattributelist[self.min_pos + 1], False, self.txtcolor3)
                if self.max_pos > 3:
                    item3 = self.uitext.render(armnamelist[self.min_pos + 2], False, self.txtcolor3)
                    cost3 = self.uitext.render(armcostlist[self.min_pos + 2], False, self.txtcolor3)
                    stat3 = self.uitext.render(armstatlist[self.min_pos + 2], False, self.txtcolor3)
                    attr3 = self.uitext.render(armattributelist[self.min_pos + 2], False, self.txtcolor3)
                if self.max_pos > 4:
                    item4 = self.uitext.render(armnamelist[self.min_pos + 3], False, self.txtcolor3)
                    cost4 = self.uitext.render(armcostlist[self.min_pos + 3], False, self.txtcolor3)
                    stat4 = self.uitext.render(armstatlist[self.min_pos + 3], False, self.txtcolor3)
                    attr4 = self.uitext.render(armattributelist[self.min_pos + 3], False, self.txtcolor3)
                if self.max_pos > 5:
                    item5 = self.uitext.render(armnamelist[self.min_pos + 4], False, self.txtcolor3)
                    cost5 = self.uitext.render(armcostlist[self.min_pos + 4], False, self.txtcolor3)
                    stat5 = self.uitext.render(armstatlist[self.min_pos + 4], False, self.txtcolor3)
                    attr5 = self.uitext.render(armattributelist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 2:
                self.max_pos = len(self.acc_list)
                item1 = self.uitext.render(accnamelist[self.min_pos], False, self.txtcolor3)
                cost1 = self.uitext.render(acccostlist[self.min_pos], False, self.txtcolor3)
                stat1 = self.uitext.render(accstatlist[self.min_pos], False, self.txtcolor3)
                attr1 = self.uitext.render(accattributelist[self.min_pos], False, self.txtcolor3)
                if self.max_pos > 2:
                    item2 = self.uitext.render(accnamelist[self.min_pos + 1], False, self.txtcolor3)
                    cost2 = self.uitext.render(acccostlist[self.min_pos + 1], False, self.txtcolor3)
                    stat2 = self.uitext.render(accstatlist[self.min_pos + 1], False, self.txtcolor3)
                    attr2 = self.uitext.render(accattributelist[self.min_pos + 1], False, self.txtcolor3)
                if self.max_pos > 3:
                    item3 = self.uitext.render(accnamelist[self.min_pos + 2], False, self.txtcolor3)
                    cost3 = self.uitext.render(acccostlist[self.min_pos + 2], False, self.txtcolor3)
                    stat3 = self.uitext.render(accstatlist[self.min_pos + 2], False, self.txtcolor3)
                    attr3 = self.uitext.render(accattributelist[self.min_pos + 2], False, self.txtcolor3)
                if self.max_pos > 4:
                    item4 = self.uitext.render(accnamelist[self.min_pos + 3], False, self.txtcolor3)
                    cost4 = self.uitext.render(acccostlist[self.min_pos + 3], False, self.txtcolor3)
                    stat4 = self.uitext.render(accstatlist[self.min_pos + 3], False, self.txtcolor3)
                    attr4 = self.uitext.render(accattributelist[self.min_pos + 3], False, self.txtcolor3)
                if self.max_pos > 5:
                    item5 = self.uitext.render(accnamelist[self.min_pos + 4], False, self.txtcolor3)
                    cost5 = self.uitext.render(acccostlist[self.min_pos + 4], False, self.txtcolor3)
                    stat5 = self.uitext.render(accstatlist[self.min_pos + 4], False, self.txtcolor3)
                    attr5 = self.uitext.render(accattributelist[self.min_pos + 4], False, self.txtcolor3)
            if self.shop_page == 3:
                self.max_pos = len(self.consume_list)
                item1 = self.uitext.render(connamelist[self.min_pos], False, self.txtcolor3)
                cost1 = self.uitext.render(concostlist[self.min_pos], False, self.txtcolor3)
                stat1 = self.uitext.render(constatlist[self.min_pos], False, self.txtcolor3)

            surf.blit(item1, (161, 339))
            surf.blit(cost1, (449, 339))

            if self.max_pos > 2:
                surf.blit(item2, (161, 399))
                surf.blit(cost2, (449, 399))

            if self.max_pos > 3:
                surf.blit(item3, (161, 459))
                surf.blit(cost3, (449, 459))

            if self.max_pos > 4:
                surf.blit(item4, (161, 519))
                surf.blit(cost4, (449, 519))

            if self.max_pos > 5:
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
                if self.shop_cursor_pos2 == 1:
                    surf.blit(self.cursor, (120, 399))
                if self.shop_cursor_pos2 == 2:
                    surf.blit(self.cursor, (120, 459))
                if self.shop_cursor_pos2 == 3:
                    surf.blit(self.cursor, (120, 519))
                if self.shop_cursor_pos2 == 4:
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
                if self.current_list != self.consume_list:
                    self.status_window(self.current_list[self.shop_cursor_pos2 + self.min_pos], player_data)


class GameEvents(MainUi):
    """Class for all special events in the game."""

    def __init__(self):
        MainUi.__init__(self)
        self.town_bg_day = pygame.image.load("data/backgrounds/The Medieval Town.jpg").convert_alpha()
        self.town_bg_eve = pygame.image.load("data/backgrounds/The Medieval Town_eve.jpg").convert_alpha()
        self.town_bg_ngt = pygame.image.load("data/backgrounds/The Medieval Town_night.jpg").convert_alpha()
        self.townDialogue = 0  # Progress for the dialogue while in the town.
        self.arenaDialogue = 0
        self.timekeep = Timer()  # Used to time the events and things
        self.dialoguecontrol = False
        self.startEvent = False
        self.thudSound = pygame.mixer.Sound('data/sounds&music/thud.wav')
        self.applauseSound = pygame.mixer.Sound('data/sounds&music/Applause1.ogg')
        self.bossRoar = pygame.mixer.Sound('data/sounds&music/Monster2.ogg')
        self.arena_bg = pygame.image.load("data/backgrounds/arenaDay.png").convert_alpha()
        self.boss_face1 = pygame.image.load("data/sprites/Boss1.png")
        self.town_location = 0  # 0-Centre 1-Bar/Inn 2-Slums
        self.game_clock = GameClock()
        self.option_selector = SelectOptions()
        self.town_talk1 = False  # Flag for drawing options menu for the 'Talk' Screen
    def town_first_visit(self, player_data):
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Bustling_Streets.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        global surf
        global screen
        runningsound = pygame.mixer.Sound('data/sounds&music/Person_running.wav')
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
        player_data.town_first_flag = False
        while not event_done:
            curwidth, curheight = screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_done = True
                    global done
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL and self.dialoguecontrol:
                        self.townDialogue += 1
                    if event.key == pygame.K_UP and choice_select:
                        self.txtbox.ch_cursorpos -= 1
                        self.cursorsound.play()
                    if event.key == pygame.K_DOWN and choice_select:
                        self.txtbox.ch_cursorpos += 1
                        self.cursorsound.play()
                    if event.key == pygame.K_RETURN and choice_select:
                        if self.txtbox.ch_cursorpos == 0:   # Pay the girl
                            dialogue_choice = 0
                            dialogue_choice2 = 0
                            choice_select = False
                            self.townDialogue += 1
                            self.dialoguecontrol = True
                        if self.txtbox.ch_cursorpos == 1:
                            dialogue_choice = 1
                            dialogue_choice2 = 1
                            choice_select = False
                            self.townDialogue += 1
                            self.dialoguecontrol = True
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()

            surf.blit(pygame.transform.scale(self.town_bg_day, (curwidth, curheight)), (0, 0))

            if not self.startEvent:
                if self.timekeep.timing() == 2 and self.townDialogue < 1:
                    self.startEvent = True
            if self.startEvent:
                self.townDialogue = 1
                self.startEvent = False
                self.dialoguecontrol = True

            if self.townDialogue == 1:
                self.txtbox.draw_textbox(None, '',
                                         'The town that the Arena is situated in gets very lively this time of the year as',
                                         'this is when most of the challengers arrive.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 2:
                self.txtbox.draw_textbox(None, '',
                                         "You\'ve been here before but never really got the chance to look around,",
                                         'so the sights of this place are still very unfamiliar to you.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 3:
                self.txtbox.draw_textbox(None, '',
                                         'Even if you had been familiar with this place in the past, It would still have been',
                                         'difficult finding your way through this place as the town has changed dramatically',
                                         'over the course of a few years.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 4:
                self.txtbox.draw_textbox(None, '',
                                         'This is mostly due to the overwhelming popularity of the arena which has brought',
                                         'visitors from all over the country to this one location.',
                                         'This has let the town flourish and expand at a very quick pace, with new buildings and',
                                         'stores being built seemingly everyday.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 5:
                self.txtbox.draw_textbox(None, '',
                                         'The presence and influence of the arena played a major role in the growth of the town,',
                                         'so much so that the people of the town decided to change it\'s old name',
                                         'and give it a new more fitting name, \"Arena Town\".',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 6:
                runningsound.play()
                self.timekeep.reset()
                self.townDialogue += 1
                self.dialoguecontrol = False
            elif self.townDialogue == 7 and timedflag1:
                self.dialoguecontrol = True
                self.txtbox.draw_textbox(None, '',
                                         'You see a young girl running towards your direction.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 8:
                self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                         'Oh no, I\'m so late, Grandpa\'s gonna get so mad!',
                                         line6='Press RCTRL to continue...')
                timedflag1 = False

            elif self.townDialogue == 9:
                self.thudSound.play()
                self.townDialogue += 1
                self.dialoguecontrol = False
                self.timekeep.reset()
            elif self.townDialogue == 10 and timedflag1:
                self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                         'Ouch!',
                                         line6='Press RCTRL to continue...')
                self.dialoguecontrol = True
            elif self.townDialogue == 11:
                self.txtbox.draw_textbox(None, '',
                                         'The girl crashes into you at full speed and topples over onto the gravel road.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 12:
                self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                         'Hey, watch where you\'re going!',
                                         line6='Press RCTRL to continue...')

            elif self.townDialogue == 13:
                self.txtbox.draw_textbox(None, '',
                                         'The girl gets up and brushes off her skirt.',
                                         line6='Press RCTRL to continue...')
            elif self.townDialogue == 14:
                self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                         'There\'s a tear in my new dress! What are you going to do about this?',
                                         line6='Press RCTRL to continue...')
                choice_select = True
            elif self.townDialogue == 15:
                self.txtbox.draw_textbox(None, '',
                                         'What do you do?',
                                         line6='Press ENTER to continue...')
                self.txtbox.select_choice('Offer to pay her money', 'Ignore her and walk away')
                self.dialoguecontrol = False
            elif dialogue_choice == 0 and self.townDialogue >= 16:  # Pay money dialogue tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                             'Oh you\'re willing to pay? I\'m going to need atleast 150 gold for the dress.',
                                             line6='Press RCTRL to continue...')
                    choice_select = True
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox(None, '',
                                             'Pay 150 gold?',
                                             line6='Press ENTER to continue...')
                    self.txtbox.select_choice('Pay her', 'Don\'t Pay')
                    self.dialoguecontrol = False
                elif self.townDialogue >= 18 and dialogue_choice2 == 0:  # Pay her
                    if player_data.gold < 150 and not paid_girl:  # if player doesn't have enough gold
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                     'Hey you don\'t even have enough gold to pay me!')
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                     'Don\'t waste my time if you don\'t have any money!')
                        if self.townDialogue == 20:
                            self.townDialogue = 21
                            dialogue_choice2 = 1
                    else:
                        if not paid_girl:
                            player_data.gold -= 150
                            player_data.paid_girl_flag = True
                        paid_girl = True
                        if self.townDialogue == 18:
                            self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                     'Well, I guess this will have to do.')
                        if self.townDialogue == 19:
                            self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                     'You better be careful next time! Be grateful that I let you off easily!')
                        elif self.townDialogue == 20:
                            self.txtbox.draw_textbox(None, '',
                                                     'The girl walks away after glaring at you in the eye.',
                                                     'You could have sworn you saw a smile for a second.')
                        elif self.townDialogue == 21:
                            self.txtbox.draw_textbox(None, '',
                                                     'The girl disappears into the crowd.')

                elif self.townDialogue >= 18 and dialogue_choice2 == 1:  # Don't pay her
                    if self.townDialogue == 18:
                        self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                 '...You\'re not going to pay?',
                                                 line6='Press RCTRL to continue...')
                    if self.townDialogue == 19:
                        self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                 'Tch.. he didn\'t fall for it')
                    elif self.townDialogue == 20:
                        self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                                 'Well don\'t waste my time then, get out of my way!')
                    elif self.townDialogue == 21:
                        self.txtbox.draw_textbox(None, '',
                                                 'The girl storms off and disappears into the crowd.')
            elif dialogue_choice == 1 and self.townDialogue >= 16:  # ignore girl tree
                if self.townDialogue == 16:
                    self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                             '....',
                                             line6='Press RCTRL to continue...')
                elif self.townDialogue == 17:
                    self.txtbox.draw_textbox("data/sprites/girl.png", '???',
                                             'Don\'t just ignore me!',
                                             line6='Press RCTRL to continue...')
                elif self.townDialogue == 18:
                    self.txtbox.draw_textbox(None, '',
                                             'You continue ignoring the girl while she makes a commotion in the middle of',
                                             'the street and proceed to the Town.',
                                             line6='Press RCTRL to continue...')
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
        '''Cutscene when challenging the first_floor boss'''
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
                        self.arenaDialogue += 1
                    if event.key == pygame.K_UP and choice_select:
                        self.txtbox.ch_cursorpos -= 1
                        self.cursorsound.play()
                    if event.key == pygame.K_DOWN and choice_select:
                        self.txtbox.ch_cursorpos += 1
                        self.cursorsound.play()
                    if event.key == pygame.K_RETURN and choice_select:
                        if self.txtbox.ch_cursorpos == 0:
                            dialogue_choice = 0
                            choice_select = False
                            self.arenaDialogue += 1
                            self.dialoguecontrol = True
                        if self.txtbox.ch_cursorpos == 1:
                            dialogue_choice = 1
                            choice_select = False
                            self.arenaDialogue += 1
                            self.dialoguecontrol = True
                if event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

            surf.blit(pygame.transform.scale(self.arena_bg, (curwidth, curheight)), (0, 0))
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
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'Ladies and gentlemen!',
                                         line6='Press RCTRL to continue...')

            elif self.arenaDialogue == 2:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'It seems like it\'s been ages since we\'ve had a challenger strong enough to',
                                         'finally get to this point!',
                                         line6='Press RCTRL to continue...')
            elif self.arenaDialogue == 3:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'But we finally have him here, someone who is both brave and foolish enough',
                                         'to step up and fight his way through some of the most powerful monsters, to',
                                         'be able to stand before you at this very moment and face against what many',
                                         'would consider suicide! ',
                                         line6='Press RCTRL to continue...')
            elif self.arenaDialogue == 4:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'Please put your hands together for.. ' + name + '!',
                                         line6='Press RCTRL to continue...')
                applause_flag2 = True
            elif self.arenaDialogue == 5:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'And his opponent.. A beast that has destroyed the dreams of many young',
                                         'adventurers, said to be the \'Gatekeeper\' of the Arena.',
                                         line6='Press RCTRL to continue...')
            elif self.arenaDialogue == 6:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'Please put your hands together for.. Tho\'k!',
                                         line6='Press RCTRL to continue...')
                boss_roar = True

            elif self.arenaDialogue == 7:
                self.txtbox.draw_textbox("data/sprites/Boss1.png", 'Tho\'k',
                                         'RAAAAAAAAAAAAAAAAAARRGGHHHHHH!!!!!',
                                         line6='Press RCTRL to continue...')
                if boss_roar:
                    self.bossRoar.play()
                    self.timekeep.reset()
                    boss_roar = False
                    self.dialoguecontrol = False
                if self.timekeep.timing() == 2:
                    self.dialoguecontrol = True

            elif self.arenaDialogue == 8:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'Now, the time has come. ' + name + ', I assume you are ready?',
                                         line6='Press ENTER to select a choice...')
                self.txtbox.select_choice('Yes, I am ready.',
                                          'I don\'t think I am.')
                self.dialoguecontrol = False
                choice_select = True
            elif self.arenaDialogue == 9:
                if dialogue_choice == 0:
                    self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                             'Good! That\'s what I expected from you!',
                                             line6='Press RCTRL to continue...')
                if dialogue_choice == 1:
                    self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                             'Well unfortunately it\'s too late to turn back now!',
                                             line6='Press RCTRL to continue...')
            elif self.arenaDialogue == 10:
                self.txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                         'It is time! Fight!',
                                         line6='Press RCTRL to continue...')
            elif self.arenaDialogue == 11:
                event_done = True
            screen.blit(surf, (0, 0))
            self.timekeep.timing()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)
            pygame.display.update()

    def intro_scene(self):
        event_done = False
        pygame.mixer.music.load('data/sounds&music/Dungeon3.ogg')
        global surf
        global screen
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.timekeep.reset()
        self.dialoguecontrol = False
        while not event_done:
            pass

    def town(self, player_data):
        '''The town and all the locations present in it.'''
        if player_data.town_first_flag:
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
                    self.option_selector.drawUi(3, 'Citizen', 'Rich Lady', 'Fan boy')
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
        self.area_music = 'data/sounds&music/Infinite_Arena.mp3'  # Music to be played in the area
        self.bell = pygame.mixer.Sound('data/sounds&music/Bell1.ogg')  # Bell sound during night time
        self.rooster = pygame.mixer.Sound('data/sounds&music/Roost.ogg')  # Morning sound
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

            if player.minutes >= 60:  # Self explanatory
                player.hours += 1
                player.minutes = 0
            if player.hours > 23:  # 24 hour clock
                player.hours = 0
            if player.hours >= 6 and player.hours < 14:  # Day
                self.time_state = "Morning"
                surf.blit(pygame.transform.scale(arena_bg1, (curwidth, curheight)), (0, 0))

            if player.hours >= 14 and player.hours < 20:  # Afternoon
                self.time_state = "Noon"
                surf.blit(pygame.transform.scale(arena_bg2, (curwidth, curheight)), (0, 0))

            if player.hours >= 20 or player.hours < 6:  # Night
                self.time_state = "Night"
                surf.blit(pygame.transform.scale(arena_bg3, (curwidth, curheight)), (0, 0))

            if (player.hours == 19 and player.minutes == 30) and (not self.bellflag):   # Music fading out
                if not self.fadeoutflag:
                    pygame.mixer.music.fadeout(6000)  # 8 seconds
                    self.fadeoutflag = True

            if (player.hours >= 20 or player.hours < 6) and (not self.bellflag):  # Playing bell sound when it becomes night
                self.bell.play()
                Currentmusic = 'data/sounds&music/night.mp3'
                pygame.mixer.music.stop()
                pygame.mixer.music.load(Currentmusic)
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play()
                self.bellflag = True

            if (player.hours >= 6 and player.hours < 14) and self.bellflag:  # Playing rooster sound when it becomes day
                self.rooster.play()
                pygame.mixer.music.load(self.area_music)
                pygame.mixer.music.play()
                self.bellflag = False
                self.fadeoutflag = False

if __name__ == "__main__":
    player = Player(item_data=item_data)
    eventManager = GameEvents()
    warrior = pyganim.PygAnimation([("data/sprites/idle1.png", 0.2), ("data/sprites/idle2.png", 0.2), ("data/sprites/idle3.png", 0.2)])

    mage = pyganim.PygAnimation([("data/sprites/midle1.png", 0.3), ("data/sprites/midle2.png", 0.3), ("data/sprites/midle3.png", 0.3)])

    castanim = [("data/sprites/b1.png", 0.3), ("data/sprites/b2.png", 0.3), ("data/sprites/b3.png", 0.3)]
    battler = SideBattle(monster_data, 'mage', castanim, "data/backgrounds/Ruins2.png",
                         'data/sounds&music/yousayrun2.mp3')

    floor1_talk = SelectOptions()  # Choices for 'Talk' in floor 1
    arena_shop = Shop(item_data)
    #####

    randbattle = 0
    timepassed = False  # Flag to check if the time passed or not
    newgtxtbox = 0
    pygame.mixer.music.load('data/sounds&music/Theme2.ogg')
    pygame.mixer.music.play()
    vol = 0.5
    surf = pygame.Surface((1366, 768))
    pygame.mixer.music.set_volume(vol)
    innsong = pygame.mixer.Sound('data/sounds&music/Town2.ogg')
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
    secretbattle = SideBattle(monster_data, 'mage', castanim, "data/backgrounds/LavaCave.png",
                              'data/sounds&music/Battle3.ogg', phealth=1000, pmana=100, pstr=1000, pstrmod=14, pdef=100,
                              pmag=2000, pluck=9)
    secretbattle.plevel = 50
    debugbattle = SideBattle(monster_data, 'mage', castanim, "data/backgrounds/DemonicWorld.png",
                             'data/sounds&music/Dungeon2.ogg', phealth=10000, pmana=1000, pstr=1000, pstrmod=14, pdef=100,
                             pmag=2000, pluck=9)
    debugbattle.plevel = 50
    healsound = pygame.mixer.Sound('data/sounds&music/Recovery.ogg')
    mage.play()
    warrior.play()
    menutext = pygame.font.Font("data/fonts/Daisy_Roots.otf", 40)
    ab = text.render(alphatext, False, (255, 255, 0))  # debug
    sel1 = seltext.render('Enter your name:', False, (255, 255, 0))
    sel2 = seltext.render('Press RCTRL to continue..', False, (255, 255, 0))
    MageDesc = seltext.render('Mages are proficient at magic but weak physically.', False, (178, 57, 63))
    WarDesc = seltext.render('Warriors specialize in physical attacks and buffs.', False, (178, 57, 63))
    clockTime = GameClock()  # Clock for the day/night system
    sel3 = seltext.render('Select your class:', False, secretbattle.txtcolor)
    sel4 = text.render('Mage', False, secretbattle.txtcolor)
    sel5 = text.render('Warrior', False, secretbattle.txtcolor)
    door = pygame.mixer.Sound('data/sounds&music/Door1.ogg')  # Door sound during newgame sequence
    gate = pygame.mixer.Sound('data/sounds&music/Door4.ogg')  # Gate sound  "          "     "
    bell = pygame.mixer.Sound('data/sounds&music/Bell1.ogg')  # Bell sound during night time
    rooster = pygame.mixer.Sound('data/sounds&music/Roost.ogg')  # Morning sound
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
    newgame = menutext.render('New Game', True, (255, 255, 0))  # Things for main menu
    loadgame = menutext.render('Load Game', True, loadgamecolor)
    quitgame = menutext.render('Quit Game', True, (255, 255, 0))
    namelist = ['']
    menubg1 = pygame.image.load("data/backgrounds/bg2.jpg").convert_alpha()
    arena_bg1 = pygame.image.load("data/backgrounds/arenaDay.png").convert_alpha()  # day time arena
    arena_bg2 = pygame.image.load("data/backgrounds/arenaEvening.png").convert_alpha()
    arena_bg3 = pygame.image.load("data/backgrounds/arenaNight.png").convert_alpha()
    inn_bg = pygame.image.load("data/backgrounds/inn.png").convert_alpha()
    logo = pygame.image.load("data/backgrounds/logo3.png").convert_alpha()  # Main menu logo
    cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
    newgbg = pygame.image.load("data/backgrounds/Meadow.png").convert_alpha()  # New game screen background
    loadsound = pygame.mixer.Sound('data/sounds&music/Load.ogg')
    cursorpos = 0
    Textbox = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()
    scene = 'menu'
    Currentmusic = 'data/sounds&music/Infinite_Arena.mp3'
    ui = MainUi()
    shh = []
    newTest = NewBattle(monster_data, item_data, sound_effects, animations, skills)  # New battle tester
    bellflag = False  # Flag for bell sound to play during time change
    txtbox = TextBox()
    timer = Timer()
    fadeoutflag = False  # Flag for music to fade out


    while not done:
        # main

        curwidth, curheight = screen.get_size()
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
                        rfile = open('savegame.dat', 'rb+')
                        pygame.mixer.music.stop()
                        loadsound.play()
                        player = pickle.load(rfile)
                        rfile.close()
                        fadein(255)
                        scene = 'arena'
                        load_flag = False
                        ui.cursorpos = 9
                        pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
                        pygame.mixer.music.play()
                    except:
                        print("Could not open")

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
                    fadein(255, 0.001)
                    door.play()
                    surf.fill((0, 0, 0))
                if event.key == pygame.K_RETURN and scene == 'new_game2' and cursorpos == 1:
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
                    fadein(255, 0.001)
                    door.play()
                    surf.fill((0, 0, 0))
                if event.key == pygame.K_RETURN and (
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
                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 0) and scene == 'arena' and controlui:  # Talk option
                    options = True
                    drawUi = False
                    controlui = False
                    event.key = 1  # So that it doesn't automatically pick the first option(input is annoying on pygame)

                if (event.key == pygame.K_RCTRL and options) or (event.key == pygame.K_RCTRL and talking):
                    drawui = True
                    controlui = True
                    ui.talked = False
                    options = False
                    talking = False

                if event.key == pygame.K_LEFT and options:  # Option screen control
                    floor1_talk.colpos -= 1
                    ui.cursorsound.play()
                if event.key == pygame.K_RIGHT and options:
                    floor1_talk.colpos += 1
                    ui.cursorsound.play()
                if event.key == pygame.K_UP and options:
                    floor1_talk.rowpos -= 1
                    ui.cursorsound.play()
                if event.key == pygame.K_DOWN and options:
                    floor1_talk.rowpos += 1
                    ui.cursorsound.play()
                if event.key == pygame.K_RETURN and options:
                    ui.txtbox.popup_reset()
                    if floor1_talk.rowpos == 0 and floor1_talk.colpos == 0:  # Option 1
                        talkval = 0
                        options = False
                        talking = True
                        floor1_talk.alert_off(1)
                    if floor1_talk.rowpos == 0 and floor1_talk.colpos == 1:  # Option 2
                        talkval = 1
                        options = False
                        talking = True
                        floor1_talk.alert_off(2)
                    if floor1_talk.rowpos == 0 and floor1_talk.colpos == 2:  # Option 3
                        talkval = 2
                        options = False
                        talking = True
                        floor1_talk.alert_off(3)
                    if floor1_talk.rowpos == 1 and floor1_talk.colpos == 0:  # Option 4
                        talkval = 3
                        options = False
                        talking = True
                        floor1_talk.alert_off(4)
                    if floor1_talk.rowpos == 1 and floor1_talk.colpos == 3:  # Back
                        drawui = True
                        controlui = True
                        ui.talked = False
                        options = False
                        talking = False

                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 1) and scene == 'arena' and controlui:  # Battle option
                    drawui = False
                    controlui = False
                    battle_choice = True
                    ui.txtbox.popup_reset()
                    ui.battalk = True
                    ui.batcursorpos = 4

                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 2) and scene == 'arena' and controlui:  # Status option
                    drawui = False
                    controlui = False
                    status = True
                if event.key == pygame.K_RCTRL and status:
                    drawui = True
                    controlui = True
                    status = False
                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 3) and scene == 'arena' and controlui:  # Shop option
                    drawui = False
                    controlui = False
                    arena_shop.txtbox.popup_reset()
                    shop = True
                if (event.key == pygame.K_RCTRL and shop) and arena_shop.shopkeep:
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
                if (
                        event.key == pygame.K_RETURN and shop) and not arena_shop.shopkeep and arena_shop.shop_selection_flag:
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
                        player.gold -= arena_shop.current_list[arena_shop.min_pos + arena_shop.shop_cursor_pos2]['cost']
                        if arena_shop.current_list == arena_shop.weapons_list:
                            player.cur_weapon = arena_shop.min_pos + arena_shop.shop_cursor_pos2
                        elif arena_shop.current_list == arena_shop.armour_list:
                            player.cur_armour = arena_shop.min_pos + arena_shop.shop_cursor_pos2
                        elif arena_shop.current_list == arena_shop.acc_list:
                            player.cur_accessory = arena_shop.min_pos + arena_shop.shop_cursor_pos2
                        player.update_stats()

                if (
                        event.key == pygame.K_RETURN and ui.cursorpos == 4) and scene == 'arena' and controlui:  # Inn option
                    pygame.mixer.music.pause()
                    fadein(255)
                    innsong.play()
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
                    innsong.stop()
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
                    randbattle = random.randrange(0, 4)
                    if randbattle == 0:
                        rand_mon = 'rat'
                    if randbattle == 1:
                        rand_mon = 'snake'
                    if randbattle == 2:
                        rand_mon = 'hornet'
                    if randbattle == 3:
                        rand_mon = 'imp'
                    battler.getplayerdetails(player)
                    battler.battle(rand_mon)
                    player.curhp = battler.curphealth
                    player.curmp = battler.curpmana
                    player.exp += battler.exp
                    player.gold += battler.gold
                    while player.check_levelup():
                        player.level += 1
                        player.hp += 25
                        player.mp += 10
                        player.str += 2
                        player.mag += 2
                        player.defe += 2

                    player.fkills += 1
                    player.tkills += 1
                    battle_choice = False
                    post_battle = True
                if (event.key == pygame.K_RETURN and ui.batcursorpos == 1) and battle_choice:
                    if player.fkills >= 5 and player.progress == 1:
                        battler.getplayerdetails(player)
                        fadein(255)
                        eventManager.firstfloor_boss(player.name)
                        battler.battle('floor_boss1', -50, True, bgm='data/sounds&music/boss_music.mp3')
                        player.curhp = battler.curphealth
                        player.curmp = battler.curpmana
                        player.exp += battler.exp
                        player.fkills = 0
                        player.tkills += 1
                        player.progress += 1
                        while player.check_levelup():
                            player.level += 1
                            player.hp += 25
                            player.mp += 10
                            player.str += 2
                            player.mag += 2
                            player.defe += 2
                    else:
                        secretbattle.buzzer.play()
                if (event.key == pygame.K_RETURN and ui.batcursorpos == 2) and battle_choice:
                    drawui = True
                    controlui = True
                    battle_choice = False
                if (event.key == pygame.K_RCTRL and battle_choice) and ui.battalk:
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
            elif event.type == VIDEORESIZE:
                curwidth, curheight = screen.get_size()
                screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                surf.blit(pygame.transform.scale(menubg1, (curwidth, curheight)), (0, 0))
                surf.blit(pygame.transform.scale(surf, (curwidth, curheight)), (0, 0))
                pygame.display.flip()
        name = "".join(namelist)
        if scene == 'menu':  # Main menu of the game(What you see on start-up)
            surf.blit(pygame.transform.scale(menubg1, (curwidth, curheight)), (0, 0))
            surf.blit(logo, (curwidth - 1100, curheight - 600))
            surf.blit(pygame.transform.scale(Textbox, (250, 180)), (450, 368))
            surf.blit(newgame, (474, 391))
            surf.blit(loadgame, (474, 431))
            surf.blit(quitgame, (474, 471))
            if shh == ['b', 'o', 's', 's'] and scene == 'menu':
                shh = []
                secretbattle.battle('secret_battle1', -10, False, bgm='data/sounds&music/Battle3.ogg')
            if shh == ['t', 'e', 's', 't'] and scene == 'menu':
                shh = []
                debugbattle.battle('debug_fight', -120, bgm='data/sounds&music/Dungeon2.ogg')
            if shh == ['t', 'o', 'w', 'n'] and scene == 'menu':
                shh = []
                fadeout(surf)
                eventManager.town_first_visit(player)
                fadeout(surf)
                pygame.mixer_music.load(Currentmusic)
                pygame.mixer_music.play()
            if shh == ['t', 'e', 't'] and scene == 'menu':
                newTest.battle('rat')
                shh = []
            if shh == ['t', 'o', 't'] and scene == 'menu':
                player.town_first_flag = False
                eventManager.town(player)
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
        if scene == 'new_game' or scene == 'new_game2':
            surf.blit(pygame.transform.scale(newgbg, (curwidth, curheight)), (0, 0))
        if scene == 'new_game':
            sel1 = seltext.render('Enter your name:' + name.capitalize(), False, secretbattle.txtcolor)
            if len(namelist) > 11:
                del namelist[len(namelist) - 1]
                secretbattle.buzzer.play()
            surf.blit(sel2, (500, 500))
            surf.blit(sel1, (300, 300))
            cursorpos = 0
        if scene == 'new_game2':

            surf.blit(sel3, (300, 300))
            surf.blit(sel4, (300, 375))
            surf.blit(sel5, (778, 375))
            warrior.blit(surf, (778, 429))
            mage.blit(surf, (300, 435))
            if cursorpos == 0:
                statstxt = seltext.render(
                    'STR:%d MAG:%d DEF:%d LUCK:%d' % (player.stre, player.mag, player.defe, player.luck), False,
                    (10, 33, 147))
                surf.blit(cursor, (260, 375))
                surf.blit(MageDesc, (260, 45))
                surf.blit(statstxt, (260, 95))
                player.str = 10
                player.mag = 25
                player.defe = 15

            elif cursorpos == 1:
                statstxt = seltext.render(
                    'STR:%d MAG:%d DEF:%d LUCK:%d' % (player.stre, player.mag, player.defe, player.luck), False,
                    (10, 33, 147))
                surf.blit(cursor, (738, 375))
                surf.blit(WarDesc, (260, 45))
                surf.blit(statstxt, (260, 95))
                player.str = 20
                player.mag = 10
                player.defe = 20
            if cursorpos < 0:
                cursorpos = 1
            if cursorpos > 1:
                cursorpos = 0
        if scene == 'new_game3':

            if timer.timing() == 2:
                timepassed = True

            if timepassed:
                surf.fill((0, 0, 0))
                if newgtxtbox == 1:
                    txtbox.draw_textbox("data/sprites/host_face.png", '???', 'Oh? who do we have here?')
                if newgtxtbox == 2:
                    txtbox.draw_textbox("data/sprites/host_face.png", '???', 'A new challenger? You seem quite young!')
                if newgtxtbox == 3:
                    txtbox.draw_textbox("data/sprites/host_face.png", '???',
                                        'Me? I\'m the one they call the host of the arena.')
                if newgtxtbox == 4:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'But you can call me Chance!')
                if newgtxtbox == 5:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'Well, if you want to register I\'m not stopping you.')
                if newgtxtbox == 6:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'So far only one warrior has emerged victorius from the arena, 2 years ago.')
                if newgtxtbox == 7:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Countless others have tried and failed.',
                                        'Many have lost their lives beyond these gates.')
                if newgtxtbox == 8:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'This is your last chance, there is no shame in turning back.')
                if newgtxtbox == 9:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', '...')
                if newgtxtbox == 10:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'You are an interesting fellow.')
                if newgtxtbox == 11:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Very well, you may step forward..')
                if newgtxtbox == 12:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', '..And enter the Arena!')
                if newgtxtbox > 12:
                    gate.play()
                    fadein(255, 0.005)
                    timepassed = False
                    timer.reset()
                    scene = 'new_game4'
                    newgtxtbox = 1
        if scene == 'new_game4':
            if timer.timing() == 1 and (not timepassed):
                pygame.mixer.music.load('data/sounds&music/Infinite_Arena.mp3')
                pygame.mixer.music.play()
                timepassed = True
            surf.blit(pygame.transform.scale(arena_bg1, (curwidth, curheight)), (0, 0))
            if timepassed:
                if newgtxtbox == 1:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Welcome to the Arena my friend!')
                if newgtxtbox == 2:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Let me explain to you how this works.')
                if newgtxtbox == 3:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'The Arena has 3 floors. Each floor has 5 regular enemies and 1 \'Floor Boss\'.')
                if newgtxtbox == 4:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'After your preparations, you can come to me if you are ready to fight.')
                if newgtxtbox == 5:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'I will let you fight a regular enemy in the floor you are on.')
                if newgtxtbox == 6:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'After you defeat 5 regular enemies you can challenge the Floor boss.')
                if newgtxtbox == 7:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'If you don\'t feel like you\'re ready you can fight more regular enemies before',
                                        'challenging the boss.')
                if newgtxtbox == 8:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'After you defeat the floor boss, you can proceed to the next floor.')
                if newgtxtbox == 9:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'Also, Enemies drop gold when they\'re defeated.',
                                        'You can use the gold to buy items and equipment from',
                                        'our shop after every battle!')
                if newgtxtbox == 10:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'If you\'re able to defeat the final Floor boss you will be crowned',
                                        'the \'Arena Champion!\'')
                if newgtxtbox == 11:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'One more thing..')
                if newgtxtbox == 12:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'Before a battle you may talk with people around the Arena.')
                if newgtxtbox == 13:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                        'Who knows, maybe you may learn a useful tip or two from them!')
                if newgtxtbox == 14:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Well, I\'m sure you\'re raring to go.',
                                        'Let me know when you\'re ready for your first battle!')
                if newgtxtbox == 15:
                    txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Good luck friend, lord knows you need it!')
                    clockTime.reset()
                if newgtxtbox > 15:
                    scene = 'arena'
        if scene == 'arena':
            clockTime.pass_time(player) # passage of ingame time
            if clockTime.time_state == 'Morning':
                surf.blit(pygame.transform.scale(arena_bg1, (curwidth, curheight)), (0, 0))  # day bg
            elif clockTime.time_state == 'Noon':
                surf.blit(pygame.transform.scale(arena_bg2, (curwidth, curheight)), (0, 0))  # Noon bg
            else:
                surf.blit(pygame.transform.scale(arena_bg3, (curwidth, curheight)), (0, 0))  # Night bg

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
                floor1_talk.drawUi(4, 'Old Man', 'Boy', 'Villager', 'Stranger')
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
        if scene == 'inn':
            surf.blit(pygame.transform.scale(inn_bg, (curwidth, curheight)), (0, 0))
            if drawui:
                ui.draw_inn(player.gold)
            if ui.cursorpos > 2:
                ui.cursorpos = 0
            if ui.cursorpos < 0:
                ui.cursorpos = 2
        if scene == 'credits':
            surf.fill((0, 0, 0))
            if newgtxtbox == 1:
                txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Hey congrats you beat the demo!')
            if newgtxtbox == 2:
                txtbox.draw_textbox("data/sprites/host_face.png", 'Chance',
                                    'There is more to come but ill save that for another time.')
            if newgtxtbox == 3:
                txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'This was a project made by Hameel and Nihal!')
            if newgtxtbox == 4:
                txtbox.draw_textbox("data/sprites/host_face.png", 'Chance', 'Stay tuned for the final project!')

            if newgtxtbox > 4:
                scene = 'menu'
        timer.timing()
        surf.blit(ab, (0, 0))
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)
        fps = "FPS:%d" % clock.get_fps()
        pygame.display.set_caption(fps)
    pygame.quit()
