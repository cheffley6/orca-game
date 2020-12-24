from collections import OrderedDict, deque
from config import *

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

 
# To store matrix cell cordinates
class Point:
    def __init__(self,x: int, y: int):
        self.x = x
        self.y = y
 
def isValidBfs(row: int, col: int):
    return (row >= 0) and (row < boardHeight) and (col >= 0) and (col < boardWidth)

# A data structure for queue used in BFS
class queueNode:
    def __init__(self,pt: Point, dist: int):
        self.pt = pt  # The cordinates of the cell
        self.dist = dist  # Cell's distance from the source
 
# These arrays are used to get row and column 
# numbers of 4 neighbours of a given cell 
rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]
 
# Function to find the shortest path between 
# a given source cell to a destination cell. 
def bfs(mat, src: Point, dest: Point):
     
    # check source and destination cell 
    # of the matrix have value 1 
    if mat[src.x][src.y]!=1 or mat[dest.x][dest.y]!=1:
        return -1
     
    visited = [[False for i in range(boardHeight)] for j in range(boardWidth)]
     
    # Mark the source cell as visited 
    visited[src.x][src.y] = True
     
    # Create a queue for BFS 
    q = deque()
     
    # Distance of source cell is 0
    s = queueNode(src,0)
    q.append(s) #  Enqueue source cell
     
    # Do a BFS starting from source cell 
    while q:
 
        curr = q.popleft() # Dequeue the front cell
         
        # If we have reached the destination cell, 
        # we are done 
        pt = curr.pt
        if pt.x == dest.x and pt.y == dest.y:
            return curr.dist
         
        # Otherwise enqueue its adjacent cells 
        for i in range(4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]
             
            # if adjacent cell is valid, has path  
            # and not visited yet, enqueue it.
            if (isValidBfs(row,col) and mat[row][col] == 1 and not visited[row][col]):
                visited[row][col] = True
                Adjcell = queueNode(Point(row,col),
                                    curr.dist+1)
                q.append(Adjcell)
    
    print(q)
    # Return -1 if destination cannot be reached 
    return -1