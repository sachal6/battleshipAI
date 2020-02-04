import numpy as np
import random
from enum import Enum


class BoardStates(Enum):
    '''
    Enumeration of possible board states
    '''
    CARRIER = 6
    BATTLESHIP = 5
    CRUISER = 4
    SUBMARINE = 3
    DESTROYER = 2
    MISS = 1
    EMPTY = 0

    @property
    def is_ship(self):
        return self not in (BoardStates.EMPTY, BoardStates.MISS)

class GameBoard:
    '''
    Abstraction of boardgame map
    '''
    DIRECTIONS = np.array([[1,0], [0,1], [-1,0], [0,-1]])

    def __init__(self, shape=(10,10)):
        self.__board = np.zeros(shape)
        self.__revealed = {ship.value:0 for ship in BoardStates if ship.is_ship}
    
    @property
    def board(self):
        return self.__board
    
    @property
    def revealed(self):
        return self.__revealed

    def __str__(self):
        return self.__board.__str__()

    def attack(self, location, opponent_board):
        '''
        Launch a strike at given location on opponent's board
        '''
        x,y = location
        if opponent_board.board[x,y]!=BoardStates.EMPTY.value:
            opposing_ship = opponent_board.board[x,y]
            self.board[x,y] = opposing_ship
            self.revealed[opposing_ship]+=1
        else:
            self.board[x,y] = BoardStates.MISS.value
        return self.board[x,y]
        

    def populate_board(self):
        '''
        Randomly places ships throughout board
        '''
        for ship in BoardStates:
            if ship.is_ship:
                ship = ship.value
                while True:
                    MAX_X, MAX_Y = self.board.shape
                    location = np.array([random.randint(0,MAX_X-1), random.randint(0, MAX_Y-1)])
                    direction = random.choice(GameBoard.DIRECTIONS)

                    if self.is_valid_placement(location, direction, ship):
                        current_location = location
                        for _ in range(ship):
                            x,y = current_location
                            self.__board[x,y]=ship
                            current_location+=direction
                        break
                    
        self.__revealed = {ship.value:ship.value for ship in BoardStates if ship.is_ship}

    def is_valid_placement(self, location, direction, ship):
        '''
        Checks that a given location and orientation for a ship does not go out of bounds or overlap with an explored miss
        '''
        currently_seen_count = self.revealed[ship]
        current_location = location.copy()
        for _ in range(ship):
            if not self.is_valid_square(current_location, ship):
                return False
            x,y = current_location
            if self.board[x][y]==ship:
                currently_seen_count-=1
            current_location = current_location + direction
        if currently_seen_count!=0:
            return False
        return True

    def is_valid_square(self, location, ship=None):
        '''
        Check that a given location is in the board and not already explored
        '''
        x,y = location
        if not (x>=0 and y>=0 and x<len(self.board) and y<len(self.board[0])):
            return False
        if not (self.board[x][y]==BoardStates.EMPTY.value or (ship is not None and self.board[x][y]==ship)):
            return False
        return True