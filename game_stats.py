class GameStats:
    """ Keep track of statistics for Alien Invasion """

    def __init__(self, ai_game):
        """ Initialize Statistics. """
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        f = open("/Users/matthewcunningham/Documents/Work study/Python/Python Crash Course 3ed/high_score", "r")
        super_score = f.read()
        print(f"High score from file: {super_score}")

        self.high_score = int(super_score)
        f.close()
    
    def reset_stats(self):
        """ Initialize statistics that will change during the game. """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1