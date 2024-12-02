# One Roulette Play

from player import Player
from roulette_wheel import RouletteWheel

class RouletteGame:
    def __init__(self, players):
        self.players = players

    def setup_game(self, players):
        """Plays the game for a set number of rounds."""
        for player in players:
            if player.is_bankrupt():
                print(f"{player.name} is out of money.")
            else:
                player.place_bet()
                
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
