# board.py
from piece import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.move_history = []
        self.white_turn = True
        self.white_castle_king_side = True
        self.black_castle_king_side = True

    def to_string(self):
        """
        Convert the current board state to a string representation.
        Basically Forsyth-Edwards Notation (FEN)
        """
        state_str = ""
        for row in self.board:
            for piece in row:
                state_str += piece.symbol if piece else "1"  # Example representation
            state_str += "/"
        return state_str

    def is_game_over(self):
        # check if either king is missing
        white_king_present = any(isinstance(piece, King) and piece.color == "white" for row in self.board for piece in row)
        black_king_present = any(isinstance(piece, King) and piece.color == "black" for row in self.board for piece in row)
        return not white_king_present or not black_king_present

    def setup_board(self):
        # Place black pieces
        self.board[0] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"),
                         King("black"), Bishop("black"), Knight("black"), Rook("black")]
        for i in range(8):
            self.board[1][i] = Pawn("black")

        # Place white pieces
        self.board[7] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"),
                         King("white"), Bishop("white"), Knight("white"), Rook("white")]
        for i in range(8):
            self.board[6][i] = Pawn("white")

    def undo_move(self):
            """
            Revert the last move made on the board.
            """
            if not self.move_history:
                print("No moves to undo.")
                return

            # Get the last move from the history
            start_pos, end_pos, captured_piece = self.move_history.pop()

            # Move the piece back to its original position
            start_row, start_col = start_pos
            end_row, end_col = end_pos
            moving_piece = self.get_piece(end_row, end_col)

            self.board[start_row][start_col] = moving_piece
            self.board[end_row][end_col] = captured_piece  # Restore captured piece, if any

    def get_all_legal_moves(self, color):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    start_pos = (row, col)
                    for end_row in range(8):
                        for end_col in range(8):
                            if piece.move(self, start_pos, (end_row, end_col)):
                                legal_moves.append((start_pos, (end_row, end_col)))
        return legal_moves

    def print_board(self):
        for row in self.board:
            print('  '.join([piece.symbol if piece else '.' for piece in row]))

    def get_piece(self, row, col):
        assert row <= 8 and col <= 8
        return self.board[row][col]

    def is_white_turn(self):
            """Check if it's white's turn."""
            return self.white_turn

    def can_castle_king_side(self, color):
        """Check if castling king-side is possible for the given color."""
        if color == 'white':
            return self.white_castle_king_side
        elif color == 'black':
            return self.black_castle_king_side
        else:
            raise ValueError("Invalid color")

    def move_piece(self, turn, start, end):
      start_row, start_col = start
      end_row, end_col = end
      moving_piece = self.get_piece(start_row, start_col)
      move_to_piece = self.get_piece(end_row, end_col)
      point = 0 # Point received if capture

      if moving_piece and moving_piece.move(self, start, end):
        if turn == moving_piece.color:
          if move_to_piece:
            point = move_to_piece.point
          self.move_history.append((start, end, move_to_piece))
          # Perform the move
          self.board[end_row][end_col] = moving_piece
          self.board[start_row][start_col] = None
          return True, point

        return False, point

      else:
        return False, 0
