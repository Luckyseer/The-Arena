#Alpha V2.0
from __future__ import print_function#For compatibility with python 2.x
import pygame
from pygame.locals import *
import pyganim
import random
import pickle
from math import floor
icon=pygame.image.load('sprites/icon2.png')
pygame.display.set_icon(icon)
class Player():
    """Hold all the player information"""
    def __init__(self,name='Zen',health=100,mana=50,strength=10,magic=20,defence=10,luck=2):
        self.name=name
        self.hp=health
        self.curhp=self.hp
        self.mp=mana
        self.curmp=self.mp
        self.str=strength
        self.defe=defence
        self.mag=magic
        self.luck=luck
        self.progress=1#progress in game
        self.gold=100
        self.level=15
        self.exp=0    
        self.inventory={'Potion':1,  #Heals 200 HP
                        'Bread':0,  #Heals 50 HP
                        'Steak':0,  #Heals 120 HP
                        'Meat Stew':0,  #Heals 250 HP
                        'Roasted Beef':0,  #Heals 500 HP
                        'Elixir':0,  #Fully heals HP and MP
                        'Mana Potion':0,  #Restores 100 MP
                        'Water':0,  #Restores 20MP
                        'Orange Juice':0,  #Restores 50MP
                        'Orc Tears':0,  #Restores 150MP
                        'Dragon\'s Breath':0, #Restores 250MP
                        }
        self.pclass='warrior'
        self.fkills=0#Kills in floor
        self.tkills=0#Total Kills
    def xp_till_levelup(self,currentlevel):#Experience needed to level up
        
        self.expreq = floor((currentlevel**4)/5)
        return self.expreq
    def check_levelup(self): #Check if player has leveled up
        self.xp_till_levelup(self.level)
        if self.exp >= self.expreq:
            return True
        else:
            return False

class Equipment:
    def __init__(self,attack,defence,luck):
        self.atk=attack
        self.defe=defence
        self.luck=luck
    def getstats(self):
        return (self.atk,self.defe,self.luck)

pygame.init()

