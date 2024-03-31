import pygame
import sys
from board import Board  # Make sure board.py is in the same directory
from player import Player
import random
from encoder import *
from model import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Font for drawing text on the board
FONT = pygame.font.SysFont('Arial', 48)

# white_player, black_player = Player("white"), Player("black")

# Usage example:
model_path = 'trained_chess_model.pth'
device = 'cpu'  # or 'cuda' if using GPU
model = load_model(model_path, device)

def draw_board(win, board):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(ROWS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.get_piece(row, col)
            if piece:
                text = FONT.render(piece.symbol, True, WHITE if piece.color == "white" else BLACK)
                win.blit(text, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))

def main():
    clock = pygame.time.Clock()
    board = Board()  # Assuming the Board class initializes the chessboard with pieces
    selected_piece = None  # Tracks the currently selected piece
    selected_pos = None  # Tracks the position (row, col) of the selected piece
    turn = "white"

    running = True
    while running:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False

          elif turn == "white" and event.type == pygame.MOUSEBUTTONDOWN:
              x, y = event.pos
              col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
              selected_pos = (row, col)

              if selected_piece: # if selected_piece not None, meaning there is a piece selected
                  x, y = event.pos
                  end_pos = (y // SQUARE_SIZE, x // SQUARE_SIZE)
                  move_piece = board.move_piece(turn, selected_piece, end_pos)
                  print(board.print_board())
                  if move_piece[0]:
                      selected_piece = None
                      point = move_piece[1]
                      turn = "black"
                  else:
                      selected_piece = end_pos
              else:
                  selected_piece =  selected_pos

              # print(f"Selected piece at {selected_pos}, the piece is {selected_piece}")
      if turn == "black":
          # Here, instead of selecting a random move, use the model to predict the move
          predicted_move = predict_move(model, board, turn)
          if predicted_move:
              start_pos, end_pos = predicted_move
              if start_pos == end_pos:
                predicted_move = predict_move(model, board, turn)
              else:
                board.move_piece(turn, start_pos, end_pos)
                turn = "white"
          else:
              print("No legal moves available for black")  # This scenario shouldn't normally happen

      if board.is_game_over():
        pygame.quit()
        sys.exit()

      draw_board(WIN, board)
      pygame.display.update()
      clock.tick(FPS)

if __name__ == "__main__":
    main()
