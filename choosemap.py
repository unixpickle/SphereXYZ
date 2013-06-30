from array import array
from math import factorial

class Choice(object):
    
    def __init__(self, flags):
        intList = map((lambda x: 1 if x else 0), flags)
        self.flags = array('B', intList)
    
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
    
    def cut_one_element(self):
        """Truncates from the left just enough to slice off the first 1"""
        firstIndex = -1
        for i in xrange(0, len(self.flags)):
            if self.flags[i]:
                firstIndex = i
                break
        assert firstIndex >= 0
        newList = []
        for i in xrange(firstIndex + 1, len(self.flags)):
            newList.append(True if self.flags[i] else False)
        return Choice(newList)
    
    def perfect_hash(self):
        if self.count_choices() == 0: return 0
        sigIndex = 0
        for i in range(0, len(self.flags)):
            if self.flags[i]: break
            rightmostLength = len(self.flags) - 1 - i
            choiceCount = self.count_choices() - 1
            # add rightmostLength choose choiceCount
            ordered = factorial(rightmostLength) / (factorial(rightmostLength - choiceCount))
            unordered = ordered / factorial(choiceCount)
            sigIndex += unordered
        return sigIndex + self.cut_one_element().perfect_hash()
        