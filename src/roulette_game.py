# One Roulette Play

from player import Player
from roulette_wheel import RouletteWheel

class RouletteGame:
    def __init__(self, players):
        self.players = players

    def setup_game(self, players, wheel):
        """Plays the game for a set number of rounds."""
        for player in players:
            player.place_bet(wheel)
                
    def play_game(self, wheel):
        result = wheel.spin()
        print("Roulette outcome:", result)

        return result

    def payout_game(self, players, wheel):
        " Calculates payout for players "
        for player in self.players:
            player.payout(wheel)

    def adjust_game(self, players, wheel):
        " Adjust betting money according to game result"
        for player in self.players:
            player.adjust_bet_money(wheel)

    def settle_game(self, players):
        num_players = 0
        for player in players:
            if player.is_ending_condition() == False:    
                num_players += 1
            """
            if player.is_max_round():
                print(f"{player.name} reaches the maximum round.")
            elif player.is_bankrupt():
                print(f"{player.name} is out of money.")
            elif player.is_lack_of_betting_money():
                print(f"{player.name} is lack of money.")
            elif player.is_double_profit():
                print(f"{player.name} achieves double profit.")
            else:
                print(f"{player.name} can continue game.")
                num_players += 1
            """
        if num_players > 0:
            return True
        else:
            return False

    def get_game_result(self, players):
        for player in players:
            player.get_report()
