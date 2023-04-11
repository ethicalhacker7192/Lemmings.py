from enum import Enum

class GameTypes(Enum):
    UNKNOWN = 0
    LEMMINGS = 1
    OHNO = 2
    XMAS91 = 3
    XMAS92 = 4
    HOLIDAY93 = 5
    HOLIDAY94 = 6

class GameTypesHelper:
    @staticmethod
    def to_string(game_type):
        return GameTypes(game_type).name

    @staticmethod
    def count():
        return len(GameTypes.__members__)

    @staticmethod
    def is_valid(game_type):
        return game_type.value > GameTypes.UNKNOWN.value and game_type.value < GameTypesHelper.count()

    @staticmethod
    def from_string(type_name):
        type_name = type_name.strip().upper()
        for game_type in GameTypes:
            if game_type.name == type_name:
                return game_type
        return GameTypes.UNKNOWN
