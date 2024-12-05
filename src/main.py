# Main - Setup and Run Simulation

from player import Player
from betting_strategy import BettingStrategy
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType

if __name__ == "__main__":

    """
    Scenario:
    1 hour: 10 round of Roulette game
    1 person plays roulette for 10 hour per day (100 rounds of Roulette game)
    Simulate 30 days result and make the first report
    """
    player1 = Player("Alice", PlayerType.HIGH_RISK, 100, 1, 100)
    player2 = Player("Bob", PlayerType.MODERATE_RISK, 100, 1, 100)
    player3 = Player("Charlie", PlayerType.LOW_RISK, 100, 1, 100)

    rouletteSimulator = RouletteSimulator([player1, player2, player3])

    rouletteSimulator.play_roulette(100)
    rouletteSimulator.show_results()
