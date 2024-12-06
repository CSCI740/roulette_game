from constants import Bet_Strategy  # Import Bet_Strategy enum


class BettingStrategy:
    def __init__(self, strategy, initial_bet):
        self.initial_bet = initial_bet
        self.strategy = strategy
        self.fibonacci_sequence = [1, 1]  # Start the Fibonacci sequence
        self.fibonacci_index = 0
        self.current_bet = initial_bet  # For Martingale, D'Alembert, and Flat tracking


    

    def init_bet_money(self, bankroll):
        """
        Initializes the bet amount for the current round based on the strategy and bankroll.
        """
        if self.strategy == Bet_Strategy.FLAT:
            self.current_bet = self.initial_bet
        elif self.strategy == Bet_Strategy.ALL_IN:
            self.current_bet = bankroll  # Bet the entire bankroll
        elif self.strategy == Bet_Strategy.MARTINGALE:
            self.current_bet = self.current_bet if bankroll >= self.current_bet else bankroll  # Ensure bet is within bankroll
        elif self.strategy == Bet_Strategy.DALEMBERT:
            self.current_bet = self.current_bet  # For D'Alembert, this is based on the previous bet
        elif self.strategy == Bet_Strategy.FIBONACCI:
            # Ensure the Fibonacci sequence has enough numbers for the current index
            while len(self.fibonacci_sequence) <= self.fibonacci_index:
                next_fib = self.fibonacci_sequence[-1] + self.fibonacci_sequence[-2]  # Fibonacci rule
                self.fibonacci_sequence.append(next_fib)
            self.current_bet = self.fibonacci_sequence[self.fibonacci_index]
        else:
            raise ValueError("Invalid betting strategy")

        return self.current_bet


    def adjust_bet_money(self, is_win, bankroll):
        """
        Adjusts the bet amount based on the outcome and strategy.
        Returns the adjusted bet amount.
        """
        if is_win:  # Win
            if self.strategy == Bet_Strategy.DALEMBERT:
                self.current_bet = max(1, self.current_bet - 1)  # Decrease by $1 after a win for D'Alembert
            

            elif self.strategy == Bet_Strategy.FIBONACCI:
                if self.fibonacci_index > 1:
                    self.fibonacci_index -= 2  # Move back two places in the Fibonacci sequence
                else:
                    self.fibonacci_index = 0  # Stay at the first position (no negative index)
                # Update the current bet based on the Fibonacci index
                self.current_bet = self.fibonacci_sequence[self.fibonacci_index]


            elif self.strategy == Bet_Strategy.MARTINGALE:
                self.current_bet = self.initial_bet  # Reset to initial bet after a win

        else:  # Loss
            if self.strategy == Bet_Strategy.MARTINGALE:
                self.current_bet *= 2  # Double the bet after a loss
            elif self.strategy == Bet_Strategy.DALEMBERT:
                self.current_bet += 1  # Increase the bet by $1 after a loss for D'Alembert
            elif self.strategy == Bet_Strategy.FIBONACCI:
                self.fibonacci_index += 1  # Move to the next number in the Fibonacci sequence
                # Ensure the Fibonacci sequence has enough numbers for the current index
                while len(self.fibonacci_sequence) <= self.fibonacci_index:
                    next_fib = self.fibonacci_sequence[-1] + self.fibonacci_sequence[-2]  # Fibonacci rule
                    self.fibonacci_sequence.append(next_fib)
                # Update the current bet based on the Fibonacci index
                self.current_bet = self.fibonacci_sequence[self.fibonacci_index]


        # Check if the player has enough money to place the bet
        if bankroll < self.current_bet:
            #print(f"Game over! You don't have enough money to place the next bet. Current Money: ${bankroll:.2f}")
            return 0  # Return 0 to end the game, as the bet cannot be placed

        return self.current_bet  # Return the adjusted bet amount


    def get_current_bet_money(self):
        """
        Returns the current bet amount.
        """
        return self.current_bet

    def get_betting_strategy(self):
        return self.strategy
