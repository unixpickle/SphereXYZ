"""
The core puzzle solver.
"""

from array import array
import sys

from .sphere import Turn


class Solver(object):
    """
    A depth-first search solver.
    """

    def __init__(self, scramble, heuristic):
        self.scramble = scramble
        self.heuristic = heuristic

        self.basis = Turn.basis()
        self.labels = Turn.basis_labels()

    def run_depth(self, depth):
        """
        Run the search to a certain depth.

        Returns:
          None if a solution is not found, or the solution
            as a list of strings representing the moves.
        """
        return self._recursive_search([], self.scramble, depth)

    def _recursive_search(self, sequence, node, depth):
        if len(sequence) == depth:
            if node.m_slice() != array('B', [1] * 16):
                return None
            if node.s_slice() != array('B', [2] * 16):
                return None
            if node.tb_pieces() != array('B', [0, 0]):
                return None
            return sequence
        moves_remaining = depth - len(sequence)
        if self.heuristic.lookup(node) > moves_remaining:
            return None
        for label, move in zip(self.labels, self.basis):
            next_sequence = sequence + [label]
            next_node = move.perform(node)
            solution = self._recursive_search(next_sequence, next_node, depth)
            if solution is not None:
                return solution
        return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python solver.py <scramble> <table file>")
        sys.exit(1)
