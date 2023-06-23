import constants as c
import random

class Board:
    def __init__(self, player1_mark, player2_mark):
        self.board = [['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],  # board[0][0-6]
                      ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],  # board[1][0-6}
                      ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                      ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                      ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                      ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪']]
        self.rows = 6
        self.columns = 7
        self.bitboard_one = 0
        self.bitboard_two = 0
        self.player1_mark = player1_mark
        self.player2_mark = player2_mark

    def make_move(self, column, player):
        height = 5
        while (self.bitboard_one | self.bitboard_two) & (1 << (column + height * 7)):
            height -= 1

        move = 1 << (column + height * 7)

        if player == 1:
            self.bitboard_one |= move
        else:
            self.bitboard_two |= move

    def remove_piece(self, column):
        height = 0
        while not (self.bitboard_one & (1 << (column + height * 7)) or self.bitboard_two & (1 << (column + height * 7))):
            height += 1
            if height > 5:
                break
        move = 1 << (column + height * 7)

        self.bitboard_one &= ~move
        self.bitboard_two &= ~move

    def is_valid_move(self, column):
        if column < 0 or column >= 7:
            return False
        return ((self.bitboard_one | self.bitboard_two) & (1 << column)) == 0

    def is_terminal(self):
        winning_patterns = [
            0b111100000000000000000000000000000000000000,  # Horizontal
            0b011110000000000000000000000000000000000000,
            0b001111000000000000000000000000000000000000,
            0b000111100000000000000000000000000000000000,
            0b000000011110000000000000000000000000000000,
            0b000000001111000000000000000000000000000000,
            0b000000000111100000000000000000000000000000,
            0b000000000011110000000000000000000000000000,
            0b000000000000001111000000000000000000000000,
            0b000000000000000111100000000000000000000000,
            0b000000000000000011110000000000000000000000,
            0b000000000000000001111000000000000000000000,
            0b000000000000000000000111100000000000000000,
            0b000000000000000000000011110000000000000000,
            0b000000000000000000000001111000000000000000,
            0b000000000000000000000000111100000000000000,
            0b000000000000000000000000000011110000000000,
            0b000000000000000000000000000001111000000000,
            0b000000000000000000000000000000111100000000,
            0b000000000000000000000000000000011110000000,
            0b000000000000000000000000000000000001111000,
            0b000000000000000000000000000000000000111100,
            0b000000000000000000000000000000000000011110,
            0b000000000000000000000000000000000000001111,

            0b100000010000001000000100000000000000000000,  # Vertical
            0b000000010000001000000100000010000000000000,
            0b000000000000001000000100000010000001000000,
            0b010000001000000100000010000000000000000000,
            0b000000001000000100000010000001000000000000,
            0b000000000000000100000010000001000000100000,
            0b001000000100000010000001000000000000000000,
            0b000000000100000010000001000000100000000000,
            0b000000000000000010000001000000100000010000,
            0b000100000010000001000000100000000000000000,
            0b000000000010000001000000100000010000000000,
            0b000000000000000001000000100000010000001000,
            0b000010000001000000100000010000000000000000,
            0b000000000001000000100000010000001000000000,
            0b000000000000000000100000010000001000000100,
            0b000001000000100000010000001000000000000000,
            0b000000000000100000010000001000000100000000,
            0b000000000000000000010000001000000100000010,
            0b000000100000010000001000000100000000000000,
            0b000000000000010000001000000100000010000000,
            0b000000000000000000001000000100000010000001,

            0b000100000001000000010000000100000000000000,  # Diagonal (bottom-right to top-left)
            0b001000000010000000100000001000000000000000,
            0b000000000010000000100000001000000010000000,
            0b010000000100000001000000010000000000000000,
            0b000000000100000001000000010000000100000000,
            0b000000000000000001000000010000000100000001,
            0b100000001000000010000000100000000000000000,
            0b000000001000000010000000100000001000000000,
            0b000000000000000010000000100000001000000010,
            0b000000010000000100000001000000010000000000,
            0b000000000000000100000001000000010000000100,
            0b000000000000001000000010000000100000001000,

            0b000100000100000100000100000000000000000000, # Diagonal (top-right to bottom-left)
            0b000010000010000010000010000000000000000000,
            0b000000000010000010000010000010000000000000,
            0b000001000001000001000001000000000000000000,
            0b000000000001000001000001000001000000000000,
            0b000000000000000001000001000001000001000000,
            0b000000100000100000100000100000000000000000,
            0b000000000000100000100000100000100000000000,
            0b000000000000000000100000100000100000100000,
            0b000000000000010000010000010000010000000000,
            0b000000000000000000010000010000010000010000,
            0b000000000000000000001000001000001000001000
        ]

        # Iterate over the winning patterns
        for pattern in winning_patterns:
            if self.bitboard_one & pattern == pattern:
                return self.player1_mark
            if self.bitboard_two & pattern == pattern:
                return self.player2_mark

        # check for tie
        if bin(self.bitboard_one | self.bitboard_two).count('1') >= 42:
            return 'TIE'
        return None



    # def distance_from_specific_number(num):
    #     def distance_key(x):
    #         return abs(x - num)
    #     return distance_key

    def get_valid_moves(self):
        moves = [col for col in [3, 2, 4, 1, 5, 0, 6] if self.is_valid_move(col)]
        # ordered_moves = sorted(moves, key=Board.distance_from_specific_number(3))
        return moves

    def get_cell(self, row, col):
        mask = 1 << (col + row * 7)
        if self.bitboard_one & mask:
            return self.player1_mark
        if self.bitboard_two & mask:
            return self.player2_mark
        return '⚪'

    def print_bitboard(self):
        print(bin(self.bitboard_one))
        print(bin(self.bitboard_two))
        for row in range(6):
            line = '|'
            for col in range(7):
                mask = 1 << (col + row * 7)
                if self.bitboard_one & mask:
                    line += 'X|'
                elif self.bitboard_two & mask:
                    line += 'O|'
                else:
                    line += ' |'
            print(line)
        print('-------------')

    def get_board(self):
        return self.board

    def get_printable_board(self):
        return f'{"|".join(c.reactions)} \n {"|".join(self.board[0])} \n {"|".join(self.board[1])} \n {"|".join(self.board[2])} \n {"|".join(self.board[3])} \n {"|".join(self.board[4])} \n {"|".join(self.board[5])}'

    def bitboard_to_board(self):
        for row in range(self.rows):
            for col in range(self.columns):
                mask = 1 << (col + row * 7)
                if self.bitboard_one & mask:
                    self.board[row][col] = self.player1_mark
                elif self.bitboard_two & mask:
                    self.board[row][col] = self.player2_mark
                else:
                    self.board[row][col] = '⚪'

    def board_to_bitboard(self):
        for row in range(self.rows):
            for col in range(self.columns):
                mask = 1 << (col + row * 7)
                if self.board[row][col] == self.player1_mark:
                    self.bitboard_one |= mask
                elif self.board[row][col] == self.player2_mark:
                    self.bitboard_two |= mask