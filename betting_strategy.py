import random

class BettingStrategy:
    def __init__(self, initial_bankroll, bet_amount, bet_placement, max_rounds, bet_types):
        if bet_placement not in bet_types:
            raise ValueError(f"Invalid bet type: {bet_placement}. Valid types: {list(bet_types.keys())}")

        self.initial_bankroll = initial_bankroll
        self.bet_amount = bet_amount  # Fixed bet amount for flat betting
        self.bet_placement = bet_placement
        self.max_rounds = max_rounds
        self.bet_types = bet_types

        # Extract win probability and payout ratio
        self.win_probability = bet_types[bet_placement]["win_probability"]
        self.payout_ratio = bet_types[bet_placement]["payout_ratio"]

        self.bankroll = initial_bankroll
        self.rounds_played = 0
        self.target_bankroll = initial_bankroll * 2  # Stop when bankroll doubles

    def simulate_round(self, bet_amount):
        """
        Simulates a single round of betting.
        """
        self.rounds_played += 1
        outcome_probability = random.random()  # Random number between 0 and 1

        # Win
        if outcome_probability < self.win_probability:
            self.bankroll -= bet_amount  # Deduct bet amount first
            self.bankroll += bet_amount * self.payout_ratio  # Add winnings
            print(f"Round {self.rounds_played}: Win! Bankroll: ${self.bankroll:.2f}")
        else:
            # Lose
            self.bankroll -= bet_amount  # Deduct entire bet amount
            print(f"Round {self.rounds_played}: Lose. Bankroll: ${self.bankroll:.2f}")

    def flat_betting(self):
        """
        Implements the flat betting strategy.
        """
        while self.rounds_played < self.max_rounds:
            if self.bankroll < self.bet_amount:
                print(f"Round {self.rounds_played}: Bankrupt! Bankroll: ${self.bankroll:.2f}")
                break

            self.simulate_round(self.bet_amount)

            if self.bankroll >= self.target_bankroll:
                print(f"Round {self.rounds_played}: Target reached! Bankroll: ${self.bankroll:.2f}")
                break

        status = self.determine_status(self.bet_amount)
        return self.result_summary(status)

    def all_in_betting(self):
        """
        Implements the all-in betting strategy.
        """
        while self.rounds_played < self.max_rounds:
            if self.bankroll <= 0:
                print(f"Round {self.rounds_played}: Bankrupt! Bankroll: $0.00")
                break

            self.simulate_round(self.bankroll)  # Bet the entire bankroll, as All-in betting

            if self.bankroll >= self.target_bankroll:
                print(f"Round {self.rounds_played}: Target reached! Bankroll: ${self.bankroll:.2f}")
                break

        status = self.determine_status(0)
        return self.result_summary(status)



    def dalembert_betting(self):
        """
        Increase bet by $1 after a loss and decrease by $1 after a win.
        """
        current_bet = self.bet_amount  # Start with the initial bet amount
        last_round_was_win = False  # Keep track of the last round outcome

        while self.rounds_played < self.max_rounds:
            if self.bankroll < current_bet or current_bet <= 0:
                print(f"Round {self.rounds_played}: Bankrupt or invalid bet! Bankroll: ${self.bankroll:.2f}")
                break

            # Record bankroll before the round to determine the outcome
            pre_round_bankroll = self.bankroll

            # Simulate the round with the current bet
            self.simulate_round(current_bet)

            # Determine the outcome of the round
            if self.bankroll > pre_round_bankroll:  # Win
                last_round_was_win = True
                current_bet = max(1, current_bet - 1)  # Decrease bet, ensure it's at least $1
            else:  # Loss
                last_round_was_win = False
                current_bet += 1  # Increase bet

            if self.bankroll >= self.target_bankroll:
                print(f"Round {self.rounds_played}: Target reached! Bankroll: ${self.bankroll:.2f}")
                break

        status = self.determine_status(current_bet)
        return self.result_summary(status)


    def martingale_betting(self):
        """
        Double the bet amount after a loss to recover losses, and resets it to the initial bet amount after a win.
        """
        current_bet = self.bet_amount  # Start with the initial bet amount

        while self.rounds_played < self.max_rounds:
            if self.bankroll < current_bet:
                print(f"Round {self.rounds_played}: Bankrupt! Bankroll: ${self.bankroll:.2f}")
                break

            # Record bankroll before the round to determine the outcome
            pre_round_bankroll = self.bankroll

            # Simulate the round with the current bet
            self.simulate_round(current_bet)

            # Determine the outcome of the round
            if self.bankroll > pre_round_bankroll:  # Win
                current_bet = self.bet_amount  # Reset bet to the initial amount
            else:  # Loss
                current_bet *= 2  # Double the bet amount

            # Check if the target bankroll is reached
            if self.bankroll >= self.target_bankroll:
                print(f"Round {self.rounds_played}: Target reached! Bankroll: ${self.bankroll:.2f}")
                break

        status = self.determine_status(current_bet)
        return self.result_summary(status)

    def fibonacci_betting(self):
        """
        Start with a stake of $1, following the Fibonacci sequence.
        Move back two places in the sequence after a win, and proceed to the next number after a loss.
        """
        fibonacci_sequence = [1, 1]  # Start with the first two numbers in the Fibonacci sequence
        current_index = 0  # Track the current position in the sequence

        while self.rounds_played < self.max_rounds:
            # Check if bankroll is insufficient for the bet
            if self.bankroll < fibonacci_sequence[current_index]:
                print(f"Round {self.rounds_played}: Bankrupt or insufficient bankroll! Bankroll: ${self.bankroll:.2f}")
                break

            # Record bankroll before the round to determine the outcome
            pre_round_bankroll = self.bankroll

            # Simulate the round with the current bet
            self.simulate_round(fibonacci_sequence[current_index])

            # Determine the outcome of the round
            if self.bankroll > pre_round_bankroll:  # Win
                # Move back two places in the Fibonacci sequence (or reset to the start)
                current_index = max(0, current_index - 2)
            else:  # Loss
                # Move to the next number in the Fibonacci sequence
                current_index += 1
                # Extend the Fibonacci sequence if necessary
                if current_index == len(fibonacci_sequence):
                    fibonacci_sequence.append(fibonacci_sequence[-1] + fibonacci_sequence[-2])

            # Check if the target bankroll is reached
            if self.bankroll >= self.target_bankroll:
                print(f"Round {self.rounds_played}: Target reached! Bankroll: ${self.bankroll:.2f}")
                break

        status = self.determine_status(fibonacci_sequence[current_index] if current_index < len(fibonacci_sequence) else 0)
        return self.result_summary(status)





    def determine_status(self, bet_amount):
        """
        Determines the final status of the betting session.
        """
        if self.bankroll < bet_amount:
            return "bankrupt"
        elif self.bankroll >= self.target_bankroll:
            return "target met"
        else:
            return "max rounds reached"

    def result_summary(self, status):
        """
        Returns a summary of the betting results.
        """
        return {
            "final_bankroll": self.bankroll,
            "rounds_played": self.rounds_played,
            "status": status
        }


