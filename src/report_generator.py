# Make Report and Plot

from constants import PlayerType, Bet_Strategy, Placement_Strategy

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class ReportGenerator:
    def __init__(self):
        self.report_data = []

    def record_data(self, players):
        for player in players:
            self.report_data.append([player.name] + player.get_player_game_result())

    def generate_report(self, players):
        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        for player in players:
            # Write to file for each player
            self.generate_report_file(player)
        
        # Generate plot
        self.generate_report_plot(players)

    def get_str_player_type(self, player_type):
        if player_type == PlayerType.HIGH_RISK:
            return "High Risk Taker"
        elif player_type == PlayerType.MODERATE_RISK:
            return "Moderate Risk Taker"
        elif player_type == PlayerType.LOW_RISK:
            return "Low Risk Taker"
        else:
            return "Invalid Player Type"

    def get_str_betting_strategy(self, betting_strategy):
        if betting_strategy == Bet_Strategy.ALL_IN :
            return "All-In Strategy"
        elif betting_strategy == Bet_Strategy.MARTINGALE:
            return "Martingale Strategy"
        elif betting_strategy == Bet_Strategy.FIBONACCI:
            return "Fibonacci Strategy"
        elif betting_strategy == Bet_Strategy.DALEMBERT:
            return "Dalembert Strategy"
        elif betting_strategy == Bet_Strategy.FLAT:
            return "Flat-Bet Strategy"
        else:
            return "Invalid Betting Strategy"

    def get_str_placement_strategy(self, placement_strategy):
        if placement_strategy == Placement_Strategy.SINGLE_NUMBER:
            return "Single Number Strategy"
        elif placement_strategy == Placement_Strategy.DOZENS:
            return "Dozen Strategy"
        elif placement_strategy == Placement_Strategy.RED_BLACK:
            return "Red or Black Strategy"
        else:
            return "Invalid Placement Strategy"

    def calculate_player_cycle_result(self, list_sum, list_cycle):
        #[_, iniBR, curBR, endRound, profit] = list_cycle
        [_, iniBR, curBR, maxRound, endRound, endBetMoney, profit] = list_cycle
        
        [initial_bankroll_sum, final_bankroll_sum, round_sum, profit_sum] = list_sum
        initial_bankroll_sum += iniBR
        final_bankroll_sum += curBR
        round_sum += endRound
        profit_sum += profit
        return [initial_bankroll_sum, final_bankroll_sum, round_sum, profit_sum]

    def generate_report_header(self, file_write, player):
        [player_name, player_type, player_bet_strategy, player_place_strategy] = player.get_player_profile()
        str_player_type = self.get_str_player_type(player_type)
        str_betting_strategy = self.get_str_betting_strategy(player_bet_strategy)
        str_placement_strategy = self.get_str_placement_strategy(player_place_strategy)

        file_write.write("Date: {}\n".format(datetime.now().strftime("%Y-%m-%d")))
        file_write.write("Player name: {} ".format(player_name))
        file_write.write("[{}]\n".format(str_player_type))
        file_write.write("Player's betting strategy: {}\n".format(str_betting_strategy))
        file_write.write("Player's placement strategy: {}\n".format(str_placement_strategy))
        file_write.write("------------------------------------------------------------------------------\n")
        file_write.write(" {:>4}".format("Day"))
        file_write.write(" {:>16}".format("Initial-Bankroll"))
        file_write.write(" {:>16}".format("Final-Bankroll"))
        file_write.write(" {:>16}".format("Game-Round"))
        file_write.write(" {:>16}\n".format("Profit"))            
        file_write.write("------------------------------------------------------------------------------\n")

    def generate_report_body(self, file_write, player, cycle_data_for_player):
        # Write overall statistics
        initial_bankroll_sum, final_bankroll_sum = 0,0
        round_sum, profit_sum = 0,0
        number_of_round, number_of_win = 0, 0
        num_bankrup, num_lack, num_max_round, num_double = 0, 0, 0, 0

        for i, single_data in enumerate(cycle_data_for_player):
            [_, iniBR, curBR, maxRound, endRound, endBetMoney, profit] = single_data
            file_write.write("{:>4}".format(i+1))
            file_write.write(" {:>16}".format(iniBR)) # initial BR
            file_write.write(" {:>16}".format(curBR)) # current BR
            file_write.write(" {:>16}".format(endRound)) # round
            file_write.write(" {:>16}\n".format(profit)) # profit
            [initial_bankroll_sum, final_bankroll_sum, round_sum, profit_sum] = self.calculate_player_cycle_result([initial_bankroll_sum, final_bankroll_sum, round_sum, profit_sum], single_data)
            number_of_round += 1
            if profit > 0:
                number_of_win += 1

            if endRound == maxRound:               
                num_max_round += 1
            elif curBR == 0:
                num_bankrup += 1
            elif curBR > iniBR * 2:
                num_double += 1
            else: 
                num_lack += 1

        file_write.write("------------------------------------------------------------------------------\n")
        file_write.write(" {:>20}".format(initial_bankroll_sum))
        file_write.write(" {:>16}".format(final_bankroll_sum))
        file_write.write(" {:>16}".format(round_sum))
        file_write.write(" {:>16}\n".format(profit_sum))
        file_write.write("------------------------------------------------------------------------------\n")

        return [number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double]

    def calculate_mean_and_variance_calculation(self, samples):
        sample_len = len(samples)
        sample_mean = 0
        sample_variance = 0
   
        for i in range(sample_len):
            sample_mean += samples[i]
        sample_mean /= sample_len
    
        for i in range(sample_len):
            sample_variance += (samples[i] - sample_mean) * (samples[i] - sample_mean)
        sample_variance /= (sample_len - 1)

        confidence_interval = 1.96 * np.sqrt(sample_variance / sample_len)   
        ci_lower = sample_mean - confidence_interval
        ci_upper = sample_mean + confidence_interval
        
        return (sample_mean, sample_variance, ci_lower, ci_upper)
        
    def get_mean_profit_for_players(self, players):
        mean_profit_list = []        
        for player in players:
            cycle_data_for_player = [element for element in self.report_data if element[0] == player.name]
            #profit_list = [element[4] for element in cycle_data_for_player]
            profit_list = [element[6] for element in cycle_data_for_player]

            (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper) = self.calculate_mean_and_variance_calculation(profit_list)
            mean_profit_list.append([player.name, profit_mean])

        return mean_profit_list

    def get_sum_profit_for_players(self, players):
        mean_profit_list = []        
        for player in players:
            cycle_data_for_player = [element for element in self.report_data if element[0] == player.name]
            #profit_list = [element[4] for element in cycle_data_for_player]
            profit_list = [element[6] for element in cycle_data_for_player]

            profit_sum = sum(profit_list)
            mean_profit_list.append([player.name, profit_sum])

        return mean_profit_list

    def get_profit_information(self, player_name):
        cycle_data_for_player = [element for element in self.report_data if element[0] == player_name]
        #profit_list = [element[4] for element in cycle_data_for_player]
        profit_list = [element[6] for element in cycle_data_for_player]

        (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper) = self.calculate_mean_and_variance_calculation(profit_list)

        return (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper)

    def get_round_information(self, player_name):
        cycle_data_for_player = [element for element in self.report_data if element[0] == player_name]
        #round_list = [element[3] for element in cycle_data_for_player]
        round_list = [element[4] for element in cycle_data_for_player]

        (round_mean, round_variance, round_ci_lower, round_ci_upper) = self.calculate_mean_and_variance_calculation(round_list)

        return (round_mean, round_variance, round_ci_lower, round_ci_upper)

    def generate_report_footer(self, file_write, player, number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double):

        winning_percentage = round(number_of_win / number_of_round * 100, 2)
        file_write.write("Winning percentage: {}%\n".format(winning_percentage))

        agerage_rounds = round(round_sum / number_of_round, 2)
        (round_mean, round_variance, round_ci_lower, round_ci_upper) = self.get_round_information(player.name)
        file_write.write("Total game rounds: {}\n".format(round_sum))
        file_write.write(" - Day average: {}\n".format(round(round_mean, 2)))
        file_write.write(" - Variance: {}\n".format(round(round_variance, 2)))
        file_write.write(" - 95% confidence interval: [{}, {}]\n".format(round(round_ci_lower, 2), round(round_ci_upper, 2)))

        (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper) = self.get_profit_information(player.name)
        if profit_sum > 0:
            file_write.write("Total final profit: ${}\n".format(profit_sum))
            file_write.write(" - Day average: ${}\n".format(round(profit_mean, 2)))
            file_write.write(" - Variance: ${}\n".format(round(profit_variance, 2)))
            file_write.write(" - 95% confidence interval: [${}, ${}]\n".format(round(profit_ci_lower, 2), round(profit_ci_upper, 2)))
        else:
            file_write.write("Total final loss: ${}\n".format(-profit_sum))
            file_write.write(" - Day average: ${}\n".format(round(profit_mean, 2)))
            file_write.write(" - Variance: ${}\n".format(round(profit_variance, 2)))
            file_write.write(" - 95% confidence interval: [${}, ${}]\n".format(round(profit_ci_lower, 2), round(profit_ci_upper, 2)))

        file_write.write("Ending condition:\n")
        file_write.write(" - Max round: {}%\n".format(round(num_max_round / number_of_round * 100, 2)))
        file_write.write(" - Bankrupcy: {}%\n".format(round(num_bankrup / number_of_round * 100, 2)))
        #file_write.write(" - Lack of bet money: {}%\n".format(round(num_lack / number_of_round * 100, 2)))
        file_write.write(" - Double profit: {}%\n".format(round(num_double / number_of_round * 100, 2)))

        file_write.write("------------------------------------------------------------------------------\n")


    def generate_report_file(self, player):

        [player_name, player_type, player_bet_strategy, player_place_strategy] = player.get_player_profile()

        filename = f"../results/Game_Report_{player_name}_{self.current_datetime}.txt"
    
        with open(filename, 'w') as f:
            f.write("")

        cycle_data_for_player = [element for element in self.report_data if element[0] == player_name]
        with open(filename, 'w') as f:
            self.generate_report_header(f, player)
            [number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double] = self.generate_report_body(f, player, cycle_data_for_player)
            self.generate_report_footer(f, player, number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double)
    
    def generate_report_plot(self, players):

        plt.figure(figsize=(10, 6))         

        for player in players:
            cycle_data_for_player = [element for element in self.report_data if element[0] == player.name]
            #profit_list = [element[4] for element in cycle_data_for_player]
            profit_list = [element[6] for element in cycle_data_for_player]

            x_values_len = len(profit_list)
            x_values = range(1, x_values_len + 1)         # x-axis index : 1, 2, ...
        
            plt.plot(x_values, profit_list, marker='o', linestyle='-', label=player.name)
                        
        plt.axhline(y=0, color='r', linestyle='--')

        plt.title("Game Result of profit [" + str(x_values_len) + " Days ]")
        plt.xlabel("Day")
        plt.ylabel("Profit (Dollars)")
        
        plt.legend(title="Players")
        
        # save the plot
        filename = f"../results/Game_Report_Plot_{player.player_type}_{self.current_datetime}.png"
        plt.savefig(filename)        

