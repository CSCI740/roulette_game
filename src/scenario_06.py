import os
import sys
import csv
import pandas as pd
from datetime import datetime  # Import datetime for the timestamp
from player import Player
from roulette_wheel import RouletteWheel
from roulette_simulator import RouletteSimulator
from constants import PlayerType
from report_generator import ReportGenerator, ReplicationReportGenerator
from random_num_gen import RandomNumGen

# Scenario 06: Common random variables variance reduction
# 1 hour: 10 rounds of Roulette game
# 1 person plays roulette for 10 hours per day (100 rounds of Roulette game)
# Simulate 30 days for all 6 different players

def scenario_06():
    wheel = RouletteWheel()
    
    player_configs = [
        ("Moderate_Risk:Martingale", PlayerType.MODERATE_RISK, 10),
        ("Moderate_Risk:Fibonacci", PlayerType.MODERATE_RISK, 0)
    ]
    
    player_list = [Player(wheel, name, player_type, bet) for name, player_type, bet in player_configs]
    
    # Create a unique folder for this experiment inside the base directory
    base_dir = os.path.join(os.getcwd(), '../results')  # Base directory for results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    folder_name = f"variance_reduction_{player_list[0].name}__{player_list[1].name}_experiment_{timestamp}"
    folder_path = os.path.join(base_dir, folder_name)  # Create full path to the folder
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    
    print(f"Created folder: {folder_path}")
    
    for player in player_list:
        single_player_simulation_with_replications(player, wheel, 1000, folder_path)  
    
    wheel2 = RouletteWheel()
    player_list_2 = [Player(wheel2, name, player_type, bet) for name, player_type, bet in player_configs]
    
    two_player_simulation_with_replications(player_list_2, wheel2, 1000, folder_path)  



def single_player_simulation_with_replications(player, wheel, number_of_simulations, folder_path):
    
    # Simulation configuration
    simulation_days = 30
    num_of_sim = number_of_simulations
    
    # Get current timestamp for file naming
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_path = os.path.join(folder_path, f"Game_Replication_All_Data_NO_VR_{player.name}_{current_datetime}.csv")
    
    # Initialize the replication report and list to store mean profits
    simulation_replication_report = ReplicationReportGenerator(num_of_sim)
    list_of_per_sim_mean_profits = []
    list_of_per_sim_mean_profits_columns = ['Player', 'replication', 'avg_num_rounds', 'variance_rounds', 'sum_profits', 'mean_day_profits', 'variance_profits']
    
    # Open CSV file and write headers
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player', 'replication', 'day_number', 'Initial_bankroll', 'end_bankroll', 'rounds_played', 'day_profit'])

        for sim in range(num_of_sim):
            simulation_report = ReportGenerator()
            print(f"*** Simulation {sim + 1} ***")
            
            for day_number in range(simulation_days):
                print(f"*** Day {day_number + 1} ***")
                player.setup_game(100, 1, 100)
                roulette_simulator = RouletteSimulator([player], wheel)
                roulette_simulator.play_roulette(100)
                roulette_simulator.show_results()
                simulation_report.record_data([player])
                simulation_report.record_data_with_replication_num([player], sim, day_number)
            
            simulation_report.generate_csv_data_only([player])
            
            mean_profits = simulation_report.get_mean_profit_for_players([player])
            sum_profits = simulation_report.get_sum_profit_for_players([player])
            simulation_replication_report.record_simulation_data([player], mean_profits, sum_profits)

            print("=============================================")
            print(f"Mean Profits: {mean_profits}")
            print(f"Sum Profits: {sum_profits}")
            print("report data", simulation_report.report_data)
            
            list_of_per_sim_mean_profits.append([
                player.name, 
                sim,  
                simulation_report.avg_num_round[player.name],
                simulation_report.variance_round[player.name],
                simulation_report.sum_profit[player.name], 
                simulation_report.avg_profit[player.name],
                simulation_report.variance_profit[player.name]
            ])
            
            print("=============================================")
            for row in simulation_report.report_all_data:
                writer.writerow(row)  # Write each row to the CSV file

    simulation_replication_report.generate_report_varaince([player], folder_path, "NO_VR")
    
    csv_file_means_path = os.path.join(folder_path, f"Game_Replication_All_MEANS_NO_VR_{player.name}_{current_datetime}.csv")
    with open(csv_file_means_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list_of_per_sim_mean_profits_columns)
        writer.writerows(list_of_per_sim_mean_profits)
    
    print(f"Report data for all replications has been saved to {csv_file_path}")
    print(f"Mean profits for all replications have been saved to {csv_file_means_path}")


