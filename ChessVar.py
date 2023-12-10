# Author: Rajvi Rajput
# GitHub username: rrajput22
# Date: 11/26/2023
# Description: Program that acts as a chess game, with methods for making moves for different pieces, checking game
# state, finding out winner based on the captured pieces

class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type

    def validate_move(self, start_row, start_col, end_row, end_col):
        """
        Method to validate the move based on the rules of ChessVar
        :param start_row: Row index of the starting position
        :param start_col: Column index of the starting position
        :param end_row: Row index of the ending position
        :param end_col: Column index of the ending position
        :return: True if the move is valid, False if not
        """
        if self.piece_type == 'Pawn':
            # Pawn move validation logic
            if self.color == 'WHITE':
                return (
                    (end_col == start_col and end_row == start_row - 1) or  # Move forward one square
                    # Move forward two squares on first move
                    (start_row == 6 and end_col == start_col and end_row == start_row - 2)
                )
            elif self.color == 'BLACK':
                return (
                    (end_col == start_col and end_row == start_row + 1) or  # Move forward one square
                    # Move forward two squares on first move
                    (start_row == 1 and end_col == start_col and end_row == start_row + 2)
                )

        elif self.piece_type == 'Knight':
            # Knight move validation logic
            # represents the vertical dist moved by knight
            row_diff = abs(start_row - end_row)
            # represents horizontal dist moved
            col_diff = abs(start_col - end_col)
            # check if knight moves in L shape
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

        elif self.piece_type == 'King':
            # King move validation logic, check if moving only 1 square in any direction
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

        elif self.piece_type == 'Queen':
            # Queen move validation logic, check if moving horizontal or vertical or diagonal
            return (
                # Horizontal or vertical movement
                    start_row == end_row or start_col == end_col or
                    # Diagonal movement
                    abs(start_row - end_row) == abs(start_col - end_col)
            )

        # allow the move if no specific conditions are met
        return True


class ChessVar:
    def __init__(self):
        # Using list comprehension to initialize the game board, set current player to white at start and
        # set game state to unfinished at start
        self.game_board = [[' ' for _ in range(8)] for _ in range(8)]
        self.current_player = 'WHITE'
        self.game_state = 'UNFINISHED'

    def get_game_state(self):
        """
        Method to return the current state of the game.
        :return: 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'
        """
        return self.game_state

    def make_move(self, start_square, end_square):
        """
        Method to make a move on the ChessVar board.
        :param start_square: The square player wants to move a piece from
        :param end_square: The square player wants to move a piece to
        :return: True if the move is successful, False if not
        """
        if self.game_state != 'UNFINISHED':
            return False

        # convert to row and coloumn
        start_row, start_col = 8 - int(start_square[1]), ord(start_square[0]) - ord('a')
        end_row, end_col = 8 - int(end_square[1]), ord(end_square[0]) - ord('a')

        # Make the move
        self.game_board[end_row][end_col] = self.game_board[start_row][start_col]
        self.game_board[start_row][start_col] = ' '

        # Check for captured pieces and update game state
        captured_player = 'BLACK' if self.current_player == 'WHITE' else 'WHITE'
        self.update_game_state(captured_player, end_row, end_col)

        # Switch player turn
        self.current_player = 'BLACK' if self.current_player == 'WHITE' else 'WHITE'

        return True

    def is_white_piece(self, row, col):
        """
        Method to check if piece at a specific row and column is white
        :return: True if white piece, false if not
        """
        return self.game_board[row][col].isupper()

    def is_black_piece(self, row, col):
        """
        Method to check if piece at a specific row and column is black
        :return: True if black piece, false if not
        """
        return self.game_board[row][col].islower()

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """
        Method to check if the move is valid based on the rules of ChessVar
        :param start_row: Row index of the starting position
        :param start_col: Column index of the starting position
        :param end_row: Row index of the ending position
        :param end_col: Column index of the ending position
        :return: True if the move is valid, False otherwise
        """
        # check if starting square is not valid, ending square is not valid, starting square is empty, current player
        # doesn't have a piece at the starting square
        if (
            not self.is_valid_square(start_row, start_col) or
            not self.is_valid_square(end_row, end_col) or
            self.game_board[start_row][start_col] == ' ' or
            self.current_player == 'WHITE' and not self.is_white_piece(start_row, start_col) or
            self.current_player == 'BLACK' and not self.is_black_piece(start_row, start_col)
        ):
            return False

        # Get the piece at the starting position
        piece = Piece(self.current_player, self.game_board[start_row][start_col])

        # Validate the move based on the piece type
        return piece.validate_move(start_row, start_col, end_row, end_col)

    def update_game_state(self, captured_player):
        """
        Method to update state of the game based on the current position of the board
        :param captured_player: The player whose piece was captured ('WHITE' or 'BLACK').
        :return: returns nothing
        """
        # Check if all pieces of the captured player are captured, if captured then the other player has won
        if all(piece.islower() for row in self.game_board for piece in row if piece.isalpha()):
            if captured_player == 'WHITE':
                self.game_state = 'BLACK_WON'
            else:
                self.game_state = 'WHITE_WON'
        else:
            self.game_state = 'UNFINISHED'
