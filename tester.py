from Games.Connect4.state import Connect4_State
from Models.normal import MCTS_NORMAL
from Models.ms_visit import MCTS_MS_VISIT
from interfaces import *

if __name__ == "__main__":
    init_state = Connect4_State(Connect4_State.get_start_position())
    model1 = MCTS_NORMAL(Player.PLAYER1)
    model2 = MCTS_MS_VISIT(Player.PLAYER2)

    resource = TimeResource(60) # Or iteration resource
    # resource = IterationResource(100000)

    # Report based on iteration count

    game_manager = GameManager(init_state, model1, model2)

    result = game_manager.start_game(resource)
    print(result)