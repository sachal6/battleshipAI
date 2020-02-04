import numpy as np
from Board import GameBoard, BoardStates
from Player import AI
from Game import Game
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import colors
from tkinter import *

class GameDisplay:
    '''
    Wrapper for game loop and display
    '''
    def __init__(self, game, root):
        self.__game = game
        self.__root = root

        title_text = StringVar(root)
        title_text.set("Battleship (AI vs AI)")

        Label(root, textvariable=title_text).pack(side='top')

        player_windows = Frame(self.__root)
        player_one_window = Frame(player_windows, borderwidth = 1, highlightbackground='black')
        player_two_window = Frame(player_windows, borderwidth = 1, highlightbackground='red')
        
        player_one_fig = Figure(figsize=(3,3))
        player_two_fig = Figure(figsize=(3,3))
        self.__ax_player_one = player_one_fig.add_subplot(111)
        self.__ax_player_two = player_two_fig.add_subplot(111)
        self.__canvas_player_one = FigureCanvasTkAgg(player_one_fig, player_one_window)
        self.__canvas_player_two = FigureCanvasTkAgg(player_two_fig, player_two_window)

        player_one_heatmap_fig = Figure(figsize=(3,3))
        player_two_heatmap_fig = Figure(figsize=(3,3))
        self.__ax_player_one_heatmap = player_one_heatmap_fig.add_subplot(111)
        self.__ax_player_two_heatmap = player_two_heatmap_fig.add_subplot(111)
        self.__canvas_player_one_heatmap = FigureCanvasTkAgg(player_one_heatmap_fig, player_one_window)
        self.__canvas_player_two_heatmap = FigureCanvasTkAgg(player_two_heatmap_fig, player_two_window)
        
        player_one_window.pack(side='left')
        player_two_window.pack(side='right')
        player_windows.pack(side='top')

        self.__canvas_player_one.get_tk_widget().pack(side='top')
        self.__canvas_player_one_heatmap.get_tk_widget().pack(side='bottom')

        self.__canvas_player_two.get_tk_widget().pack(side='top')
        self.__canvas_player_two_heatmap.get_tk_widget().pack(side='bottom')

        console = Frame(self.__root)
        button = Button(console, text="Step", command=self.step)
        button.pack(side='bottom')

        self.__turn_text = StringVar(console)
        self.__turn_text.set(f'Turn: {self.__game.turn}')
        Label(console, textvariable=self.__turn_text).pack(side='top')

        self.__result_text = StringVar(console)
        Label(console, textvariable=self.__result_text).pack(side='bottom')

        console.pack(side='top')

        zero_initialization = np.zeros(game.GRID_SIZE)
        
        self.plot_figure(zero_initialization, self.__ax_player_one, self.__canvas_player_one, title='Player One Board')
        self.plot_figure(zero_initialization, self.__ax_player_two, self.__canvas_player_two, title='Player Two Board')
        self.plot_figure(zero_initialization, self.__ax_player_two_heatmap, self.__canvas_player_two_heatmap, heatmap = True, title='Next Hit Probabilities')
        self.plot_figure(zero_initialization, self.__ax_player_one_heatmap, self.__canvas_player_one_heatmap, heatmap = True, title='Next Hit Probabilities')

    @property
    def game(self):
        return self.__game

    def step(self):
        '''
        Perform one iteration of gameloop and update display
        '''
        result = self.game.step()
        self.__turn_text.set(f'Turn: {self.__game.turn}')

        if not self.game.is_player_one_turn:
            current_board = self.game.player_one.opponent_map.board
            current_heat_map = self.game.player_one.most_recent_probabilities
            self.plot_figure(current_board, self.__ax_player_one, self.__canvas_player_one, title='Player One Board')
            self.plot_figure(current_heat_map, self.__ax_player_one_heatmap, self.__canvas_player_one_heatmap, heatmap = True, title='Next Hit Probabilities')
        else:
            current_board = self.game.player_two.opponent_map.board
            current_heat_map = self.game.player_two.most_recent_probabilities
            self.plot_figure(current_board, self.__ax_player_two, self.__canvas_player_two, title='Player Two Board')
            self.plot_figure(current_heat_map, self.__ax_player_two_heatmap, self.__canvas_player_two_heatmap, heatmap = True, title='Next Hit Probabilities')

        self.__result_text.set(result)

    def plot_figure(self, board_map, axes, canvas, heatmap = False, title = None):
        '''
        Generate updated plot of board states
        '''
        axes.clear()
        if heatmap:
            axes.pcolormesh(board_map, edgecolors='k', linewidth=1, cmap = 'RdBu_r')
        else:
            axes.pcolormesh(board_map, edgecolors='k', linewidth=1, vmin=0, vmax=len(BoardStates), cmap = 'plasma')
        axes.grid(which='minor', color='w', linestyle='-', linewidth=2)
        if title:
            axes.set_title(title)
        canvas.draw()