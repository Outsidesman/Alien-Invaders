class SidewaysSettings:
    """ A class to hold all of the settings used in Sideways Shooter. """
    def __init__(self):
        """ Initialize the game's static settings. """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 20.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100000

        # Boss settings
        self.boss_speed = 5.0
        self.boss_direction = 1

        # Speed-up factor
        self.speedup_scale = 5.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game. """
        self.ship_speed = 1.5
        self.bullet_speed = 20.0
        self.boss_speed = 5.0
        self.fleet_direction = 1

    def increase_speed(self):
        """ Increase speed settings. """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.boss_speed *= self.speedup_scale
        