import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Initialize the alien and set its starting position. """

    def __init__(self, ai_game):
        """ Initialization method for creating an alien """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set the rect attribute
        self.image = pygame.image.load('/Users/matthewcunningham/Documents/Work study/Python/Python Crash Course 3ed/Chapter 13 - Alien Invasion 2/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Return true if the alien is at an edge of the screen """
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """ Move the alien to the right or left """
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