if __name__ == "__main__":
    # Define payout ratios and win probabilities for different bet types
    BET_TYPES = {
        "single_number": {"win_probability": 1/38, "payout_ratio": 36},  # Single number bet
        "dozen": {"win_probability": 12/38, "payout_ratio": 3},         # Dozen bet
        "color": {"win_probability": 18/38, "payout_ratio": 2},         # Black/Red bet
        "green": {"win_probability": 2/38, "payout_ratio": 18},         # Green bet
    }

    # Instantiate the betting strategy class
    betting_strategy = BettingStrategy(
        initial_bankroll=100,
        bet_amount=1,  # Fixed bet amount
        bet_placement="dozen",  # Change this to 'single_number', 'color', or 'green' for different bets
        max_rounds=10,
        bet_types=BET_TYPES
    )

    # Test the flat betting strategy
    # result_flat_bet = betting_strategy.flat_betting()
    # print(result_flat_bet)

    # Test the all-in betting strategy
    # result_all_in = betting_strategy.all_in_betting()
    # print(result_all_in)

    # Test the D'Alembert betting strategy
    # result_dalembert = betting_strategy.dalembert_betting()
    # print(result_dalembert)

    # Test the Martingale betting strategy
    # result_martingale = betting_strategy.martingale_betting()
    # print(result_martingale)

    # Test the Fibonacci betting strategy
    result_fibonacci = betting_strategy.fibonacci_betting()
    print(result_fibonacci)

