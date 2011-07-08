from __future__ import print_function
import time
import re

# Used for timing a function; from http://www.daniweb.com/code/snippet368.html
# decorator: put @print_timing before a function to time it.
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print('{name} took {time:0.3f} ms'.format(name=func.__name__, time=(t2-t1)*1000.0))
        return res
    return wrapper

class TagHighlightOptionDict(dict):
    """Customised version of a dictionary that allows access by attribute."""
    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, name):
        if name not in self:
            from .options import AllOptions
            for option in AllOptions.keys():
                if option == name:
                    return AllOptions[option]['Default']
        return super(TagHighlightOptionDict, self).__getitem__(name)

    def __setattr__(self, name, value):
        self[name] = value

class SetDict(dict):
    """Customised version of a dictionary that auto-creates non-existent keys as sets."""
    def __getitem__(self, key):
        if key not in self:
            self[key] = set()
        return super(SetDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(value, set):
            super(SetDict, self).__setitem__(key, value)
        else:
            super(SetDict, self).__setitem__(key, set([value]))

class DictDict(dict):
    """Customised version of a dictionary that auto-creates non-existent keys as SetDicts."""
    def __getitem__(self, key):
        if key not in self:
            self[key] = SetDict()
        return super(DictDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(value, SetDict):
            super(DictDict, self).__setitem__(key, value)
        else:
            raise NotImplementedError

def GenerateValidKeywordRange(iskeyword):
    ValidKeywordSets = iskeyword.split(',')
    rangeMatcher = re.compile('^(?P<from>(?:\d+|\S))-(?P<to>(?:\d+|\S))$')
    falseRangeMatcher = re.compile('^^(?P<from>(?:\d+|\S))-(?P<to>(?:\d+|\S))$')
    validList = []
    for valid in ValidKeywordSets:
        m = rangeMatcher.match(valid)
        fm = falseRangeMatcher.match(valid)
        if valid == '@':
            for ch in [chr(i) for i in range(0,256)]:
                if ch.isalpha():
                    validList.append(ch)
        elif m is not None:
            # We have a range of ascii values
            if m.group('from').isdigit():
                rangeFrom = int(m.group('from'))
            else:
                rangeFrom = ord(m.group('from'))

            if m.group('to').isdigit():
                rangeTo = int(m.group('to'))
            else:
                rangeTo = ord(m.group('to'))

            validRange = list(range(rangeFrom, rangeTo+1))
            for ch in [chr(i) for i in validRange]:
                validList.append(ch)

        elif fm is not None:
            # We have a range of ascii values: remove them!
            if fm.group('from').isdigit():
                rangeFrom = int(fm.group('from'))
            else:
                rangeFrom = ord(fm.group('from'))

            if fm.group('to').isdigit():
                rangeTo = int(fm.group('to'))
            else:
                rangeTo = ord(fm.group('to'))

            validRange = range(rangeFrom, rangeTo+1)
            for ch in [chr(i) for i in validRange]:
                for i in range(validList.count(ch)):
                    validList.remove(ch)

        elif len(valid) == 1:
            # Just a char
            validList.append(valid)

        else:
            raise ValueError('Unrecognised iskeyword part: ' + valid)

    return validList


def IsValidKeyword(keyword, iskeyword):
    for char in keyword:
        if not char in iskeyword:
            return False
    return True


if __name__ == "__main__":
    import pprint
    test_obj = SetDict()
    # Should be able to add an item to the list
    pprint.pprint(test_obj)
    test_obj['MyIndex'].add('Hello')
    test_obj['SetList'] = ['This', 'Is', 'A', 'List']
    test_obj['SetString'] = 'This is a string'
    # These should all be lists:
    pprint.pprint(test_obj)
