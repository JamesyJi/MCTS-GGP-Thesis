from Games.Connect4.state import Connect4_State
from Models.normal import MCTS_NORMAL
from Models.ms_visit import MCTS_MS_VISIT
from interfaces import *

X = Player.PLAYER1
O = Player.PLAYER2

if __name__ == "__main__":
    init_state = Connect4_State(Connect4_State.get_start_position())
    model1 = MCTS_MS_VISIT(Player.PLAYER1)
    model2 = MCTS_MS_VISIT(Player.PLAYER2)

    # resource = TimeResource(5) # Or iteration resource
    resource = IterationResource(10000)

    # Report based on iteration count

    # pos = [
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, X, X, O, 0, 0],
    #     [0, 0, O, X, O, 0, 0],
    #     [0, O, O, O, X, 0, 0],
    #     [0, X, X, O, O, O, X],
    #     [0, X, O, X, O, X, X],
    # ]
    # init_state = Connect4_State(pos)
    
    game_manager = GameManager(init_state, model1, model2)

    result = game_manager.start_game(resource)
    print(result)