# Betting Strategy

from constants import Bet_Strategy

class BettingStrategy:
    def __init__(self, bet_strategy):
        self.bet_strategy = bet_strategy

        self.current_bet = 1
        self.previous_bet = 1               # for Fibonacci strategy

    def init_bet_money(self, bankroll):
        """Adjusts the bet based on the outcome (win/loss)."""
        if self.bet_strategy == Bet_Strategy.ALL_IN:
            # Bet the entire bankroll
            next_bet = bankroll
        else:
            next_bet = self.current_bet

        self.previous_bet = self.current_bet
        self.current_bet = next_bet

        return self.current_bet

    def adjust_bet_money(self, is_win, bankroll):
        """Adjusts the bet based on the outcome (win/loss)."""
        if self.bet_strategy == Bet_Strategy.ALL_IN:
            # Bet the entire bankroll
            next_bet = bankroll
        elif self.bet_strategy == Bet_Strategy.MARTINGALE:
            # Double the bet after loss
            if is_win:
                next_bet = self.current_bet
            else:
                next_bet = self.current_bet + self.current_bet  
        elif self.bet_strategy == Bet_Strategy.FIBONACCI:
            # Use the Fibonacci sequence to determine bets after loss
            if is_win:
                next_bet = self.current_bet
            else:
                next_bet = self.previous_bet + self.current_bet
        elif self.bet_strategy == Bet_Strategy.DALEMBERT:
            # Increase the bet by 1 unit after a loss and descrease by 1 unit after a win
            if is_win:
                if self.current_bet > 1:
                    # current_bet should be greater than 1 unit. 
                    next_bet = self.current_bet - 1
                else:
                    next_bet = self.current_bet
            else:
                next_bet = self.current_bet + 1   
        elif self.bet_strategy == Bet_Strategy.FLAT:
            # Bet the same fixed amount on every spin, regardless of wins or losses    
            next_bet = self.current_bet
        else:
            print("Unknown betting strategy")

        if next_bet > bankroll:
            next_bet = bankroll

        self.previous_bet = self.current_bet
        self.current_bet = next_bet

        return self.current_bet
