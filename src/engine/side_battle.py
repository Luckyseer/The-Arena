import pygame
import random
from data import pyganim
from src.utils.timer import Timer, fadein, fadeout
from src.models.player import Player

class SideBattle:
    """ The sidebattle class, which provides us with the main gameplay(the battle system)
        Needs some work, could be a lot more efficient.
        Currently, needs some work on the aesthetics side.
        THIS CLASS IS DEPRECATED AND ONLY EXISTS FOR COMPATIBILITY"""

    # The stats for the monster are by default for the weakest enemy 'rat', remember to change the stats as needed.
    def __init__(self, surface, monsterdata, monster, animationdata, background, music, phealth=100, pmana=50, pstr=10, pstrmod=1, pdef=10,
                 pmag=20, pluck=2):
        self.surface = surface
        self.mondata = monsterdata
        self.pclass = monster
        self.players = [1, pyganim.PygAnimation(animationdata)]
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

        self.surface.blit(pygame.transform.scale(self.ui1, (curwidth, 300)), (0, 430))
        self.surface.blit(self.nametext, (332, 474))
        self.surface.blit(self.hptxt, (463, 474))
        self.surface.blit(self.mptxt, (675, 474))
        self.surface.blit(curhealth, (503, 474))
        self.surface.blit(curmana, (715, 474))
        if self.state == 'player':
            self.surface.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            self.surface.blit(self.atk, (38, 474))
            self.surface.blit(self.item, (38, 534))
            if self.pclass == 'mage':
                self.surface.blit(self.mag, (38, 504))
            if self.pclass == 'warrior':
                self.surface.blit(self.ski, (38, 504))

            if self.cursorpos == 0:
                self.surface.blit(self.cursor, (6, 474))
            elif self.cursorpos == 1:
                self.surface.blit(self.cursor, (6, 504))
            elif self.cursorpos == 2:
                self.surface.blit(self.cursor, (6, 534))
        if self.state == 'skill':
            self.getskills()
            self.surface.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            self.surface.blit(self.skitxt, (38, 464))
            self.surface.blit(self.cancel, (38, 494))
            if self.cursorpos == 0:  # burst
                self.surface.blit(self.cursor, (6, 464))
                self.surface.blit(self.burstdesc, (328, 577))
            elif self.cursorpos == 1:  # cancel
                self.surface.blit(self.cursor, (6, 494))

        if self.state == 'magic':
            self.getmagic()
            self.surface.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            self.surface.blit(self.magtxt1, (38, 464))
            self.surface.blit(self.magtxt2, (38, 494))
            self.surface.blit(self.magtxt3, (38, 524))
            self.surface.blit(self.magtxt4, (38, 554))
            self.surface.blit(self.magtxt5, (38, 584))
            self.surface.blit(self.cancel, (38, 614))
            if self.cursorpos == 0:  # fire
                self.surface.blit(self.cursor, (6, 464))
                self.surface.blit(self.firedesc, (328, 577))
                if self.plevel < 5:
                    self.surface.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 1:  # ice
                self.surface.blit(self.cursor, (6, 494))
                self.surface.blit(self.icedesc, (328, 577))
                if self.plevel < 8:
                    self.surface.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 2:  # cure
                self.surface.blit(self.cursor, (6, 524))
                self.surface.blit(self.curedesc, (328, 577))
                if self.plevel < 12:
                    self.surface.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 3:  # death
                self.surface.blit(self.cursor, (6, 554))
                self.surface.blit(self.deathdesc, (328, 577))
                if self.plevel < 18:
                    self.surface.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 4:  # tsunami
                self.surface.blit(self.cursor, (6, 584))
                self.surface.blit(self.tsunamidesc, (328, 577))
                if self.plevel < 20:
                    self.surface.blit(self.notlearnedtxt, (328, 547))
            elif self.cursorpos == 5:  # cancel
                self.surface.blit(self.cursor, (6, 614))
        if self.state == 'item':
            self.getitems()
            self.surface.blit(pygame.transform.scale(self.ui2, (300, 300)), (0, 430))
            self.surface.blit(self.itemtxtlist[0], (38, 464))
            self.surface.blit(self.cancel, (38, 494))
            if self.cursorpos == 0:
                self.surface.blit(self.cursor, (6, 464))
                self.surface.blit(self.potiondesc, (328, 577))
            elif self.cursorpos == 1:
                self.surface.blit(self.cursor, (6, 494))

        if self.pstatus == 'burst':
            self.surface.blit(self.staticon1, (800, 474))
        if self.bgflag:
            self.surface.blit(self.actionbg, (495, 73))
            self.surface.blit(self.bgtxt, (604, 83))

    def healthbar(self, animpos=0):  # Enemy health bar
        healthpercent = (self.virtualMonsterHealth / self.mmaxhealth) * 100
        if healthpercent < 0:
            healthpercent = 0.1
        self.surface.blit(pygame.transform.scale(self.hpbarEmpty, (260, 18)),
                  (self.monpos[0], self.monpos[1] + 100 - animpos))
        self.surface.blit(pygame.transform.scale(self.hpbarFull, (int(246 * (healthpercent / 100)), 18)),
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
        dark = pygame.Surface(self.surface.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        self.surface.blit(dark, (0, 0))

        deftxt = pygame.font.Font("data/fonts/Daisy_Roots.otf", 70)
        defeat = deftxt.render('Defeat!', True, (255, 0, 0)).convert_alpha()
        cont = self.uitext.render(
            'Your journey isn\'t over yet! Move onward!', True, (255, 255, 0)).convert_alpha()
        self.surface.blit(defeat, ((curwidth / 3) - 30, curheight / 5))
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
                        # global scene, battle_choice, post_battle, drawui, controlui
                        scene = 'menu'
                        battle_choice = False
                        post_battle = False
                        drawui = True
                        controlui = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posfinder()
            if not cFlag:
                if timer.dothing(2):
                    self.surface.blit(cont, (407, 253))

                    cFlag = True

            screen.blit(self.surface, (0, 0))
            clock.tick(60)
            pygame.display.update()

    # raises the victory flag,ends the match when set to true.
    def victory(self):
        timer = Timer()
        pygame.mixer.music.pause()
        pygame.mixer.music.load('data/sounds&music/Victory_and_Respite.mp3')
        pygame.mixer.music.play()
        dark = pygame.Surface(self.surface.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        self.surface.blit(dark, (0, 0))
        self.surface.blit(self.vicimg, (curwidth / 3, curheight / 5))
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
                    self.surface.blit(gold, (427, 253))
                    self.coinanim.play()
                    gFlag = True
            if not eFlag:
                if timer.dothing(2):
                    self.surface.blit(exp, (427, 287))
                    self.xpanim.play()
                    eFlag = True
            if not lFlag:
                if timer.dothing(6):
                    if (self.exp >= self.xptolevel) and (eFlag and gFlag):
                        self.levelupsound.play()
                        self.surface.blit(lvlup, (427, 321))
                        self.surface.blit(statup, (427, 354))
                    lFlag = True

            self.coinanim.blit(self.surface, (397, 253))
            self.xpanim.blit(self.surface, (397, 287))
            screen.blit(self.surface, (0, 0))
            clock.tick(60)
            pygame.display.update()

    # Method to get the players current stats and other details.
    def getplayerdetails(self, player):
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
        fadein(pygame.display.get_surface(), 255)
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
        # global screen
        while self.battling:
            curwidth, curheight = screen.get_size()
            self.surface.blit(pygame.transform.scale(
                self.bg, (curwidth, curheight)), (0, 0))

            if get:
                self.monpos = (curwidth - 1080, 200 + self.extraheight)

                get = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.battling = False
                    # global done
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
            self.surface.blit(self.pshadow, [curwidth - 320, 305])
            self.players[0].blit(self.surface, [curwidth - 331, 280])
            self.players[1].blit(self.surface, [curwidth - 331, 280])
            self.burstanim.blit(self.surface, [curwidth - 331, 280])
            self.cureanim.blit(self.surface, [curwidth - 391, 240])
            if not enemydead:
                self.surface.blit(self.monsters, self.monpos)

            # battleflow timer - controls flow of battle(animations,timing,etc.)
            self.battleflow.timing()
            self.mhurt.blit(self.surface, [curwidth - 331, 280])
            self.slashanim.blit(self.surface, self.monpos)
            self.clawanim.blit(self.surface, [curwidth - 381, 255])
            self.specialanim.blit(self.surface, [curwidth - 381, 255])
            self.thunderanim.blit(self.surface, [curwidth - 381, 255])
            self.castanim.blit(self.surface, [curwidth - 409, 200])
            self.fireanim.blit(
                self.surface, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.iceanim.blit(
                self.surface, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.deathanim.blit(
                self.surface, (self.monpos[0], self.monpos[1] - self.extraheight))
            self.wateranim.blit(
                self.surface, (self.monpos[0], (self.monpos[1] + 100) - self.extraheight))
            self.statuswindow()
            self.surface.blit(ab, (0, 0))
            screen.blit(self.surface, [0, 0])

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
                self.surface.blit(
                    dmgtxt, (self.monpos[0] + 100, self.monpos[1] - dmgtxtpos))
                screen.blit(self.surface, (0, 0))

            if cure:
                self.surface.blit(dmgtxt, [curwidth - 331, 240])
                screen.blit(self.surface, (0, 0))
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
                        screen.blit(self.surface, (0, 0))
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
                    self.surface.blit(
                        dmgtxt, (self.monpos[0] + 100, self.monpos[1] - dmgtxtpos))
                    self.healthbar(hpbarpos)
                    screen.blit(self.surface, (0, 0))

                if critted:
                    self.surface.blit(self.crittxt,
                              (self.monpos[0] + 100, self.monpos[1] - 70))
                    screen.blit(self.surface, (0, 0))

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
                    self.surface.blit(dmgtxt, [curwidth - 331, 280])
                    screen.blit(self.surface, (0, 0))
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
                self.surface.blit(self.deathsprite, [curwidth - 331, 280])
                screen.blit(self.surface, (0, 0))
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
        dark_surf = pygame.Surface(self.surface.get_size(), 32)
        dark_surf.set_alpha(128, pygame.RLEACCEL)
        self.surface.blit(dark_surf, (0, 0))
        gold_txt = self.ui_font.render(
            'Gold:+%d' % self.f_gold, True, (255, 255, 0))
        exp_txt = self.ui_font.render(
            'Exp:+%d' % self.f_exp, True, (244, 240, 66))
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
        alpha = text.render(alphatext, False, (255, 255, 0))
        self.battling = True
        self.monster_flag = True
        self.draw_menu = True
        self.add_flag = False
        self.get_monster_details(monster_name)
        self.get_player_details(player_data)
        self.play_sound('encounter')
        self.set_instance(player_data)
        fadein(pygame.display.get_surface(), 255)
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
            screen.blit(self.surface, (self.camera_x, self.camera_y))
            pygame.display.update()
            clock.tick(60)
            fps = "FPS:%d" % clock.get_fps()
            pygame.display.set_caption(fps)
