from config import *
from utilities import *
import random
import collections
import queue




class Shark:

    def __init__(self, orca):
        candidate_position = (random.randint(1, boardWidth - 2), random.randint(1, boardHeight - 2))
        while get_manhattan_distance(candidate_position, orca.getPosition()) < 0.25 * (boardHeight + boardWidth):
            candidate_position = (random.randint(1, boardWidth - 2), random.randint(1, boardHeight - 2))
        self.X, self.Y = candidate_position
        self.lastTenSpots = SpotChecker()
    
    def getPosition(self):
        return (self.X, self.Y)

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def createNewShark(self):
        self.X = random.randint(1, boardWidth - 2)
        self.Y = random.randint(1, boardHeight - 2)
    
    def canSeeOrca(self, target):
        return True

    def moveRandomly(self, game, options):
        nextPosition = None
        choices = [self.getPosition()]
        for option in options[1:]:
            if isValid(option, game.valid_chase_spots):
                choices.append(option)
        
        if len(choices) == 0:
            raise Exception("Shark out of moves.")

        nextPosition = random.choice(choices)
        self.X, self.Y = nextPosition
        self.lastTenSpots.add(nextPosition)
        

    def move(self, target, game):
        options = [
            (self.X, self.Y),
            (self.X - 1, self.Y),
            (self.X + 1, self.Y),
            (self.X, self.Y - 1),
            (self.X, self.Y + 1)
        ]
        
        if random.randint(1, 100) == 1:
            self.moveRandomly(game, options)
        else:
            self.hunt(target, game, options)


    # given a game environment with valid spots, return the
    # next location that follows BFS to the target


    def hunt(self, target, game, options):
        path = astar(game.valid_chase_spots, self.getPosition(), target)
        self.X, self.Y = path[1] if len(path) > 1 else path[0]


class Orca():

    def __init__(self):

        self.X = random.randint(1, boardWidth - 1)
        self.Y = random.randint(1, boardHeight - 1)
        self.key = None
        self.points = 0

    def move(self, game): # move and change direction with wasd
        moves = {
            "w": lambda x, y : (x, y - 1),
            "s": lambda x, y : (x, y + 1),
            "a": lambda x, y : (x - 1, y),
            "d": lambda x, y : (x + 1, y),
            None: lambda x, y : (x, y)
        }

        attemptedMove = moves[self.key](self.X, self.Y)
        
        if isValid(attemptedMove, game.valid_chase_spots):
            self.X, self.Y = attemptedMove

    def checkGameOver(self, coords):
        if self.X == coords[0] and self.Y == coords[1]:
            return True # Orca eaten by shark
        return False
    
    def checkFinishChase(self, game):
        return self.getPosition() == game.chamber.getPortal()

    def getKey(self, event):

        if event.char == "w" or event.char == "d" or event.char == "s" or event.char == "a" or event.char == " ":
            self.key = event.char

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def setX(self, X):
        self.X = X

    def setY(self, Y):
        self.Y = Y
    
    def getPosition(self):
        return (self.X, self.Y)

    def getPoints(self):
        return self.points