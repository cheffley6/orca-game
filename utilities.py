from collections import OrderedDict

def get_manhattan_distance(source, destination):
    return abs(source[0] - destination[0]) + abs(source[1] - destination[1])

def get_manhattan_delta(option, source, destination):
    return get_manhattan_distance(option, destination) - get_manhattan_distance(source, destination)

class SpotChecker:
    def __init__(self):
        self.store = []
    
    def add(self, item):
        self.store.append(item)
        if len(self.store) > 10:
            self.store = self.store[1:]
    
    def size(self):
        return len(set(self.store))