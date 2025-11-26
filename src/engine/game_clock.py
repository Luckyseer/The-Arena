import pygame
from src.utils.timer import Timer

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
        
        # Load backgrounds
        self.arena_bg1 = pygame.image.load(
            "data/backgrounds/arenaDay.png").convert_alpha()  # day time arena
        self.arena_bg2 = pygame.image.load(
            "data/backgrounds/arenaEvening.png").convert_alpha()
        self.arena_bg3 = pygame.image.load(
            "data/backgrounds/arenaNight.png").convert_alpha()

    def toggle_clock(self):     # Pauses/Unpauses the flow of ingame time
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def reset(self):
        self.clockTime.reset()

    def pass_time(self, surface, player_details, area_music='data/sounds&music/Infinite_Arena.mp3'):
        player = player_details
        self.area_music = area_music
        self.curTime = self.clockTime.timing()  # Current time
        curwidth, curheight = surface.get_size()
        
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
            surface.blit(pygame.transform.scale(
                self.arena_bg1, (curwidth, curheight)), (0, 0))

        if player.hours >= 14 and player.hours < 20:  # Afternoon
            self.time_state = "Noon"
            surface.blit(pygame.transform.scale(
                self.arena_bg2, (curwidth, curheight)), (0, 0))

        if player.hours >= 20 or player.hours < 6:  # Night
            self.time_state = "Night"
            surface.blit(pygame.transform.scale(
                self.arena_bg3, (curwidth, curheight)), (0, 0))

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