isfullscreen=True
screen_width=1280
screen_height=720
##Note to self: remove debug lines after done##
block_list = pygame.sprite.Group()
all_sprites_list= pygame.sprite.Group()
clock = pygame.time.Clock()
screen=pygame.display.set_mode([screen_width,screen_height],HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('The Arena')
done=False
def posfinder():#Used to find position of mouse
    posx,posy=pygame.mouse.get_pos()
    print (posx,posy)

class Timer():
    """The Timer class, used to time things in-game."""
    def __init__(self,delay=100):
        self.start = int(pygame.time.get_ticks())
        self.delay = delay
    def timing(self):
        seconds = int((pygame.time.get_ticks()-self.start)/1000)#How many seconds passed
        return seconds
    def reset(self):
        self.start = int(pygame.time.get_ticks())
    def dothing(self,time):
        seconds=self.timing()
        if seconds>=time:
            print("Doing thing")#debug
            return True
        
def fadein(rgb,time=1):#fadein effect
     global screen
     for color in range(0,rgb):
             pygame.time.wait(time)
             r=color
             g=color
             b=color
             screen.fill([r,g,b])
             pygame.display.flip()
             
class sidebattle():
    """ The sidebattle class, which provides us with the main gameplay(the battle system)
        Needs some work, could be a lot more efficient.
        Currently the battles are completely customizable which makes things very convenient. """
    #The stats for the monster are by default for the weakest enemy 'rat', remember to change the stats as needed.
    def __init__(self,pclass,castanim,monstersprites,bg,bgm,phealth=100,pmana=50,pstr=10,pstrmod=10,pdef=10,pmag=20,pluck=2,mhealth=240,mstr=15,mdef=12,mmag=10,gold=100,exp=50):
        self.players=[1,pyganim.PygAnimation(castanim)]
        self.pname='Zen'
        self.plevel=5
        self.xptolevel=100
        self.monsters=pygame.image.load(monstersprites).convert_alpha()
        self.inventory={'Potion':1,'Mana Potion':1}
        self.mhurt=pyganim.PygAnimation([('sprites/mhurt1.png',0.3),('sprites/mhurt2.png',0.3),('sprites/mhurt3.png',0.3)])
        self.staticon1=pygame.image.load('sprites/attack+.png').convert_alpha()
        self.pshadow=pygame.image.load('system/Shadow1.png').convert_alpha()
        self.encountersound=pygame.mixer.Sound('sounds&music/Battle2.ogg')
        self.cursorsound=pygame.mixer.Sound('sounds&music/Cursor1.ogg')
        self.buzzer=pygame.mixer.Sound('sounds&music/Buzzer1.ogg')
        self.bg=pygame.image.load(bg).convert_alpha()
        self.players[1].convert_alpha()
        self.turn=1
        self.burstanim=pyganim.PygAnimation([('sprites/burst1.png',0.3),('sprites/burst2.png',0.3),('sprites/burst3.png',0.3)])
        self.castanim=pyganim.PygAnimation([('sprites/cast1.png',0.1),('sprites/cast2.png',0.1),('sprites/cast3.png',0.1),('sprites/cast4.png',0.1),('sprites/cast5.png',0.5)],False)
        self.coinanim=pyganim.PygAnimation([('sprites/coin1.png',0.1),('sprites/coin2.png',0.1),('sprites/coin3.png',0.1),('sprites/coin4.png',0.1),('sprites/coin5.png',0.1),('sprites/coin6.png',0.1),('sprites/coin7.png',0.1),('sprites/coin8.png',0.1),('sprites/coin9.png',0.1)])
        self.fireanim=pyganim.PygAnimation([('sprites/Fire1.png',0.1),('sprites/Fire2.png',0.1),('sprites/Fire3.png',0.1),('sprites/Fire4.png',0.1),('sprites/Fire5.png',0.1),('sprites/Fire6.png',0.1),('sprites/Fire7.png',0.1),('sprites/Fire8.png',0.1)],False)
        self.iceanim=pyganim.PygAnimation([('sprites/Ice1.png',0.09),('sprites/Ice2.png',0.09),('sprites/Ice3.png',0.09),('sprites/Ice4.png',0.09),('sprites/Ice5.png',0.09),('sprites/Ice6.png',0.09),('sprites/Ice7.png',0.09),('sprites/Ice8.png',0.09),('sprites/Ice9.png',0.09),('sprites/Ice10.png',0.09),('sprites/Ice11.png',0.09),('sprites/Ice12.png',0.09),('sprites/Ice13.png',0.09),('sprites/Ice14.png',0.09),('sprites/Ice15.png',0.09),('sprites/Ice16.png',0.09),('sprites/Ice17.png',0.09),('sprites/Ice18.png',0.1)],False)
        self.deathanim=pyganim.PygAnimation([('sprites/Death1.png',0.1),('sprites/Death2.png',0.1),('sprites/Death3.png',0.1),('sprites/Death4.png',0.1),('sprites/Death5.png',0.1),('sprites/Death6.png',0.1),('sprites/Death7.png',0.1),('sprites/Death8.png',0.1),('sprites/Death9.png',0.1),('sprites/Death10.png',0.1),('sprites/Death11.png',0.1),('sprites/Death12.png',0.1)],False)
        self.cureanim=pyganim.PygAnimation([('sprites/Cure1.png',0.1),('sprites/Cure2.png',0.1),('sprites/Cure3.png',0.1),('sprites/Cure4.png',0.1),('sprites/Cure5.png',0.1),('sprites/Cure6.png',0.1),('sprites/Cure7.png',0.1),('sprites/Cure8.png',0.1),('sprites/Cure9.png',0.1),('sprites/Cure10.png',0.1),('sprites/Cure11.png',0.1),('sprites/Cure12.png',0.1),('sprites/Cure13.png',0.1),('sprites/Cure14.png',0.1),('sprites/Cure15.png',0.1)],False)
        self.curesound=pygame.mixer.Sound('sounds&music/Item3.ogg')
        self.icesound=pygame.mixer.Sound('sounds&music/Ice4.ogg')
        self.deathmagsound=pygame.mixer.Sound('sounds&music/Darkness5.ogg')
        self.firesound=pygame.mixer.Sound('sounds&music/Fire2.ogg')
        self.watersound1=pygame.mixer.Sound('sounds&music/Water5.ogg')
        self.watersound2=pygame.mixer.Sound('sounds&music/Water1.ogg')
        self.levelupsound=pygame.mixer.Sound('sounds&music/levelup.wav')
        self.coinanim.convert_alpha()
        self.castsound=pygame.mixer.Sound('sounds&music/Magic4.ogg')
        self.attacksound=pygame.mixer.Sound('sounds&music/Slash1.ogg')
        self.thunderanim = pyganim.PygAnimation([('sprites/Thunder1.png',0.2),('sprites/Thunder2.png',0.1),('sprites/Thunder3.png',0.1),('sprites/Thunder4.png',0.1),('sprites/Thunder5.png',0.1)],False)
        self.thunderanim.convert_alpha()
        self.wateranim=pyganim.PygAnimation([('sprites/Water1.png',0.1),('sprites/Water2.png',0.1),('sprites/Water3.png',0.1),('sprites/Water4.png',0.1),('sprites/Water5.png',0.1),('sprites/Water6.png',0.1),('sprites/Water7.png',0.1),('sprites/Water8.png',0.1),('sprites/Water9.png',0.1),('sprites/Water10.png',0.1),('sprites/Water11.png',0.1),('sprites/Water12.png',0.1),('sprites/Water13.png',0.1),('sprites/Water14.png',0.1),('sprites/Water15.png',0.1),('sprites/Water16.png',0.1),('sprites/Water17.png',0.1),('sprites/Water18.png',0.1)],False)
        self.thundersound=pygame.mixer.Sound('sounds&music/Thunder9.ogg')
        self.deathsprite=pygame.image.load('sprites/death.png').convert_alpha()
        self.attacksound2=pygame.mixer.Sound('sounds&music/Slash2.ogg')
        self.deadsound=pygame.mixer.Sound('sounds&music/Collapse1.ogg')
        self.skillsound=pygame.mixer.Sound('sounds&music/Skill1.ogg')
        self.attack='attack'
        self.state='player'
        self.enemymovelist=['attack']
        self.phealth=phealth#p-player m-monster
        self.curphealth=phealth
        self.pmana=pmana
        self.curpmana=self.pmana
        self.pstr=pstr
        self.slashanim=pyganim.PygAnimation([('sprites/Slash1.png',0.1),('sprites/Slash2.png',0.1),('sprites/Slash3.png',0.1),('sprites/Slash4.png',0.1),('sprites/Slash5.png',0.1)],False)
        self.slashanim.convert_alpha()
        self.clawanim=pyganim.PygAnimation([('sprites/Claw1.png',0.1),('sprites/Claw2.png',0.1),('sprites/Claw3.png',0.1),('sprites/Claw4.png',0.1),('sprites/Claw5.png',0.1)],False)
        self.clawanim.convert_alpha()
        self.xpanim=pyganim.PygAnimation([('sprites/xp1.png',0.1),('sprites/xp2.png',0.1),('sprites/xp3.png',0.1),('sprites/xp4.png',0.1),('sprites/xp5.png',0.1),('sprites/xp6.png',0.1),('sprites/xp7.png',0.1),('sprites/xp8.png',0.1),('sprites/xp9.png',0.1)])
        self.xpanim.convert_alpha()
        self.specialanim=pyganim.PygAnimation([('sprites/Special1.png',0.1),('sprites/Special2.png',0.1),('sprites/Special3.png',0.1),('sprites/Special4.png',0.1),('sprites/Special5.png',0.1),('sprites/Special6.png',0.1),('sprites/Special7.png',0.1),('sprites/Special8.png',0.1),('sprites/Special9.png',0.1),('sprites/Special10.png',0.1),('sprites/Special11.png',0.1),('sprites/Special12.png',0.1),('sprites/Special13.png',0.1),('sprites/Special14.png',0.1),('sprites/Special15.png',0.1),('sprites/Special16.png',0.1),('sprites/Special17.png',0.1),('sprites/Special18.png',0.1),('sprites/Special19.png',0.1),('sprites/Special20.png',0.1),],False)
        self.specialanim.convert_alpha()
        self.enemyattacking=False
        self.bgm=bgm
        self.pclass=pclass
        self.pstrmod=pstrmod
        self.pdef=pdef
        self.pmag=pmag
        self.pluck=pluck
        self.mhealth=mhealth
        self.mmaxhealth=self.mhealth
        self.mstr=mstr
        self.mdef=mdef
        self.mmag=mmag
        self.pstatus='normal'
        self.gold=gold
        self.crit=0
        self.exp=exp
        self.magic=['Fire','Ice','Cure','Death','Tsunami']
        self.skilllist=['Burst']
        self.cursorpos=0
        self.txtcolor=(21,57,114)   
        self.gotskills=False
        self.gotmagic=False
        self.gotitems=False
        self.battleflow=Timer()
        self.ui1=pygame.image.load('backgrounds/rpgtxt.png').convert_alpha()
        self.ui2=pygame.image.load('backgrounds/rpgtxt.png').convert_alpha()
        self.cursor=pygame.image.load('sprites/Cursor.png').convert_alpha()
        self.cursormax=2
        self.uitext=pygame.font.Font('runescape_uf.ttf',30)#Default font for Ui
        self.uitext2=pygame.font.Font('Vecna.otf',30)
        self.burstdesc=self.uitext.render('Greatly strengthens next attack for 1 turn. MP COST:15',False,(37,61,36))
        self.firedesc=self.uitext.render('Deal small Fire damage to the enemy. MP COST:5',False,(37,61,36))
        self.icedesc=self.uitext.render('Deal small Ice damage to the enemy. MP COST:10',False,(37,61,36))
        self.curedesc=self.uitext.render('Restores a small amount of health. MP COST:15',False,(37,61,36))
        self.deathdesc=self.uitext.render('Invokes death upon your foe. Chance of instantly killing your enemy. MP COST:30',False,(37,61,36))
        self.tsunamidesc=self.uitext.render('Creates a devastating flood and deals massive Water damage to enemies. MP COST:50',False,(37,61,36))
        self.potiondesc=self.uitext.render('Heals 50 Health',False,(37,61,36))
        self.atk=self.uitext.render('Attack',False,self.txtcolor).convert_alpha()
        self.mag=self.uitext.render('Magic',False,(self.txtcolor)).convert_alpha()
        self.ski=self.uitext.render('Skill',False,self.txtcolor).convert_alpha()
        self.item=self.uitext.render('Item',False,self.txtcolor).convert_alpha()
        self.cancel=self.uitext.render('Cancel',False,self.txtcolor).convert_alpha()
        self.crittxt=self.uitext2.render('Critical!',False,(200,0,0)).convert_alpha()
        self.nametext=self.uitext.render(self.pname,False,(61,61,58)).convert_alpha()
        self.hptxt=self.uitext.render('HP:',True,(255,21,45)).convert_alpha()
        self.mptxt=self.uitext.render('MP:',True,(29,21,255)).convert_alpha()
        self.notlearnedtxt=self.uitext.render('Not learned yet!',True,(255,21,45)).convert_alpha()
        self.victoryflag=False
        self.defeatflag=False
        self.bgtxt=self.uitext.render('',False,(self.txtcolor)).convert_alpha()#Action bg txt
        self.bgflag=False #action bg flag
        self.actionbg=pygame.transform.scale(self.ui1,((300,50)))
        self.vicimg=pygame.image.load('sprites/victory.png').convert_alpha()
        self.mdeathresist=False #Check if monster resists the 'death' spell or not
        self.extraheight=0 #Extra height for position of monster image if needed
        self.hpbarEmpty=pygame.image.load('sprites/hpbar1.png').convert_alpha()
        self.hpbarFull=pygame.image.load('sprites/hpbar2.png').convert_alpha()
                                         

    def getitems(self):
        self.itemtxtlist=[]
        self.itemlist=[]
        if self.gotitems==False:
           for item in self.inventory:
            if self.inventory[item]>0:
             txt=self.uitext.render(str(item)+'   x'+str(self.inventory[item]),False,self.txtcolor)
             self.itemtxtlist.append(txt)
             self.itemlist.append(item)
           self.gotitems==True
        
    def getskills(self):
        if self.gotskills==False:
          self.skitxt=self.uitext.render(self.skilllist[0],False,self.txtcolor)
          self.gotskills=True
          
    def getmagic(self):
        if self.gotmagic==False:
          if self.plevel>=5:  
           self.magtxt1=self.uitext.render(self.magic[0],False,self.txtcolor)
          elif self.plevel<5:
           self.magtxt1=self.uitext.render(self.magic[0],False,(105,109,114))
           
          if self.plevel>=8: 
            self.magtxt2=self.uitext.render(self.magic[1],False,self.txtcolor)
          else:
           self.magtxt2=self.uitext.render(self.magic[1],False,(105,109,114))
          
          if self.plevel>=12:  
            self.magtxt3=self.uitext.render(self.magic[2],False,self.txtcolor)
          else:
           self.magtxt3=self.uitext.render(self.magic[2],False,(105,109,114))
         
          if self.plevel>=18:  
             self.magtxt4=self.uitext.render(self.magic[3],False,self.txtcolor)
          else:
           self.magtxt4=self.uitext.render(self.magic[3],False,(105,109,114))                                 
          if self.plevel>=20:   
             self.magtxt5=self.uitext.render(self.magic[4],False,self.txtcolor)
          else:
           self.magtxt5=self.uitext.render(self.magic[4],False,(105,109,114))                                 
          self.gotmagic=True
          
          
    def calcdamage(self,dmgtype='normal'):#The damage calculation formula, calculates player damage during players turn and enemies damage during the enemies turn.
        if dmgtype=='thunder' and self.state=='enemy':#temp make sure to change
            damage=(self.pmag*self.pstrmod)/((0.3)*self.pdef)-random.randrange(0,10)
        if dmgtype=='fire':
            damage=(self.pmag*self.pstrmod)/((0.3)*self.mdef)-random.randrange(0,10)
        if dmgtype=='ice':
            damage=(self.pmag*self.pstrmod)/((0.2)*self.mdef)-random.randrange(0,10)
        if dmgtype=='water':
            damage=(self.pmag*self.pstrmod)*3/((0.2)*self.mdef)-random.randrange(0,10)
        if dmgtype=='death':
            if self.mdeathresist:
                return 'Resist!'
            else:
                deathluck=random.randrange(1,6)#1 in 5 chance of success
                print ('Deathluck:',deathluck)
                if deathluck==5:
                    damage=99999
                else:
                    return 'Failed!'
        if dmgtype=='cure':#Not really damage but eh
            damage=((self.phealth*10)/35)-random.randrange(0,6)
        elif self.state == 'attack':
            if self.attack=='attack':
               
                self.crit=random.randrange(self.pluck,11)#critical strike chance, higher probability with higher luck,will always crit if player has 10 luck.
                if self.pluck>=10:
                    self.crit=10
                print (self.crit)
                if self.pstatus=='burst':
                     damage=((self.pstr*self.pstrmod)/((0.5)*self.mdef)*5)-random.randrange(0,10)
                elif self.crit == 10:
                    damage=((self.pstr*self.pstrmod)/((0.5)*self.mdef)*4)-random.randrange(0,10)
                else:
                    damage=((self.pstr*self.pstrmod)/((0.5)*self.mdef)*2)-random.randrange(0,10)
        elif self.state == 'enemyattack':
            if self.attack=='attack':
                damage=(self.mstr*self.pstrmod)/((0.5)*self.pdef)-random.randrange(0,10)
        print(self.state)
        if damage<0:
            damage=0
        elif damage>99999:
            damage=99999
        return int(damage)
    
    def statuswindow(self):#The main UI during the battle. Needs some work
        self.nametext=self.uitext.render(self.pname,False,(61,61,58)).convert_alpha()

        curhealth=self.uitext.render(str(self.curphealth)+'/'+str(self.phealth),False,(114,21,45))

        curmana=self.uitext.render(str(self.curpmana)+'/'+str(self.pmana),False,(29,21,114))
        
        surf.blit(pygame.transform.scale(self.ui1, ((curwidth , 300 ))),(0,430))
        surf.blit(self.nametext,(332,474))
        surf.blit(self.hptxt,(463,474))
        surf.blit(self.mptxt,(675,474))
        surf.blit(curhealth,(503,474))
        surf.blit(curmana,(715,474))
        if self.state == 'player':
            surf.blit(pygame.transform.scale(self.ui2, ((300 , 300 ))),(0,430))
            surf.blit(self.atk,(38,474))
            surf.blit(self.item,(38,534))
            if self.pclass=='mage':
              surf.blit(self.mag,(38,504))
            if self.pclass=='warrior':
              surf.blit(self.ski,(38,504))
            
            if self.cursorpos == 0:
             surf.blit(self.cursor,(6,474))
            elif self.cursorpos == 1:
             surf.blit(self.cursor,(6,504))
            elif self.cursorpos == 2:
             surf.blit(self.cursor,(6,534))   
        if self.state == 'skill':
            self.getskills()
            surf.blit(pygame.transform.scale(self.ui2, ((300 , 300 ))),(0,430))
            surf.blit(self.skitxt,(38,464))
            surf.blit(self.cancel,(38,494))
            if self.cursorpos == 0:#burst
             surf.blit(self.cursor,(6,464))
             surf.blit(self.burstdesc,(328,577))
            elif self.cursorpos == 1:#cancel
             surf.blit(self.cursor,(6,494))
            
        if self.state == 'magic':
            self.getmagic()
            surf.blit(pygame.transform.scale(self.ui2, ((300 , 300 ))),(0,430))
            surf.blit(self.magtxt1,(38,464))
            surf.blit(self.magtxt2,(38,494))
            surf.blit(self.magtxt3,(38,524))
            surf.blit(self.magtxt4,(38,554))
            surf.blit(self.magtxt5,(38,584))
            surf.blit(self.cancel,(38,614))
            if self.cursorpos == 0:#fire
             surf.blit(self.cursor,(6,464))
             surf.blit(self.firedesc,(328,577))
             if self.plevel<5:
               surf.blit(self.notlearnedtxt,(328,547))     
            elif self.cursorpos == 1:#ice
             surf.blit(self.cursor,(6,494))
             surf.blit(self.icedesc,(328,577))
             if self.plevel<8:
               surf.blit(self.notlearnedtxt,(328,547))
            elif self.cursorpos == 2:#cure
             surf.blit(self.cursor,(6,524))
             surf.blit(self.curedesc,(328,577))
             if self.plevel<12:
               surf.blit(self.notlearnedtxt,(328,547))
            elif self.cursorpos == 3:#death
             surf.blit(self.cursor,(6,554))
             surf.blit(self.deathdesc,(328,577))
             if self.plevel<18:
               surf.blit(self.notlearnedtxt,(328,547))
            elif self.cursorpos == 4:#tsunami
             surf.blit(self.cursor,(6,584))
             surf.blit(self.tsunamidesc,(328,577))
             if self.plevel<20:
               surf.blit(self.notlearnedtxt,(328,547))
            elif self.cursorpos == 5:#cancel
             surf.blit(self.cursor,(6,614))   
        if self.state == 'item':
            self.getitems()
            surf.blit(pygame.transform.scale(self.ui2, ((300 , 300 ))),(0,430))
            surf.blit(self.itemtxtlist[0],(38,464))
            surf.blit(self.cancel,(38,494))
            if self.cursorpos == 0:
             surf.blit(self.cursor,(6,464))
             surf.blit(self.potiondesc,(328,577))
            elif self.cursorpos == 1:
             surf.blit(self.cursor,(6,494))
        
        if self.pstatus == 'burst':
            surf.blit(self.staticon1,(800,474))
        if self.bgflag:
            surf.blit(self.actionbg,(495,73))
            surf.blit(self.bgtxt,(604,83))
    def healthbar(self):#Enemy health bar
        healthpercent=(self.mhealth/self.mmaxhealth)*100
        if healthpercent<0:
            healthpercent=0.1
        surf.blit(pygame.transform.scale(self.hpbarEmpty,(260,18)),self.monpos)
        surf.blit(pygame.transform.scale(self.hpbarFull,(int(246*(healthpercent/100)),18)),(self.monpos[0]+7,self.monpos[1]+1))
        
    def skillanim(self):#Skill logic and animation queues
        if self.state == 'burst': #burst skill start
            self.specialanim.play()
            self.skillsound.play()
            self.battleflow.reset()
            self.state='burstanim'
            self.bgflag=True
            self.bgtxt=self.uitext.render('Burst',False,self.txtcolor)
        

        if self.battleflow.timing() == 3 and self.state == 'burstanim':
            self.bgflag=False
            self.pstatus='burst'
            self.players[0].stop()
            self.burstanim.play()
            self.state='enemy'
            self.curpmana-=15
            self.enemyattacking=True
            self.currentturn=self.turn
            self.battleflow.reset()
        if self.pstatus == 'burst':
            if self.turn - self.currentturn == 2:
                self.pstatus='normal'
                self.burstanim.stop()
                self.players[0].play() #burst skill end
        if self.state == 'fire': #Fire magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus='firecast'
            self.state='enemy'
            self.enemyattacking=True
        if self.state == 'ice': #Ice magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus='icecast'
            self.state='enemy'
            self.enemyattacking=True
        if self.state == 'water': #Water magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus='watercast'
            self.state='enemy'
            self.enemyattacking=True
        if self.state == 'death': #Death magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus='deathcast'
            self.state='enemy'
            self.enemyattacking=True
        if self.state == 'cure': #Cure magic start
            self.players[1].play()
            self.players[0].stop()
            self.battleflow.reset()
            self.pstatus='curecast'
            self.state='enemy'
            self.enemyattacking=True    
        
        
    def defeat(self):#raises the defeat flag,ends the match when set to true and sends player back to main menu.
        timer=Timer()
        pygame.mixer.music.pause()
        pygame.mixer.music.load('sounds&music/Gameover2.ogg')
        pygame.mixer.music.play()
        dark = pygame.Surface(surf.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark, (0, 0))
       
        deftxt=pygame.font.Font('Daisy_Roots.otf',70)
        defeat=deftxt.render('Defeat!',True,(255,0,0)).convert_alpha()
        cont=self.uitext.render('Your journey isn\'t over yet! Move onward!',True,(255,255,0)).convert_alpha()
        surf.blit(defeat,((curwidth/3)-30,curheight/5))
        cFlag=False
        while self.defeatflag:
          
          
          
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
              if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_DOWN:
                      self.defeatflag=False
                      self.battling=False
                      pygame.mixer.music.load('sounds&music/Theme2.ogg')
                      self.mhealth=self.mmaxhealth#reseting instance
                      self.state='player'
                      global scene
                      scene='menu'
                      pygame.mixer.music.play()
                      
              if event.type== pygame.MOUSEBUTTONDOWN:
                  posfinder()
          if not cFlag:
              if timer.dothing(2):
                  surf.blit(cont,(427,253))
                  
                  cFlag=True
          
          screen.blit(surf,(0,0))
          clock.tick(60)
          pygame.display.update()
          
    def victory(self):#raises the victory flag,ends the match when set to true and awards the player with the expected exp and gold(and items?)
        timer=Timer()
        pygame.mixer.music.pause()
        pygame.mixer.music.load('sounds&music/Victory1.ogg')
        pygame.mixer.music.play()
        dark = pygame.Surface(surf.get_size(), 32)
        dark.set_alpha(128, pygame.RLEACCEL)
        surf.blit(dark, (0, 0))
        surf.blit(self.vicimg,(curwidth/3,curheight/5))
        gold=self.uitext.render('Gold:+%d'%self.gold,True,(255,255,0))
        exp=self.uitext.render('Exp:+%d'%self.exp,True,(244,240,66))
        lvlup=self.uitext.render('Level Up!',True,(120,240,66))
        statup=self.uitext.render('All stats up!',True,(110,255,66))
        gFlag=False
        eFlag=False
        lFlag=False
        while self.victoryflag:
          
          
          
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
              if event.type == pygame.KEYDOWN:
                  if (event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_RCTRL) and lFlag:
                      self.victoryflag=False
                      self.battling=False
                      pygame.mixer.music.load('sounds&music/Infinite_Arena.mp3')
                      pygame.mixer.music.play()
                      self.mhealth=self.mmaxhealth#reseting instance
                      self.state='player'
                      
            
              if event.type== pygame.MOUSEBUTTONDOWN:
                  posfinder()
          if not gFlag:
              if timer.dothing(1):
                  surf.blit(gold,(427,253))
                  self.coinanim.play()
                  gFlag=True
          if not eFlag:
              if timer.dothing(2):
                  surf.blit(exp,(427,287))
                  self.xpanim.play()
                  eFlag=True
          if not lFlag:
           if timer.dothing(6):   
            if (self.exp>=self.xptolevel) and (eFlag and gFlag):
              self.levelupsound.play()
              surf.blit(lvlup,(427,321))
              surf.blit(statup,(427,354))
            lFlag=True
              
          self.coinanim.blit(surf,(397,253))
          self.xpanim.blit(surf,(397,287))
          screen.blit(surf,(0,0))
          clock.tick(60)
          pygame.display.update()
          
    def getplayerdetails(self,level,name,hp,mp,curhp,curmp,stre,defe,mag,pclass,luck): #Method to get the players current stats and other details.
        self.plevel=level 
        self.pname=name
        self.phealth=hp
        self.pmana=mp
        self.curphealth=curhp
        self.curpmana=curmp
        self.pstr=stre
        self.pdef=defe
        self.pmage=mag
        self.pclass=pclass
        self.pluck=luck

    
    def battle(self):#The main battle scene
        if self.pclass=='warrior':
            self.players[0]=pyganim.PygAnimation([('sprites/idle1.png',0.2),('sprites/idle2.png',0.2),('sprites/idle3.png',0.2)])
        elif self.pclass=='mage':
            self.players[0]=pyganim.PygAnimation([('sprites/midle1.png',0.3),('sprites/midle2.png',0.3),('sprites/midle3.png',0.3)])
        self.players[0].play()
        self.players[0].convert_alpha()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.bgm)
        self.encountersound.play()
        fadein(255)
        pygame.time.wait(300)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        self.battling=True
        win=False
        lose=False
        self.state='player'
        text=pygame.font.Font('runescape_uf.ttf',50)
        ab=text.render('Alpha Build v2.0 - Demo version',False,(255,255,0))#debug
        doneflag=False
        get=True #monsterpos flag
        attackdone=False#flag for attacking
        playedOnce=False #deathsound flag
        attacking=False
        attacked=False
        attackedp=False
        casted=False
        cure=False #For cure magic
        enemydead=False
        enemyskill=''
        critted=False #crit txt flag
        global screen
        while self.battling:
         curwidth,curheight=screen.get_size()   
         surf.blit(pygame.transform.scale(self.bg, ((curwidth , curheight ))),(0,0))
         
         if get:
             self.monpos=(curwidth-1080,200+self.extraheight)
             
             get=False
         for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
          if event.type==KEYDOWN:
            if event.key== pygame.K_ESCAPE:
             pygame.mixer.music.pause()
             bgm.play()
             battling=False
            if self.state=='player' and event.key == pygame.K_DOWN or self.state=='player' and event.key == pygame.K_UP:
             self.cursorsound.play()
            if event.key == pygame.K_DOWN:
                self.cursorpos+=1
            if event.key == pygame.K_UP:
                self.cursorpos-=1
            if self.state=='skill' and event.key == pygame.K_DOWN or self.state=='state' and event.key == pygame.K_UP:
             self.cursorsound.play()
            if event.key == pygame.K_w:
              self.victoryflag=True
              self.victory()   
              if self.state == 'player':
                  self.state = 'enemy'
                  print (self.state)
              elif self.state == 'enemy':
                 self.state = 'player'
                 print (self.state)
            if self.cursorpos == 2 and event.key == pygame.K_RETURN and self.state=='player':#items
                self.state='item'
                self.gotitems=False
                self.cursorpos=3
            if (self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state=='player') and self.pclass=='warrior':#magic/skill
                self.state='skill'
                self.cursorpos=99
            if (self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state=='player') and self.pclass=='mage':#magic/skill
                self.state='magic'
                self.cursormax=5
                self.cursorpos=99
            if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state=='player':#attack
            
                attacking=True
            if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state=='skill':#burst
                if self.curpmana>=10:
                  self.state='burst'
                else:
                    self.buzzer.play()
            if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state=='magic':#Fire
                if self.curpmana>=5 and self.plevel>=5:
                  self.state='fire'
                else:
                    self.buzzer.play()
            if self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state=='magic':#Ice
                if self.curpmana>=10 and self.plevel>=8:
                  self.state='ice'
                else:
                    self.buzzer.play()
            if self.cursorpos == 2 and event.key == pygame.K_RETURN and self.state=='magic':#Cure
                if self.curpmana>=15 and self.plevel>=12:
                    self.state='cure'
                else:
                    self.buzzer.play()
            if self.cursorpos == 3 and event.key == pygame.K_RETURN and self.state=='magic':#Death
                if self.curpmana>=30 and self.plevel>=18:
                    self.state='death'
                else:
                    self.buzzer.play()
            if self.cursorpos == 4 and event.key == pygame.K_RETURN and self.state=='magic':#Tsunami
                if self.curpmana>=50 and self.plevel>=20:
                    self.state='water'
                else:
                    self.buzzer.play()
            if self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state=='skill':#Cancel
                self.state='player'
            if self.cursorpos == 5 and event.key == pygame.K_RETURN and self.state=='magic':#Cancel
                self.state='player'     
    
            if self.cursorpos == 0 and event.key == pygame.K_RETURN and self.state=='item':#item1
                print (self.itemlist)
                self.inventory[self.itemlist[0]]+=1
                print(self.inventory[self.itemlist[0]])
            if self.cursorpos == 1 and event.key == pygame.K_RETURN and self.state=='item':#Cancel
                self.state='player'
                self.cursorpos=2
                
          if event.type==pygame.constants.USEREVENT:
              pygame.mixer.music.load(self.bgm)
              pygame.mixer.music.play()
          if event.type==VIDEORESIZE:
            screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            surf.blit(pygame.transform.scale(surf, ((curwidth , curheight ))),(0,0))
            self.monpos=(curwidth-1080,270)
            if curwidth-1080<=0:
                self.monpos=(0,270)
            pygame.display.flip()
          if event.type==pygame.MOUSEBUTTONDOWN:
              
              posfinder()
             
         if self.cursorpos<0:
             self.cursorpos=self.cursormax
         if self.cursorpos>self.cursormax:
             self.cursorpos=0
         #Battle blits below This line#
         self.skillanim()
         surf.blit(self.pshadow,[curwidth-320,305])
         self.players[0].blit(surf,[curwidth-331,280])
         self.players[1].blit(surf,[curwidth-331,280])
         self.burstanim.blit(surf,[curwidth-331,280])
         self.cureanim.blit(surf,[curwidth-391,240])
         if not enemydead:
          surf.blit(self.monsters,self.monpos)
         
         self.battleflow.timing() #battleflow timer - controls flow of battle(animations,timing,etc.)
         self.mhurt.blit(surf,[curwidth-331,280])
         self.slashanim.blit(surf,self.monpos)
         self.clawanim.blit(surf,[curwidth-381,255])
         self.specialanim.blit(surf,[curwidth-381,255])
         self.thunderanim.blit(surf,[curwidth-381,255])
         self.castanim.blit(surf,[curwidth-409,200])
         self.fireanim.blit(surf,(self.monpos[0],self.monpos[1]-self.extraheight))
         self.iceanim.blit(surf,(self.monpos[0],self.monpos[1]-self.extraheight))
         self.deathanim.blit(surf,(self.monpos[0],self.monpos[1]-self.extraheight))
         self.wateranim.blit(surf,(self.monpos[0],(self.monpos[1]+100)-self.extraheight))
         self.statuswindow()
         surf.blit(ab,(0,0))
         screen.blit(surf,[0,0])
         
         #Battle blits above this line#
         if self.pstatus=='firecast' and self.state=='firecasting':#fire
            self.bgtxt=self.uitext.render('Fire',False,self.txtcolor)
            self.bgflag=True
            self.castsound.play()
            self.castanim.play()
            self.state='fireanim'
            dmg=self.calcdamage('fire')
            dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
    
         if self.battleflow.timing() == 2 and self.state=='fireanim':
            
            self.bgflag=False
            self.pstatus='normal'
            
            self.fireanim.play()
            self.firesound.play()
            self.state='animdone'
            self.curpmana-=5
            casted=True

         if self.pstatus=='icecast' and self.state=='icecasting':#ice
            self.bgtxt=self.uitext2.render('Ice',False,self.txtcolor)
            self.bgflag=True
            self.castsound.play()
            self.castanim.play()
            self.state='iceanim'
            dmg=self.calcdamage('ice')
            dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
    
         if self.battleflow.timing() == 2 and self.state=='iceanim':
            
            self.bgflag=False
            self.pstatus='normal'
            
            self.iceanim.play()
            self.icesound.play()
            self.state='animdone'
            self.curpmana-=10
            casted=True
         if self.pstatus=='watercast' and self.state=='watercasting':#Tsunami
            self.bgtxt=self.uitext.render('Tsunami',False,self.txtcolor)
            self.bgflag=True
            self.castsound.play()
            self.castanim.play()
            self.state='wateranim'
            dmg=self.calcdamage('water')
            dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
    
         if self.battleflow.timing() == 2 and self.state=='wateranim':
            
            self.bgflag=False
            self.pstatus='normal'
            
            self.wateranim.play()
            self.watersound1.play()
            self.watersound2.play()
            self.state='animdone'
            self.curpmana-=50
            casted=True
         if self.pstatus=='deathcast' and self.state=='deathcasting':#Death(magic)
            self.bgtxt=self.uitext2.render('Death',False,self.txtcolor)
            self.bgflag=True
            self.castsound.play()
            self.castanim.play()
            self.state='deathanim'
            dmg=self.calcdamage('death')
            dmgtxt=self.uitext2.render(str(dmg),True,(119, 17, 38))
            casted=False
         if self.battleflow.timing() == 2 and self.state=='deathanim':
            
            self.bgflag=False
            self.pstatus='normal'
            
            self.deathanim.play()
            self.deathmagsound.play()
            self.state='animdone'
            self.curpmana-=30
            casted=True
            death=True
         if self.pstatus=='curecast' and self.state=='curecasting':#Cure
            self.bgtxt=self.uitext2.render('Cure',False,self.txtcolor)
            self.bgflag=True
            self.castsound.play()
            self.castanim.play()
            self.state='cureanim'
            dmg=self.calcdamage('cure')
            dmgtxt=self.uitext2.render(str(dmg),True,(55, 181, 27))
            cure=False
         if self.battleflow.timing() == 2 and self.state=='cureanim':
            
            self.bgflag=False
            self.pstatus='normal'
            
            self.cureanim.play()
            self.curesound.play()
            self.state='animdone'
            self.curpmana-=15
            cure=True  

         if casted:
             self.healthbar()
             surf.blit(dmgtxt,(self.monpos[0]+100,self.monpos[1]-35))
             
             screen.blit(surf,(0,0))
             
         if cure:
             surf.blit(dmgtxt,[curwidth-331,240])
             screen.blit(surf,(0,0))
         if self.battleflow.timing() ==5 and self.state=='animdone':
            self.players[1].stop()
            self.players[0].play()
            casted=False
            if type(dmg) == int and not cure:
               self.mhealth-=dmg
            if cure:
                self.curphealth+=dmg
                cure=False
            self.battleflow.reset()
            self.state='player'
         if attacking:#Attack state
             if self.state=='player':
                 attackedp=False
                 print(attackedp,self.crit,self.pstatus)
                 self.state='attack'
                 dmg=self.calcdamage()
                 self.battleflow.reset()
          
             if self.battleflow.timing()==1 and attackdone==False:
                 if (attackedp==False and self.crit==10) and self.pstatus!='burst':
                    self.slashanim.play()
                    self.attacksound.play()
                    dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
                    critted=True
                    screen.blit(surf,(0,0))
                    attackedp=True
                    print(critted)



                 if (attackedp==False and self.crit!=10) or (attackedp==False and self.pstatus=='burst'):

                    self.slashanim.play()
                    self.attacksound.play()
                    dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
                    attackedp=True
                 self.healthbar()
                 surf.blit(dmgtxt,(self.monpos[0]+100,self.monpos[1]-35))
                 
                 screen.blit(surf,(0,0))
                 
             if critted:
                     surf.blit(self.crittxt,(self.monpos[0]+100,self.monpos[1]-70))
                     screen.blit(surf,(0,0))
                     
                     
             if self.battleflow.timing()==2 and attackdone==False:
                     print('done:player')#debug
                     attackdone=True
                     critted=False
                     self.battleflow.reset()
             if self.battleflow.timing()==2 and attackdone==True:
                self.mhealth-=dmg
                attacking=False
                
                attackdone=False
                if self.mhealth<=0:
                    self.state='victory'
                else:    
                  self.state='enemy'
                  attackedp=False
                  self.enemyattacking=True
         if self.enemyattacking:     
          if self.state=='enemy':
             move=random.randrange(0,len(self.enemymovelist))
             if self.enemymovelist[move]=='attack':
               attacked=False
             elif self.enemymovelist[move]=='thunder':#enemy casting thunder
               attacked=True
               enemyskill='thunder'
               self.bgtxt=self.uitext.render('Thunder',False,self.txtcolor)
               self.bgflag=True

           
          self.state='enemyattack'
          if self.battleflow.timing()==2 and attackdone==False:
                 if attacked==False:
                     
                     self.clawanim.play()
                     self.attacksound2.play()
                     dmg=self.calcdamage()
                     dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
                     attacked=True
                     
                 if enemyskill=='thunder':
                     self.thunderanim.play()
                     self.thundersound.play()
                     dmg=self.calcdamage('thunder')
                     dmgtxt=self.uitext2.render(str(dmg),True,(255,255,255))
                     enemyskill=''
                 surf.blit(dmgtxt,[curwidth-331,280])
                 screen.blit(surf,(0,0))
          if self.battleflow.timing()==4 and attackdone==False:
                 print('done:enemy')#debug
                 self.bgflag=False
                 attackdone=True
                 self.battleflow.reset()
          if self.battleflow.timing()==1 and attackdone==True:
                 self.curphealth-=dmg
                 attackdone=False
                 self.enemyattacking=False
                 self.turn+=1
                 if self.pstatus=='firecast':
                   self.state='firecasting'
                   self.battleflow.reset()

                 elif self.pstatus=='icecast':
                   self.state='icecasting'
                   self.battleflow.reset()
                 elif self.pstatus=='watercast':
                   self.state='watercasting'
                   self.battleflow.reset()
                 elif self.pstatus=='deathcast':
                   self.state='deathcasting'
                   self.battleflow.reset()
                 elif self.pstatus=='curecast':
                   self.state='curecasting'
                   self.battleflow.reset()   
                 else:
                   self.state='player'
         
         if self.mhealth <=0:
             if playedOnce==False:
                self.deadsound.play()
                enemydead=True
                self.battleflow.reset
                playedOnce=True
             self.state='victory'
             win=True
         if self.battleflow.timing()==3 and win==True:
              self.victoryflag=True
              self.victory()
         if self.curphealth <=0:
             self.state='defeat'
             self.curphealth=0
             self.players[0].stop()
             self.burstanim.stop()
             self.players[1].stop()
             surf.blit(self.deathsprite,[curwidth-331,280])
             screen.blit(surf,(0,0))
             lose=True
         if self.curphealth>self.phealth:
             self.curphealth=self.phealth
         if self.battleflow.timing()==3 and lose==True:
              self.defeatflag=True
              self.defeat()
         clock.tick(60)
         fps="FPS:%d"%clock.get_fps()
         pygame.display.set_caption(fps)

         pygame.display.update()
   
         
