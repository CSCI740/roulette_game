# Roulette wheel

from random_num_gen import RandomNumGen

class RouletteWheel:
    def __init__(self):
        self.ourcome = None
        self.random_num = RandomNumGen(0, 37,probabilities=None)

        self.house_profit = 0

        # Functions for Digital Twin
        self.participants_strategies = dict()
        self.participants_bet_result = dict()
        
    def spin(self):
        """Simulates spinning the roulette wheel."""
        # American Roulette (0, 00, 1-36)
        self.outcome = self.random_num.randint()

        return self.outcome

    def get_outcome(self):
        return self.outcome

    def store_house_profit(self, payout):
        self.house_profit += payout

    def report_house_profit(self):
        return self.house_profit

    # Functions for Digital Twin
    def put_participants_strategies(self, name, bet_strategy, place_strategy):
        self.participants_strategies[name] = [bet_strategy, place_strategy]

    def get_participants_strategies(self, name): 
        return (self.participants_strategies[name][0], self.participants_strategies[name][1])

    def put_participants_bet_result(self, name, place_result):
        self.participants_bet_result[name] = place_result

    def get_participants_bet_result(self, name):
        return self.participants_bet_result[name]

    # Variance Reduction
    def spin_AVR(self):
        """Simulates spinning the roulette wheel."""
        # American Roulette (0, 00, 1-36)
        self.outcome = self.random_num.randint_AVR()

        return self.outcome
    
