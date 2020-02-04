from Board import GameBoard, BoardStates
from Player import AI
import numpy as np

class Game:
    '''
    Abstraction of game loop
    '''
    GRID_SIZE = (10,10)

    def __init__(self, player_one, player_two):
        self.__turn_count = 0
        self.__is_player_one_turn = True
        self.__player_one = player_one
        self.__player_two = player_two
        self.__is_over = False

    @property
    def turn(self):
        return self.__turn_count
    
    @property 
    def is_player_one_turn(self):
        return self.__is_player_one_turn

    @property
    def player_one(self):
        return self.__player_one
    
    @property
    def player_two(self):
        return self.__player_two
    
    @property
    def active_player_id(self):
        return 1+int(self.__is_player_one_turn)

    def step(self):
        '''
        Perform one iteration of game loop abstraction
        '''
        if self.__is_over:
            return 'Game already over! Please reset'

        if self.is_player_one_turn:
            self.__turn_count+=1
            current_player = self.player_one
            next_player = self.player_two
        else:
            current_player = self.player_two
            next_player = self.player_one
        
        self.__is_player_one_turn = not self.__is_player_one_turn
        result = f'Player {self.active_player_id}: ' + current_player.strike_opponent(next_player)

        if current_player.has_won:
            self.__is_over = True
            return f"Game over! Player {int(not current_player)+1} has won!"
        return result