class TextBox:
    """The textbox class, used to draw textboxes during dialogue."""
    def __init__(self,txtcolor=(21,57,114)):
        self.bg=pygame.image.load('backgrounds/rpgtxt.png').convert_alpha()
        self.txtcolor=(txtcolor)  
        self.uitext=pygame.font.Font('runescape_uf.ttf',35)
        
    def draw_textbox(self,pic=None,name='',line1='',line2='',line3='',line4='',line5='',line6=''):
     
      
      surf.blit(pygame.transform.scale(self.bg, ((curwidth , 300 ))),(0,430))
      if pic!=None:
          speaker=pygame.image.load(pic).convert_alpha()
          surf.blit(speaker,(110,490))
          nameplate=self.uitext.render(name,True,(255,21,45))
          surf.blit(nameplate,(131,655))
      row1=self.uitext.render(line1,False,self.txtcolor)
      surf.blit(row1,(270,490))
      row2=self.uitext.render(line2,False,self.txtcolor)
      surf.blit(row2,(270,520))
      row3=self.uitext.render(line3,False,self.txtcolor)
      surf.blit(row3,(270,550))
      row4=self.uitext.render(line4,False,self.txtcolor)
      surf.blit(row4,(270,580))
      row5=self.uitext.render(line5,False,self.txtcolor)
      surf.blit(row5,(270,610))
      row6=self.uitext.render(line6,False,self.txtcolor)
      surf.blit(row6,(270,640))




