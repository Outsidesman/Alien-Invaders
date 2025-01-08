import pygame
from pygame.sprite import Sprite

class SidewaysBullet(Sprite):
    """ A class to manage bullets fired from the ship """

    def __init__(self, sw_game):
        """ Create a bullet object at the ship's current position. """
        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0), then set the current position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.center = sw_game.ship.rect.center

        # Store the bullet's position as a float
        self.x = float(self.rect.x)

    def update(self):
        """ Move the mullet right across the screen """
        # Update the exact position of the bullet
        self.x += self.settings.bullet_speed
        # Update the rect positon
        self.rect.x = self.x

    def draw_bullet(self):
        """ Draw the bullet to the screen """
        pygame.draw.rect(self.screen, self.color, self.rect)