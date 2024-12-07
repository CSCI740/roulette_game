# Main - Setup and Run Simulation
import sys

from player import Player
from betting_strategy import BettingStrategy
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType
from report_generator import ReportGenerator

def scenario_01():

    """
    Scenario:
    1 hour: 10 round of Roulette game
    1 person plays roulette for 10 hour per day (100 rounds of Roulette game)
    Simulate 30 days result and make the first report
    """

    simulation_report = ReportGenerator()
    
    player1 = Player("Alice", PlayerType.HIGH_RISK)
    player2 = Player("Bob", PlayerType.MODERATE_RISK)
    player3 = Player("Charlie", PlayerType.LOW_RISK)
    
    simulation_days = 30
    for day_number in range(simulation_days):
        print("*** Day ", day_number + 1, " ***")
        
        player1.setup_game(100, 1, 100)
        player2.setup_game(100, 1, 100)
        player3.setup_game(100, 1, 100)

        rouletteSimulator = RouletteSimulator([player1, player2, player3])

        rouletteSimulator.play_roulette(100)
        rouletteSimulator.show_results()
        
        simulation_report.record_data([player1, player2, player3])

    simulation_report.generate_report([player1, player2, player3])

def main():
    # Get system arguments
    args = sys.argv

    # Check number of arguments
    if len(args) == 1:
        print("---------------------------------------------")
        print("Run the simulation with 2 arguments like so:")
        print("$ python3 main.py <scenario_number>")
        print("  Scenario 1: General game for 3 Players 30 Days")
        print("  Scenario 2: Not implemented yet")
        print("---------------------------------------------")
        return

    # Check arguments
    scenario_num = int(args[1])

    if scenario_num == 1:
        scenario_01()
    else:
        print("Not implemented yet")

if __name__ == "__main__":
    main()
    