drawui=True#Flag to signify whether to draw the ui or not




class MainUi:
    """The Main UI of the game(outside of battle.)"""
    def __init__(self):
        self.bg=pygame.image.load('backgrounds/rpgtxt.png').convert_alpha()
        self.txtcolor=(21,57,114)
        self.txtcolor2=(117, 17, 67)
        self.txtcolor3=(23, 18, 96)
        self.uitext=pygame.font.Font('runescape_uf.ttf',35)
        self.cursor=pygame.image.load('sprites/Cursor.png').convert_alpha()
        self.cursorsound=pygame.mixer.Sound('sounds&music/Cursor1.ogg')
        self.cursorpos=0
        self.talktxt=self.uitext.render('Talk',False,self.txtcolor)
        self.talkdesc=self.uitext.render('Talk with people around the Arena.',False,self.txtcolor)
        self.talkdesc2=self.uitext.render('Talk with people around the Inn.',False,self.txtcolor)
        self.battxt=self.uitext.render('Battle',False,self.txtcolor)
        self.batdesc=self.uitext.render('Battle monsters in the Arena.',False,self.txtcolor)
        self.systxt=self.uitext.render('System',False,self.txtcolor)
        self.sysdesc=self.uitext.render('System options.',False,self.txtcolor)
        self.inntxt=self.uitext.render('Inn',False,self.txtcolor)
        self.inndesc=self.uitext.render('Go to the Inn.',False,self.txtcolor)
        self.shoptxt=self.uitext.render('Shop',False,self.txtcolor)
        self.shopdesc=self.uitext.render('Buy items/equipment to use in the Arena.',False,self.txtcolor)
        self.stattxt=self.uitext.render('Status',False,self.txtcolor)
        self.statdesc=self.uitext.render('Check player status/equipment',False,self.txtcolor)
        self.backtxt=self.uitext.render('Leave',False,self.txtcolor)
        self.backdesc=self.uitext.render('Return to the Arena',False,self.txtcolor)
        self.sleeptxt=self.uitext.render('Rest',False,self.txtcolor)
        self.sleepdesc=self.uitext.render('Spend a night at the Inn. (20 Gold)',False,self.txtcolor)
        self.txtbox=TextBox()
        self.statustxt=self.uitext.render('- STATUS -',True,self.txtcolor)
        self.face=pygame.image.load('sprites/f1.png').convert_alpha()
        self.wepicon=pygame.image.load('sprites/wepicon.png').convert_alpha()
        self.armicon=pygame.image.load('sprites/armicon.png').convert_alpha()
        self.accicon=pygame.image.load('sprites/accicon.png').convert_alpha()
        self.talked=False
        self.shopkeep=True
        self.buysound=pygame.mixer.Sound('sounds&music/Shop1.ogg')
        self.shoplist={'Potion':20,'Iron Sword':60,'Iron Armour':100}
        self.Talk=-1
        self.sysopt1=self.uitext.render('Save Game',False,self.txtcolor)
        self.sysopt2=self.uitext.render('Quit Game',False,self.txtcolor)
        self.sysopt3=self.uitext.render('Cancel',False,self.txtcolor)
        self.syscursorpos=0
        self.savesound=pygame.mixer.Sound('sounds&music/Save.ogg')
        self.batopt1=self.uitext.render('Fight a regular enemy',False,self.txtcolor)
        self.battalk=True
        self.batcursorpos=False
        self.pb_dialogue=False
        self.pbtalk=0
    def draw(self,floor=1):
       surf.blit(pygame.transform.scale(self.bg, ((int(curwidth/1.5) , 300 ))),(0,430))
       surf.blit(pygame.transform.scale(self.bg, (150 , 50 )),(10,48))
       surf.blit(pygame.transform.scale(self.bg, (300 , 300 )),(905,430))
       surf.blit(self.talktxt,(946,496))
       surf.blit(self.battxt,(946,526))
       surf.blit(self.stattxt,(946,556))
       surf.blit(self.shoptxt,(946,586))
       surf.blit(self.inntxt,(946,616))
       surf.blit(self.systxt,(946,646))
       self.cur=self.uitext.render('Floor:  %d'%floor,False,self.txtcolor)
       surf.blit(self.cur,(27,61))
       if self.cursorpos==0:
           surf.blit(self.cursor,(916,496))
           surf.blit(self.talkdesc2,(112,490))
       if self.cursorpos==1:
           surf.blit(self.cursor,(916,526))
           surf.blit(self.batdesc,(112,490))
       if self.cursorpos==2:
           surf.blit(self.cursor,(916,556))
           surf.blit(self.statdesc,(112,490))
       if self.cursorpos==3:
           surf.blit(self.cursor,(916,586))
           surf.blit(self.shopdesc,(112,490))
       if self.cursorpos==4:
           surf.blit(self.cursor,(916,616))
           surf.blit(self.inndesc,(112,490))
       if self.cursorpos==5:
           surf.blit(self.cursor,(916,646))
           surf.blit(self.sysdesc,(112,490)) 
           
    def talk(self):
        global  drawui
        drawui=False
        
        if not self.talked:
         self.Talk+=1
        if self.Talk==0 and player.progress==1:
           self.talked=True
           self.txtbox.draw_textbox('sprites/oldman.png','Old Man','I heard the monsters on the first floor are quite weak.','You mustn\'t underestimate them However!','Consider Equipping yourself with new equipment from the Shop.',line6='              Press RCTRL to continue...')
        elif self.Talk==1 and player.progress==1:
           self.talked=True
           self.txtbox.draw_textbox('sprites/boy.png','Boy','Wow mister you\'re going to fight in the Arena? So cool!',line6='              Press RCTRL to continue...')

        elif self.Talk==2 and player.progress==1:
           self.talked=True
           self.txtbox.draw_textbox('sprites/youngman.png','Young Man','In the 50 years that the Arena has been open, there has been only one winner.',' It was the legendary Hero known as Zen.','That was 2 years ago though, nobody has seen him since.',line6='              Press RCTRL to continue...')  
        elif self.Talk==3 and player.progress==1:
           self.talked=True
           self.txtbox.draw_textbox('sprites/mysteryman.png','Stranger','You...','Nevermind. Good luck in the Arena, I\'ll be keeping an eye on you.',line6='              Press RCTRL to continue...')
        if self.Talk>3:
            self.Talk=-1
            
    def status(self,name='Zen',classt='Warrior',pstr=1,pdef=1,pluck=1,pmag=1,level=1,xpleft=1,wep='Rusty Sword',arm='Dusty Cloth',acc='None',floorkills=0,totalkills=0):
        surf.blit(pygame.transform.scale(self.bg, ((int(curwidth/1.5) , curheight ))),(53,30))
        nametxt=self.uitext.render('Name: '+name,False,self.txtcolor)
        surf.blit(nametxt,(169,207))
        strtxt=self.uitext.render('STR: %d'%pstr,False,self.txtcolor)
        surf.blit(strtxt,(169,247))
        deftxt=self.uitext.render('DEF: %d'%pdef,False,self.txtcolor)
        surf.blit(deftxt,(169,287))
        lucktxt=self.uitext.render('LUCK: %d'%pluck,False,self.txtcolor)
        surf.blit(lucktxt,(169,327))
        magtxt=self.uitext.render('MAG: %d'%pmag,False,self.txtcolor)
        surf.blit(magtxt,(169,367))
        lvltxt=self.uitext.render('Level: %d'%level,False,self.txtcolor2)
        surf.blit(lvltxt,(607,396))
        xptxt=self.uitext.render('Exp till next level: %d'%xpleft,False,self.txtcolor2)
        surf.blit(xptxt,(607,426))
        surf.blit(self.face,(679,207))
        classtxt=self.uitext.render(classt.capitalize(),False,self.txtcolor)
        surf.blit(classtxt,(697,366))
        surf.blit(self.statustxt,(417,141))
        weptxt=self.uitext.render('WEAPON: '+wep,False,self.txtcolor2)
        armtxt=self.uitext.render('ARMOR: '+arm,False,self.txtcolor2)
        acctxt=self.uitext.render('ACCESORY: '+acc,False,self.txtcolor2)
        surf.blit(self.wepicon,(169,407))
        surf.blit(weptxt,(209,407))
        surf.blit(self.armicon,(169,447))
        surf.blit(armtxt,(209,447))
        surf.blit(self.accicon,(169,487))
        surf.blit(acctxt,(209,487))
        floorktxt=self.uitext.render('Enemies killed on this floor: %d'%floorkills,False,self.txtcolor3)
        totktxt=self.uitext.render('Total enemies killed: %d'%totalkills,False,self.txtcolor3)
        surf.blit(floorktxt,(169,527))
        surf.blit(totktxt,(168,567))
        
    def shop(self,gold=100):
        if self.shopkeep:
            self.txtbox.draw_textbox('sprites/shopkeep.png','Shopkeeper','Welcome to the Arena shop! How can I help you?',line6='              Press RCTRL to continue...')
        if not self.shopkeep:
            surf.blit(pygame.transform.scale(self.bg, ((int(curwidth/1.5) , curheight ))),(53,30))
            contrtxt=self.uitext.render('Under Construction! Press Enter to go back!',False,self.txtcolor3)
            surf.blit(contrtxt,(317,141))       
    def system(self):
          surf.blit(pygame.transform.scale(self.bg, ((int(curwidth/2.7) , int(curheight/3) ))),(470,200))
          surf.blit(self.sysopt1,(528,259))
          surf.blit(self.sysopt2,(528,299))
          surf.blit(self.sysopt3,(528,339))
          if self.syscursorpos==0:
              surf.blit(self.cursor,(498,259))
          if self.syscursorpos==1:
              surf.blit(self.cursor,(498,299))
          if self.syscursorpos==2:
              surf.blit(self.cursor,(498,339))
          if self.syscursorpos>2:
              self.syscursorpos=0
          if self.syscursorpos<0:
              self.syscursorpos=2
    def battle_choice(self,monkill):
          if self.battalk:
              montokill=5-monkill
              if monkill<5:
                 self.txtbox.draw_textbox('sprites/host_face.png','Chance','You have %d monter(s) left to kill. You\'re almost there!'%montokill,line6='             Press RCTRL to continue...')
              if monkill>=5:
                 self.txtbox.draw_textbox('sprites/host_face.png','Chance','You can challenge the floor boss! Are you prepared for it?',line6='             Press RCTRL to continue...')
              
          if not self.battalk:
           if monkill>=5:
             self.batopt2=self.uitext.render('Challenge the floor boss',False,self.txtcolor)
           elif monkill<5:
             self.batopt2=self.uitext.render('Challenge the floor boss',False,(105,109,114))  
           surf.blit(pygame.transform.scale(self.bg, ((int(curwidth/2.7) , int(curheight/3) ))),(470,200))
           surf.blit(self.batopt1,(528,259))
           surf.blit(self.batopt2,(528,299))
           surf.blit(self.sysopt3,(528,339))
           if self.batcursorpos==0:
               surf.blit(self.cursor,(498,259))
           if self.batcursorpos==1:
               surf.blit(self.cursor,(498,299))
           if self.batcursorpos==2:
               surf.blit(self.cursor,(498,339))
           if self.batcursorpos>2:
               self.batcursorpos=0
           if self.batcursorpos<0:
               self.batcursorpos=2
    def post_battle(self,progress=1): #where progress is what point in the story the player is on
      if not self.pb_dialogue:
          self.pbtalk=random.randrange(0,4)
      if self.pbtalk==0 and progress==1:
          self.pb_dialogue=True
          ui.txtbox.draw_textbox('sprites/host_face.png','Chance','That was a good battle! If you\'re injured make sure to rest up at the inn.',line6='             Press RCTRL to continue...')
      elif self.pbtalk==1 and progress==1:
          self.pb_dialogue=True 
          ui.txtbox.draw_textbox('sprites/host_face.png','Chance','Good job! Make sure to use the gold from your battle to buy equipment from','our Shop.',line6='             Press RCTRL to continue...')
      elif self.pbtalk==2 and progress==1:
          self.pb_dialogue=True  
          ui.txtbox.draw_textbox('sprites/host_face.png','Chance','Nice work! You\'re pretty skilled, are you sure you haven\'t done this before?',line6='             Press RCTRL to continue...')
      elif self.pbtalk==3 and progress==1:
          self.pb_dialogue=True
          ui.txtbox.draw_textbox('sprites/host_face.png','Chance','Good work out there! I overheard some strange people talking about you.','Something about.. A debt?',line6='             Press RCTRL to continue...')
    def draw_inn(self,gold):
       surf.blit(pygame.transform.scale(self.bg, ((int(curwidth/1.5) , 300 ))),(0,430))
       surf.blit(pygame.transform.scale(self.bg, (150 , 50 )),(10,48))
       surf.blit(pygame.transform.scale(self.bg, (300 , 300 )),(905,430))
       surf.blit(self.talktxt,(946,496))
       surf.blit(self.sleeptxt,(946,526))
       surf.blit(self.backtxt,(946,556))
       self.cur=self.uitext.render('Gold:  %d'%gold,False,self.txtcolor)
       surf.blit(self.cur,(27,61))
       if self.cursorpos==0:
           surf.blit(self.cursor,(916,496))
           surf.blit(self.talkdesc2,(112,490))
       if self.cursorpos==1:
           surf.blit(self.cursor,(916,526))
           surf.blit(self.sleepdesc,(112,490))
       if self.cursorpos==2:
           surf.blit(self.cursor,(916,556))
           surf.blit(self.backdesc,(112,490))
       
