# Simulation Scenario
    
"""
    Scenario: Digital Twin and Intervention 
    1 hour: 10 rounds of Roulette game
    1 person plays roulette for 10 hours per day (100 rounds of Roulette game)
    Each player's betting strategy is deterministic.
    Each player has their twin replica. Twin replica follows same strategy and same chip placement as twin original.
    Simulate 30 day with 3 original players and 3 replica players, and replicate this simulation 1000 times
    Calculate profit mean, variance and confidence interval 
"""

from player import Player
from betting_strategy import BettingStrategy
from roulette_wheel import RouletteWheel
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType
from report_generator import ReportGenerator, ReplicationReportGenerator

def scenario_05():

    wheel = RouletteWheel()

    player1 = Player(wheel, "H_Risk\nAll-In", PlayerType.HIGH_RISK, 10)                               
    player2 = Player(wheel, "H_Risk\nAll-In(R)", PlayerType.HIGH_RISK, 10, "H_Risk\nAll-In")           
    player3 = Player(wheel, "H_Risk\nMartin", PlayerType.HIGH_RISK, 0)          
    player4 = Player(wheel, "H_Risk\nMartin(R)", PlayerType.HIGH_RISK, 0, "H_Risk\nMartin")          
    player5 = Player(wheel, "M_Risk\nMartin", PlayerType.MODERATE_RISK, 10)
    player6 = Player(wheel, "M_Risk\nMartin(R)", PlayerType.MODERATE_RISK, 10, "M_Risk\nMartin")
    player7 = Player(wheel, "M_Risk\nFibo", PlayerType.MODERATE_RISK, 0)
    player8 = Player(wheel, "M_Risk\nFibo(R)", PlayerType.MODERATE_RISK, 0, "M_Risk\nFibo")
    player9 = Player(wheel, "L_Risk\nDalem", PlayerType.LOW_RISK, 10)
    player10 = Player(wheel, "L_Risk\nDalem(R)", PlayerType.LOW_RISK, 10, "L_Risk\nDalem")
    player11 = Player(wheel, "L_Risk\nFlat", PlayerType.LOW_RISK, 0)  
    player12 = Player(wheel, "L_Risk\nFlat(R)", PlayerType.LOW_RISK, 0, "L_Risk\nFlat")  
    player_list = [player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12]

    simulation_days = 30 
    num_of_sim = 1000        # 10000

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
            player7.setup_game(100, 1, 100)
            player8.setup_game(100, 1, 100)
            player9.setup_game(100, 1, 100)
            player10.setup_game(100, 1, 100)
            player11.setup_game(100, 1, 100)
            player12.setup_game(100, 1, 100)

            rouletteSimulator = RouletteSimulator(player_list, wheel)

            rouletteSimulator.play_roulette(100)
            rouletteSimulator.show_results()
        
            simulation_report.record_data(player_list)

        mean_profits = simulation_report.get_mean_profit_for_players(player_list)
        sum_profits = simulation_report.get_sum_profit_for_players(player_list)
        simulation_replication_report.record_simulation_data(player_list, mean_profits, sum_profits)

    simulation_replication_report.generate_report(player_list)
