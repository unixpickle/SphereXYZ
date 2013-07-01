import choosemap
import sphere
import sys
import struct
import Queue
from array import array
from copy import copy

class Indexer(object):
    
    def __init__(self, maxDepth):
        self.basis = sphere.Turn.basis()
        self.queue = Queue.Queue()
        self.queue.put((sphere.Sphere(), 0))
        
        self.buffer = array('B')
        self.added = 0
        self.depth = 0
        self.maxDepth = maxDepth
        
        print("initializing cache...")
        self.cache = choosemap.ChoiceCache(14)
        
        # the correct size is (34 choose 16) = 2203961430 bytes
        # we will append 117645 size buffers 18734 times.
        print("initializing buffer")
        appendArray = array('B', [255] * 117645)
        for i in xrange(0, 18734):
            self.buffer.extend(appendArray)
    
    def has_expanded(self, aSphere):
        flags = []
        for i in range(0, 34):
            flags += [True if aSphere.pieces[i] == 1 else False]
        index = choosemap.Choice(flags).perfect_hash(self.cache)
        value = self.buffer[index]
        if value == 255: return False
        return True

    def step(self):
        if self.queue.empty():
            return False
        node, depth = self.queue.get()
        
        self.depth = depth
        # set the value in the pruning table
        flags = []
        for i in range(0, 34):
            flags += [True if node.pieces[i] == 1 else False]
        index = choosemap.Choice(flags).perfect_hash(self.cache)
        if self.buffer[index] != 255: return True
        else: self.buffer[index] = depth
        
        self.added += 1
        
        if depth == self.maxDepth: return True
        
        # expand the node by applying all Turns in our basis
        dest = sphere.Sphere()
        for turn in self.basis:
            self.queue.put((turn.perform(node), depth + 1))
        
        return True
    
    def save(self, filename):
        f = open(filename, 'wb')
        f.write(struct.pack('<H', self.maxDepth))
        self.buffer.tofile(f)
        f.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python indexer.py <output> <max depth>")
        sys.exit(1)
    
    indexer = Indexer(int(sys.argv[2]))
    while indexer.step():
        if not indexer.added % 100:
            status = "Expanded %(added)d nodes, depth = %(depth)d." % \
                {'added': indexer.added, 'depth': indexer.depth}
            print(status)
    print("Saving...")
    indexer.save(sys.argv[1])

main()