player=Player()

warrior=pyganim.PygAnimation([('sprites/idle1.png',0.2),('sprites/idle2.png',0.2),('sprites/idle3.png',0.2)])
        
mage=pyganim.PygAnimation([('sprites/midle1.png',0.3),('sprites/midle2.png',0.3),('sprites/midle3.png',0.3)])

castanim=[('sprites/b1.png',0.3),('sprites/b2.png',0.3),('sprites/b3.png',0.3)]
#Initialize Mob monsters below this line
rat=sidebattle('warrior',castanim,'enemies/Rat.png','backgrounds/Ruins2.png','sounds&music/2000_Thief.ogg',exp=5000)
snake=sidebattle('warrior',castanim,'sv_enemies/Snake.png','backgrounds/Ruins2.png','sounds&music/2000_Thief.ogg',mhealth=175,mstr=20,mdef=15,mmag=5,gold=75,exp=6000)
imp=sidebattle('warrior',castanim,'sv_enemies/Imp.png','backgrounds/Ruins2.png','sounds&music/2000_Thief.ogg',mhealth=150,mstr=7,mdef=14,mmag=450,gold=120,exp=7500)
imp.enemymovelist=['attack','thunder']
hornet=sidebattle('warrior',castanim,'sv_enemies/Hornet.png','backgrounds/Ruins2.png','sounds&music/2000_Thief.ogg',mhealth=100,mstr=23,mdef=13,mmag=1,gold=100,exp=7000)
slime=sidebattle('warrior',castanim,'sv_enemies/Slime.png','backgrounds/Ruins2.png','sounds&music/2000_Thief.ogg')
skeleton=sidebattle('warrior',castanim,'sv_enemies/Skeleton.png','backgrounds/Ruins2.png','sounds&music/2000_Thief.ogg')
#Mob monsters above this line

