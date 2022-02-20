import copy
from enum import Enum
from queue import Empty
from interfaces import Player, Result, State
from colorama import Fore, Style

"""
PLAYER1 : 1
PLAYER2 : -1
Empty is 0. Board size is 6 high, 7 wide
    0,0 top left.
    5,6 bottom right.

Moves are defined by: (x, y, z) where:
    x : player 1 or -1
    y : row index (0 - 5)
    z : column index (0 - 6)
"""

EMPTY = 0

class Connect4_State(State):        
    def evaluate_state(self, last_move=None) -> Result:
        """
        Evaluation is much more efficient if we know the last made move        
        """
        # print(f"Evaluation of last_move {last_move}")
        # print(self.position)
        # self.print_position()

        if last_move == None:
            return Result.ONGOING

        player = last_move[0]
        row = last_move[1]
        col = last_move[2]

        win_counter = 0
        for c in self.position[row]:
            if c == player:
                win_counter += 1
                if win_counter == 4:
                    return Result(player)
            else:
                win_counter = 0
        
        win_counter = 0
        for r in self.position:
            if r[col] == player:
                win_counter += 1
                if win_counter == 4:
                    return Result(player)
            else:
                win_counter = 0

        win_counter = 0
        # Check topleft - bottomright diagonal
        offset = min(row, col)
        i = row - offset
        j = col - offset
        while i < 6 and j < 7:
            if self.position[i][j] == player:
                win_counter += 1
                if win_counter == 4:
                    return Result(player)
            else:
                win_counter = 0
            i += 1
            j += 1
        
        win_counter = 0
        # Check bottomleft - topright diagonal
        offset = min(5 - row, col)
        i = row + offset
        j = col - offset
        while i < 6 and j < 7:
            if self.position[i][j] == player:
                win_counter += 1
                if win_counter == 4:
                    return Result(player)
            else:
                win_counter = 0
            i -= 1
            j += 1

        # Game is still ongoing or a draw
        if row == 0:
            if EMPTY not in self.position[row]:
                return Result.DRAW 

        # print("Ongoing")
        return Result.ONGOING        

    def get_legal_moves(self, player_turn: Player):
        legal_moves = []

        # For each column, find the lowest row
        row = 5
        col = 0
        while col < 7:
            while row >= 0:
                if self.position[row][col] == EMPTY:
                    legal_moves.append((player_turn, row, col))
                    break
                row -= 1
            col += 1
            row = 5
        
        return legal_moves

    def make_move(self, move) -> State:
        new_state = copy.deepcopy(self)

        new_state.position[move[1]][move[2]] = move[0]

        return new_state
    
    def simulate_move(self, move) -> None:
        # print(f"Simulating move {move}")
        self.position[move[1]][move[2]] = move[0]

    def get_start_position():
        col = [0, 0, 0, 0, 0, 0, 0]
        board = [col[:] for row in range(6)]
        return board

    def print_position(self) -> None:
        for row in self.position:
            for col in row:
                if col == Player.PLAYER1:
                    print(f"{Fore.BLUE}X{Style.RESET_ALL}", end="")
                elif col == Player.PLAYER2:
                    print(f"{Fore.RED}O{Style.RESET_ALL}", end="")
                else:
                    print("?",end="")
                print(" | ", end="")
            print("")