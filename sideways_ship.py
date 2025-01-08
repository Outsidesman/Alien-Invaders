# A class to manage the sideways ship.
import pygame

class SidewaysShip:
    def __init__(self, sw_game):
        """
        Initialize the ship's screen to that of the passed-in game
        instance's
        """
        self.screen = sw_game.screen
        self.settings = sw_game.settings

        # Set the ship's screen rectangle to that of the game instance
        self.screen_rect = sw_game.screen.get_rect()

        # Load the ship image and get its rectangular bounds.
        self.image = pygame.image.load('/Users/matthewcunningham/Documents/Work study/Python/Python Crash Course 3ed/Chapter 12 - Alien Invasion 1/images/sideways_ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the middle left of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's exact vertical position.
        self.y = float(self.rect.y)

        # Create a movement flag to determine whether the ship is moving
        # up or down
        self.moving_up = False
        self.moving_down = False

    """
    Update the ship's position depending on the movement flag.
    Use separate if statements (not elif) so no direction takes
    precedence.
    """
    def update(self):
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update the rect object from self.y
        self.rect.y = self.y

    def center_ship(self):
        """ Center the ship on the screen after death """
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)