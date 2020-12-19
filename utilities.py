from config import *

def isValid(position):
    return position[0] < boardWidth and position[1] < boardHeight and position[0] >= 0 and position[1] >= 0

def get_manhattan_distance(source, destination):
    return abs(source[0] - destination[0]) + abs(source[1] - destination[1])
