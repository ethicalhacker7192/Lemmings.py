from enum import Enum

class GameStateTypes(Enum):
    UNKNOWN = 0
    RUNNING = 1
    FAILED_OUT_OF_TIME = 2
    FAILED_LESS_LEMMINGS = 3
    SUCCEEDED = 4

class GameStateTypeHelper:
    @staticmethod
    def toString(state_type: GameStateTypes) -> str:
        return state_type.name

    @staticmethod
    def count() -> int:
        return len(GameStateTypes)

    @staticmethod
    def isValid(state_type: GameStateTypes) -> bool:
        return GameStateTypes.UNKNOWN < state_type < GameStateTypes(GameStateTypeHelper.count())

    @staticmethod
    def fromString(type_name: str) -> GameStateTypes:
        type_name = type_name.strip().upper()

        for state_type in GameStateTypes:
            if state_type.name == type_name:
                return state_type

        return GameStateTypes.UNKNOWN
