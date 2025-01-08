import sys
import pygame
from star_settings import StarSettings
from star import Star

class StarrySky:
    """ Class to manage the sky full of stars """
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # Create an instance of the setting class for use in the program
        self.settings = StarSettings()

        # Create a game window using the pygame module
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # Give the window a title
        pygame.display.set_caption("Starry night")

        # Create a group to hold the stars
        self.stars = pygame.sprite.Group()

        # Create the fleet of stars
        self._create_all_stars()

    def _check_events(self):
        """ Respond to key presses """
        for event in pygame.event.get():
            # Quit the game q is pressed
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_stars(self):
        """ Update the position of the stars and get rid of old stars """
        self._check_star_edges()
        self.stars.update()
        # Delete stars from memory if they have left the screen
        for star in self.stars.copy():
            if star.rect.top >= self.settings.screen_height:
                self.stars.remove(star)

    def _update_screen(self):
        """ Redraw the stars """
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_single_star(self, x_position, y_position):
        """ Create a star and place it in the row """
        new_star = Star(self)
        new_star.x = x_position
        new_star.y = y_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)

    def _create_star_row(self):
        """ Generate a single row of stars """
        star = Star(self)
        star_width, star_height = star.rect.size

        current_x, current_y = star_width, star_height
        while current_x < (self.settings.screen_width -2 * star_width):
            self._create_single_star(current_x, current_y)
            current_x += 2 * star_width

    def _create_all_stars(self):
        """ Create the stars in the sky """
        # Create a star and keep adding stars until there's no room left
        # Spacing between stars is one star width and one star height
        star = Star(self)
        star_width, star_height = star.rect.size

        current_x, current_y = star_width, star_height
        while current_y < (self.settings.screen_height -3 * star_height):
            while current_x < (self.settings.screen_width -2 * star_width):
                self._create_single_star(current_x, current_y)
                current_x += 2 * star_width

            # Finished a row; reset x value, increment y value
            current_x = star_width
            current_y += star_height * 2

    def _check_star_edges(self):
        """ Check if a row of stars has reached the bottom """
        for star in self.stars.sprites():
            if star.check_edges():
                if not any(star.rect.top <= star.rect.height * 2 for star in self.stars):
                    self._create_star_row()
                # Generate a new row of stars 
                #self._create_star_row()
                print("Added a row of stars.")
                break

    def run_sky(self):
        """ Start the main loop for the 'game' """
        while True:
            # Watch for keyboard events
            self._check_events()
            # Update star positions
            self._update_stars()
            # Redraw everything on the screen
            self._update_screen()
            # Make sure a full 60th of a second passes before re-looping
            self.clock.tick(10)

if __name__ == '__main__':
    ss = StarrySky()
    ss.run_sky()