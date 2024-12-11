# Simulation Scenario

"""
    Scenario: Betting Strategy Analysis
    1 hour: 10 rounds of Roulette game
    1 person plays roulette for 10 hours per day (100 rounds of Roulette game)
    Simulate 30 days with 6 different players with their digital twins, and make the initial report.
    Each player's betting strategy is deterministic.
"""

import sys

from player import Player
from betting_strategy import BettingStrategy
from roulette_wheel import RouletteWheel
from roulette_game import RouletteGame
from roulette_simulator import RouletteSimulator
from constants import PlayerType
from report_generator import ReportGenerator, ReplicationReportGenerator

def scenario_high():

    simulation_report = ReportGenerator()
    
    wheel = RouletteWheel()

    player1 = Player(wheel, "High_Risk_All-In", PlayerType.HIGH_RISK, 10)                               # risk level: Lowest(0) ~ Higest(10) 
    player2 = Player(wheel, "High_Risk_All-In(R)", PlayerType.HIGH_RISK, 10, "High_Risk_All-In")          # risk level: Lowest(0) ~ Higest(10) 
    player3 = Player(wheel, "High_Risk_Martingale", PlayerType.HIGH_RISK, 0)          
    player4 = Player(wheel, "High_Risk_Martingale(R)", PlayerType.HIGH_RISK, 0, "High_Risk_Martingale")          
    player_list = [player1, player2, player3, player4]

    simulation_days = 30
    for day_number in range(simulation_days):
        print("*** Day ", day_number + 1, " ***")
        
        player1.setup_game(100, 1, 100)
        player2.setup_game(100, 1, 100)
        player3.setup_game(100, 1, 100)
        player4.setup_game(100, 1, 100)

        rouletteSimulator = RouletteSimulator(player_list, wheel)

        rouletteSimulator.play_roulette(100)
        rouletteSimulator.show_results()
        
        simulation_report.record_data(player_list)

    simulation_report.generate_report(player_list)

def scenario_moderate():

    simulation_report = ReportGenerator()
    
    wheel = RouletteWheel()

    player1 = Player(wheel, "Moderate_Risk_Martingale", PlayerType.MODERATE_RISK, 10)
    player2 = Player(wheel, "Moderate_Risk_Martingale(R)", PlayerType.MODERATE_RISK, 10, "Moderate_Risk_Martingale")
    player3 = Player(wheel, "Moderate_Risk_Fibonacci", PlayerType.MODERATE_RISK, 0)
    player4 = Player(wheel, "Moderate_Risk_Fibonacci(R)", PlayerType.MODERATE_RISK, 0, "Moderate_Risk_Fibonacci")
    player_list = [player1, player2, player3, player4]

    simulation_days = 30
    for day_number in range(simulation_days):
        print("*** Day ", day_number + 1, " ***")
        
        player1.setup_game(100, 1, 100)
        player2.setup_game(100, 1, 100)
        player3.setup_game(100, 1, 100)
        player4.setup_game(100, 1, 100)

        rouletteSimulator = RouletteSimulator(player_list, wheel)

        rouletteSimulator.play_roulette(100)
        rouletteSimulator.show_results()
        
        simulation_report.record_data(player_list)

    simulation_report.generate_report(player_list)

def scenario_low():

    simulation_report = ReportGenerator()
    
    wheel = RouletteWheel()

    player1 = Player(wheel, "Low_Risk_Dalembert", PlayerType.LOW_RISK, 10)
    player2 = Player(wheel, "Low_Risk_Dalembert(R)", PlayerType.LOW_RISK, 10, "Low_Risk_Dalembert")
    player3 = Player(wheel, "Low_Risk_Flat-Bet", PlayerType.LOW_RISK, 0)  
    player4 = Player(wheel, "Low_Risk_Flat-Bet(R)", PlayerType.LOW_RISK, 0, "Low_Risk_Flat-Bet")  
    player_list = [player1, player2, player3, player4]

    simulation_days = 30
    for day_number in range(simulation_days):
        print("*** Day ", day_number + 1, " ***")
        
        player1.setup_game(100, 1, 100)
        player2.setup_game(100, 1, 100)
        player3.setup_game(100, 1, 100)
        player4.setup_game(100, 1, 100)

        rouletteSimulator = RouletteSimulator(player_list, wheel)

        rouletteSimulator.play_roulette(100)
        rouletteSimulator.show_results()
        
        simulation_report.record_data(player_list)

    simulation_report.generate_report(player_list)
   
def scenario_02():
    scenario_high()
    scenario_moderate()
    scenario_low()