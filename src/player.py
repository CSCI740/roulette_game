# Player class

from random_num_gen import RandomNumGen
from betting_strategy import BettingStrategy
from placement_strategy import PlacementStrategy

import betting_strategy
from constants import PlayerType, Bet_Strategy, Placement_Strategy

class Player:
    def __init__(self, name, player_type, risk_level=5):
        self.name = name
        self.player_type = player_type

        #print("*** Risk Level: ", risk_level)

        if player_type == PlayerType.HIGH_RISK:
            probabilities = {
                Bet_Strategy.ALL_IN: (risk_level, 10),                  # Outcome Bet_Strategy.ALL_IN has a probability of risk_level/10
                Bet_Strategy.MARTINGALE: (10 - risk_level, 10)}         # Outcome Bet_Strategy.MARTINGALE has a probability of (10 - risk_level)/10}

            self.random_num = RandomNumGen(Bet_Strategy.ALL_IN, Bet_Strategy.MARTINGALE, probabilities)
            self.bet_strategy = self.random_num.randint()

            self.place_strategy = Placement_Strategy.SINGLE_NUMBER
            self.random_num_bet = RandomNumGen(0,37, probabilities=None)
            if self.bet_strategy == Bet_Strategy.ALL_IN:
                print(f"{self.name}'s strategy - bet:ALL_IN, placement:SINGLE_NUMBER")
            else:
                print(f"{self.name}'s strategy - bet:MARTINGALE, placement:SINGLE_NUMBER")
            

        elif player_type == PlayerType.MODERATE_RISK:
            probabilities = {
                Bet_Strategy.MARTINGALE: (risk_level, 10),              # Outcome Bet_Strategy.MARTINGALE has a probability of risk_level/10
                Bet_Strategy.FIBONACCI: (10 - risk_level, 10)}          # Outcome Bet_Strategy.FIBONACCI has a probability of (10 - risk_level)/10}

            self.random_num = RandomNumGen(Bet_Strategy.MARTINGALE, Bet_Strategy.FIBONACCI, probabilities)
            self.bet_strategy = self.random_num.randint()
            
            self.place_strategy = Placement_Strategy.DOZENS
            self.random_num_bet = RandomNumGen(0, 2, probabilities=None)
            if self.bet_strategy == Bet_Strategy.MARTINGALE:
                print(f"{self.name}'s strategy - bet:MARTINGALE, placement:DOZENS")
            else:
                print(f"{self.name}'s strategy - bet:FIBONACCI, placement:DOZENS")

        elif player_type == PlayerType.LOW_RISK:
            probabilities = {
                Bet_Strategy.DALEMBERT: (risk_level, 10),            # Outcome Bet_Strategy.DALEMBERT has a probability of risk_level/10
                Bet_Strategy.FLAT: (10 - risk_level, 10)}           # Outcome Bet_Strategy.FLAT has a probability of (10 - risk_level)/10}

            self.random_num = RandomNumGen(Bet_Strategy.DALEMBERT, Bet_Strategy.FLAT, probabilities)
            self.bet_strategy = self.random_num.randint()

            self.place_strategy = Placement_Strategy.RED_BLACK
            self.random_num_bet = RandomNumGen(0, 1, probabilities=None)
            if self.bet_strategy == Bet_Strategy.DALEMBERT:
                print(f"{self.name}'s strategy - bet:DALEMBERT, placement:RED_BLACK")
            else:
                print(f"{self.name}'s strategy - bet:FLAT, placement:RED_BLACK")
            
        else:
            print("Unknown Player type")

    def setup_game(self, bankroll, initial_bet_money, max_round_number):
        self.initial_bankroll = bankroll
        self.current_bankroll = bankroll
        
        self.initial_bet_money = initial_bet_money

        self.max_round_number = max_round_number
        self.current_round_number = 0

        self.on_game = True

        self.betting_strategy = BettingStrategy(self.bet_strategy, self.initial_bet_money)
        self.current_bet_money = self.betting_strategy.init_bet_money(self.current_bankroll)

        self.placement_strategy = PlacementStrategy(self.place_strategy)

    def get_initial_bankroll(self):
        return self.initial_bankroll

    def get_current_bankroll(self):
        return self.current_bankroll

    def get_profit(self):
        return self.current_bankroll - self.initial_bankroll

    def get_round(self):
        return self.current_round_number

    def place_bet(self):        
        if self.on_game == False:
            return

        self.current_round_number += 1             

        """Places a bet on a random number."""
        if self.player_type == PlayerType.HIGH_RISK:
            result = self.random_num_bet.randint()
            print(f"{self.name}'s bet ${self.current_bet_money} on {result} of Single Number")
        elif self.player_type == PlayerType.MODERATE_RISK:
            result = self.random_num_bet.randint() 

            print(f"{self.name}'s bet ${self.current_bet_money} on {result+1}th dozen")
        elif self.player_type == PlayerType.LOW_RISK:
            result = self.random_num_bet.randint() 
            if(result == 0):
                print(f"{self.name}'s bet ${self.current_bet_money} on Red")
            else:
                print(f"{self.name}'s bet ${self.current_bet_money} on Black")    
        else:
            print("Unknown player type")

        self.placement_strategy.place_bet(result)
        
        return self.current_bet_money
    
    def payout(self, wheel):
        if self.on_game == False:
            return

        wheel_outcome = wheel.get_outcome()
        bet_result = self.placement_strategy.is_winning_place(wheel_outcome)

        if bet_result:
            payout = self.placement_strategy.payout(self.current_bet_money)
            self.current_bankroll += payout - self.current_bet_money
            wheel.store_house_profit(-payout + self.current_bet_money)
            print(f"{self.name} wins! - current bankroll:{self.current_bankroll}")
        else:
            payout = -self.current_bet_money
            self.current_bankroll += payout
            wheel.store_house_profit(-payout)
            print(f"{self.name} loses! - current bankroll:{self.current_bankroll}")


    def adjust_bet_money(self, wheel):
        if self.on_game == False:
            return

        wheel_outcome = wheel.get_outcome()
        bet_result = self.placement_strategy.is_winning_place(wheel_outcome)

        if bet_result:
            self.current_bet_money = self.betting_strategy.adjust_bet_money(True, self.current_bankroll)
            print(f"{self.name} wins! - next bet money:{self.current_bet_money}")
        else:
            self.current_bet_money = self.betting_strategy.adjust_bet_money(False, self.current_bankroll)
            print(f"{self.name} loses! - next bet money:{self.current_bet_money}")

    def is_max_round(self):
        if self.current_round_number >= self.max_round_number:
            self.on_game = False
            return True

        return False

    def is_bankrupt(self):
        if self.current_bankroll == 0:
            self.on_game = False
            return True

        return False

    def is_lack_of_betting_money(self):
        current_bet_money = self.betting_strategy.get_current_bet_money()
        if self.current_bankroll < current_bet_money:
            self.on_game = False
            return True

        return False

    def is_double_profit(self):
        if self.current_bankroll >= self.initial_bankroll * 2:
            self.on_game = False
            return True

        return False

    def get_player_profile(self):
        return [self.name, self.player_type, self.bet_strategy, self.place_strategy]

    def get_player_game_result(self):
        return [self.initial_bankroll, self.current_bankroll, self.current_round_number, self.current_bankroll - self.initial_bankroll]

    def get_report(self):
        print(f"--- {self.name}'s type: {self.player_type}")
        print(f"betting strategy: {self.betting_strategy.get_betting_strategy()}, placement strategy: {self.placement_strategy.get_placement_strategy()}")
        print(f"initial and final bankroll: ${self.initial_bankroll}, ${self.current_bankroll}")
        print(f"profit after {self.current_round_number} round is ${self.current_bankroll - self.initial_bankroll}")
