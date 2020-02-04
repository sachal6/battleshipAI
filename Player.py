import numpy as np
import random
from Board import GameBoard, BoardStates
from abc import ABC, abstractmethod

class Player(ABC):
    '''
    abstract base class of a player
    '''
    def __init__(self):
        self.__game_board = GameBoard()
        self.__opponent_map = GameBoard()
        self.__game_board.populate_board()

    @property
    def game_board(self):
        return self.__game_board

    @property
    def opponent_map(self):
        return self.__opponent_map

    @abstractmethod
    def strike_opponent(self, opponent):
        pass

    @property
    def has_won(self):
        '''
        Checks if a player has already discovered all enemy ships
        '''
        for ship, found in self.opponent_map.revealed.items():
            if found != BoardStates(ship).value:
                return False
        return True

    def print_map(self, map):
        '''
        Debugging utility for printing out current board space
        '''
        with np.printoptions(precision=3, floatmode='maxprec', suppress=True):
            print(map, end='\n\n')

class AI(Player):
    '''
    Probabilistically greedy Player
    Explores all possibile positions for any given ship and selects next strike location
     as the location present in the most valid configurations
    '''
    def __init__(self):
        super().__init__()
        self.__most_recent_probabilities = np.zeros_like(self.game_board.board)

    @property
    def most_recent_probabilities(self):
        return self.__most_recent_probabilities

    def strike_opponent(self, opponent):      
        likelihoods = self.calculate_ship_likelihoods()
        likelihoods[self.opponent_map.board!=0]=0
        self.__most_recent_probabilities = likelihoods

        argmax = likelihoods.argmax()
        max_x, max_y = argmax//len(likelihoods[0]), argmax%len(likelihoods[0])
        attack_location = (max_x, max_y)
        result = self.opponent_map.attack(attack_location, opponent.game_board)
        text = self.generate_result_text(attack_location, result)
        return text


    def generate_result_text(self, attack_location, result):
        '''
        Takes output of previous action and generates displayable string to communicate the information
        '''
        result_text = f"Attack at position ({attack_location[0]}, {attack_location[1]})"  
        if result == BoardStates.MISS.value:
            result_text += ' missed'
        else:
            ship = self.opponent_map.board[attack_location]
            ship_name = BoardStates(ship).name
            if self.opponent_map.revealed[ship] == BoardStates(ship).value:
                result_text += f' sunk {ship_name}'
            else:
                result_text += f' hit {ship_name}'
        return result_text + '!'
            
    def calculate_ship_likelihoods(self):
        '''
        Probablistically explores all possible states and returns map with relative likelihoods that any given location containing a ship
        '''
        known = self.opponent_map
        ships = [ship.value for ship in BoardStates if ship.is_ship]
        likelihoods = np.zeros_like(known.board)
        for ship in ships:
            ship_likelihood = np.zeros_like(known.board)
            for i in range(len(known.board)):
                for k in range(len(known.board[0])):
                    location = np.array([i,k])
                    for direction in GameBoard.DIRECTIONS:  
                        if known.is_valid_placement(location, direction, ship):
                            current_location = location
                            for _ in range(ship):
                                x,y = current_location
                                ship_likelihood[x][y]+=1
                                current_location+=direction
            likelihoods=np.maximum(likelihoods, ship_likelihood/ship_likelihood.sum())
        return likelihoods

x = AI().calculate_ship_likelihoods()
