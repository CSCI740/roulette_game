# Roulette wheel

from random_num_gen import RandomNumGen

class RouletteWheel:
    def __init__(self):
        self.ourcome = None
        self.random_num = RandomNumGen()

    def spin(self):
        """Simulates spinning the roulette wheel."""
        # American Roulette (0, 00, 1-36)
        self.outcome = self.random_num.randint(0, 37)

        return self.outcome

    def get_outcome(self):
        return self.outcome
