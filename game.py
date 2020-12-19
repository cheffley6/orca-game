from tkinter import *
from utilities import *
import random
import threading
from pygame import mixer

from Agents import *
from Chamber import *
from config import *
from time import sleep
import inspect



tilesize = 10            

class GameLoop:

    def repaint(self):

        canvas.after(200, self.repaint)
        canvas.delete(ALL)

        if not orca.checkGameOver((shark.getX(), shark.getY())):

            orca.move()
            orca.checkGameOver((shark.getX(), shark.getY()))
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
            while i < 200:    
                i += 1
            i = 0
            canvas.create_text(150, 100, fill="black", font="Times 32 bold", text="GAME OVER!")
            while i < 200:    
                i += 1



started_gameover_music = False
chamber = Chamber()
orca = Orca()
shark = Shark()
root = Tk()

canvas = Canvas(root, width=300, height=300)
canvas.configure(background="blue")
canvas.pack()

input("waiting...")
# mixer.pre_init(44100, 16, 2, 4096)
mixer.init()

mixer.music.load("audio/snare_intro_copy.wav")
mixer.music.play()
mixer.music.load("audio/puzzle_1_copy.wav")
mixer.music.play(-1)
gameLoop = GameLoop()
gameLoop.repaint()

root.title("Orca")
root.bind('<KeyPress>', orca.getKey)
root.mainloop()