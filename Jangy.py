# Author: Sean Henry
# Date: 3/11/21
# Description: This program is for a game of Janggi with 2 players red and blue. It contains an initial setup of a board with each piece in the correct orientation at the beginning of the game. There are methods
#for each piece in the game to make legal moves. The board is setup via algebraic notation 1 through 10 and a - i. The game is finished when the general of the opposing player
#is in check. 

class JanggiGame:
    ''' The JanggiGame Class holds parameters for the board and piece location, the legal moves for each piece, turn taking, the state of the game (who has won or if unfinished
        and allows for the board to be printed'''

    def __init__(self):
        """ Init method containts the board, current turn and game state for unfinished """

        self._board = [
            ['rChariot', 'rElephant', 'rHorse', 'rGuard', ' ', 'rGuard', 'rElephant', 'rHorse', 'rChariot'],
            [' ', ' ', ' ', ' ', 'rGeneral', ' ', ' ', ' ', ' '],
            [' ', 'rCannon', ' ', ' ', ' ', ' ', ' ', 'rCannon', ' '],
            ['rSoldier', ' ', 'rSoldier', ' ', 'rSoldier', ' ', 'rSoldier', ' ', 'rSoldier'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['bSoldier', ' ', 'bSoldier', ' ', 'bSoldier', ' ', 'bSoldier', ' ', 'bSoldier'],
            [' ', 'bCannon', ' ', ' ', ' ', ' ', ' ', 'bCannon', ' '],
            [' ', ' ', ' ', ' ', 'bGeneral', ' ', ' ', ' ', ' '],
            ['bChariot', 'bElephant', 'bHorse', 'bGuard', ' ', 'bGuard', 'bElephant', 'bHorse', 'bChariot']
        ]
        self._current_turn = 'b'  
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """ Get method for the game state"""
        return self._game_state

    def is_in_check(self, color):
        """ Is in check method takes a color as an argument, checks the position of the general based on row and column,  if the location of others pieces
             are in close proximity to the general and can capture in the next move, returns true and otherwise returns false. r = row and c = column"""
        old_turn = self._current_turn
        general_r, general_c = -1, -1
        for row in range(len(self._board)):
          for col in range(len(self._board[row])):
            if self._board[row][col] == color[0] + 'General':
              general_r, general_c = row, col
              break
        general_pos = chr(ord('a') + general_c) + str(general_r + 1)
        for row in range(len(self._board)):
          for col in range(len(self._board[row])):
            if self._board[row][col][0] == ('r' if color[0] == 'b' else 'b'):
              piece = self._board[row][col]
              piece_pos = chr(ord('a') + col) + str(row + 1)
              self._board[general_r][general_c] = ' '
              self._current_turn = 'r' if color[0] == 'b' else 'b'
              is_in_check = self.make_move(piece_pos, general_pos)
              self._current_turn = old_turn
              self._board[general_r][general_c] = color[0] + 'General'
              self._board[row][col] = piece
              if is_in_check:
                return True
        return False
    
    def make_move(self, pos1, pos2):
        ''' This method assigns the piece to the first position and passes a second position that the piece will move. It also allows for a turn to be passed. r = row and c = column'''
        piece = self.get_piece(pos1)
        if piece[0] != self._current_turn:
            return False
        if piece == ' ':
          return False
        if 'WON' in self._game_state:
            return False
        if pos1 == pos2:
            self.pass_turn()
            return True
        if self.get_piece(pos2)[0] == self._current_turn:
            return False

        if piece == 'bSoldier':
            return self.move_blue_soldier(pos1, pos2)
        elif piece == 'rSoldier':
            return self.move_red_soldier(pos1, pos2)
        elif 'Cannon' in piece:
            return self.move_cannon(pos1, pos2)
        elif 'Chariot' in piece:
            return self.move_chariot(pos1, pos2)
        elif 'rGeneral' == piece:
            return self.move_red_general(pos1, pos2)
        elif 'bGeneral' == piece:
            return self.move_blue_general(pos1, pos2)
        elif 'rGuard' == piece:
            return self.move_red_guard(pos1, pos2)
        elif 'bGuard' == piece:
            return self.move_blue_guard(pos1, pos2)
        elif 'rHorse' == piece:
            return self.move_red_horse(pos1, pos2)
        elif 'bHorse' == piece:
            return self.move_blue_horse(pos1, pos2)
        elif 'rElephant' == piece:
            return self.move_red_elephant(pos1, pos2)
        elif 'bElephant' == piece:
            return self.move_blue_elephant(pos1, pos2)
        else:
            return False

    def move_blue_horse(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves blue horse based on starting postion and iterates through board and legal moves. r = row and c = column """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)
        if r1 == r2 and c1 == c2:
          self.pass_turn()
          return True
        if r2 in range(10) and c2 in range(9):
          paths = [
            [(r1+1, c1), (r1+2, c1+1)],
            [(r1+1, c1), (r1+2, c1-1)],
            [(r1, c1+1), (r1+1, c1+2)],
            [(r1, c1+1), (r1-1, c1+2)],
            [(r1-1, c1), (r1-2, c1-1)],
            [(r1-1, c1), (r1-2, c1+1)],
            [(r1, c1-1), (r1-1, c1-2)],
            [(r1, c1-1), (r1+1, c1-2)]
          ]
          for path in paths:
            if path[-1][0] == r2 and path[-1][1] == c2:
              for (r, c) in path[:-1]:
                if self._board[r][c] != ' ':
                  return False
              if self._board[r2][c2] == ' ':
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'bHorse'
                self.pass_turn()
                return True
              elif self._board[r2][c2][0] == 'b':
                return False
              else:
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'bHorse'
                self.pass_turn()
                return True
          return False
        else:
          return False

    def move_red_horse(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves red horse based on starting postion and iterates through paths board and legal moves. r = row and c = column """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)
        if r1 == r2 and c1 == c2:
          self.pass_turn()
          return True
        if r2 in range(10) and c2 in range(9):
          paths = [
            [(r1+1, c1), (r1+2, c1+1)],
            [(r1+1, c1), (r1+2, c1-1)],
            [(r1, c1+1), (r1+1, c1+2)],
            [(r1, c1+1), (r1-1, c1+2)],
            [(r1-1, c1), (r1-2, c1-1)],
            [(r1-1, c1), (r1-2, c1+1)],
            [(r1, c1-1), (r1-1, c1-2)],
            [(r1, c1-1), (r1+1, c1-2)]
          ]
          for path in paths:
            if path[-1][0] == r2 and path[-1][1] == c2:
              for (r, c) in path[:-1]:
                if self._board[r][c] != ' ':
                  return False
              if self._board[r2][c2] == ' ':
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'rHorse'
                self.pass_turn()
                return True
              elif self._board[r2][c2][0] == 'r':
                return False
              else:
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'rHorse'
                self.pass_turn()
                return True
          return False
        else:
          return False

    def move_red_elephant(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves red elephant based on starting postion and iterates through paths based on board and legal moves. 
            Moves one space forward and 2 diagonal spaces. r = row and c = column """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)
        if r1 == r2 and c1 == c2:
          self.pass_turn()
          return True
        if r2 in range(10) and c2 in range(9):
          paths = [
            [(r1+1, c1), (r1+2, c1+1), (r1+3, c1+2)],
            [(r1+1, c1), (r1+2, c1-1), (r1+3, c1-2)],
            [(r1, c1+1), (r1+1, c1+2), (r1+2, c1+3)],
            [(r1, c1+1), (r1-1, c1+2), (r1-2, c1+3)],
            [(r1-1, c1), (r1-2, c1-1), (r1-3, c1-2)],
            [(r1-1, c1), (r1-2, c1+1), (r1-3, c1+2)],
            [(r1, c1-1), (r1-1, c1-2), (r1-2, c1-3)],
            [(r1, c1-1), (r1+1, c1-2), (r1+2, c1-3)]
          ]
          for path in paths:
            if path[-1][0] == r2 and path[-1][1] == c2:
              for (r, c) in path[:-1]:
                if self._board[r][c] != ' ':
                  return False
              if self._board[r2][c2] == ' ':
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'rElephant'
                self.pass_turn()
                return True
              elif self._board[r2][c2][0] == 'r':
                return False
              else:
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'rElephant'
                self.pass_turn()
                return True
          return False
        else:
          return False
    
    def move_blue_elephant(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves blue elephant based on starting postion and iterates through paths based on board and legal moves. 
            Moves on space forward and two diagonol spaces. r = row and c = column """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)
        if r1 == r2 and c1 == c2:
          self.pass_turn()
          return True
        if r2 in range(10) and c2 in range(9):
          paths = [
            [(r1+1, c1), (r1+2, c1+1), (r1+3, c1+2)],
            [(r1+1, c1), (r1+2, c1-1), (r1+3, c1-2)],
            [(r1, c1+1), (r1+1, c1+2), (r1+2, c1+3)],
            [(r1, c1+1), (r1-1, c1+2), (r1-2, c1+3)],
            [(r1-1, c1), (r1-2, c1-1), (r1-3, c1-2)],
            [(r1-1, c1), (r1-2, c1+1), (r1-3, c1+2)],
            [(r1, c1-1), (r1-1, c1-2), (r1-2, c1-3)],
            [(r1, c1-1), (r1+1, c1-2), (r1+2, c1-3)]
          ]
          for path in paths:
            if path[-1][0] == r2 and path[-1][1] == c2:
              for (r, c) in path[:-1]:
                if self._board[r][c] != ' ':
                  return False
              if self._board[r2][c2] == ' ':
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'bElephant'
                self.pass_turn()
                return True
              elif self._board[r2][c2][0] == 'b':
                return False
              else:
                self._board[r1][c1] = ' '
                self._board[r2][c2] = 'bElephant'
                self.pass_turn()
                return True
          return False
        else:
          return False

    def move_red_guard(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves based on red generals parameters.  """
        return self.move_red_general(pos1, pos2)

    def move_blue_guard(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves based on blue generals parameters.  """
        return self.move_blue_general(pos1, pos2)

    def move_red_general(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves within the column and rows of the "palace". r = row and c = palace. """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)

        if (r1, c1) == (0, 3) and (r2, c2) in [(0, 4), (1, 3), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (0, 4) and (r2, c2) in [(0, 3), (0, 5), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (0, 5) and (r2, c2) in [(0, 4), (1, 5), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (1, 3) and (r2, c2) in [(0, 3), (2, 3), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (1, 5) and (r2, c2) in [(0, 5), (2, 5), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (2, 3) and (r2, c2) in [(1, 3), (2, 4), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (2, 4) and (r2, c2) in [(2, 3), (2, 5), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (2, 5) and (r2, c2) in [(2, 4), (1, 5), (1, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (1, 4) and abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
            return self.move(r1, c1, r2, c2)
        else:
            return False

    def move_blue_general(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Moves within the column and rows of the "palace". r = row and c = palace. """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)

        if (r1, c1) == (7, 3) and (r2, c2) in [(7, 4), (8, 3), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (7, 4) and (r2, c2) in [(7, 3), (7, 5), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (7, 5) and (r2, c2) in [(7, 4), (8, 5), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (8, 3) and (r2, c2) in [(7, 3), (9, 3), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (8, 5) and (r2, c2) in [(7, 5), (9, 5), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (9, 3) and (r2, c2) in [(8, 3), (9, 4), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (9, 4) and (r2, c2) in [(9, 3), (9, 5), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (9, 5) and (r2, c2) in [(9, 4), (8, 5), (8, 4)]:
            return self.move(r1, c1, r2, c2)
        elif (r1, c1) == (8, 4) and abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
            return self.move(r1, c1, r2, c2)
        else:
            return False

    def move_chariot(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Can move horizontally, vertically, or diagonally in palace. r = row and c = palace. """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)

        # 1. Move horizontally
        if r1 == r2:
            pieces, _ = self.count_between_columns(c1, c2, r1)
            if pieces == 0:
                return self.move(r1, c1, r2, c2)
            return False
        # 2. Move vertically
        elif c1 == c2:
            pieces, _ = self.count_between_rows(r1, r2, c1)
            if pieces == 0:
                return self.move(r1, c1, r2, c2)
            return False
        # 3. Move diagonally in either palace
        #    In the red palace
        elif (r1, c1) == (0, 3):
            if (r2, c2) == (1, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (2, 5) and self._board[2][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (0, 5):
            if (r2, c2) == (1, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (2, 3) and self._board[2][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (1, 3):
            if (r2, c2) == (1, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (0, 5) and self._board[2][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (2, 5):
            if (r2, c2) == (1, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (0, 3) and self._board[2][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (1, 4):
            if (r2, c2) in [(0, 3), (0, 5), (2, 3), (2, 5)]:
                return self.move(r1, c1, r2, c2)
            else:
                return False
        #    In the blue palace
        elif (r1, c1) == (7, 3):
            if (r2, c2) == (8, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (9, 5) and self._board[8][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (7, 5):
            if (r2, c2) == (8, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (9, 3) and self._board[8][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (9, 3):
            if (r2, c2) == (8, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (7, 5) and self._board[8][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (9, 5):
            if (r2, c2) == (8, 4):
                return self.move(r1, c1, r2, c2)
            elif (r2, c2) == (7, 3) and self._board[8][4] == ' ':
                return self.move(r1, c1, r2, c2)
            else:
                return False
        elif (r1, c1) == (8, 4):
            if (r2, c2) in [(7, 3), (7, 5), (9, 3), (9, 5)]:
                return self.move(r1, c1, r2, c2)
            else:
                return False
        else:
            return False

    def move_cannon(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Can move horizontally, vertically, or diagonally in palace. r = row and c = palace. """
        # A cannon may also not capture another cannon.
        if 'Cannon' in self.get_piece(pos2):
            return False

        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)

        # 1. Move horizontally
        if r1 == r2:
            pieces, cannons = self.count_between_columns(c1, c2, r1)
            if pieces == 1 and cannons == 0:
                return self.move(r1, c1, r2, c2)
            return False
        # 2. Move vertically
        elif c1 == c2:
            pieces, cannons = self.count_between_rows(r1, r2, c1)
            if pieces == 1 and cannons == 0:
                return self.move(r1, c1, r2, c2)
            return False
        # 3. Move diagonally in either palace
        elif self.is_in_blue_palace(r1, c1):
            if (r1, c1) == (7, 3) and (r2, c2) == (9, 5) and self._board[8][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (9, 5) and (r2, c2) == (7, 3) and self._board[8][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (9, 3) and (r2, c2) == (7, 5) and self._board[8][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (7, 5) and (r2, c2) == (9, 3) and self._board[8][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            return False
        elif self.is_in_red_palace(r1, c1):
            if (r1, c1) == (0, 3) and (r2, c2) == (2, 5) and self._board[1][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (2, 5) and (r2, c2) == (0, 3) and self._board[1][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (2, 3) and (r2, c2) == (0, 5) and self._board[1][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (0, 5) and (r2, c2) == (2, 3) and self._board[1][4] != ' ' and not 'Cannon' in self._board[8][4]:
                return self.move(r1, c1, r2, c2)
            return False
        else:
            return False

    def is_in_blue_palace(self, r, c):
        """ Accepts 2 arguments for row and column for blue palace along with boundaries """
        return 7 <= r <= 9 and 3 <= c <= 5

    def is_in_red_palace(self, r, c):
        """ Accepts 2 arguments for row and column for red palace along with boundaries """
        return 0 <= r <= 2 and 3 <= c <= 5

    def count_between_rows(self, r1, r2, c):
        """ Allows for cannon to jump other pieces in rows. r = rows and c = columns"""
        pieces = 0
        cannons = 0

        if r1 > r2:
            r1, r2 = r2, r1

        for r in range(r1 + 1, r2):
            if self._board[r][c] != ' ':
                pieces += 1
            if 'Cannon' in self._board[r][c]:
                cannons += 1

        return pieces, cannons

    def count_between_columns(self, c1, c2, r):
        """ Allows for cannon to jump other pieces in columns. r = rows and c = columns"""
        pieces = 0
        cannons = 0

        if c1 > c2:
            c1, c2 = c2, c1

        for c in range(c1 + 1, c2):
            if self._board[r][c] != ' ':
                pieces += 1
            if 'Cannon' in self._board[r][c]:
                cannons += 1

        return pieces, cannons

    def move_blue_soldier(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Parameter for reaching end of the board, can move straight and sideways. r = row and c = palace. """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)

        # 1. Reach the end of the board
        if r1 == 0:
            if r2 != 0 or abs(c1 - c2) != 1:
                return False
            return self.move(r1, c1, r2, c2)

            # 2. Move straight forward
        if c1 == c2 and r1 != r2:
            if r1 - r2 != 1:
                return False
            return self.move(r1, c1, r2, c2)

        # 3. Move sideways
        if r1 == r2 and c1 != c2:
            if abs(c1 - c2) != 1:
                return False
            return self.move(r1, c1, r2, c2)

        # 4. In the enemy palace
        if 0 <= r1 <= 2 and 3 <= c1 <= 5:
            if (r1, c1) in [(2, 3), (2, 5)] and (r2, c2) == (1, 4):
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (1, 4) and (r2, c2) in [(0, 3), (0, 5)]:
                return self.move(r1, c1, r2, c2)
            return False

        return False

    def move_red_soldier(self, pos1, pos2):
        """ Takes 2 arguments for current and secondary position. Parameter for reaching end of the board, can move straight and sideways. r = row and c = palace. """
        r1, c1 = self.convert(pos1)
        r2, c2 = self.convert(pos2)

        # 1. Reach the end of the board
        if r1 == 9:
            if r2 != 9 or abs(c1 - c2) != 1:
                return False
            return self.move(r1, c1, r2, c2)

            # 2. Move straight forward
        if c1 == c2 and r1 != r2:
            if r2 - r1 != 1:
                return False
            return self.move(r1, c1, r2, c2)

        # 3. Move sideways
        if r1 == r2 and c1 != c2:
            if abs(c1 - c2) != 1:
                return False
            return self.move(r1, c1, r2, c2)

        # 4. In the enemy palace
        if 7 <= r1 <= 9 and 3 <= c1 <= 5:
            if (r1, c1) in [(7, 3), (7, 5)] and (r2, c2) == (8, 4):
                return self.move(r1, c1, r2, c2)
            if (r1, c1) == (8, 4) and (r2, c2) in [(9, 3), (9, 5)]:
                return self.move(r1, c1, r2, c2)
            return False

        return False

    def move(self, r1, c1, r2, c2):
        """ Method for moving pieces along the board """
        self._board[r2][c2] = self._board[r1][c1]
        self._board[r1][c1] = ' '
        self.pass_turn()
        return True

    def pass_turn(self):
        """ Method for passing a turn when no legal moves can be made """
        if self._current_turn == 'b':
            self._current_turn = 'r'
        else:
            self._current_turn = 'b'

    def get_piece(self, pos):
        """ Get method for pieces and position. """
        row, col = self.convert(pos)
        return self._board[row][col]

    def convert(self, pos):
        """ Converts column and rows on board to take 'a1' style notation """
        col = ord(pos[0]) - ord('a')
        row = int(pos[1:]) - 1
        return row, col

    def print_board(self):
      """ Print board method to help visualize the game board and debug """
      print('   |  ', end='')
      for i in range(len(self._board[0])):
        print(chr(ord('a') + i), end='  |  ')
      print('\n---|-----|-----|-----|-----|-----|-----|-----|-----|-----|')
      for row in range(len(self._board)):
        print('{:2d} |  '.format(row+1), end='')
        for cell in self._board[row]:
          if cell == ' ':
            print('   | ', end='')
          else:
            print('{} | '.format(cell[:2]), end='')
          print(' ', end='')
        print('\n---|-----|-----|-----|-----|-----|-----|-----|-----|-----|')

#game = JanggiGame()

#game.print_board()
#game.make_move('b10','d7')
#game.make_move('g4','g5')
#game.make_move('e7','e6')
#game.make_move('e4','e5')
#game.make_move('d7','g5')
#print('##############################################')
#game.print_board()

#print(game.is_in_check('red'))
