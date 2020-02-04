import numpy as np
from Board import GameBoard, BoardStates
from Player import AI
from Game import Game
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import colors
from tkinter import *
from GameDisplay import GameDisplay


if __name__ == "__main__":
    player_one = AI()
    player_two = AI()
    game = Game(player_one, player_two)

    root = Tk()
    game_display = GameDisplay(game, root)
    root.mainloop()