class ReplicationReportGenerator:
    def __init__(self, num_of_replication):
        self.report_replication_data = []
        self.report_replication_sum_profits = []
        self.num_of_replication = num_of_replication

    def record_simulation_data(self, players, profits, sum_profits):
        self.report_replication_data.extend(profits)
        self.report_replication_sum_profits.extend(sum_profits)

    def generate_report(self, players):
        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Write to file for each player
        self.generate_report_file(players)
        
        # Generate plot
        #self.generate_report_plot(players)
        self.generate_report_plot_sum_profit(players)

    def calculate_mean_and_variance_calculation(self, samples):
        sample_len = len(samples)
        sample_mean = 0
        sample_variance = 0
   
        for i in range(sample_len):
            sample_mean += samples[i]
        sample_mean /= sample_len
    
        for i in range(sample_len):
            sample_variance += (samples[i] - sample_mean) * (samples[i] - sample_mean)
        sample_variance /= (sample_len - 1)

        confidence_interval = 1.96 * np.sqrt(sample_variance / sample_len)   
        ci_lower = sample_mean - confidence_interval
        ci_upper = sample_mean + confidence_interval
        
        return (sample_mean, sample_variance, ci_lower, ci_upper)

    def generate_report_plot_mean_profit(self, players):
        filename = f"../results/Game_Replication_Plot_{self.current_datetime}.png"

        players_name = []
        players_profit_mean = []
        players_profit_std = []
        for player in players:
            cycle_data_for_player = [element for element in self.report_replication_data if element[0] == player.name]
            profit_list = [element[1] for element in cycle_data_for_player]
            (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper) = self.calculate_mean_and_variance_calculation(profit_list)

            players_name.append(player.name)
            players_profit_mean.append(profit_mean)
            players_profit_std.append(profit_variance**0.5)

        plt.figure(figsize=(10, 6))
        plt.errorbar(players_name, players_profit_mean, yerr=players_profit_std, fmt='o', linestyle='--', capsize=5, capthick=2, label='Mean Profit with Std Dev')
       
        for xi, yi, yerr_i in zip(players_name, players_profit_mean, players_profit_std):
            plt.text(xi, yi + yerr_i + 0.2, f'{yi:.2f}', ha='center', va='bottom', fontsize=9)

        plt.xlabel('Players')
        plt.ylabel('1 Day Profit Mean Estimate (dollars)')
        plt.title('1 Day Profit for Players [' + str(self.num_of_replication) + ' replicaitons]')
        plt.grid(True)
        
        plt.legend(title="Player Type")
        
        # save the plot
        plt.savefig(filename)       

    def generate_report_file(self, players):
        filename = f"../results/Game_Replication_Report_{self.current_datetime}.txt"
    
        with open(filename, 'w') as f:
            f.write("")

            f.write("Date: {}\n".format(datetime.now().strftime("%Y-%m-%d")))
            f.write("------------------------------------------------------------------------------\n")
            players_name = []
            players_profit_mean = []
            players_profit_std = []
            for player in players:
                cycle_data_for_player = [element for element in self.report_replication_sum_profits if element[0] == player.name]
                profit_list = [element[1] for element in cycle_data_for_player]
                (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper) = self.calculate_mean_and_variance_calculation(profit_list)

                player_replaced_name = player.name.replace("\n", "_")           # To display name in one line
                f.write("Player name: {}\n".format(player_replaced_name))
                f.write("- profit mean': {}\n".format(round(profit_mean, 2)))
                f.write("- profit variance: {}\n".format(round(profit_variance, 2)))
                f.write("- 95% confidence interval: [{}, {}]\n".format(round(profit_ci_lower, 2), round(profit_ci_upper, 2)))

                f.write("------------------------------------------------------------------------------\n")

    def generate_report_plot_sum_profit(self, players):
        #print("generate plot")
        filename = f"../results/Game_Replication_Plot_{self.current_datetime}.png"

        players_name = []
        players_profit_mean = []
        players_profit_std = []
        for player in players:
            cycle_data_for_player = [element for element in self.report_replication_sum_profits if element[0] == player.name]
            profit_list = [element[1] for element in cycle_data_for_player]
            (profit_mean, profit_variance, profit_ci_lower, profit_ci_upper) = self.calculate_mean_and_variance_calculation(profit_list)

            players_name.append(player.name)
            players_profit_mean.append(profit_mean)
            players_profit_std.append(profit_variance**0.5)

        plt.figure(figsize=(10, 6))
        plt.errorbar(players_name, players_profit_mean, yerr=players_profit_std, fmt='o', linestyle='--', capsize=5, capthick=2, label='Mean Profit with Std Dev')
       
        for xi, yi, yerr_i in zip(players_name, players_profit_mean, players_profit_std):
            plt.text(xi, yi + yerr_i + 0.2, f'{yi:.2f}', ha='center', va='bottom', fontsize=9)

        plt.xlabel('Players')
        plt.ylabel('30 Day Profit Mean Estimate (dollars)')

        plt.axhline(y=0, color='r', linestyle='--')

        plt.title('30 Day Profit for Players [' + str(self.num_of_replication) + ' replicaitons]')
        plt.grid(True)
        
        plt.legend(title="Player Type")
        
        # save the plot
        plt.savefig(filename)       
