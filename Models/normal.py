import copy
from pickle import NONE
from interfaces import *

class MCTS_NORMAL(Model):
    def execute_strategy(self):
        # SELECTION
        promising_node = self.select_best_child()

        # EXPANSION
        if promising_node.state.evaluate_state(promising_node.last_move) == Result.ONGOING:
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
