import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """ Overall class that will manage game assets and behaviors """
    def __init__(self):
        """ Initialize the game and create game resources """
        pygame.init()
        self.clock = pygame.time.Clock()

        # Create an instance of the settings class for use in the
        # program
        self.settings = Settings()

        # Create a game window using the pygame module with dimensions
        # we set in the Settings module.
        self.screen = pygame.display.set_mode(
           (self.settings.screen_width, self.settings.screen_height))
        
        # Give the game window a title
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics and create a
        # scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create an instance of the ship and assign it to the ship
        # attribute of this game
        self.ship = Ship(self)

        # Create groups to hold both the bullets and aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create the fleet of aliens
        self._create_fleet()

        # Start the game and set the active flag
        self.game_active = False

        # Make and display the Easy button
        self.play_button = Button(self, "Easy")

        # Make and display the Medium button
        self.medium_button = Button(self, "")
        self.medium_button.rect.y += 100
        self.medium_button._prep_msg("Medium")

        # Make and display the Hard button
        self.hard_button = Button(self, "")
        self.hard_button.rect.y += 200
        self.hard_button._prep_msg("Hard")

    def _check_keydown_events(self, event):
        """ Manage keydown events """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.sb.write_score()
            print("Leaving game (2)")
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """ Manage keyup events """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _reset_stats(self):
        """ Reset the battle field for a new game """
        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

    def _start_game(self):
        """ Start a new game """
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.score = 0
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        print("Started a game.")
        self.game_active = True
            
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _check_easy_button(self, mouse_pos):
        """ Start a new game when the player clicks Play or presses P """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            print("Got Easy button")
            self.settings.initialize_dynamic_settings()
            self._start_game()
        for event in pygame.event.get():
            if event.key == pygame.K_p and not self.game_active:
                self._start_game()

    def _check_medium_button(self, mouse_pos):
        """ Start medium if the player clicked the medium button """
        button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            print("Got Medium button")
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.settings.increase_speed()
            self._start_game()
        for event in pygame.event.get():
            if event.key == pygame.K_p and not self.game_active:
                self._start_game()

    def _check_hard_button(self, mouse_pos):
        """ Start hard if the player clicked the hard button """
        button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            print("Got Hard Button")
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.settings.increase_speed()
            self.settings.increase_speed()
            self.settings.increase_speed()
            self._start_game()
        for event in pygame.event.get():
            if event.key == pygame.K_p and not self.game_active:
                self._start_game()

    def _check_events(self):
        """ Respond to key presses """
        for event in pygame.event.get():
            # Quit the pygame module if the window is exited out
            if event.type == pygame.QUIT:
                print("Leaving game (1)")
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_easy_button(mouse_pos)
                self._check_medium_button(mouse_pos)
                self._check_hard_button(mouse_pos)


    def _update_bullets(self):
        """ Update the position of bullets and get rid of old bullets """
        self.bullets.update()
        # Delete bullets from memory if they have left the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        Check for any bullets that have hit aliens and get rid of those
        bullets/aliens
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # If the alien fleet is totally empty, make new aliens
        if not self.aliens:
            # Destroy any bullets remaining on the screen and create the
            # new alien fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ Update the positions of all aliens in the fleet """
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens reaching the bottom of the screen
        self._check_aliens_bottom()

    def _update_screen(self):
        """ Redraw the screen and ship """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score
        self.sb.show_score(  )

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_alien(self, x_position, y_position):
        """ Create an alien and place it in the row """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """ Check if any aliens have reached an edge, change their direction """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """ Check if any aliens have reached the bottom of the screen """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat aliens reaching the bottm the same as if the ship
                # got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """ Drop the alien fleet down and reverse their direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """
        Create the fleet of aliens:
        Create a single alien and keep adding aliens until there's no room
        left.
        Spacing between aliens is one alien witdh and one alien height.
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height -3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien. """
        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard
            self.stats.ships_left -=1
            self.sb.prep_ships()
            print("Ship hit!")

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet of aliens and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            # Watch for keyboard events
            self._check_events()

            if self.game_active:
                # Update ship position
                self.ship.update()
                # Update bullet positions
                self._update_bullets()
                # Update alien positions
                self._update_aliens()

            # Redraw everything on the screen
            self._update_screen()
            # Make sure a full 60th of a second passes before re-looping
            self.clock.tick(60)

if __name__ == '__main__':
    """ Make a game instance and run the game """
    ai = AlienInvasion()
    ai.run_game()

