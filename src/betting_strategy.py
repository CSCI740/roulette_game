# Betting Strategy

#import random  # for testing
from constants import Bet_Strategy  # Import Bet_Strategy enum

class Betting:
    def __init__(self, initial_bet, strategy):
        self.initial_bet = initial_bet
        #self.current_money = 50  # Default bankroll - comment it out, just for testing
        self.strategy = strategy
        self.fibonacci_sequence = [1, 1]  # Start the Fibonacci sequence
        self.fibonacci_index = 0
        self.current_bet = initial_bet  # For Martingale, D'Alembert, and Flat tracking


    # def play(self):
    #     """
    #     Simulates the game until the player runs out of money and returns the current bet amount
    #     after each round.
    #     """
    #     current_money = self.current_money  # Use initial money value
    #
    #     while current_money > 0:
    #         bet_amount = self.init_bet_money(current_money)  # Get the current bet amount
    #
    #         if bet_amount > current_money:
    #             print(f"I am in play...Game over! You don't have enough money to place the next bet. Current Money: ${current_money:.2f}")
    #             break  # End the game if the bet exceeds the available money
    #
    #         outcome = self.simulate_round()  # Simulate the round
    #
    #         if outcome:
    #             current_money += bet_amount  # Win: add bet to current money
    #             print(f"Bet: ${bet_amount:.2f}, Win! ,Current Money: ${current_money:.2f}")
    #         else:
    #             current_money -= bet_amount  # Loss: subtract bet from current money
    #             print(f"Bet: ${bet_amount:.2f}, Loss!, Current Money: ${current_money:.2f}")
    #
    #         # Adjust the bet based on the outcome and get the new bet
    #         self.current_bet = self.adjust_bet_money(outcome, current_money)
    #
    #         if current_money <= 0:
    #             print("Game over, you ran out of money.")
    #             break
    #
    #     print(f"Game over! Final Money: ${current_money:.2f}")


    # def simulate_round(self):
    #     """
    #     Simulate the game outcome, assuming a 50% win rate.
    #     Returns True for win and False for loss.
    #     """
    #     return random.random() < 0.5
    #     #return random.random() < 0.2

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
        # elif self.strategy == Bet_Strategy.FIBONACCI:
        #     self.current_bet = self.fibonacci_sequence[self.fibonacci_index]
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
                    self.fibonacci_index -= 2  # Move back two places in the Fibonacci sequence after a win
                else:
                    self.fibonacci_index = 0  # Stay at the first position (no negative index)
            elif self.strategy == Bet_Strategy.MARTINGALE:
                self.current_bet = self.initial_bet  # Reset to initial bet after a win
        else:  # Loss
            if self.strategy == Bet_Strategy.MARTINGALE:
                self.current_bet *= 2  # Double the bet after a loss
            elif self.strategy == Bet_Strategy.DALEMBERT:
                self.current_bet += 1  # Increase the bet by $1 after a loss for D'Alembert
            elif self.strategy == Bet_Strategy.FIBONACCI:
                self.fibonacci_index += 1  # Move to the next number in the Fibonacci sequence

        # Check if the player has enough money to place the bet
        if bankroll < self.current_bet:
            print(f"Game over! You don't have enough money to place the next bet. Current Money: ${bankroll:.2f}")
            return 0  # Return 0 to end the game, as the bet cannot be placed

        return self.current_bet  # Return the adjusted bet amount

    def get_current_bet_money(self):
        """
        Returns the current bet amount.
        """
        return self.current_bet


# if __name__ == "__main__":
#     initial_bet = 10
#
#     print("Choose a strategy: flat, all_in, martingale, dalembert, fibonacci")
#     strategy_input = input("Enter your betting strategy: ").strip().lower()
#
#     # Convert user input to corresponding Bet_Strategy enum
#     strategy_map = {
#         "flat": Bet_Strategy.FLAT,
#         "all_in": Bet_Strategy.ALL_IN,
#         "martingale": Bet_Strategy.MARTINGALE,
#         "dalembert": Bet_Strategy.DALEMBERT,
#         "fibonacci": Bet_Strategy.FIBONACCI
#     }
#
#     strategy = strategy_map.get(strategy_input)
#     if strategy is None:
#         print("Invalid strategy. Please choose from: flat, all_in, martingale, dalembert, fibonacci.")
#     else:
#         betting_game = Betting(initial_bet, strategy)
#         betting_game.play()
