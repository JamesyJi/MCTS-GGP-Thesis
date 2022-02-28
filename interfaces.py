from __future__ import annotations
from abc import ABC, abstractmethod
import copy
from enum import IntEnum
import math
from platform import node
import time
from typing import List
from operator import attrgetter
import random

MAX_INT = float('inf')
MIN_INT = float('-inf')

class Player(IntEnum):
    PLAYER1 = 3
    PLAYER2 = -3

class Result(IntEnum):
    PLAYER1_WIN = Player.PLAYER1
    PLAYER2_WIN = Player.PLAYER2
    DRAW = 0
    ONGOING = 1

class Resource(ABC):
    @abstractmethod
    def reset_start(self) -> None:
        pass

    @abstractmethod
    def use_resource(self) -> bool:
        pass

class TimeResource(Resource):
    def __init__(self, limit_sec: int):
        self.limit_sec = limit_sec
        self.end = None

    def reset_start(self) -> None:
        self.end = time.perf_counter() + self.limit_sec

    def use_resource(self) -> bool:
        return time.perf_counter() < self.end

class IterationResource(Resource):
    def __init__(self, limit_iter: int):
        self.limit_iter = limit_iter
        self.cur = 0

    def reset_start(self) -> None:
        self.cur = 0
    
    def use_resource(self) -> bool:
        self.cur += 1
        return self.cur <= self.limit_iter

class State(ABC):
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def evaluate_state(self, last_move=None) -> Result:
        """Evaluates and returns the state of the game"""
        pass

    @abstractmethod
    def get_legal_moves(self, player_turn: Player):
        """Returns a list of legal possible moves"""
        pass

    @abstractmethod
    def make_move(self, move) -> State:
        """Makes a move, returning a copy of the state. Assumes the given move is legal"""
        pass

    @abstractmethod
    def simulate_move(self, move) -> None:
        """Makes a move, modifying the state itself. Assumes the given move is legal"""
        pass

    @abstractmethod
    def get_start_position() -> State:
        """Returns an instance of the starting position for the game"""
        pass

    @abstractmethod
    def print_position(self) -> None:
        "Prints the current position of the state"
        pass

class Node:
    def __init__(self, state: State, player_turn: Player, parent=None, last_move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0
        self.last_move = last_move
        self.player_turn = player_turn

    def get_random_child(self):
        return random.choice(self.children)

    def get_most_visited_child(self):
        return max(self.children, key=attrgetter("value"))        

    def expand_node(self):
        """Expands the node, adding all the legal possible nodes as children"""
        legal_moves = self.state.get_legal_moves(self.player_turn)

        for move in legal_moves:
            self.children.append(Node(self.state.make_move(move), Player(-self.player_turn), self, move))

    def get_child_with_highest_score(self):
        """Returns the child with the highest node score"""
        return max(self.children, key=lambda c : c.get_node_score(MAX_INT))

    def get_child_with_most_visits(self):
        """Returns the child with the most visits"""
        return max(self.children, key=lambda c : c.visits)

    def get_node_score(self, default=MAX_INT):
        """Returns the score of this node"""
        if self.visits == 0:
            return default
        else:
            return (self.value/self.visits + 1.41 * math.sqrt(math.log(self.parent.visits)/self.visits))

    def get_child(self, opponent_move) -> Node:
        """Returns the child node after the given move or creates it if it doesn't exist"""
        print(f"Getting child based on move {opponent_move}")
        child_node = next((child for child in self.children if child.last_move == opponent_move), None)

        if child_node is None:
            # Create the child
            print("Creating child...")
            child_node = Node(self.state.make_move(opponent_move), Player(-self.player_turn), self, opponent_move)

        return child_node


class Model(ABC):
    """Abstract model class for maintaining tree and making game decisions"""
    def __init__(self, player: Player) -> None:
        self.root = None
        self.player = player
    
    def initialise(self, state) -> None:
        self.root = Node(copy.deepcopy(state), Player.PLAYER1)

    def decide_move(self, resource) -> State:
        """Keeps simulating until resource limit is hit and then returns the best
        state to move into"""
        print(f"{self.player} is deciding move...")
        while resource.use_resource():
            self.execute_strategy()

        # Selects the child with the most visits
        # best_node = self.root.get_child_with_most_visits()
        # if self.player is Player.PLAYER1:
        best_node = self.root.get_child_with_highest_score()
        # elif self.player is Player.PLAYER2:
        #     best_node = self.root.get_child_with_lowest_score()


        print(f"new root vists is {best_node.visits} and value is {best_node.value} with score {best_node.get_node_score()}")
        scores = []
        moves = []
        for child in self.root.children:
            # scores.append(child.get_node_score())
            scores.append(child.get_node_score())
            moves.append(child.last_move)
        print(scores)
        print(moves)

        self.root = best_node
        self.root.parent = None

        # print("Looking at children...")
        # for child in self.root.children:
        #     print("============================")
        #     print(f"Visits {child.visits} Value {child.value}")
        #     child.state.print_position()
        #     print("============================")

        print("Finished looking at children...")
        return best_node.last_move


    def notify_of_opponent_move(self, opponent_move) -> None:
        """The opponent has made a move. We will advance the model accordingly"""
        # print(f"{self.player} is getting child")
        # print(f"{self.player} Notified of opponent move {opponent_move}")

        self.root = self.root.get_child(opponent_move)
        self.root.parent = None
        
        # self.root.state.print_position()

    @abstractmethod
    def execute_strategy(self):
        """Executes one iteration of the steps in the strategy"""
        pass

    @abstractmethod
    def select_best_child(self) -> Node:
        """Selects the best child node, dependent on our selection policy"""
        pass

    @abstractmethod
    def simulate(self, node) -> Result:
        """Executes our simulation policy, returning the evaluation at the end"""
        pass

    @abstractmethod
    def back_propagate(self, node, evaluation) -> Result:
        """Backpropagates the simulation result"""
        pass
    
    def back_propagate_proven(self, node, evaluation) -> Result:
        """Backpropagates proven results"""
        if evaluation == Result.ONGOING or Result.DRAW:
            return

        if evaluation == node.player_turn:
            # The player who moved into this turn lost
            node.value = MIN_INT

            node = node.parent
        elif evaluation == -node.player_turn:
            # The player who moved into this turn won
            node.value = MAX_INT
            node.parent.value = MIN_INT

            node = node.parent.parent

        # Try to back propagate everything up the tree
        while node != None:
            # All children must be min_int in order for the node to be a win
            for child in node.children:
                if child.value != MIN_INT:
                    return
            node.value = MAX_INT

            if node.parent:
                # If this is a win, then the prior move must be a loss
                node = node.parent
                node.value = MIN_INT

            node = node.parent



class GameManager():
    def __init__(self, state: State, model1: Model, model2: Model):
        self.state = state

        model1.initialise(state)
        model2.initialise(state)

        self.player1 = model1
        self.player2 = model2

        self.cur_player = self.player1
        self.opp_player = self.player2
        
    def start_game(self, resource: Resource) -> Result:
        """Starts the game between the 2 players and continues until it has been decided.
        A result is returned indicating the outcome"""
        move = None
        while self.state.evaluate_state(move) is Result.ONGOING:
            resource.reset_start()
            move = self.cur_player.decide_move(resource)

            self.opp_player.notify_of_opponent_move(move)

            self.state.simulate_move(move)

            self.cur_player, self.opp_player = self.opp_player, self.cur_player
            print("=========================")
            self.state.print_position()
            print("=========================")



        return self.state.evaluate_state(move)