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

import numpy as np

tilesize = 10            

INCLUDE_SHARK = True
loopCount = 0

class GameLoop:

    def __init__(self, chamber):
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
        # print(self.valid_chase_spots)
        # [:] = (chamber.getDims()[0] + 1) * [chamber.getDims()[1] * [False]]
        # # self.valid_spots[chamber.getEntry()[0]][chamber.getEntry()[1]] = True
        # # self.valid_spots[chamber.getX() + 1][chamber.getY() + 1] = True
        # print("AFTER :", self.valid_spots[chamber.getY():chamber.getY()+chamber.getDims()[0]][chamber.getX():chamber.getX()+chamber.getDims()[1]])
    def repaint_chase(self):

        canvas.after(200, self.repaint_chase)
        canvas.delete(ALL)


        if (not INCLUDE_SHARK) or not orca.checkGameOver((shark.getX(), shark.getY())):
            
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
            if INCLUDE_SHARK:
                global loopCount
                if loopCount >= 5:
                    shark.move((orca.getX(), orca.getY()), self)
                else:
                    shark.move((orca.getX(), orca.getY()), self, loopCount)
                    loopCount += 1
                orca.checkGameOver((shark.getX(), shark.getY()))


            canvas.create_rectangle(orca.getX() * tilesize, orca.getY() * tilesize,
                                    orca.getX() * tilesize + tilesize,
                                    orca.getY() * tilesize + tilesize, fill="white")  # Head
            if INCLUDE_SHARK:
                canvas.create_rectangle(shark.getX() * tilesize, shark.getY() * tilesize,
                                    shark.getX() * tilesize + tilesize,
                                    shark.getY() * tilesize + tilesize, fill="red")  # Shark

            
                    

        else:   # GameOver Message
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



started_gameover_music = False
chamber = Chamber()
orca = Orca()
root = Tk()

shark = None
if INCLUDE_SHARK:
    shark = Shark()


canvas = Canvas(root, width=10 * boardWidth, height=10 * boardHeight)
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