#####

#Initialize boss monsters below this line
floorboss1=sidebattle('warrior',castanim,'sv_enemies/Orc.png','backgrounds/Ruins2.png','sounds&music/floorboss.ogg',mhealth=750,mstr=30,mdef=15,mmag=14,gold=500,exp=25000)
floorboss1.extraheight=-50
floorboss1.mdeathresist=True
#Boss monters above this line
randbattle=0
timepassed=False #Flag to check if the time passed or not
newgtxtbox=0
pygame.mixer.music.load('sounds&music/Theme2.ogg')
pygame.mixer.music.play()
vol=0.5
surf=pygame.Surface((1366,768))
pygame.mixer.music.set_volume(vol)
innsong=pygame.mixer.Sound('sounds&music/Town2.ogg')
talked=False# Ui flags
status=False
shop=False
system=False
talking=False
battle_choice=False
post_battle=False #After battle shenanigans
controlui=True# Flag to check if player can control ui
text=pygame.font.Font('runescape_uf.ttf',50)
seltext=pygame.font.Font('runescape_uf.ttf',50)
secretbattle=sidebattle('mage',castanim,'enemies/Cerberus.png','backgrounds/LavaCave.png','sounds&music/Battle3.ogg',phealth=1000,pmana=100, pstr=1000, pstrmod=14, pdef=100,pmag=2000,pluck=9, mhealth=2000,mstr=1000,mdef=200,mmag=900,gold=1000,exp=10000)
secretbattle.plevel=50
secretbattle.enemymovelist=['attack','thunder']
healsound=pygame.mixer.Sound('sounds&music/Recovery.ogg')
mage.play()
warrior.play()
menutext=pygame.font.Font('Daisy_Roots.otf',40)
ab=text.render('Alpha Build v2.0 - Demo version',False,(255,255,0))#debug
sel1=seltext.render('Enter your name:',False,(255,255,0))
sel2=seltext.render('Press RCTRL to continue..',False,(255,255,0))
MageDesc=seltext.render('Mages are proficient at magic but weak physically.',False,(178,57,63))
WarDesc=seltext.render('Warriors specialize in physical attacks and buffs.',False,(178,57,63))

sel3=seltext.render('Select your class:',False,(rat.txtcolor))
sel4=text.render('Mage',False,(rat.txtcolor))
sel5=text.render('Warrior',False,(rat.txtcolor))
door=pygame.mixer.Sound('sounds&music/Door1.ogg')
gate=pygame.mixer.Sound('sounds&music/Door4.ogg')
loadgamecolor=(255,255,0)
nosavefile=True # Check if a savefile is already present or not
try:
    rfile=open('savegame.dat','rb')
    rfile.close()
    loadgamecolor=(255,255,0)
    nosavefile=False
except:
    loadgamecolor=(105,109,114)
    nosavefile=True
newgame=menutext.render('New Game',True,(255,255,0))#Things for main menu
loadgame=menutext.render('Load Game',True,loadgamecolor)
quitgame=menutext.render('Quit Game',True,(255,255,0))
namelist=['']
menubg1=pygame.image.load('backgrounds/bg2.jpg').convert_alpha()
arena_bg=pygame.image.load('backgrounds/arenabg.png').convert_alpha()
inn_bg=pygame.image.load('backgrounds/inn.png').convert_alpha()
logo=pygame.image.load('backgrounds/logo3.png').convert_alpha()
cursor=pygame.image.load('sprites/Cursor.png').convert_alpha()
newgbg=pygame.image.load('backgrounds/Meadow.png').convert_alpha()
loadsound=pygame.mixer.Sound('sounds&music/Load.ogg')
cursorpos=0
Textbox=pygame.image.load('backgrounds/rpgtxt.png').convert_alpha()
scene='menu'
ui=MainUi()
shh=[]
txtbox=TextBox()
timer=Timer()



