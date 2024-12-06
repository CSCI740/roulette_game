from player import Player 
from constants import Bet_Strategy

class SimulationReport:
    def __init__(self):
        self.total_simulation_house_profit = 0
        self.player_reports = []

    def add_player_report(self, player):
        """
        Collects and stores data for a specific player at the end of the simulation
        """
        try:
            # Convert betting_strategy to Bet_Strategy enum if it's an int
            if isinstance(player.betting_strategy.strategy, int):
                strategy_name = Bet_Strategy(player.betting_strategy.strategy).name
            else:
                strategy_name = player.betting_strategy.get_betting_strategy().name

            report = {
                "name": player.name,
                "player_type": player.player_type.name,
                "initial_bankroll": player.get_initial_bankroll(),
                "final_bankroll": player.get_current_bankroll(),
                "total_profit": player.get_current_bankroll() - player.get_initial_bankroll(),
                "rounds_played": player.current_round_number,
                "strategy": strategy_name,
                "placement_strategy": player.placement_strategy.get_placement_strategy().name,
            }

            self.player_reports.append(report)

        except AttributeError as e:
            print(f"Error processing player {player.name}: {e}")

    def set_house_profit(self, profit):
        self.total_simulation_house_profit = profit

    def generate_report(self):
        """
        Generates and prints the final simulation report summarizing the results.
        """
        print("\n--- Simulation Report ---\n")
        print(f"House Total Profit: ${self.total_simulation_house_profit:.2f}\n")

        print("Player Results:")
        if not self.player_reports:
            print("No players participated.")
        for report in self.player_reports:
            print(f"Player: {report['name']} ({report['player_type']})")
            print(f"  - Initial Bankroll: ${report['initial_bankroll']:.2f}")
            print(f"  - Final Bankroll: ${report['final_bankroll']:.2f}")
            print(f"  - Total Profit: ${report['total_profit']:.2f}")
            print(f"  - Rounds Played: {report['rounds_played']}")
            print(f"  - Betting Strategy: {report['strategy']}")
            print(f"  - Placement Strategy: {report['placement_strategy']}\n")

        print("--- End of Report ---")
