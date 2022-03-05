"""
MCTS focused on trap detection throughout the game
"""
import copy
from pickle import NONE
from interfaces import *
import interfaces

MAX_INT = float('inf')
MIN_INT = float('-inf')
DEPTH = 3

class MCTS_TRAP_FINDER(Model):
    def execute_strategy(self):
        if interfaces.TURN_NUMBER not in trap_stats:
            trap_stats[interfaces.TURN_NUMBER] = 0
            # Run a minimax to detect traps
            if self.root.state.evaluate_state() == Result.ONGOING:
                if not self.root.children:
                    self.root.expand_node()

                for child in self.root.children:
                    evaluation = self.minimax(child.state, child.last_move, DEPTH, MIN_INT, MAX_INT, child.player_turn)
                    if evaluation == child.player_turn:
                      trap_stats[interfaces.TURN_NUMBER] += 1
                      break


        # SELECTION
        promising_node = self.select_best_child()

        # EXPANSION
        if promising_node.state.evaluate_state() == Result.ONGOING:
            promising_node.expand_node()

        # SIMULATION
        if promising_node.children:
            explore_node = promising_node.get_random_child()
        else:
            explore_node = promising_node
        evaluation = self.simulate(explore_node)

        # BACK PROPAGATION
        self.back_propagate(explore_node, evaluation)

    def select_best_child(self) -> Node:
        best_child = self.root

        while best_child.children:
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
            # simulate_state.print_position()
            player_turn = Player(-player_turn)

        # simulate_state.print_position()
        # print("Finished simulation...")
        return simulate_state.evaluate_state(move)

    def back_propagate(self, node, evaluation) -> Result:
        current_node = node

        while current_node != None:
            if current_node.player_turn == -evaluation:
                # The player who moved into this turn won
                current_node.value += 1
            elif current_node.player_turn == evaluation:
                # The player who moved into this turn lost
                current_node.value -= 1
            
            current_node.visits += 1
            current_node = current_node.parent

    def minimax(self, state, last_move, depth, alpha, beta, player) -> Result:
        """Returns result from minimax"""
        if depth == 0 or state.evaluate_state(last_move) != Result.ONGOING:
            evaluation = state.evaluate_state(last_move)

            return evaluation
        
        if player == Player.PLAYER1:
            max_evaluation = MIN_INT
            for move in state.get_legal_moves(player):
                new_state = copy.deepcopy(state)
                new_state.simulate_move(move)
                evaluation = self.minimax(new_state, move, depth - 1, alpha, beta, Player.PLAYER2)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, max_evaluation)
                if beta <= alpha:
                    break
            # print(f"Max eval is {max_evaluation} for player {player}")
            # state.print_position()
            return max_evaluation
        else:
            min_evaluation = MAX_INT
            for move in state.get_legal_moves(player):
                new_state = copy.deepcopy(state)
                new_state.simulate_move(move)
                evaluation = self.minimax(new_state, move, depth - 1, alpha, beta, Player.PLAYER1)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, min_evaluation)
                if beta <= alpha:
                    break
            # print(f"Min eval is {min_evaluation} for player {player}")
            # state.print_position()
            return min_evaluation