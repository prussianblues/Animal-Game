# Author: Andy Kim
# GitHub username: prussianblues
# Date: 3/13/2026
# Description: Script contains classes to create an animal-themed abstract board game that takes place on a
# 7x7 grid, pieces with differing directions/distances/locomotion, and two players.

class AnimalGame:
    """ Class represents an animal-based board game which takes place on a 7x7 grid, locations labeled with
        algebraic notation (columns labeled a-g rows labeled 1-7). Manages game state, board, turn, moves. """

    def __init__(self):
        """Initializes the board, captured piece lists, current turn/current player, game state"""
        tangerine = "Tangerine"
        amethyst = "Amethyst"
        self.__board = [[Pika(tangerine), Trilobite(tangerine), Wombat(tangerine), Beluga(tangerine), Wombat(tangerine), Trilobite(tangerine), Pika(tangerine)],
                        [None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None],
                        [Pika(amethyst), Trilobite(amethyst), Wombat(amethyst), Beluga(amethyst), Wombat(amethyst), Trilobite(amethyst), Pika(amethyst)]]
        self.__tangerine_captures = []
        self.__amethyst_captures = []
        self.__current_turn = "Tangerine"
        self.__game_state = "UNFINISHED"

    def get_game_state(self):
        """Returns the current state of the game"""
        return self.__game_state

    def get_turn(self):
        """Returns the current player / who's turn it is."""
        return self.__current_turn

    def get_amethyst_captures(self):
        """Returns list of pieces amethyst has captured"""
        return self.__amethyst_captures

    def get_tangerine_captures(self):
        """Returns list of pieces tangerine has captured"""
        return self.__tangerine_captures

    def update_turn(self):
        """Changes the current turn by switching the player."""
        if self.__current_turn == "Tangerine":
            self.__current_turn = "Amethyst"
        elif self.__current_turn == "Amethyst":
            self.__current_turn = "Tangerine"

    def update_board(self, row, col, piece):
        """Takes row (int), column(int), piece object parameters and places the specified piece object at the row and column on board_grid"""
        self.__board[row][col] = piece

    def convert_coord(self, coord):
        """Takes a string coordinate parameter converts it into a row, column tuple using dictionaries. Maps letters to columns
        and digit characters to rows."""
        # for example, a6 should be col = 1, row = 6
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6} #column dictionary
        row_dict = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6} # row dictionary
        col = coord[0]
        row = coord[1]
        coord_tuple = (row_dict[row],col_dict[col])
        return coord_tuple

    def update_game_state(self):
        """Update the game state to 'TANGERINE_WON', or 'AMETHYST_WON'"""
        if self.__current_turn == "Tangerine":
            self.__game_state = 'TANGERINE_WON'
        elif self.__current_turn == "Amethyst":
            self.__game_state = 'AMETHYST_WON'

    def make_move(self, start, destination):
        """Takes a starting and destination coordinate. Moves a piece from the start to the destination coordinate if
        the move is valid. Checks the game state and verifies that the piece is the current player's, verifies move
        with the piece object's valid move method. Checks for blocking pieces, captured pieces. Updates board and turn.
        Returns true if the move was valid and completed, or false if the move was invalid."""
        if self.get_game_state() != "UNFINISHED": # if game is finished
            return False

        begin = self.convert_coord(start) #converting starting coordinate to tuple
        end = self.convert_coord(destination) #converting end coordinate to tuple

        #begin[0] will contain row, begin[1] will contain column
        # end[0] will contain row, end[1] will contain column
        begin_row = begin[0]
        begin_col = begin[1]
        end_row = end[0]
        end_col = end[1]

        # check that there is a piece at the location of starting coordinates
        if self.__board[begin_row][begin_col] is None:
            return False
        start_piece = self.__board[begin_row][begin_col]
        # check that the starting piece *is* the current player's
        if start_piece.get_player() != self.__current_turn:
            return False
        #Input the starting coordinate into the piece object.
        # list of valid moves
        if end not in start_piece.get_valid_moves(begin_row, begin_col):
            return False

        # at this point end must be in start_piece.get_valid_moves(begin_row,begin_col)

        if start_piece.get_type() == "Pika" or start_piece.get_type() == "Trilobite": # jumping pieces bypass this following part
            row_direction = 0  # determining the direction of the row to get to destination -1 up, 0 neutral, +1 down
            col_direction = 0  # determining direction of col to get to destination, -1 left, 0 neutral, +1 right
            if end_row > begin_row:
                row_direction = 1 # moving down
            elif end_row < begin_row:
                row_direction = -1 # moving up
            else:
                row_direction = 0

            if end_col > begin_col: # right
                col_direction = 1
            elif end_col < begin_col: # left
                col_direction = -1
            else:
                col_direction = 0

            # now if row_direction = 1 and col_direction = 1 that means its moving down/right direction
            # if row_direction = 1 and col_direction = -1 that means its moving down/left
            # if row_direction = -1 and col_direction is -1 then its moving up/left direcion
            # if row_direction = -1 and col_direction is 1 then its moving up/right direcion

            current_row = begin_row + row_direction
            current_col = begin_col + col_direction
            #step through path to get to end position
            while (current_row, current_col) != (end_row, end_col):
                if self.__board[current_row][current_col] is not None: #if there is a piece in the way
                    return False
                current_row += row_direction
                current_col += col_direction

        # if there is a piece in destination...
        if self.__board[end_row][end_col] is not None:
            end_piece = self.__board[end_row][end_col]
            if end_piece.get_player() == self.__current_turn: # if the piece is friendly
                return False
            elif end_piece.get_player() != self.get_turn():
                # enemy piece is at destination coordinate
                if end_piece.get_type() == "Beluga":
                    self.update_game_state() #update game state for victory!

                if self.get_turn() == "Tangerine":
                    self.get_tangerine_captures().append(end_piece.get_type())
                elif self.get_turn() == "Amethyst":
                    self.get_amethyst_captures().append(end_piece.get_type())

                # remove start piece AND move it to destination
                self.update_board(begin_row, begin_col, None)
                self.update_board(end_row,end_col,start_piece)
                self.update_turn()
                return True

        #remove start piece AND move it to destination
        self.update_board(begin_row, begin_col, None)
        self.update_board(end_row, end_col, start_piece)
        self.update_turn()
        return True

    def print_board(self):
        """Purely for testing, prints board"""
        for row in self.__board:
            for element in row:
                if element is None:
                    print(" ")
                else:
                    print(element)
                print('|')

