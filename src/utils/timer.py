import pygame

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
            # print("Doing thing")  # debug
            return True

def posfinder():  # Used to find position of cursor
    posx, posy = pygame.mouse.get_pos()
    print(posx, posy)

def fadein(screen, rgb=None, time=0.0001, fadetimer=None):  # fadein effect
    if fadetimer is None:
        fadetimer = Timer()
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
                col += 3 # Speed up slightly
                fadetimer.reset()
        fade_done = True
        if fade_done:
            break
    return fade_done


def fadeout(screen, time=0.000001, fadetimer=None, fade_in=False, optional_bg=None):  # fadeout effect
    if fadetimer is None:
        fadetimer = Timer()
    
    # Capture the current screen content
    current_surface = screen.copy()
    
    fade_done = False
    alpha = 255
    while True:
        while alpha >= 0 and not fade_done:
            if fadetimer.timing(1) >= time:
                current_surface.set_alpha(alpha)
                screen.fill([0, 0, 0])
                screen.blit(current_surface, (0, 0))
                pygame.display.flip()
                alpha -= 3
                fadetimer.reset()
        fade_done = True
        if fade_done:
            if fade_in:
                # This part of original code seemed to fade back in? 
                # For now let's just break as we usually want to switch scenes after fadeout
                break
            else:
                break
    return fade_done
