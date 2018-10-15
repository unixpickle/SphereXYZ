"""
Representation of the puzzle and moves thereof.

Defines Sphere, the puzzle state, and Turn, a move
affecting the puzzle state.
"""


from copy import copy
from array import array


class Sphere(object):
    """
    The M slice is the slice going from the front to the back.
    It is ordered from top going towards the front.

    The S slice is the slice going from the right to the left.
    It is ordered from top going towards the right.

    The plastic pieces are labeled with numbers 0, 1, 2.
    The M slice color is 1, S slice is 2, poles are 0.
    """

    def __init__(self, pieces=None):
        if pieces:
            self.pieces = pieces
        else:
            ident = [1] * 16
            ident += [2] * 16
            ident += [0, 0]
            self.pieces = array('B', ident)

    def __copy__(self):
        return Sphere(copy(self.pieces))

    def __eq__(self, other):
        if isinstance(other, Sphere):
            return other.pieces == self.pieces
        else:
            return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        else:
            return not result

    def m_slice(self):
        """Get the colors along the M slice."""
        return self.pieces[:16]

    def s_slice(self):
        """Get the colors along the S slice."""
        return self.pieces[16:32]

    def tb_pieces(self):
        """Get the top/bottom pieces."""
        return self.pieces[32:]

    def to_s(self):
        """
        Get a human-readable representation of the state.

        This representation can be passed back to parse().
        """
        value = ''
        for val in self.m_slice():
            value += val
        value += ' '
        for val in self.s_slice():
            value += val
        value += ' '
        for val in self.tb_pieces():
            value += val
        return value

    @classmethod
    def parse(cls, value):
        """
        Parse the puzzle from a string.

        The puzzle string is of the form:
        "MMMMMMMMMMMMMMMM SSSSSSSSSSSSSSSS TB",
        where the Ms are the colors on the M-slice, the Ss
        are the colors on the S-slice, and TB are the
        top/bottom colors.
        """
        parts = value.split(' ')
        if len(parts) != 3:
            return None
        if len(parts[0]) != 16:
            return None
        if len(parts[1]) != 16:
            return None
        if len(parts[2]) != 2:
            return None

        values = []
        for char in parts[0] + parts[1] + parts[2]:
            if char not in ['0', '1', '2']:
                return None
            values += [ord(char) - ord('0')]

        sphere = cls()
        sphere.pieces = array('B', values)
        return sphere


class Turn(object):
    """
    A move on the puzzle.

    A U turn means to turn the top hemisphere clockwise.
    An M turn means to move the top of the M slice towards
    the front.
    An S turn means to move the top of the S slice towards
    the right.
    """

    def __init__(self, mapping):
        self.mapping = copy(mapping)

    def perform(self, sphere):
        result = Sphere()
        for i in range(34):
            source = self.mapping[i]
            result.pieces[i] = sphere.pieces[source]
        return result

    def perform_to(self, sphere, out):
        for i in range(34):
            source = self.mapping[i]
            out.pieces[i] = sphere.pieces[source]

    def exp(self, exponent):
        assert exponent >= 0
        result = Turn(list(range(34)))
        for x in range(exponent):
            temp = Turn(result.mapping)
            for i in range(34):
                source = self.mapping[i]
                result.mapping[i] = temp.mapping[source]
        return result

    def inverse(self):
        result = Turn(list(range(34)))
        for i in range(34):
            source = self.mapping[i]
            result.mapping[source] = i
        return result

    @staticmethod
    def generate_m():
        return Turn([32, 0, 1, 2, 3, 4, 5, 6, 33, 8, 9, 10, 11, 12, 13, 14] +
                    list(range(16, 32)) +
                    [15, 7])

    @staticmethod
    def generate_s():
        return Turn(list(range(16)) +
                    [32, 16, 17, 18, 19, 20, 21, 22, 33, 24, 25, 26, 27, 28, 29, 30] +
                    [31, 23])

    @staticmethod
    def generate_u():
        return Turn([31, 30, 29, 28, 4, 5, 6, 7, 8, 9, 10, 11, 19, 18, 17, 16] +
                    [0, 1, 2, 3, 20, 21, 22, 23, 24, 25, 26, 27, 12, 13, 14, 15] +
                    [32, 33])

    @staticmethod
    def basis():
        moves = []
        for i in range(1, 5):
            m_regular = Turn.generate_m().exp(i)
            s_regular = Turn.generate_s().exp(i)
            moves += [m_regular, s_regular, m_regular.inverse(), s_regular.inverse()]
        u_turn = Turn.generate_u()
        moves += [u_turn, u_turn.inverse(), u_turn.exp(2)]
        return moves

    @staticmethod
    def basis_labels():
        return ['M', 'S', 'Mi', 'Si', 'M2', 'S2', 'Mi2', 'Si2',
                'M3', 'S3', 'Mi3', 'Si3', 'M4', 'S4', 'Mi4', 'Si4',
                'Ui', 'U', 'U2']
