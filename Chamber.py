from config import *
import random

class Chamber:

    def __init__(self):
        self.X = random.randint(1, boardWidth - 3)
        self.Y = random.randint(1, boardHeight - 3)

        self.dims = (self.X + 2, self.Y + 2)
        self.entry = random.choice([(self.X + 1, self.Y), (self.X, self.Y + 1), (self.X + 2, self.Y + 1), (self.X + 1, self.Y + 2)])