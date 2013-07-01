from array import array
from copy import copy
from math import factorial
import bisect

def choose(a, b):
    series = 1
    for i in xrange(a - b + 1, a + 1):
        series *= i
    series /= factorial(b)
    return series

class Choice(object):
    
    def __init__(self, flags):
        intList = map((lambda x: 1 if x else 0), flags)
        self.flags = array('B', intList)
        self.hash = None
    
    def __eq__(self, other):
        if isinstance(other, Choice):
            return other.flags == self.flags
        else: return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        else: return not result
    
    def __lt__(self, other):
        if not isinstance(other, Choice): return NotImplemented
        assert len(other.flags) == len(self.flags)
        for i in xrange(0, len(self.flags)):
            if other.flags[i] > self.flags[i]: return True
            if other.flags[i] < self.flags[i]: return False
        return False
    
    def __gt__(self, other):
        if not isinstance(other, Choice): return NotImplemented
        assert len(other.flags) == len(self.flags)
        for i in xrange(0, len(self.flags)):
            if other.flags[i] < self.flags[i]: return True
            if other.flags[i] > self.flags[i]: return False
        return False
    
    def __copy__(self):
        return Choice(copy(self.flags))
        
    def count_choices(self):
        count = 0
        for i in self.flags:
            if i == True: count += 1
        return count
    
    def is_maximal(self):
        for i in xrange(0, self.count_choices()):
            index = len(self.flags) - i - 1
            if not self.flags[index]: return False
        return True
    
    def increment(self):
        if self.is_maximal():
            raise OverflowError('cannot increment a maximal choice')
        lastBlank = -1
        for i in xrange(0, self.count_choices()):
            index = len(self.flags) - i - 1
            if not self.flags[index]:
                lastBlank = index
                break
        assert lastBlank > 0
        
        # the number of 1 to shift
        numMove = len(self.flags) - lastBlank - 1
        
        # given the last 0 position, we must now move the first
        # 1 prior to that down, and then we must move all other
        # 1s after the blank back up.
        for i in reversed(xrange(0, lastBlank)):
            if self.flags[i]:
                self.flags[i] = 0
                self.flags[i + 1] = 1
                for j in xrange(0, numMove):
                    self.flags[i + 2 + j] = 1
                for j in xrange(i + 2 + numMove, len(self.flags)):
                    self.flags[j] = 0
                break
        self.hash = None
    
    def cut_one_element(self):
        """Truncates from the left just enough to slice off the first 1"""
        firstIndex = -1
        for i in xrange(0, len(self.flags)):
            if self.flags[i]:
                firstIndex = i
                break
        assert firstIndex >= 0
        result = Choice([])
        result.flags = self.flags[(firstIndex + 1):]
        return result
    
    def perfect_hash(self, cache=None):
        if self.count_choices() == 0: return 0
        if self.hash != None: return self.hash
        if cache and cache.length == len(self.flags):
            return cache.lookup(self)
        
        # calculate the hash manually
        sigIndex = 0
        for i in range(0, len(self.flags)):
            if self.flags[i]: break
            rightmostLength = len(self.flags) - 1 - i
            choiceCount = self.count_choices() - 1
            # add rightmostLength choose choiceCount
            sigIndex += choose(rightmostLength, choiceCount)
        self.hash = sigIndex + self.cut_one_element().perfect_hash(cache)
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
    