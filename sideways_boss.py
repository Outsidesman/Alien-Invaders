import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
    """ Initialize the boss and set its starting position. """

    def __init__(self, ss_game):
        """ Initialization method for creating a boss """
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings

        # Load the boss image and set the rect attribute
        self.image = pygame.image.load('/Users/matthewcunningham/Documents/Work study/Python/Python Crash Course 3ed/Chapter 13 - Alien Invasion 2/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new boss near the middle left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the boss' vertical and horizontal positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """ Return true if the alien is at the edge of the screen """
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0)
                
    def update(self):
        """ Move the boss up or down """
        self.y += self.settings.boss_speed * self.settings.boss_direction
        self.rect.y = self.y