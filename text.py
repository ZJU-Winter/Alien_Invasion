import pygame.font


class Text:
    """A class to show text information."""

    def __init__(self, ai_game):
        """Initialize text attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.width, self.height = 200, 50

    def diaplay(self, text, shift=-1, size=100, style=None):
        font = pygame.font.SysFont(style, size)
        Surface = font.render(text, True, (30, 30, 30))
        TextRect = Surface.get_rect()
        TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + shift * self.height)
        self.screen.blit(Surface, TextRect)

    def title(self):
        font = pygame.font.SysFont("Consolas", 115)
        Surface = font.render('Alien Invasion', True, (30, 30, 30))
        TextRect = Surface.get_rect()
        TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 2 * -2 * self.height)
        self.screen.blit(Surface, TextRect)

    def help(self):
        font = pygame.font.SysFont("Consolas", 30)
        segment = ["In Alien Invasion, the player controls a rocket ship that appears",
                   "at the bottom center of the screen. The player can move the ship",
                   "right and left using the arrow keys and shoot bullets using the",
                   "spacebar. When the game begins, a fleet of aliens fills the sky",
                   "and moves across and down the screen. The player shoots and",
                   "destroys the aliens. If the player shoots all the aliens, a new fleet",
                   "appears that moves faster than the previous fleet. If any alien hits",
                   "the player’s ship or reaches the bottom of the screen, the player",
                   "loses a ship. If the player loses three ships, the game ends.",
                   "",
                   "spacebar — fire       z/c — fire anterolaterally (level>3)",
                   "arrow — move       q/esc — quit       p — pause"]
        shift = 1
        for sen in segment:
            Surface = font.render(sen, True, (30, 30, 30))
            TextRect = Surface.get_rect()
            TextRect.center = (self.screen.get_rect().centerx, shift * self.height)
            shift += 1
            self.screen.blit(Surface, TextRect)

    def record(self, st, nd, rd):
        font = pygame.font.SysFont("Consolas", 70)
        st = "{:,}".format(int(st))
        nd = "{:,}".format(int(nd))
        rd = "{:,}".format(int(rd))
        padding = len(st)
        if len(nd) < padding:
            nd = ' ' * (padding - len(nd)) + nd
        if len(rd) < padding:
            rd = ' ' * (padding - len(rd)) + rd

        segment = ["1st: " + st,
                   "2nd: " + nd,
                   "3rd: " + rd]
        shift = -1
        for sen in segment:
            Surface = font.render(sen, True, (30, 30, 30))
            TextRect = Surface.get_rect()
            TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 2.5 * shift * self.height)
            shift += 1
            self.screen.blit(Surface, TextRect)

    def finial(self, score, rank):
        score = "{:,}".format(int(score))

        self.diaplay("Game Over", -4.5, 90)
        self.diaplay("Your Score:", -1.5, 70)

        font = pygame.font.SysFont("Consolas", 80)
        Surface = font.render(score, True, (30, 30, 30))
        TextRect = Surface.get_rect()
        TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 0.5 * self.height)
        self.screen.blit(Surface, TextRect)

        if rank == 1:
            font = pygame.font.SysFont(None, 50)
            Surface = font.render("A New Record! Cong!", True, (30, 30, 30))
            TextRect = Surface.get_rect()
            TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 3.5 * self.height)
            self.screen.blit(Surface, TextRect)
        elif rank == 2:
            font = pygame.font.SysFont(None, 50)
            Surface = font.render("Excellent!", True, (30, 30, 30))
            TextRect = Surface.get_rect()
            TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 3.5 * self.height)
            self.screen.blit(Surface, TextRect)
        elif rank == 3:
            font = pygame.font.SysFont(None, 50)
            Surface = font.render("Good Job!", True, (30, 30, 30))
            TextRect = Surface.get_rect()
            TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 3.5 * self.height)
            self.screen.blit(Surface, TextRect)

    def goon(self):
        font = pygame.font.SysFont(None, 40)
        Surface = font.render("Press R to Continue", True, (30, 30, 30))
        TextRect = Surface.get_rect()
        TextRect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 5 * self.height)
        self.screen.blit(Surface, TextRect)
