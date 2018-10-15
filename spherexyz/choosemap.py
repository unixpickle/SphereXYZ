"""
Perfect hashing for bitstrings with a fixed number of 1s.
Maps such bitstrings (Choices) to integers.
"""

from array import array
import bisect
from copy import copy
from math import factorial


class Choice(object):
    """
    A bitstring with a pre-determined number of 1s.

    The bitstrings have a well-defined ordering, and this
    ordering can be mapped to integers using perfect
    hashing.
    """

    def __init__(self, flags):
        self.flags = array('B', [1 if x else 0 for x in flags])
        self.hash = None

    def __eq__(self, other):
        if isinstance(other, Choice):
            return other.flags == self.flags
        else:
            return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        else:
            return not result

    def __lt__(self, other):
        if not isinstance(other, Choice):
            return NotImplemented
        assert len(other.flags) == len(self.flags)
        for flag, other_flag in zip(self.flags, other.flags):
            if other_flag > flag:
                return True
            elif other_flag < flag:
                return False
        return False

    def __gt__(self, other):
        if not isinstance(other, Choice):
            return NotImplemented
        assert len(other.flags) == len(self.flags)
        for flag, other_flag in zip(self.flags, other.flags):
            if other_flag < flag:
                return True
            elif other_flag > flag:
                return False
        return False

    def __copy__(self):
        return Choice(copy(self.flags))

    def count_choices(self):
        count = 0
        for i in self.flags:
            if i:
                count += 1
        return count

    def is_maximal(self):
        for i in range(self.count_choices()):
            if not self.flags[len(self.flags) - i - 1]:
                return False
        return True

    def increment(self):
        if self.is_maximal():
            raise OverflowError('cannot increment a maximal choice')
        last_blank = -1
        for i in range(self.count_choices()):
            index = len(self.flags) - i - 1
            if not self.flags[index]:
                last_blank = index
                break
        assert last_blank > 0

        # the number of 1 to shift
        num_move = len(self.flags) - last_blank - 1

        # given the last 0 position, we must now move the first
        # 1 prior to that down, and then we must move all other
        # 1s after the blank back up.
        for i in reversed(range(0, last_blank)):
            if self.flags[i]:
                self.flags[i] = 0
                self.flags[i + 1] = 1
                for j in range(0, num_move):
                    self.flags[i + 2 + j] = 1
                for j in range(i + 2 + num_move, len(self.flags)):
                    self.flags[j] = 0
                break
        self.hash = None

    def cut_one_element(self):
        """
        Truncates from the left just enough to slice off
        the first 1.
        """
        first_index = -1
        for i in range(0, len(self.flags)):
            if self.flags[i]:
                first_index = i
                break
        assert first_index >= 0
        result = Choice([])
        result.flags = self.flags[(first_index + 1):]
        return result

    def perfect_hash(self, cache=None):
        if self.count_choices() == 0:
            return 0
        if self.hash is not None:
            return self.hash
        if cache and cache.length == len(self.flags):
            return cache.lookup(self)

        sig_index = 0
        for i in range(0, len(self.flags)):
            if self.flags[i]:
                break
            rightmost_length = len(self.flags) - 1 - i
            choice_count = self.count_choices() - 1
            sig_index += _choose(rightmost_length, choice_count)
        self.hash = sig_index + self.cut_one_element().perfect_hash(cache)
        return self.hash


class ChoiceCache(object):

    def __init__(self, length):
        self.length = length
        self.choices = []
        for i in range(0, length + 1):
            # generate all (length choose i)
            start = Choice([True] * i + [False] * (length - i))
            while not start.is_maximal():
                self.add_choice(copy(start))
                start.increment()
            self.add_choice(start)

    def add_choice(self, choice):
        bisect.insort_left(self.choices, choice)
        choice.perfect_hash()

    def lookup(self, choice):
        i = bisect.bisect_left(self.choices, choice)
        assert i < len(self.choices)
        return self.choices[i].perfect_hash()


def _choose(a, b):
    series = 1
    for i in range(a - b + 1, a + 1):
        series *= i
    series //= factorial(b)
    return series
