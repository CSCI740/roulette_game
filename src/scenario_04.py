# Simulation Scenario
    
"""
    Scenario: Digital Twin and Intervention 
    1 hour: 10 rounds of Roulette game
    1 person plays roulette for 10 hours per day (100 rounds of Roulette game)
    Each player's betting strategy is non-deterministic.
    Each player has their twin replica. Twin replica follows same strategy and same chip placement as twin original.
    Simulate 30 day with 3 original players and 3 replica players, and replicate this simulation 10000 times
    Calculate profit mean, variance and confidence interval 
"""

from player import Player
from betting_strategy import BettingStrategy
from roulette_wheel import RouletteWheel
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType
from report_generator import ReportGenerator, ReplicationReportGenerator

def scenario_04():

    wheel = RouletteWheel()

    player1 = Player(wheel, "High_Risk", PlayerType.HIGH_RISK, 3)                           
    player2 = Player(wheel, "High_Risk\n(Replica)", PlayerType.HIGH_RISK, 3, "High_Risk")          
    player3 = Player(wheel, "Moderate_Risk", PlayerType.MODERATE_RISK, 5)
    player4 = Player(wheel, "Moderate_Risk\n(Replica)", PlayerType.MODERATE_RISK, 5, "Moderate_Risk")
    player5 = Player(wheel, "Low_Risk", PlayerType.LOW_RISK, 7)
    player6 = Player(wheel, "Low_Risk\n(Replica)", PlayerType.LOW_RISK, 7, "Low_Risk")
    player_list = [player1, player2, player3, player4, player5, player6]

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

            rouletteSimulator = RouletteSimulator(player_list, wheel)

            rouletteSimulator.play_roulette(100)
            rouletteSimulator.show_results()
        
            simulation_report.record_data(player_list)

        mean_profits = simulation_report.get_mean_profit_for_players(player_list)
        sum_profits = simulation_report.get_sum_profit_for_players(player_list)
        simulation_replication_report.record_simulation_data(player_list, mean_profits, sum_profits)

    simulation_replication_report.generate_report(player_list)