def two_player_simulation_with_replications(two_players, wheel, number_of_simulations, folder_path):
    
    player1, player2 = two_players
    player_type = player1.player_type
    
    # Risk mapping for random number generation
    risk_mapping = {
        PlayerType.HIGH_RISK: (0, 37),
        PlayerType.MODERATE_RISK: (0, 2),
        PlayerType.LOW_RISK: (0, 1)
    }
    
    random_num_bet = RandomNumGen(*risk_mapping[player_type], probabilities=None) if player_type in risk_mapping else None
    
    # Simulation configuration
    simulation_days = 30
    num_of_sim = number_of_simulations
    
    # Get current timestamp for file naming
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_path = os.path.join(folder_path, f"Game_Replication_All_Data_VR_{current_datetime}.csv")
    
    # Initialize the replication report and list to store mean profits
    simulation_replication_report = ReplicationReportGenerator(num_of_sim)
    list_of_per_sim_mean_profits = []
    list_of_per_sim_mean_profits_columns = ['Player', 'replication', 'avg_num_rounds', 'variance_rounds', 'sum_profits', 'mean_day_profits', 'variance_profits']
    
    # Open CSV file and write headers
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player', 'replication', 'day_number', 'Initial_bankroll', 'end_bankroll', 'rounds_played', 'day_profit'])

        for sim in range(num_of_sim):
            simulation_report = ReportGenerator()
            print(f"*** Simulation {sim + 1} ***")
            
            for day_number in range(simulation_days):
                print(f"*** Day {day_number + 1} ***")
                player1.setup_game(100, 1, 100)
                player2.setup_game(100, 1, 100)
                
                # Initialize and play the roulette simulator
                roulette_simulator = RouletteSimulator([player1, player2], wheel)
                num_bet = random_num_bet.randint() if random_num_bet else None
                roulette_simulator.play_roulette_VR(100, num_bet)
                roulette_simulator.show_results()
                
                # Record player data for the day
                simulation_report.record_data([player1, player2])
                simulation_report.record_data_with_replication_num([player1, player2], sim, day_number)
            
            simulation_report.generate_csv_data_only([player1, player2])
            
            mean_profits = simulation_report.get_mean_profit_for_players([player1, player2])
            sum_profits = simulation_report.get_sum_profit_for_players([player1, player2])
            simulation_replication_report.record_simulation_data([player1, player2], mean_profits, sum_profits)

            print("=============================================")
            print(f"Mean Profits: {mean_profits}")
            print(f"Sum Profits: {sum_profits}")
            print("report data", simulation_report.report_data)
            
            for player in [player1, player2]:
                list_of_per_sim_mean_profits.append([
                    player.name, 
                    sim,  
                    simulation_report.avg_num_round[player.name],
                    simulation_report.variance_round[player.name],
                    simulation_report.sum_profit[player.name], 
                    simulation_report.avg_profit[player.name],
                    simulation_report.variance_profit[player.name]
                ])
            
            print("=============================================")
            for row in simulation_report.report_all_data:
                writer.writerow(row)  # Write each row to the CSV file

    simulation_replication_report.generate_report_varaince([player1, player2], folder_path, "VR")
    
    csv_file_means_path = os.path.join(folder_path, f"Game_Replication_All_MEANS_VR_{current_datetime}.csv")
    with open(csv_file_means_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list_of_per_sim_mean_profits_columns)
        writer.writerows(list_of_per_sim_mean_profits)
    
    print(f"Report data for all replications has been saved to {csv_file_path}")
    print(f"Mean profits for all replications have been saved to {csv_file_means_path}")

