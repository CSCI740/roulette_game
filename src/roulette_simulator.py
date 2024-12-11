# Game Simulation

from player import Player
from roulette_wheel import RouletteWheel
from roulette_game import RouletteGame
from roulette_simulation_report import SimulationReport 

class RouletteSimulator:
    def __init__(self, players, wheel):
        self.players = players
        self.rounds = 10

        self.game = RouletteGame(self.players)        
        #self.wheel = RouletteWheel()
        self.wheel = wheel
        self.report = SimulationReport()  
             
    def play_roulette(self, roundCount = 10):
        """Plays the game for a set number of rounds."""

        self.rounds = roundCount

        for round_number in range(self.rounds):
            print(f"\n--- {round_number+1} Round ---")
            self.game.setup_game(self.players, self.wheel)
            
            self.game.play_game(self.wheel)
            
            self.game.payout_game(self.players, self.wheel)
            self.game.adjust_game(self.players, self.wheel)
            
            if self.game.settle_game(self.players) == False:
                print(f"\n--- Game ends ---")
                print(f"There is no player.")
                break
    def show_results(self):
        """ Displays the final results of the simulation. """
        # Add house profit to the report
        house_profit = self.wheel.report_house_profit()
        self.report.set_house_profit(house_profit)

        # Add each player's performance to the report
        for player in self.players:
            self.report.add_player_report(player)

        # Generate and display the report
        self.report.generate_report()