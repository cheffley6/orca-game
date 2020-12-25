from tkinter import *
from utilities import *
import random
import threading
from pygame import mixer

from Agents import *
from Chamber import *
from config import *
from time import sleep
import os
from Puzzle import Puzzle

import numpy as np

tilesize = 10            

INCLUDE_SHARK = True


class GameLoop:

    def __init__(self, chamber):

        # initialize valid chase spots
        self.chamber = chamber
        self.valid_chase_spots = np.empty((boardHeight, boardWidth))
        chamberX, chamberY = chamber.getX(), chamber.getY()
        entryX, entryY = chamber.getEntry()
        for index, entry in enumerate(self.valid_chase_spots):
            entry.fill(True)
            if index in range(chamberY, chamberY+chamber.getDims()[0]):
                entry[chamberX:chamberX+chamber.getDims()[1]] = chamber.getDims()[1] * [False]
            self.valid_chase_spots[index] = entry
        
        self.valid_chase_spots[chamberY+1][chamberX+1] = True
        self.valid_chase_spots[entryY][entryX] = True

        # initialize puzzle grid
        self.puzzle = Puzzle(self)
        self.valid_puzzle_spots = np.empty((boardHeight, boardWidth))
        self.valid_puzzle_spots.fill(True)

    def renderGameover(self):
        global started_gameover_music
        if not started_gameover_music:
            mixer.music.stop()
            mixer.music.load("audio/gameover.wav")
            mixer.music.play(-1)
        started_gameover_music = True
        canvas.delete(ALL)
        canvas.configure(background="black")
        i = 0

        canvas.create_text(150, 100, fill="red", font="Times 32 bold", text="GAME OVER!")

    def repaint_chase(self):

        
        canvas.delete(ALL)


        if not orca.checkGameOver((shark.getX(), shark.getY())):
            
            canvas.create_rectangle(chamber.X * tilesize, chamber.Y * tilesize,
                                    chamber.X * tilesize + 3 * tilesize,
                                    chamber.Y * tilesize + 3 * tilesize, fill="grey")  # Shark
            canvas.create_rectangle(chamber.entry[0] * tilesize, chamber.entry[1] * tilesize,
                                    chamber.entry[0] * tilesize + tilesize,
                                    chamber.entry[1] * tilesize + tilesize, fill="blue"
                                )
            canvas.create_rectangle((chamber.X + 1) * tilesize, (chamber.Y + 1) * tilesize,
                                    (chamber.X + 1) * tilesize + tilesize,
                                    (chamber.Y + 1) * tilesize + tilesize, fill="yellow"
                                )
            orca.move(self)
            if orca.checkFinishChase(self):
                global started_puzzle_music
                if not started_puzzle_music:
                    mixer.music.stop()
                    mixer.music.load("audio/puzzle_1.wav")
                    mixer.music.play(0)
                    started_puzzle_music = True
                return self.render_first_frame_of_puzzle()
            if INCLUDE_SHARK:
                shark.move((orca.getX(), orca.getY()), self)
                orca.checkGameOver((shark.getX(), shark.getY()))


            canvas.create_rectangle(orca.getX() * tilesize, orca.getY() * tilesize,
                                    orca.getX() * tilesize + tilesize,
                                    orca.getY() * tilesize + tilesize, fill="white")  # Head
            if INCLUDE_SHARK:
                canvas.create_rectangle(shark.getX() * tilesize, shark.getY() * tilesize,
                                    shark.getX() * tilesize + tilesize,
                                    shark.getY() * tilesize + tilesize, fill="red")  # Shark
            canvas.after(frameDelay, self.repaint_chase)

            
                    

        else:   # GameOver Message
            self.renderGameover()

    def render_first_frame_of_puzzle(self):
        canvas.delete(ALL)

        startX, startY = self.puzzle.start["x"], self.puzzle.start["y"]
        
        orca_render = canvas.create_rectangle(startX * tilesize, startY * tilesize,
                                startX * tilesize + tilesize,
                                startY * tilesize + tilesize, fill="white")  # Head
        canvas.after(frameDelay, self.repaint_puzzle, orca_render)
        orca.setX(startX)
        orca.setY(startY)
        endX, endY = self.puzzle.portal["x"], self.puzzle.portal["y"]
        canvas.create_rectangle(endX * tilesize, endY * tilesize,
                                endX * tilesize + tilesize,
                                endY * tilesize + tilesize, fill="yellow")
    
    def repaint_puzzle(self, orca_render):
        canvas.after(frameDelay, self.repaint_puzzle, orca_render)
        canvas.delete(orca_render)
        orca.move(self)
        
        orca_render = canvas.create_rectangle(orca.getX() * tilesize, orca.getY() * tilesize,
                                orca.getX() * tilesize + tilesize,
                                orca.getY() * tilesize + tilesize, fill="white")  # Head



started_gameover_music = False
started_puzzle_music = False
chamber = Chamber()
orca = Orca()
root = Tk()

shark = None
if INCLUDE_SHARK:
    shark = Shark()


canvas = Canvas(root, width=10 * boardWidth, height=10 * boardHeight, bd=0, highlightthickness=0,)
canvas.configure(background="blue")
canvas.pack()

def start_music():
    mixer.init()
    mixer.music.load("audio/snare_intro.wav")
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mixer.music.load("audio/chase_1.wav")
    mixer.music.play(-1)

start_music()

gameLoop = GameLoop(chamber)
gameLoop.repaint_chase()

root.title("Orca")
root.bind('<KeyPress>', orca.getKey)
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
root.mainloop()