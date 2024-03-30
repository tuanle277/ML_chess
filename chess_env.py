import numpy as np
from piece import *
from board import *
import pygame
from constants import *

pygame.init()
FONT = pygame.font.SysFont('Arial', 48)

class ChessEnv:
    def __init__(self):
        self.board = Board()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))  # Pygame window for drawing
        pygame.display.set_caption("Chess Visualization")

    def reset(self):
        """
        Reset the board to the initial state.
        Game history to prevent repetitive moves
        """
        self.board = Board()  # Reinitialize the board

    def is_game_over(self):
        # check if either king is missing
        white_king_present = any(isinstance(piece, King) and piece.color == "white" for row in self.board.board for piece in row)
        black_king_present = any(isinstance(piece, King) and piece.color == "black" for row in self.board.board for piece in row)
        return not white_king_present or not black_king_present

    def get_legal_moves(self, color):
        """Get all legal moves for the given color."""
        return self.board.get_all_legal_moves(color)

    def has_won(self, color):
        # Simplified check: Assume win if opponent's king is not found
        opponent_color = "black" if color == "white" else "white"
        for row in self.board:
            for piece in row:
                if piece and piece.color == opponent_color and isinstance(piece, King):
                    return False  # Opponent's king found, game not won by current player
        return True  # Opponent's king not found, current player has won

    def get_piece_value(self, piece):
        if piece is None:
            return 0

        return piece.point

    def make_move(self, move, color):
        """Try to make a move and return whether it was successful, and any points scored."""
        start, end = move
        move_success, points = self.board.move_piece(color, start, end)

        if not move_success:
            return None, -0.1, False  # Small negative reward for illegal move

        # if self.is_game_over():
        #     if self.has_won(color):
        #         reward = 1  # Win
        #     else:
        #         reward = -1  # Loss
        #     return self.get_board_state(), reward, True

        # Optional: Incremental rewards for capturing a piece
        # reward = self.get_piece_value(captured_piece) if captured_piece else 0

        # return self.get_board_state(), reward, False
        return move_success, points

    def draw(self):
        print("drawing board....")

        self.win.fill(BLACK)
        for row in range(ROWS):
            for col in range(ROWS):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(self.win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = self.board.get_piece(row, col)
                if piece:
                    text = FONT.render(piece.symbol, True, WHITE if piece.color == "white" else BLACK)
                    self.win.blit(text, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))
        pygame.display.update()
        print("board drawn!")


    def get_board_state(self):
        # Map each piece type to an index
        piece_to_index = {
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11,
        }
        # Initialize an empty state representation
        state = np.zeros((12, 8, 8), dtype=np.float32)

        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    # Use the symbol of the piece to determine the channel
                    channel = piece_to_index[piece.symbol]
                    state[channel, row, col] = 1
        return state


    def render(self):
        """Print the board to the console."""
        self.board.print_board()