if __name__== "__main__":
 while not done:
    #main
    
    curwidth,curheight=screen.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.MOUSEBUTTONDOWN: #All the required controls
            posfinder()
        elif event.type== pygame.KEYDOWN:
            if event.key == pygame.K_b and scene=='menu':
                shh.append('b')
                
                print(shh)
            if event.key == pygame.K_o and scene=='menu':
                shh.append('o')
                print(shh)
            if event.key == pygame.K_s and scene=='menu':
                shh.append('s')
                print(shh)
            if event.key == pygame.K_RETURN and cursorpos==0 and scene=='menu':
                pygame.mixer.music.stop()
                fadein(255)
                pygame.time.wait(1000)
                pygame.mixer.music.load('bgm/Castle1.ogg')
                pygame.mixer.music.play()
                
                scene='new_game'
                
            if (event.key == pygame.K_RETURN and cursorpos==1 and scene=='menu') and not nosavefile:
                try:
                    rfile=open('savegame.dat','rb+')
                    pygame.mixer.music.stop()
                    loadsound.play()
                    player=pickle.load(rfile)
                    rfile.close()
                    fadein(255)
                    scene='arena'
                    ui.cursorpos=9
                    pygame.mixer.music.load('sounds&music/Infinite_Arena.mp3')
                    pygame.mixer.music.play()
                except:
                    print("Could not open")
                    
            if event.key == pygame.K_RETURN and cursorpos==2 and scene=='menu':
                done=True
            if event.key == pygame.K_UP and scene=='menu':
                rat.cursorsound.play()
                cursorpos-=1
            if event.key == pygame.K_DOWN and scene=='menu':
                cursorpos+=1
                rat.cursorsound.play()
            if shh==['b','o','s','s'] and scene=='menu':
                del shh[0]
                secretbattle.battle()
            if event.key== pygame.K_q and scene=='new_game':
                namelist.append('q')
            if event.key== pygame.K_w and scene=='new_game':
                namelist.append('w')
            if event.key== pygame.K_e and scene=='new_game':
                namelist.append('e')
            if event.key== pygame.K_r and scene=='new_game':
                namelist.append('r')
            if event.key== pygame.K_t and scene=='new_game':
                namelist.append('t')
            if event.key== pygame.K_y and scene=='new_game':
                namelist.append('y')
            if event.key== pygame.K_u and scene=='new_game':
                namelist.append('u')
            if event.key== pygame.K_i and scene=='new_game':
                namelist.append('i')
            if event.key== pygame.K_o and scene=='new_game':
                namelist.append('o')
            if event.key== pygame.K_p and scene=='new_game':
                namelist.append('p')
            if event.key== pygame.K_a and scene=='new_game':
                namelist.append('a')
            if event.key== pygame.K_s and scene=='new_game':
                namelist.append('s')
            if event.key== pygame.K_d and scene=='new_game':
                namelist.append('d')
            if event.key== pygame.K_f and scene=='new_game':
                namelist.append('f')
            if event.key== pygame.K_g and scene=='new_game':
                namelist.append('g')
            if event.key== pygame.K_h and scene=='new_game':
                namelist.append('h')
            if event.key== pygame.K_j and scene=='new_game':
                namelist.append('j')
            if event.key== pygame.K_k and scene=='new_game':
                namelist.append('k')
            if event.key== pygame.K_l and scene=='new_game':
                namelist.append('l')
            if event.key== pygame.K_z and scene=='new_game':
                namelist.append('z')
            if event.key== pygame.K_x and scene=='new_game':
                namelist.append('x')
            if event.key== pygame.K_c and scene=='new_game':
                namelist.append('c')
            if event.key== pygame.K_v and scene=='new_game':
                namelist.append('v')
            if event.key== pygame.K_b and scene=='new_game':
                namelist.append('b')
            if event.key== pygame.K_n and scene=='new_game':
                namelist.append('n')
            if event.key== pygame.K_m and scene=='new_game':
                namelist.append('m')
            if event.key==pygame.K_BACKSPACE and scene=='new_game':
                if len(namelist)>0:
                    namelist.pop()
                else:
                    pass
            if (event.key==pygame.K_RCTRL and scene=='new_game') and len(namelist)>1:
                scene="new_game2"
                name="".join(namelist).capitalize()
                player.name=name
            if event.key==pygame.K_LEFT and scene=='new_game2':
                cursorpos-=1
            if event.key==pygame.K_RIGHT and scene=='new_game2':
                cursorpos+=1
            if event.key==pygame.K_RETURN and scene=='new_game2' and cursorpos==0:
                player.pclass='mage'
                rfile=open('savegame.dat','wb+')
                scene='new_game3'
                pygame.mixer.music.stop()
                try:
                    pickle.dump(player,rfile)
                    rfile.close()
                except:
                    print("Could not create save file.")
                    pass
                timer.reset()
                fadein(255,10)
                door.play()
            if event.key==pygame.K_RETURN and scene=='new_game2' and cursorpos==1:
                player.pclass='warrior'
                rfile=open('savegame.dat','wb+')   
                scene='new_game3'
                pygame.mixer.music.stop()
                try:
                    pickle.dump(player,rfile)
                    rfile.close()
                except:
                    print("Could not create save file.")
                    pass
                timer.reset()
                fadein(255,10)
                door.play()
            if event.key==pygame.K_RETURN and (scene=='new_game3' or scene=='new_game4') or scene=='credits':
                newgtxtbox+=1
            if (event.key==pygame.K_DOWN and (scene=='arena' or scene=='inn')) and controlui:
                ui.cursorsound.play()
                ui.cursorpos+=1
                
            if (event.key==pygame.K_UP and (scene=='arena' or scene=='inn')) and controlui:
                ui.cursorsound.play()
                ui.cursorpos-=1
            if (event.key==pygame.K_DOWN and scene=='arena') and system:
                ui.cursorsound.play()
                ui.syscursorpos+=1
            if (event.key==pygame.K_UP and scene=='arena') and system:
                ui.cursorsound.play()
                ui.syscursorpos-=1
            if (event.key==pygame.K_DOWN and scene=='arena') and battle_choice:
                ui.cursorsound.play()
                ui.batcursorpos+=1
            if (event.key==pygame.K_UP and scene=='arena') and battle_choice:
                ui.cursorsound.play()
                ui.batcursorpos-=1
            if (event.key==pygame.K_RETURN and ui.cursorpos==0) and scene=='arena' and controlui:
                talking=True
                controlui=False
                
                
            if event.key==pygame.K_RCTRL and ui.talked:
                
                drawui=True
                controlui=True
                ui.talked=False
                talking=False
            if (event.key==pygame.K_RETURN and ui.cursorpos==1) and scene=='arena' and controlui:
                drawui=False
                controlui=False
                battle_choice=True
                ui.battalk=True
                ui.batcursorpos=4
                
            if (event.key==pygame.K_RETURN and ui.cursorpos==2) and scene=='arena' and controlui:
                drawui=False
                controlui=False
                status=True
            if event.key==pygame.K_RCTRL and status:
                drawui=True
                controlui=True
                status=False
            if (event.key==pygame.K_RETURN and ui.cursorpos==3) and scene=='arena' and controlui:
                drawui=False
                controlui=False
                shop=True
            if (event.key==pygame.K_RCTRL and shop) and ui.shopkeep:
                ui.shopkeep=False
            if (event.key==pygame.K_RETURN and shop) and not ui.shopkeep:
                drawui=True
                controlui=True
                shop=False
                ui.shopkeep=True
            if (event.key==pygame.K_RETURN and ui.cursorpos==4) and scene=='arena' and controlui:
                pygame.mixer.music.pause()
                fadein(255)
                innsong.play()
                scene='inn'
            if (event.key==pygame.K_RETURN and ui.cursorpos==5) and scene=='arena' and controlui:
                drawui=False
                controlui=False
                system=True
                ui.syscursorpos=4
            if (event.key==pygame.K_RETURN and ui.cursorpos==1) and scene=='inn' and controlui:
                if player.gold>=20:#rest
                  player.curhp=player.hp
                  player.curmp=player.mp
                  healsound.play()
                  fadein(255)
                  player.gold-=20
            if (event.key==pygame.K_RETURN and ui.cursorpos==2) and scene=='inn' and controlui:
                innsong.stop()
                fadein(255)
                pygame.mixer.music.play()
                scene='arena'
            if (event.key==pygame.K_RETURN and ui.syscursorpos==0) and system:
                try:
                    rfile=open('savegame.dat','wb+')
                    pickle.dump(player,rfile)
                    ui.savesound.play()
                    drawui=True
                    controlui=True
                    system=False
                    rfile.close()
                except:
                    print ("Could not create save file")
            if (event.key==pygame.K_RETURN and ui.syscursorpos==1) and system:
                done=True
            if (event.key==pygame.K_RETURN and ui.syscursorpos==2) and system:
                drawui=True
                controlui=True
                system=False
        
            if event.key==pygame.K_RCTRL and system:
                drawui=True
                controlui=True
                system=False
            if (event.key==pygame.K_RETURN and ui.batcursorpos==0) and battle_choice:
                randbattle=random.randrange(0,4)
                if randbattle==0:
                   rat.getplayerdetails(player.level,player.name,player.hp,player.mp,player.curhp,player.curmp,player.str,player.defe,player.mag,player.pclass,player.luck)
    
                   rat.xptolevel=player.xp_till_levelup(player.level)-player.exp
                   rat.battle()
                   player.curhp=rat.curphealth
                   player.curmp=rat.curpmana
                   player.exp+=rat.exp
                   player.gold+=rat.gold
                if randbattle==1:
                   snake.getplayerdetails(player.level,player.name,player.hp,player.mp,player.curhp,player.curmp,player.str,player.defe,player.mag,player.pclass,player.luck)
                
                   snake.xptolevel=player.xp_till_levelup(player.level)-player.exp
                   snake.battle()
                   snake.curhp=snake.curphealth
                   snake.curmp=snake.curpmana
                   player.exp+=snake.exp
                   player.gold+=snake.gold
                if randbattle==2:
                   hornet.getplayerdetails(player.level,player.name,player.hp,player.mp,player.curhp,player.curmp,player.str,player.defe,player.mag,player.pclass,player.luck)
                   
                   hornet.xptolevel=player.xp_till_levelup(player.level)-player.exp
                   hornet.battle()
                   player.curhp=hornet.curphealth
                   player.curmp=hornet.curpmana
                   player.exp+=hornet.exp
                   player.gold+=hornet.gold
                if randbattle==3:
                   imp.getplayerdetails(player.level,player.name,player.hp,player.mp,player.curhp,player.curmp,player.str,player.defe,player.mag,player.pclass,player.luck)
                   
                   imp.xptolevel=player.xp_till_levelup(player.level)-player.exp
                   imp.battle()
                   player.curhp=imp.curphealth
                   player.curmp=imp.curpmana
                   player.exp+=imp.exp
                   player.gold+=imp.gold
                while player.check_levelup():
                    player.level+=1
                    player.hp+=25
                    player.mp+=10
                    player.str+=2
                    player.mag+=2
                    player.defe+=2
                    
                player.fkills+=1
                player.tkills+=1
                battle_choice=False
                post_battle=True
            if (event.key==pygame.K_RETURN and ui.batcursorpos==1) and battle_choice:
                if player.fkills>=5 and player.progress==1:
                    floorboss1.getplayerdetails(player.level,player.name,player.hp,player.mp,player.curhp,player.curmp,player.str,player.defe,player.mag,player.pclass,player.luck)

                    floorboss1.battle()
                    player.curhp=floorboss1.curphealth
                    player.curmp=floorboss1.curpmana
                    player.exp+=floorboss1.exp
                    player.fkills=0
                    player.tkills+=1
                    player.progress+=1
                    scene='credits'
                    newgtxtbox=1
                    if player.check_levelup():
                     player.level+=1
                     player.hp+=25
                     player.mp+=10
                     player.str+=2
                     player.mag+=2
                     player.defe+=2
                else:
                    rat.buzzer.play()
            if (event.key==pygame.K_RETURN and ui.batcursorpos==2) and battle_choice:
                drawui=True
                controlui=True
                battle_choice=False
            if (event.key==pygame.K_RCTRL and battle_choice) and ui.battalk:
                ui.battalk=False
            if (event.key==pygame.K_RCTRL and post_battle):
                ui.pb_dialogue=False
                post_battle=False
                drawui=True
                controlui=True
            
        elif event.type==pygame.constants.USEREVENT:
            pygame.mixer.music.load('sounds&music/Infinite_Arena.mp3')
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        elif event.type==VIDEORESIZE:
            curwidth,curheight=screen.get_size()
            screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            surf.blit(pygame.transform.scale(menubg1,(curwidth,curheight)),(0,0))
            surf.blit(pygame.transform.scale(surf, ((curwidth , curheight ))),(0,0))
            pygame.display.flip()
    name="".join(namelist)
    if scene=='menu':
      surf.blit(pygame.transform.scale(menubg1,(curwidth,curheight)),(0,0))
      surf.blit(logo,(curwidth-1100,curheight-600))
      surf.blit(pygame.transform.scale(Textbox,(250,180)),(450,368))
      surf.blit(newgame,(474,391))
      surf.blit(loadgame,(474,431))
         
      surf.blit(quitgame,(474,471))
      if cursorpos==0:
          surf.blit(cursor,(434,400))
      elif cursorpos==1:
          surf.blit(cursor,(434,443))
      elif cursorpos==2:
          surf.blit(cursor,(434,483))
      if cursorpos<0:
             cursorpos=2
      if cursorpos>2:
             cursorpos=0
    if scene=='new_game' or scene=='new_game2':
        surf.blit(pygame.transform.scale(newgbg,(curwidth,curheight)),(0,0))
    if scene=='new_game':
        sel1=seltext.render('Enter your name:'+name.capitalize(),False,(rat.txtcolor))
        if len(namelist)>11:
            del namelist[len(namelist)-1]
            rat.buzzer.play()
        surf.blit(sel2,(500,500))
        surf.blit(sel1,(300,300))
        cursorpos=0
    if scene=='new_game2':
       
    
        surf.blit(sel3,(300,300))
        surf.blit(sel4,(300,375))
        surf.blit(sel5,(778,375))
        warrior.blit(surf,(778,429))
        mage.blit(surf,(300,435))
        if cursorpos==0:
          statstxt=seltext.render('STR:%d MAG:%d DEF:%d LUCK:%d'%(player.str,player.mag,player.defe,player.luck),False,(10,33,147))  
          surf.blit(cursor,(260,375))
          surf.blit(MageDesc,(260,45))
          surf.blit(statstxt,(260,95))
          player.str=10
          player.mag=25
          player.defe=15
          
        elif cursorpos==1:
          statstxt=seltext.render('STR:%d MAG:%d DEF:%d LUCK:%d'%(player.str,player.mag,player.defe,player.luck),False,(10,33,147))  
          surf.blit(cursor,(738,375))
          surf.blit(WarDesc,(260,45))
          surf.blit(statstxt,(260,95))
          player.str=20
          player.mag=10
          player.defe=20
        if cursorpos<0:
             cursorpos=1
        if cursorpos>1:
             cursorpos=0
    if scene=='new_game3':
        
        if timer.timing() == 2:
            timepassed=True
            
        if timepassed:
          surf.fill((0,0,0))
          if newgtxtbox==1:
           txtbox.draw_textbox('sprites/host_face.png','???','Oh? who do we have here?')
          if newgtxtbox==2:
           txtbox.draw_textbox('sprites/host_face.png','???','A new challenger? You seem quite young!')
          if newgtxtbox==3:
            txtbox.draw_textbox('sprites/host_face.png','???','Me? I\'m the one they call the host of the arena.')
          if newgtxtbox==4:
            txtbox.draw_textbox('sprites/host_face.png','Chance','But you can call me Chance!')
          if newgtxtbox==5:
              txtbox.draw_textbox('sprites/host_face.png','Chance','Well, if you want to register I\'m not stopping you.')
          if newgtxtbox==6:
              txtbox.draw_textbox('sprites/host_face.png','Chance','So far only one warrior has emerged victorius from the arena, 2 years ago.')
          if newgtxtbox==7:
              txtbox.draw_textbox('sprites/host_face.png','Chance','Countless others have tried and failed.','Many have lost their lives beyond these gates.')
          if newgtxtbox==8:
              txtbox.draw_textbox('sprites/host_face.png','Chance','This is your last chance, there is no shame in turning back.')
          if newgtxtbox==9:
              txtbox.draw_textbox('sprites/host_face.png','Chance','...')
          if newgtxtbox==10:
              txtbox.draw_textbox('sprites/host_face.png','Chance','You are an interesting fellow.')
          if newgtxtbox==11:
              txtbox.draw_textbox('sprites/host_face.png','Chance','Very well, you may step forward..')
          if newgtxtbox==12:
              txtbox.draw_textbox('sprites/host_face.png','Chance','..And enter the Arena!')
          if newgtxtbox>12:
              gate.play()
              fadein(255,5)
              timepassed=False
              timer.reset()
              scene='new_game4'
              newgtxtbox=1
    if scene=='new_game4':
        if timer.timing()==1 and (not timepassed):
            pygame.mixer.music.load('sounds&music/Infinite_Arena.mp3')
            pygame.mixer.music.play()
            timepassed=True
        surf.blit(pygame.transform.scale(arena_bg,(curwidth,curheight)),(0,0))    
        if timepassed:
          if newgtxtbox==1:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Welcome to the Arena my friend!')
          if newgtxtbox==2:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Let me explain to you how this works.')
          if newgtxtbox==3:
           txtbox.draw_textbox('sprites/host_face.png','Chance','The Arena has 3 floors. Each floor has 5 regular enemies and 1 \'Floor Boss\'.')
          if newgtxtbox==4:
           txtbox.draw_textbox('sprites/host_face.png','Chance','After your preparations, you can come to me if you are ready to fight.')
          if newgtxtbox==5:
           txtbox.draw_textbox('sprites/host_face.png','Chance','I will let you fight a regular enemy in the floor you are on.')
          if newgtxtbox==6:
           txtbox.draw_textbox('sprites/host_face.png','Chance','After you defeat 5 regular enemies you can challenge the Floor boss.')
          if newgtxtbox==7:
           txtbox.draw_textbox('sprites/host_face.png','Chance','If you don\'t feel like you\'re ready you can fight more regular enemies before', 'challenging the boss.')
          if newgtxtbox==8:
           txtbox.draw_textbox('sprites/host_face.png','Chance','After you defeat the floor boss, you can proceed to the next floor.')
          if newgtxtbox==9:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Also, Enemies drop gold when they\'re defeated.','You can use the gold to buy items and equipment from','our shop after every battle!')
          if newgtxtbox==10:
           txtbox.draw_textbox('sprites/host_face.png','Chance','If you\'re able to defeat the final Floor boss you will be crowned','the \'Arena Champion!\'')
          if newgtxtbox==11:
           txtbox.draw_textbox('sprites/host_face.png','Chance','One more thing..')
          if newgtxtbox==12:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Before a battle you may talk with people around the Arena.')
          if newgtxtbox==13:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Who knows, maybe you may learn a useful tip or two from them!')
          if newgtxtbox==14:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Well, I\'m sure you\'re raring to go.','Let me know when you\'re ready for your first battle!')
          if newgtxtbox==15:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Good luck friend, lord knows you need it!')
          if newgtxtbox>15:
            scene='arena'
    if scene=='arena':
       surf.blit(pygame.transform.scale(arena_bg,(curwidth,curheight)),(0,0))  
       if drawui: 
        
        ui.draw(player.progress)
        if ui.cursorpos>5:
            ui.cursorpos=0
        if ui.cursorpos<0:
            ui.cursorpos=4
       if talking:
           ui.talk()
       if status:
           ui.status(player.name,player.pclass,player.str,player.defe,player.luck,player.mag,player.level,player.xp_till_levelup(player.level)-player.exp,floorkills=player.fkills,totalkills=player.tkills)
       if shop:
           ui.shop()
       if system:
           ui.system()
       if battle_choice:
           ui.battle_choice(player.fkills)
       if post_battle:
           ui.post_battle(player.progress)
    if scene=='inn':
        surf.blit(pygame.transform.scale(inn_bg,(curwidth,curheight)),(0,0))  
        if drawui:
            ui.draw_inn(player.gold)
        if ui.cursorpos>2:
            ui.cursorpos=0
        if ui.cursorpos<0:
            ui.cursorpos=2    
    if scene=='credits':
          surf.fill((0,0,0))
          if newgtxtbox==1:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Hey congrats you beat the demo!')
          if newgtxtbox==2:
           txtbox.draw_textbox('sprites/host_face.png','Chance','There is more to come but ill save that for another time.')
          if newgtxtbox==3:
           txtbox.draw_textbox('sprites/host_face.png','Chance','This was a project made by Hameel and Nihal!')
          if newgtxtbox==4:
           txtbox.draw_textbox('sprites/host_face.png','Chance','Stay tuned for the final project!')
    
          if newgtxtbox>4:
              scene='menu'
    timer.timing()
    surf.blit(ab,(0,0))
    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)
    fps="FPS:%d"%clock.get_fps()
    pygame.display.set_caption(fps)
 pygame.quit()

    
