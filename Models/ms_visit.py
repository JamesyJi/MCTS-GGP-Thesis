"""
MCTS with minimax alpha beta in the selection and expansion phase

Using a visit count threshold as the criteria
"""
import copy
from pickle import NONE
from interfaces import *

MAX_INT = float('inf')
MIN_INT = float('-inf')
N_VISITS = 2
DEPTH = 4

class MCTS_MS_VISIT(Model):
    def execute_strategy(self):
        # SELECTION
        promising_node = self.select_best_child()

        # EXPANSION
        if promising_node.state.evaluate_state() == Result.ONGOING:
            promising_node.expand_node()

        # if promising_node.value == MIN_INT or promising_node.value == MAX_INT:
            # print("Found a forced promising node")
            # promising_node.state.print_position()
            # input()

        # SIMULATION
        if promising_node.children:
            explore_node = promising_node.get_random_child()
        else:
            explore_node = promising_node
        evaluation = self.simulate(explore_node)
        # print(f"Evaluation result is {evaluation} for simulated position which has value {explore_node.value}:")
        # if explore_node.parent:
        #     print(f"parent value is {explore_node.parent.value}")
        #     if explore_node.parent.parent:
        #         print(f"grandparent value is {explore_node.parent.parent.value}")
        # explore_node.state.print_position()

        # BACK PROPAGATION
        self.back_propagate(explore_node, evaluation)


    def select_best_child(self) -> Node:
        """Will run a minimax when we reach a child which meets the visit threshold"""
        best_child = self.root

        while best_child.children:
            if best_child.visits == MIN_INT or best_child.visits == MAX_INT:
                # No need to continue with children when we have a guaranteed result already
                break

            if best_child.visits == N_VISITS:
                # print(f"running minimax...")
                # best_child.state.print_position()
                evaluation = self.minimax(best_child.state, best_child.last_move, DEPTH, MIN_INT, MAX_INT, best_child.player_turn)
                if evaluation == best_child.player_turn:
                    # The player who moved into this turn lost.
                    # print(f"Found a forced win for {best_child.player_turn}")
                    # best_child.state.print_position()
                    # input()
                    best_child.value = MIN_INT
                elif evaluation == -best_child.player_turn:
                    # The player who moved into this turn won
                    # print(f"Found a forced win for {-best_child.player_turn}")
                    # best_child.state.print_position()
                    # input()
                    best_child.value = MAX_INT
                    best_child.parent.value = MIN_INT

            best_child = best_child.get_child_with_highest_score()

        return best_child


    def simulate(self, node: Node) -> Result:
        """Simulate with random move selection policy"""
        simulate_state = copy.deepcopy(node.state)
        player_turn = node.player_turn
        move = node.last_move

        # print("================")
        # print("Simulating...")
        # simulate_state.print_position()
        # print("================")

        while simulate_state.evaluate_state(move) == Result.ONGOING:
            legal_moves = simulate_state.get_legal_moves(player_turn)
            # print(f"legal moves are {legal_moves}")
            move = random.choice(legal_moves)
            # move = random.choice(simulate_state.get_legal_moves(player_turn))
            simulate_state.simulate_move(move)
            player_turn = Player(-player_turn)

        # simulate_state.print_position()
        # print("Finished simulation...")
        return simulate_state.evaluate_state(move)

    def back_propagate(self, node, evaluation) -> Result:
        current_node = node
        while current_node != None:
            if current_node.player_turn == evaluation:
                current_node.value -= 1
            elif current_node.player_turn == -evaluation:
                current_node.value += 1
            
            current_node.visits += 1
            current_node = current_node.parent

    def minimax(self, state, last_move, depth, alpha, beta, player) -> Result:
        """Returns result from minimax"""
        if depth == 0 or state.evaluate_state(last_move) != Result.ONGOING:
            evaluation = state.evaluate_state(last_move)
            # print(f"Reached end. Evaluation is {evaluation} for player {player}")
            # state.print_position()
            return evaluation
            # return state.evaluate_state()
        
        if player == Player.PLAYER1:
            max_evaluation = Result.PLAYER2_WIN
            for move in state.get_legal_moves(player):
                new_state = copy.deepcopy(state)
                new_state.simulate_move(move)
                evaluation = self.minimax(new_state, move, depth - 1, alpha, beta, Player.PLAYER2)

                if evaluation == Result.PLAYER1_WIN:
                    max_evaluation = Result.PLAYER1_WIN
                elif evaluation == Result.DRAW and max_evaluation == Result.PLAYER2_WIN:
                    max_evaluation = Result.DRAW

                alpha = max(alpha, max_evaluation)
                if beta <= alpha:
                    break
            # print(f"Max eval is {max_evaluation} for player {player}")
            # state.print_position()
            return max_evaluation
        else:
            min_evaluation = Result.PLAYER1_WIN
            for move in state.get_legal_moves(player):
                new_state = copy.deepcopy(state)
                new_state.simulate_move(move)
                evaluation = self.minimax(new_state, move, depth - 1, alpha, beta, Player.PLAYER1)

                if evaluation == Result.PLAYER2_WIN:
                    min_evaluation = Result.PLAYER2_WIN
                elif evaluation == Result.DRAW and max_evaluation == Result.PLAYER1_WIN:
                    min_evaluation = Result.DRAW
                
                beta = min(beta, min_evaluation)
                if beta <= alpha:
                    break
            # print(f"Min eval is {min_evaluation} for player {player}")
            # state.print_position()
            return min_evaluation
