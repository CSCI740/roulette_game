# Game Simulation

from player import Player
from roulette_wheel import RouletteWheel
from roulette_game import RouletteGame

class RouletteSimulator:
    def __init__(self, players):
        self.players = players
        self.rounds = 10

        self.game = RouletteGame(self.players)        
        self.wheel = RouletteWheel()

    def show_results(self):
        """Displays the final results."""
        print("\n--- Final Results ---")

        profit = self.wheel.report_house_profit()
        print(f"House profit: ${profit}")

        print(f"Players' total profit: ${-profit}")        
        self.game.get_game_result(self.players)
        
    def play_roulette(self, roundCount = 10):
        """Plays the game for a set number of rounds."""

        self.rounds = roundCount

        for round_number in range(self.rounds):
            print(f"\n--- {round_number+1} Round ---")
            self.game.setup_game(self.players)
            
            self.game.play_game(self.wheel)
            
            self.game.payout_game(self.players, self.wheel)
            self.game.adjust_game(self.players, self.wheel)
            
            if self.game.settle_game(self.players) == False:
                print(f"\n--- Game ends ---")
                print(f"There is no player.")
                break