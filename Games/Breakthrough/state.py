import copy

from interfaces import Player, Result, State
from colorama import Fore, Style

"""
PLAYER2 : -1 (starts at top)
PLAYER1 : 1 (starts at bottom)
Empty is 0. Board size is 7x7
0,0 top left
6,6 bottom right

Moves are defined by: (x, y1, y2, z1, z2) where:
    x : player who made this move
    y1 : row index before move (0 - 6)
    y2 : row index after move (0 - 6)
    z1 : col index before move (0 - 6)
    z2 : col index after move (0 - 6)
"""

EMPTY = 0

class Connect4_State(State):
    def evaluate_state(self, last_move=None) -> Result:
        if last_move == None:
            return Result.ONGOING
        
        player = last_move[0]
        prev_row = last_move[1]
        cur_row = last_move[2]
        prev_col = last_move[3]
        cur_col = last_move[4]

        # Determine based on the last move
        if player is Player.PLAYER1 and cur_row == 6:
            return Result.PLAYER1_WIN
        elif player is Player.PLAYER2 and cur_row == 0:
            return Result.PLAYER2_WIN
        