class Piece:
    """Represents a piece in the game. Has information on which player's piece it is."""

    def __init__(self, player):
        """Initializes the piece and its player. Player is a string parameter """
        self.__player = player

    def get_player(self):
        """Returns the player who owns the piece."""
        return self.__player

    def get_valid_moves(self, row, col):
        """
        Takes row, column(starting coordinate) parameters
         Generates list of valid (row,col) coordinates the piece can move to from the given point based on its
        direction/distance/locomotion. Returns a list of tuples
        """
        return []

    def get_type(self):
        """Returns type of piece"""
        return None

class Pika(Piece):
    """Represents a Pika piece which is orthogonal, moves 4 spaces, sliding"""
    def __init__(self, player):
        """Takes a player string parameter. Initializes Pika piece with the player who owns it."""
        super().__init__(player)

    def get_valid_moves(self, row, col):
        """Takes row, col integer parameters. Creates directional lists up to 4 spaces(up, down, left, right) , and includes coordinates that
        go 1 square in each diagonal direction. Returns all possible valid coordinates as a list of tuples"""
        valid = []
        for i in range(4): #goes from 0 1 2 3
            valid.append((row+i+1,col)) # positive vertical movement
            valid.append((row-i-1,col)) # negative vertical movement
            valid.append((row, col+i+1)) #positive horizontal movement
            valid.append((row, col-i-1)) #negative horizontal movement

        # add the 1 square in each diagonal direction
        valid.append((row - 1, col - 1))
        valid.append((row + 1, col + 1))
        valid.append((row - 1, col + 1))
        valid.append((row + 1, col - 1))

        # comb through afterwards, and remove coordinates that go off the board
        for pair in valid[:]: #have to create copy, because if i remove elements it won't iterate properly
            if pair[0] > 6 or pair[0] < 0:
                valid.remove(pair)
            elif pair[1] > 6 or pair[1] < 0:
                valid.remove(pair)
        return valid

    def get_type(self):
        """Returns type of piece"""
        return "Pika"


