from config import *
import random

class Puzzle:

    def __init__(self, game):
        mapping = [
            (
                {"x": boardWidth, "y": boardHeight},
                {"x": 0, "y": 0}
            ),
            (
                {"x": 0, "y": 0},
                {"x": boardWidth, "y": boardHeight}
            ),
            (
                {"x": 0, "y": boardWidth},
                {"x": boardHeight, "y": 0},
            ),
            (
                {"x": boardHeight, "y": 0},
                {"x": 0, "y": boardWidth},
            )
            

        ]
        self.portal, self.start = random.choice(mapping)
