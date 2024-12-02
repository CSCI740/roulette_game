# Roulette Constants

from enum import Enum, IntEnum

# Player Type
class PlayerType(IntEnum):
    HIGH_RISK = 0
    MODERATE_RISK = 1
    LOW_RISK = 2

# Betting Strategy
class Bet_Strategy(IntEnum):
    ALL_IN = 0
    MARTINGALE = 1
    FIBONACCI = 2
    DALEMBERT = 3
    FLAT = 4

# Placement Strategy
class Placement_Strategy(IntEnum):
    SINGLE_NUMBER = 0
    DOZENS = 1
    RED_BLACK = 2

# Roulette Wheel
class Roulette_Number(IntEnum):
    ZERO = 0
    DOUBLE_ZERO = 37

class Roulette_Dozen(IntEnum):
    FIRST = 0
    SECOND = 1
    THIRD = 2

class Roulette_Color(IntEnum):
    RED = 0
    BLACK = 1
    GREEN = 2

ROULETTE_COLOR_RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
ROULETTE_COLOR_BLACK = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
ROULETTE_COLOR_GREEN = {0, 37}
