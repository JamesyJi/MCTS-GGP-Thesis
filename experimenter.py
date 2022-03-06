"""
Used for self-play
"""
from Games.Connect4.state import Connect4_State
from Models.normal import MCTS_NORMAL
from Models.ms_visit import MCTS_MS_VISIT
from Models.trap_finder import MCTS_TRAP_FINDER
from interfaces import *

X = Player.PLAYER1
O = Player.PLAYER2

if __name__ == "__main__":
    init_state = Connect4_State(Connect4_State.get_start_position())
    model1 = MCTS_TRAP_FINDER(Player.PLAYER1)
    # model2 = model1

    # resource = TimeResource(5) # Or iteration resource
    resource = IterationResource(100000)

    game_manager = GameManager(init_state, model1, model1)

    result = game_manager.start_game(resource, 50)
    print(result)