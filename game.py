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

class GameLoop:

    def __init__(self, chamber):
        self.valid_spots = boardHeight * [boardWidth * [True]]
        # print(chamber.getX(), chamber.getY())
        # print("BEFORE:", self.valid_spots[chamber.getY():chamber.getY()+chamber.getDims()[0]])
        # self.valid_spots[chamber.getY():chamber.getY()+chamber.getDims()[0]][chamber.getX():chamber.getX()+chamber.getDims()[1]] = (chamber.getDims()[0] + 1) * [(chamber.getDims()[1] + * [False]]
        # # self.valid_spots[chamber.getEntry()[0]][chamber.getEntry()[1]] = True
        # # self.valid_spots[chamber.getX() + 1][chamber.getY() + 1] = True
        # print("AFTER :", self.valid_spots[chamber.getY():chamber.getY()+chamber.getDims()[0]][chamber.getX():chamber.getX()+chamber.getDims()[1]])

    def repaint(self):

        canvas.after(200, self.repaint)
        canvas.delete(ALL)

        if not orca.checkGameOver((shark.getX(), shark.getY())):

            orca.move(self)
            shark.hunt((orca.getX(), orca.getY()))
            orca.checkGameOver((shark.getX(), shark.getY()))
            canvas.create_rectangle(orca.getX() * tilesize, orca.getY() * tilesize,
                                    orca.getX() * tilesize + tilesize,
                                    orca.getY() * tilesize + tilesize, fill="white")  # Head

            # for i in range(1, orca.getOrcaLength(), 1):
            #     canvas.create_rectangle(orca.getOrcaX(i) * tilesize, orca.getOrcaY(i) * tilesize,
            #                             orca.getOrcaX(i) * tilesize + tilesize,
            #                             orca.getOrcaY(i) * tilesize + tilesize, fill="blue")  # Body

            canvas.create_rectangle(shark.getX() * tilesize, shark.getY() * tilesize,
                                    shark.getX() * tilesize + tilesize,
                                    shark.getY() * tilesize + tilesize, fill="red")  # Shark

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
                    

        else:   # GameOver Message
            global started_gameover_music
            if not started_gameover_music:
                mixer.music.stop()
                mixer.music.load("audio/gameover_copy.wav")
                mixer.music.play(-1)
            started_gameover_music = True
            canvas.delete(ALL)
            canvas.configure(background="black")
            i = 0

            canvas.create_text(150, 100, fill="red", font="Times 32 bold", text="GAME OVER!")

            # while i < 2000:    
            #     i += 1
            # i = 0
            # canvas.create_text(150, 100, fill="black", font="Times 32 bold", text="GAME OVER!")
            # while i < 2000:    
            #     i += 1



started_gameover_music = False
chamber = Chamber()
orca = Orca()
shark = Shark()
root = Tk()

canvas = Canvas(root, width=300, height=300)
canvas.configure(background="blue")
canvas.pack()

mixer.init()

mixer.music.load("audio/snare_intro_copy.wav")
mixer.music.play()
while mixer.music.get_busy():
    pass
mixer.music.load("audio/chase_1_copy.wav")
mixer.music.play(-1)
gameLoop = GameLoop(chamber)
gameLoop.repaint()

root.title("Orca")
root.bind('<KeyPress>', orca.getKey)
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
root.mainloop()