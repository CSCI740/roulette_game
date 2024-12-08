# Main - Setup and Run Simulation
import sys

from player import Player
from betting_strategy import BettingStrategy
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType
from report_generator import ReportGenerator, ReplicationReportGenerator

def scenario_01():

    """
    Scenario:
    1 hour: 10 rounds of Roulette game
    1 person plays roulette for 10 hours per day (100 rounds of Roulette game)
    Simulate 30 days with 3 different player types and make the initial report.
    Each player's betting strategy is random choice among 2 strategies.
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

def scenario_02():
    
    """
    Scenario:
    1 hour: 10 rounds of Roulette game
    1 person plays roulette for 10 hours per day (100 rounds of Roulette game)
    Simulate 30 day with 5 players and replicate this simulation 10000 times
    Calculate profit mean, variance and confidence interval 
    """
    
    player1 = Player("High_Risk\nAll-In", PlayerType.HIGH_RISK, 10)          # risk level: Lowest(0) ~ Higest(10) 
    player2 = Player("High_Risk\nMartingale", PlayerType.HIGH_RISK, 0)          
    player3 = Player("Moderate_Risk\nMartingale", PlayerType.MODERATE_RISK, 10)
    player4 = Player("Moderate_Risk\nFibonacci", PlayerType.MODERATE_RISK, 0)
    player5 = Player("Low_Risk\nDalembert", PlayerType.LOW_RISK, 10)
    player6 = Player("Low_Risk\nFlat-Bet", PlayerType.LOW_RISK, 0)  

    simulation_days = 30 
    num_of_sim = 100        # 10000

    simulation_replication_report = ReplicationReportGenerator(num_of_sim)
    
    for sim in range(num_of_sim):
        simulation_report = ReportGenerator()
    
        print("*** Simulation ", sim + 1, "***")
        for day_number in range(simulation_days):
            print("*** Day ", day_number + 1, " ***")
        
            player1.setup_game(100, 1, 100)
            player2.setup_game(100, 1, 100)
            player3.setup_game(100, 1, 100)
            player4.setup_game(100, 1, 100)
            player5.setup_game(100, 1, 100)
            player6.setup_game(100, 1, 100)

            rouletteSimulator = RouletteSimulator([player1, player2, player3, player4, player5, player6])

            rouletteSimulator.play_roulette(100)
            rouletteSimulator.show_results()
        
            simulation_report.record_data([player1, player2, player3, player4, player5, player6])

        mean_profits = simulation_report.get_mean_profit_for_players([player1, player2, player3, player4, player5, player6])
        sum_profits = simulation_report.get_sum_profit_for_players([player1, player2, player3, player4, player5, player6])
        simulation_replication_report.record_simulation_data([player1, player2, player3, player4, player5, player6], mean_profits, sum_profits)

    simulation_replication_report.generate_report([player1, player2, player3, player4, player5, player6])

def scenario_03():
    
    """
    Scenario:
    Intervention (digital twin)
    """
    print("Not implemented yet")

def how_to_run_simulation():
    print("---------------------------------------------")
    print("Scenarios: ")
    print("---------------------------------------------")
    print("  Scenario 1: General Player Type Analysis - Simulations for 3 Players with non-deterministic Betting Strategy")
    print("  Scenario 2: Betting Strategy Analysis - Simulation Replications for 6 Betting Strategies")
    print("  Scenario 3: Intervention Analysis - Digital Twins (Not implemented yet)")
    print("---------------------------------------------")
    print("Run the simulation with 2 arguments like so:")
    print("$ python3 main.py <scenario_number>")
    print("---------------------------------------------")

def main():
    # Get system arguments
    args = sys.argv

    # Check number of arguments
    if len(args) == 1:
        how_to_run_simulation()
        return

    # Check arguments
    scenario_num = int(args[1])

    # Run simulation
    if scenario_num == 1:
        scenario_01()
    elif scenario_num == 2:
        scenario_02()
    elif scenario_num == 3:
        scenario_03()
    else:
        print("Not Abailable scenario")

if __name__ == "__main__":
    main()
    