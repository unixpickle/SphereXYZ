from heuristic import Heuristic
import sphere
import sys
from array import array

class Solver(object):
    
    def __init__(self, scramble, heuristic):
        self.scramble = scramble
        self.basis = sphere.Turn.basis()
        self.labels = sphere.Turn.basis_labels()
        self.heuristic = heuristic
    
    def run_depth(self, depth):
        return self.recursive_search([], self.scramble, depth)
    
    def recursive_search(self, sequence, node, depth):
        if len(sequence) == depth:
            if node.m_slice() != array('B', [1] * 16): return False
            if node.s_slice() != array('B', [2] * 16): return False
            if node.tb_pieces() != array('B', [0, 0]): return False
            print("Found solution: " + str(sequence))
            return True
        movesRemaining = depth - len(sequence)
        heuristicValue = self.heuristic.lookup(node)
        if heuristicValue > movesRemaining: return False
        for i in range(0, len(self.basis)):
            label = self.labels[i]
            move = self.basis[i]
            nextNode = move.perform(node)
            nextSequence = sequence + [label]
            solved = self.recursive_search(nextSequence, nextNode, depth)
            if solved: return True
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python solver.py <scramble> <table file>")
        sys.exit(1)
    scramble = sphere.Sphere.parse(sys.argv[1])
    if not scramble:
        print("Invalid scramble.")
        sys.exit(1)
    heuristic = Heuristic(sys.argv[2])
    solver = Solver(scramble, heuristic)
    for i in range(0, 20):
        print("Trying " + str(i) + " move solutions...")
        solved = solver.run_depth(i)
        if solved: break
    heuristic.close()

main()
