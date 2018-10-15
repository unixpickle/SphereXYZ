"""
Generating heuristic tables.
"""

from array import array
import struct
from queue import Queue

from .choosemap import ChoiceCache
from .heuristic import sphere_m_choice
from .sphere import Sphere, Turn


class Indexer(object):
    """
    A BFS for building a heuristic pruning table.
    """

    def __init__(self, max_depth):
        self.max_depth = max_depth

        self.basis = Turn.basis()
        self.queue = Queue()
        self.queue.put((Sphere(), 0))

        self.buffer = array('B')
        self.added = 0
        self.depth = 0

        self.cache = ChoiceCache(14)

        # Not entirely sure why, but this builds up
        # (34 choose 16) bytes as 117645 * 18734.
        append_array = array('B', [255] * 117645)
        for i in range(18734):
            self.buffer.extend(append_array)

    def step(self):
        """
        Run a step of the search.

        Returns:
          True if the search is continuing, or False if it
            has completed.
        """
        if self.queue.empty():
            return False
        node, depth = self.queue.get()

        self.depth = depth
        index = sphere_m_choice(node).perfect_hash(self.cache)
        if self.buffer[index] != 255:
            return True

        self.buffer[index] = depth
        self.added += 1

        if depth < self.max_depth:
            for turn in self.basis:
                self.queue.put((turn.perform(node), depth + 1))

        return True

    def save(self, filename):
        f = open(filename, 'wb')
        f.write(struct.pack('<H', self.max_depth))
        self.buffer.tofile(f)
        f.close()
