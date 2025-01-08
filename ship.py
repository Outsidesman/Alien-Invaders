# A class to manage the ship.
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        """
        Initialize the ship's screen to that of the passed-in game
        instance's
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Set the ship's screen rectangle to that of the game instance
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rectangular bounds.
        self.image = pygame.image.load('/Users/matthewcunningham/Documents/Work study/Python/Python Crash Course 3ed/Chapter 13 - Alien Invasion 2/images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)

        # Create a movement flag to determine whether the ship is moving
        # to the right or left
        self.moving_right = False
        self.moving_left  = False

    def update(self):
        """ 
        Update the ship's position depending on the movement flag.
        Use separate if statements (not elif) so right does not always
        take precedence.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        
        # update the rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """ Center the ship on the screen after death """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image,self.rect)