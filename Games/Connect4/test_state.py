from state import *
from interfaces import *

X = Player.PLAYER1
O = Player.PLAYER2

def test_state1():
    position = [
        [X, 0, 0, 0, 0, 0, 0],
        [X, 0, 0, 0, 0, 0, 0],
        [O, 0, 0, 0, 0, 0, 0],
        [X, 0, 0, 0, 0, 0, 0],
        [X, 0, O, 0, 0, 0, 0],
        [X, O, O, O, 0, 0, 0],
    ]

    s = Connect4_State(position)
    assert s.evaluate_state((X, 0, 0)) == Result.ONGOING

def test_state2():
    position = [
        [O, 0, 0, X, 0, 0, 0],
        [O, 0, 0, X, 0, 0, 0],
        [X, 0, X, X, X, O, 0],
        [O, 0, X, O, O, X, 0],
        [O, X, O, O, X, X, O],
        [O, O, X, X, X, O, O],
    ]

    s = Connect4_State(position)
    assert s.evaluate_state((O, 0, 0)) == Result.ONGOING