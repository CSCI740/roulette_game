# Placement Strategy

from constants import Placement_Strategy
from constants import Roulette_Number, Roulette_Dozen, Roulette_Color
from constants import ROULETTE_COLOR_RED, ROULETTE_COLOR_BLACK, ROULETTE_COLOR_GREEN

class PlacementStrategy:
    def __init__(self, placementStrategy):
        self.placementStrategy = placementStrategy
        self.bet = None

    def place_bet(self, bet):
        self.bet = bet

    def is_winning_place(self, rouletteNumber) -> bool:
        if self.placementStrategy == Placement_Strategy.SINGLE_NUMBER:
            return self.is_winning_number(rouletteNumber)
        elif self.placementStrategy == Placement_Strategy.DOZENS:
            return self.is_winning_dozen(rouletteNumber)
        elif self.placementStrategy == Placement_Strategy.RED_BLACK:
            return self.is_winning_red_black(rouletteNumber)
        else :
            print("Unknown Placement Strategy")

    def is_winning_number(self, rouletteNumber) -> bool:
        if rouletteNumber == self.bet:
            return True
        else:
            return False

    def is_winning_dozen(self, rouletteNumber) -> bool:
        if rouletteNumber == Roulette_Number.ZERO or rouletteNumber == Roulette_Number.DOUBLE_ZERO:
            return False
        if (rouletteNumber - 1) // 12 == self.bet:
            return True
        else:
            return False 

    def is_winning_red_black(self, rouletteNumber) -> bool:
        if self.bet == Roulette_Color.RED:          # 0: RED
            if rouletteNumber in ROULETTE_COLOR_RED:
                return True
            else:
                return False
        elif self.bet == Roulette_Color.BLACK:      # 1: BLACK
            if rouletteNumber in ROULETTE_COLOR_BLACK:
                return True
            else:
                return False

        return False

    def payout(self, bet_money):
        payout_money = 0
        if self.placementStrategy == Placement_Strategy.SINGLE_NUMBER:
            payout_money = bet_money * 36       
        elif self.placementStrategy == Placement_Strategy.DOZENS:
            payout_money = bet_money * 3
        elif self.placementStrategy == Placement_Strategy.RED_BLACK:
            payout_money = bet_money * 2
        else:
            print("Unknown placement strategy")

        return payout_money
