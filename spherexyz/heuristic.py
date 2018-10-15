"""
Search heuristics that store lower bounds for the number
of moves to solve a state.
"""

import struct

from .choosemap import Choice


class Heuristic(object):
    """
    A pruning table, which maps states to moves.
    """

    def __init__(self, filename):
        self.file = open(filename, 'rb')
        depth_buf = self.file.read(2)
        assert len(depth_buf) == 2
        self.max_depth = struct.unpack('<H', depth_buf)[0]

    def close(self):
        self.file.close()

    def lookup(self, sphere):
        """
        Find the move lower bound for a Sphere.
        """
        m_choice = sphere_m_choice(sphere)
        value1 = self.lookup_choice(m_choice)
        if value1 > self.max_depth:
            return value1
        s_choice = sphere_s_choice(sphere)
        value2 = self.lookup_choice(s_choice)
        return max(value1, value2)

    def lookup_choice(self, choice):
        """
        Find the heuristic value for a M/S color Choice,
        which has (34 choose 16) possibilities.
        """
        index = 2 + choice.perfect_hash()
        self.file.seek(index)
        value = self.file.read(1)[0]
        if value == 255:
            return self.max_depth + 1
        assert value <= self.max_depth
        return value


def sphere_m_choice(sphere):
    return Choice([p == 1 for p in sphere.pieces])


def sphere_s_choice(sphere):
    rotated = sphere.s_slice() + sphere.m_slice() + sphere.tb_pieces()
    return Choice([p == 2 for p in rotated])
