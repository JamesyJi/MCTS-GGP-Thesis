from Models.ms_visit import MCTS_MS_VISIT
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

def test_state3():
    position = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, X, X, O, 0, 0],
        [0, O, O, X, O, 0, 0],
        [0, O, O, O, X, 0, 0],
        [0, X, X, O, O, O, X],
        [X, X, O, X, O, X, X],
    ]

    s = Connect4_State(position)
    assert s.evaluate_state((O, 2, 1)) == Result.PLAYER2_WIN

def test_state4():
    position = [
        [0, X, 0, O, X, 0, O],
        [0, X, 0, X, O, O, X],
        [0, O, 0, O, O, X, O],
        [O, X, 0, X, X, O, O],
        [X, X, O, O, O, O, X],
        [X, O, X, X, O, X, X],
    ]

    s = Connect4_State(position)
    assert s.evaluate_state((O, 4, 2)) == Result.PLAYER2_WIN

def test_state5():
    position = [
        [0, 0, 0, O, X, 0, O],
        [O, X, 0, X, O, O, X],
        [X, O, 0, O, O, X, O],
        [O, X, 0, X, X, O, O],
        [X, X, X, O, O, O, X],
        [X, O, X, X, O, X, X],
    ]

    s = Connect4_State(position)
    assert s.evaluate_state((X, 4, 2)) == Result.PLAYER1_WIN

def test_forced_win1():
    position = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, O, O, 0, 0, 0],
        [0 ,0 ,X, X, 0, 0, 0]
    ]

    s = Connect4_State(position)
    ms_visit_1 = MCTS_MS_VISIT(Player.PLAYER1)
    assert ms_visit_1.minimax(s, (Player.PLAYER2, 4, 3), 4, MIN_INT, MAX_INT, Player.PLAYER1) == Result.PLAYER1_WIN

def test_forced_loss1():
    position = [
        [0, 0, 0, X, O, 0, 0],
        [0, O, 0, X, X, 0, O],
        [0, X, X, X, O, 0, O],
        [0, X, O, O, O, 0, X],
        [0, O, X, X, X, 0, O],
        [0, X ,O, X, O, 0, O]
    ]

    s = Connect4_State(position)
    ms_visit_1 = MCTS_MS_VISIT(Player.PLAYER1)
    ms_visit_2 = MCTS_MS_VISIT(Player.PLAYER2)
    assert ms_visit_2.minimax(s, (Player.PLAYER2, 1, 6), 4, MIN_INT, MAX_INT, Player.PLAYER1) == Result.ONGOING

def test_forced_loss2():
    position = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, O, 0, O, 0, 0, 0],
        [0, X, 0, X, 0, 0, 0],
        [0, X, X, O, 0, 0, 0],
        [0, O ,X, X, O, 0, 0]
    ]

    s = Connect4_State(position)
    ms_visit_1 = MCTS_MS_VISIT(Player.PLAYER1)
    ms_visit_2 = MCTS_MS_VISIT(Player.PLAYER2)
    assert ms_visit_2.minimax(s, (Player.PLAYER1, 4, 2), 4, MIN_INT, MAX_INT, Player.PLAYER2) == Result.PLAYER2_WIN

def test_forced_loss3():
    position = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, X, X, O, 0, 0],
        [0, 0, O, X, O, 0, 0],
        [0, 0, O, O, X, 0, 0],
        [0, X, X, O, O, O, X],
        [0, X, O, X, O, X, X],
    ]

    s = Connect4_State(position)
    ms_visit_1 = MCTS_MS_VISIT(Player.PLAYER1)
    ms_visit_2 = MCTS_MS_VISIT(Player.PLAYER2)
    assert ms_visit_2.minimax(s, (Player.PLAYER1, 4, 1), 4, MIN_INT, MAX_INT, Player.PLAYER2) == Result.PLAYER2_WIN


def test_equals1():
    position1 = [
        [0, 0, 0, O, X, 0, O],
        [O, X, 0, X, O, O, X],
        [X, O, 0, O, O, X, O],
        [O, X, 0, X, X, O, O],
        [X, X, X, O, O, O, X],
        [X, O, X, X, O, X, X],
    ]

    position2 = [
        [0, 0, 0, O, X, 0, O],
        [O, X, 0, X, O, O, X],
        [X, O, 0, O, O, X, O],
        [O, X, 0, X, X, O, O],
        [X, X, X, O, O, O, X],
        [X, O, X, X, O, X, X],
    ]

    s1 = Connect4_State(position1)
    s2 = Connect4_State(position2)

    assert s1.equals(s2)