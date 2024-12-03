# Game Simulation

from player import Player
from roulette_wheel import RouletteWheel
from roulette_game import RouletteGame

class RouletteSimulator:
    def __init__(self, players):
        self.players = players
        self.rounds = 10

    def show_results(self):
        """Displays the final results."""
        print("\n--- Final Results ---")
        for player in self.players:
            print(f"{player.name}'s initial and final bankroll: ${player.get_initial_bankroll()}, ${player.get_current_bankroll()}")

    def play_roulette(self, roundCount = 10):
        """Plays the game for a set number of rounds."""

        self.rounds = roundCount

        self.game = RouletteGame(self.players)        
        wheel = RouletteWheel()

        for round_number in range(self.rounds):
            print(f"\n--- {round_number+1} Round ---")
            self.game.setup_game(self.players)
            self.game.play_game(wheel)
            self.game.payout_game(self.players, wheel)
            self.game.adjust_game(self.players, wheel)
