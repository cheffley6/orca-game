from config import *
from utilities import *
import random

import queue
from pprint import pprint

def isValid(position, game):
    return position[1] in range(len(game.valid_chase_spots)) and position[0] in range(len(game.valid_chase_spots[0])) and game.valid_chase_spots[position[1]][position[0]]




class Shark:

    def __init__(self):
        self.X = random.randint(1, boardWidth - 2)
        self.Y = random.randint(1, boardHeight - 2)
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
            if isValid(option, game):
                choices.append(option)
        
        if len(choices) == 0:
            raise Exception("Shark out of moves.")

        nextPosition = random.choice(choices)
        self.X, self.Y = nextPosition
        self.lastTenSpots.add(nextPosition)
        

    def move(self, target, game, loopCount=5):
        options = [
            (self.X, self.Y),
            (self.X - 1, self.Y),
            (self.X + 1, self.Y),
            (self.X, self.Y - 1),
            (self.X, self.Y + 1)
        ]
        
        if random.randint(1, 10) == 1 or (self.lastTenSpots.size() < 7 and loopCount >= 5):
            self.moveRandomly(game, options)
        else:
            self.hunt(target, game, options)

    def hunt(self, target, game, options):
        choices = [options[0]]

        best_score = 0

        for option in options[1:]:
            score = get_manhattan_delta(option, (self.X, self.Y), target)
            if isValid(option, game):
                if score < best_score:
                    choices = [option]
                    best_score = score
                elif score == best_score:
                    choices.append(option)
        
        nextPosition = random.choice(choices)
        self.X, self.Y = nextPosition
        self.lastTenSpots.add(nextPosition)


class Orca():

    def __init__(self):

        self.X = random.randint(0, boardWidth)
        self.Y = random.randint(0, boardHeight)
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
        
        if isValid(attemptedMove, game):
            self.X, self.Y = attemptedMove

    def checkGameOver(self, coords):
        if self.X == coords[0] and self.Y == coords[1]:
            return True # Orca eaten by shark
        return False

    def getKey(self, event):

        if event.char == "w" or event.char == "d" or event.char == "s" or event.char == "a" or event.char == " ":
            self.key = event.char

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getPoints(self):
        return self.points