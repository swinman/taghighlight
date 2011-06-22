# Used for timing a function; from http://www.daniweb.com/code/snippet368.html
# decorator: put @print_timing before a function to time it.
import time
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

class AttributeDict(dict):
    """Customised version of a dictionary that allows access by attribute."""
    def __getattr__(self, name):
        return self[name]

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
