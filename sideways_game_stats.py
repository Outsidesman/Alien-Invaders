class SidewaysGameStats:
    """ Keep track of statistics for Sideways Shooter """

    def __init__(self, ss_game):
        self.settings = ss_game.settings
        self.reset_stats()

    def reset_stats(self):
        """ Initialize statistics that will change during the game. """
        self.ships_left = self.settings.ship_limit