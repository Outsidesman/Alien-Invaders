import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """ A class to represent a single star in the sky """
    
    def __init__(self, sky):
        super().__init__()
        self.screen = sky.screen
        self.settings = sky.settings

        # Load the star image and set its rect attribute
        self.image = pygame.image.load('/Users/matthewcunningham/Documents/Work study/Python/Python Crash Course 3ed/Chapter 13 - Alien Invasion 2/images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new star at the same place, we will move this later
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the star's exact horizontal position
        self.y = float(self.rect.y)

    def check_edges(self):
        """ Return true if the star has fallen off the screen """
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom)

    def update(self):
        """
        Make the 'stars' fall down until they drop off the screen.
        """
        self.y += self.settings.star_speed
        self.rect.y = self.y