class Trilobite(Piece):
    """Represents a Trilobite piece which is diagonal, moves 2 spaces, sliding"""
    def __init__(self, player):
        """Initializes Trilobite piece with the player who owns it."""
        super().__init__(player)

    def get_valid_moves(self, row, col):
        """Takes row, col integer parameters. Creates directional lists up to 2 spaces(up-right, up-left, down-right, down-left),
            and includes coordinates that go 1 square in each orthogonal direction. Returns all
            possible valid coordinates as a list of tuples"""
        valid = []

        for i in range(2): #goes from 0 1
            valid.append((row+i+1,col+i+1)) # up right
            valid.append((row-i-1,col-i-1)) # down right
            valid.append((row-i-1, col+i+1)) # up left
            valid.append((row+i+1, col-i-1)) # down left

        # 1 square orthogonal directions
        valid.append((row, col - 1))
        valid.append((row, col + 1))
        valid.append((row - 1, col))
        valid.append((row + 1, col))

        # comb through afterwards, and remove coordinates that go off the board
        for pair in valid[:]:  # have to create copy, because if i remove elements it won't iterate properly.....ahhh
            if pair[0] > 6 or pair[0] < 0:
                valid.remove(pair)
            elif pair[1] > 6 or pair[1] < 0:
                valid.remove(pair)

        return valid

    def get_type(self):
        """Returns type of piece"""
        return "Trilobite"

class Wombat(Piece):
    """Represents a Wombat piece which is orthogonal, moves 1 space, jumping"""

    def __init__(self, player):
        """Takes a player string parameter. Initializes Wombat piece with the player who owns it."""
        super().__init__(player)

    def get_valid_moves(self, row, col):
        """Takes row, col integer parameters. Creates directional lists up to 1 space, and includes coordinates that go 1 square in each
       diagonal direction. Returns all possible valid coordinates as a list of tuples"""
        valid = []

        # 1 square orthogonal directions
        valid.append((row, col - 1))
        valid.append((row, col + 1))
        valid.append((row - 1, col))
        valid.append((row + 1, col))

        # add the 1 square in each diagonal direction
        valid.append((row - 1, col - 1))
        valid.append((row + 1, col + 1))
        valid.append((row - 1, col + 1))
        valid.append((row + 1, col - 1))

        # comb through afterwards, and remove coordinates that go off the board
        for pair in valid[:]:  # have to create copy, because if i remove elements it won't iterate properly.....ahhh
            if pair[0] > 6 or pair[0] < 0:
                valid.remove(pair)
            elif pair[1] > 6 or pair[1] < 0:
                valid.remove(pair)
        return valid

    def get_type(self):
        """Returns type of piece"""
        return "Wombat"


class Beluga(Piece):
    """Represents a Beluga piece which is diagonal, moves 3 spaces, jumping"""
    def __init__(self, player):
        """Takes a player string parameter. Initializes Beluga piece with the player who owns it."""
        super().__init__(player)

    def get_valid_moves(self, row, col):
        """Takes row, col integer parameters. Creates directional lists that go 3 squares in each diagonal direction or
         one square in each orthogonal direction. Returns all possible valid coordinates as a list of tuples"""
        valid = []

        # 3 spaces diagonally
        valid.append((row+3,col+3)) # up right
        valid.append((row-3,col-3)) # down right
        valid.append((row-3, col+3)) # up left
        valid.append((row+3, col-3)) # down left

        # 1 square orthogonal directions
        valid.append((row, col - 1))
        valid.append((row, col + 1))
        valid.append((row - 1, col))
        valid.append((row + 1, col))

        # comb through afterwards, and remove coordinates that go off the board
        for pair in valid[:]:  # have to create copy, because if i remove elements it won't iterate properly.....ahhh
            if pair[0] > 6 or pair[0] < 0:
                valid.remove(pair)
            elif pair[1] > 6 or pair[1] < 0:
                valid.remove(pair)

        return valid

    def get_type(self):
        """Returns type of piece"""
        return "Beluga"
