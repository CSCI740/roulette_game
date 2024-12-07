# Make Report and Plot

from constants import PlayerType, Bet_Strategy, Placement_Strategy

from datetime import datetime
import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self):
        self.report_data = []

    def record_data(self, players):

        for i, player in enumerate(players):
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
        [_, iniBR, curBR, endRound, profit] = list_cycle
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

    def generate_report_body(self, file_write, cycle_data_for_player):
        # Write overall statistics
        initial_bankroll_sum, final_bankroll_sum = 0,0
        round_sum, profit_sum = 0,0
        number_of_round, number_of_win = 0, 0
        num_bankrup, num_lack, num_max_round, num_double = 0, 0, 0, 0

        for i, single_data in enumerate(cycle_data_for_player):
            [_, iniBR, curBR, endRound, profit] = single_data
            file_write.write("{:>4}".format(i+1))
            file_write.write(" {:>16}".format(iniBR)) # initial BR
            file_write.write(" {:>16}".format(curBR)) # current BR
            file_write.write(" {:>16}".format(endRound)) # round
            file_write.write(" {:>16}\n".format(profit)) # profit
            [initial_bankroll_sum, final_bankroll_sum, round_sum, profit_sum] = self.calculate_player_cycle_result([initial_bankroll_sum, final_bankroll_sum, round_sum, profit_sum], single_data)
            number_of_round += 1
            if profit > 0:
                number_of_win += 1
                
            if curBR == 0:
                num_bankrup += 1
            elif endRound == 100: # change it!
                num_max_round += 1
            elif curBR > iniBR * 2:
                num_double += 1
            else: #player.is_lack_of_betting_money():
                num_lack += 1

        file_write.write("------------------------------------------------------------------------------\n")
        file_write.write(" {:>20}".format(initial_bankroll_sum))
        file_write.write(" {:>16}".format(final_bankroll_sum))
        file_write.write(" {:>16}".format(round_sum))
        file_write.write(" {:>16}\n".format(profit_sum))
        file_write.write("------------------------------------------------------------------------------\n")

        return [number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double]

    def generate_report_footer(self, file_write, number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double):

        agerage_rounds = round(round_sum / number_of_round, 2)
        file_write.write("Average rounds per day: {}\n".format(str(agerage_rounds)))

        winning_percentage = round(number_of_win / number_of_round * 100, 2)
        file_write.write("Winning percentage: {}%\n".format(str(winning_percentage)))
        if profit_sum > 0:
            file_write.write("Final profit: ${}\n".format(profit_sum))
        else:
            file_write.write("Final loss: ${}\n".format(-profit_sum))

        file_write.write("Ending condition:\n")
        file_write.write("- Bankrupcy: {}%\n".format(str(round(num_bankrup / number_of_round * 100, 2))))
        file_write.write("- Lack of bet money: {}%\n".format(str(round(num_lack / number_of_round * 100, 2))))
        file_write.write("- Max round: {}%\n".format(str(round(num_max_round / number_of_round * 100, 2))))
        file_write.write("- Double profit: {}%\n".format(str(round(num_double / number_of_round * 100, 2))))

        file_write.write("------------------------------------------------------------------------------\n")


    def generate_report_file(self, player):

        [player_name, player_type, player_bet_strategy, player_place_strategy] = player.get_player_profile()

        filename = f"../results/Game_Report_{player_name}_{self.current_datetime}.txt"
    
        with open(filename, 'w') as f:
            f.write("")

        cycle_data_for_player = [element for element in self.report_data if element[0] == player_name]
        with open(filename, 'w') as f:
            self.generate_report_header(f, player)
            [number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double] = self.generate_report_body(f, cycle_data_for_player)
            self.generate_report_footer(f, number_of_round, round_sum, number_of_win, profit_sum, num_bankrup, num_lack, num_max_round, num_double)
    
    def generate_report_plot(self, players):
        filename = f"../results/Game_Report_Plot_{self.current_datetime}.png"

        for player in players:
            cycle_data_for_player = [element for element in self.report_data if element[0] == player.name]
            profit_list = [element[4] for element in cycle_data_for_player]
            
            x_values_len = len(profit_list)
            x_values = range(1, x_values_len + 1)         # x-axis index : 1, 2, ...
        
            plt.plot(x_values, profit_list, marker='o', label=player.name)
        
            plt.title("Game Result of profit [" + str(x_values_len) + "Days ]")
            plt.xlabel("Day")
            plt.ylabel("Profit")
        
            plt.legend(title="Players")
        
        # save the plot
        plt.savefig(filename)        