# Main - Setup and Run Simulation

from player import Player
from betting_strategy import BettingStrategy
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType

if __name__ == "__main__":

    player1 = Player("Alice", PlayerType.HIGH_RISK)
    player2 = Player("Bob", PlayerType.MODERATE_RISK)
    player3 = Player("Charlie", PlayerType.LOW_RISK)

    rouletteSimulator = RouletteSimulator([player1, player2, player3])

    rouletteSimulator.play_roulette(100)
    rouletteSimulator.show_results()
