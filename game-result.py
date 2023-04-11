from game import Game
from game_state_types import GameStateTypes

class GameResult:
def init(self, game: Game):
self.survivor_percentage = game.get_victory_condition().get_survivor_percentage()
self.survivors = game.get_victory_condition().get_survivors_count()
self.state = game.get_game_state()
self.replay = game.get_command_manager().serialize()
self.duration = game.get_game_timer().get_game_ticks()
