import choosemap
import struct

class Heuristic(object):
    """ Performs lookups and loads from a pruning table """
    
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        depthBuff = self.file.read(2)
        assert len(depthBuff) == 2
        self.maxDepth = struct.unpack('<H', depthBuff)[0]
    
    def close(self):
        self.file.close()
    
    def lookup(self, sphere):
        """ Find the heuristic value for a sphere """
        mChoice = self.sphere_m_choice(sphere)
        sChoice = self.sphere_s_choice(sphere)
        value1 = self.lookup_choice(mChoice)
        if value1 > self.maxDepth: return value1
        value2 = self.lookup_choice(sChoice)
        if value1 > value2: return value1
        else: return value2
        
    def lookup_choice(self, choice):
        """ Find the heuristic value for a color permutation (34 choose 16) """
        index = 2 + choice.perfect_hash()
        self.file.seek(index)
        value = self.file.read(1)
        if ord(value) == 255: return self.maxDepth + 1
        assert ord(value) <= self.maxDepth
        return ord(value)
    
    def sphere_m_choice(self, sphere):
        flags = []
        for i in sphere.pieces:
            flags += [True if i == 1 else False]
        return choosemap.Choice(flags)
    
    def sphere_s_choice(self, sphere):
        flags = []
        rotated = sphere.s_slice() + sphere.m_slice() + sphere.tb_pieces()
        for i in rotated:
            flags += [True if i == 2 else False]
        return choosemap.Choice(flags)
    