import sys
from time import sleep
import pygame
from sideways_settings import SidewaysSettings
from sideways_game_stats import SidewaysGameStats
from sideways_button import Button
from sideways_ship import SidewaysShip
from sideways_bullet import SidewaysBullet
from sideways_boss import Boss

class SidewaysShooter:
    """ Overall class that will manage game assets and behaviors """
    def __init__(self):
        """ Initiate the game and create game resources """
        pygame.init()
        self.clock = pygame.time.Clock()

        # Create an instance of the settings class for use in the
        # program
        self.settings = SidewaysSettings()

        # Create a game window using the pygame module with dimensions
        # we set in the Settings module
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        
        # Give the game window a title
        pygame.display.set_caption("Sideways Shooter")

        # Create an instance to store game statistics.
        self.stats = SidewaysGameStats(self)

        # Create an instance of the ship and assign it to the ship
        # attribute of this game
        self.ship = SidewaysShip(self)

        # Create a group to hold the bullets and the boss
        self.bullets = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()

        # Create the 'fleet' for the boss.
        self._create_boss_fleet()

        # Start the game in an active state.
        self.game_active = False

        # Make and display the play button
        self.play_button = Button(self, "Play")

    def _check_keydown_events(self, event):
        """ Manage keydown events """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Manage keyup events """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = SidewaysBullet(self)
            self.bullets.add(new_bullet)

    def _reset_stats(self):
        """ Reset the battle fleid for a new game """
        # Get rid of any remaining bullets.
        self.bullets.empty()

        # Create a new boss and center the ship. TODO
        self.ship.center_ship()

    def _start_game(self):
        """ Start a new game """
        # Reset the game statistics
        self._reset_stats()
        self.game_active = True

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play or presses P """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()
            self.settings.initialize_dynamic_settings()
        for event in pygame.event.get():
            if event.key == pygame.K_p and not self.game_active:
                self._start_game()

    def _check_events(self):
        """ Respond to key presses """
        for event in pygame.event.get():
            # Quit the pygame module if the window is exited out
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_bullets(self):
        """ Update the position of bullets and get rid of old bullets """
        self.bullets.update()
        # Delete bullets from memory if they have left the screen and
        # also call _target_missed()
        for bullet in self.bullets.copy():
            if bullet.rect.right >= 1200:
                self.bullets.remove(bullet)
                self._target_missed()
        self._check_bullet_boss_collisions()

    def _check_bullet_boss_collisions(self):
        """
        Check for any bullets that have hit the boss and get rid of
        those bullets / print a message that they hit the boss.
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.boss, True, True)
        if collisions:
            print("Boss hit!")
            self.settings.increase_speed()
        
    def _update_boss(self):
        """ Update the position of the boss """
        self._check_boss_edges()
        self.boss.update()
    
    def _update_screen(self):
        """ Redraw the screen and ship """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.boss.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_boss(self, x_position, y_position):
        """ Create a boss and place it on the screen """
        boss = Boss(self)
        boss.y = y_position
        boss.rect.x = x_position
        boss.rect.y = y_position
        self.boss.add(boss)

    def _check_boss_edges(self):
        """ Check if the boss has reached top/bottom, change its direction """
        for boss in self.boss.sprites():
            if boss.check_edges():
                self._change_boss_direction()
                break

    def _change_boss_direction(self):
        """ Reverse the boss' direction """
        self.settings.boss_direction *= -1

    def _create_boss_fleet(self):
        """
        Create the 'fleet' for the boss.
        """
        boss = Boss(self)
        boss_width, boss_height = boss.rect.size

        current_x, current_y = self.settings.screen_width - boss_width, boss_height
        self._create_boss(current_x, current_y)

    def _target_missed(self):
        """ Respond to the ship missing the target. """
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            print("Target missed!")

            # Get rid of any remaining bullets and the boss
            self.bullets.empty()
            self.boss.empty()

            # Create a new boss and center the ship.
            self._create_boss_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            # Watch for keyboard events.
            self._check_events()

            if self.game_active:
                # Update the location of the ship.
                self.ship.update()
                # Update the bullets.
                self._update_bullets()
                # Update the boss.
                self._update_boss()
                
            # Redraw the screen (and ship) during each pass through the
            # loop.
            self._update_screen()
            # Make sure a full 60th of a second passes before re-looping
            self.clock.tick(60)

if __name__ == '__main__':
    """ Make a game instance and run the game """
    sw =  SidewaysShooter()
    sw.run_game()