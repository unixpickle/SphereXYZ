# M slice color = 1, S slice = 2, top-bottom = 0
# M slice is ordered from top going towards the front
# S slice is ordered from top going towards the right
# A U turn is actually a U' on a 3x3x3 Rubik's cube: this is because I'm stupid...

from copy import copy
from array import array

class Sphere(object):
    
    def __init__(self, pieces=None):
        if pieces:
            self.pieces = pieces
        else:
            ident = [1]*16
            ident += [2]*16
            ident += [0, 0]
            self.pieces = array('B', ident);
    
    def __copy__(self):
        return Sphere(copy(self.pieces))
    
    def __eq__(self, other):
        if isinstance(other, Sphere):
            return other.pieces == self.pieces
        else: return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        else: return not result
    
    def m_slice(self):
        return self.pieces[:16]
    
    def s_slice(self):
        return self.pieces[16:32]
    
    def tb_pieces(self):
        return self.pieces[32:]
    
    def to_s(self):
        value = ''
        for val in self.m_slice(): value += val
        value += ' '
        for val in self.s_slice(): value += val
        value += ' '
        for val in self.tb_pieces(): value += val
        return value
    
    @staticmethod
    def parse(value):
        # ensure that the data is split correctly
        parts = value.split(' ')
        if len(parts) != 3: return None
        if len(parts[0]) != 16: return None
        if len(parts[1]) != 16: return None
        if len(parts[2]) != 2: return None
        # process the numerical values
        values = []
        for char in parts[0] + parts[1] + parts[2]:
            if not char in ['0', '1', '2']: return None
            values += [ord(char) - ord('0')]
        # create a sphere object
        sphere = Sphere()
        sphere.pieces = array('B', values)
        return sphere

class Turn(object):
    
    def __init__(self, mapping):
        self.mapping = copy(mapping)
    
    def perform(self, sphere):
        result = Sphere()
        for i in range(0, 34):
            source = self.mapping[i]
            result.pieces[i] = sphere.pieces[source]
        return result
    
    def perform_to(self, sphere, out):
        for i in range(0, 34):
            source = self.mapping[i]
            out.pieces[i] = sphere.pieces[source]
    
    def exp(self, exponent):
        assert exponent >= 0
        result = Turn(range(0, 34))
        for x in range(0, exponent):
            temp = Turn(result.mapping)
            for i in range(0, 34):
                source = self.mapping[i]
                result.mapping[i] = temp.mapping[source]
        return result
    
    def inverse(self):
        result = Turn(range(0, 34))
        for i in range(0, 34):
            source = self.mapping[i]
            result.mapping[source] = i
        return result
    
    @staticmethod
    def generate_m():
        turnData = [32, 0, 1, 2, 3, 4, 5, 6, 33, 8, 9, 10, 11, 12, 13, 14]
        turnData += range(16, 32)
        turnData += [15, 7]
        return Turn(turnData)
    
    @staticmethod
    def generate_s():
        turnData = range(0, 16)
        turnData += [32, 16, 17, 18, 19, 20, 21, 22, 33, 24, 25, 26, 27, 28, 29, 30]
        turnData += [31, 23]
        return Turn(turnData)
    
    @staticmethod
    def generate_u():
        turnData = [31, 30, 29, 28, 4, 5, 6, 7, 8, 9, 10, 11, 19, 18, 17, 16]
        turnData += [0, 1, 2, 3, 20, 21, 22, 23, 24, 25, 26, 27, 12, 13, 14, 15]
        turnData += [32, 33]
        return Turn(turnData)

    @staticmethod
    def basis():
        moves = []
        for i in range(1, 5):
            mRegular = Turn.generate_m().exp(i)
            sRegular = Turn.generate_s().exp(i)
            moves += [mRegular, sRegular]
            moves += [mRegular.inverse(), sRegular.inverse()]
        uTurn = Turn.generate_u()
        moves += [uTurn, uTurn.inverse(), uTurn.exp(2)]
        return moves
    
    @staticmethod
    def basis_labels():
        return ['M', 'S', 'Mi', 'Si', 'M2', 'S2', 'Mi2', 'Si2',
                'M3', 'S3', 'Mi3', 'Si3', 'M4', 'S4', 'Mi4', 'Si4',
                'Ui', 'U', 'U2']
