import pygame

screen = None


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
    local_screen = screen or pygame.display.get_surface()
    fade_done = False
    col = 0
    while True:
        while col < 256:
            if fadetimer.timing(1) >= time:
                r = col
                g = col
                b = col
                local_screen.fill([r, g, b])
                pygame.display.flip()
                col += 1
                fadetimer.reset()
        fade_done = True
        if fade_done:
            break
    return fade_done


def fadeout(
    surface,
    time=0.000001,
    fadetimer=Timer(),
    fade_in=False,
    optional_bg=pygame.image.load("data/backgrounds/Meadow.png"),
):  # fadeout effect
    global screen
    local_screen = screen or pygame.display.get_surface()
    if optional_bg != "":
        post_fade_bg = optional_bg  # Image to show on screen when it fades back in
    fade_done = False
    alpha = 255
    while True:
        while alpha >= 0 and not fade_done:
            if fadetimer.timing(1) >= time:
                surface.set_alpha(alpha)
                local_screen.fill([0, 0, 0])
                local_screen.blit(surface, (0, 0))
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
                        local_screen.blit(surface, (0, 0))
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


def posfinder():  # Used to find position of cursor
    posx, posy = pygame.mouse.get_pos()
    print(posx, posy)
