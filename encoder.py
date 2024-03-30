import torch
import random

from torch.nn.modules.container import ParameterDict

def encode_board_state(board):
    """
    Encode the board state into a tensor suitable for neural network input.

    :param board: A 2D array representing the board state, with each cell containing a piece object or None.
    :return: A PyTorch tensor of shape (1, 12, 8, 8) representing the encoded board state.
    """
    # Initialize an empty tensor with zeros. Shape: (15, 8, 8).
    # 15 channels for the pieces: PW, NW, BW, RW, QW, KW, PB, NB, BB, RB, QB, KB (P=pawn, N=knight, B=bishop, R=rook, Q=queen, K=king, W=white, B=black)
    encoded_board = torch.zeros((12, 8, 8), dtype=torch.float32)

    piece_to_channel = {
        'PW': 0, 'NW': 1, 'BW': 2, 'RW': 3, 'QW': 4, 'KW': 5,
        'PB': 6, 'NB': 7, 'BB': 8, 'RB': 9, 'QB': 10, 'KB': 11
    }

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None:
                symbol = piece.symbol.upper() if piece.color == 'white' else piece.symbol.lower()
                color = 'W' if piece.color == 'white' else 'B'
                channel = piece_to_channel[f'{symbol.upper()}{color}']
                encoded_board[channel, row, col] = 1

    # Channel 12: Whose turn it is (1 for white's turn, 0 for black's turn)
    # encoded_board[12, :, :] = 1 if board.is_white_turn() else 0
    # # Channel 13: Can white castle king-side
    # encoded_board[13, :, :] = 1 if board.can_castle_king_side('white') else 0
    # # Channel 14: Can black castle king-side
    # encoded_board[14, :, :] = 1 if board.can_castle_king_side('black') else 0

    assert encoded_board.shape[0] == 12
    # Add an extra dimension at the beginning to indicate batch size of 1
    encoded_board = encoded_board.unsqueeze(0)
    return encoded_board

def decode_move(move_index, board, legal_moves):
  if legal_moves:
    # Ensure move_index is within bounds, otherwise pick a random legal move
    if move_index >= len(legal_moves):
      print("Predicted move index is out of bounds, selecting a random legal move.")
      return random.choice(legal_moves)
    return legal_moves[move_index]
  else:
    print("No legal moves available.")
    return None

def predict_move(model, board, color):
    board_tensor = encode_board_state(board)
    legal_moves = board.get_all_legal_moves(color)
    print(board, board_tensor.shape)
    with torch.no_grad():
        output = model(board_tensor)
        predicted_move_index = output.argmax(1).item()
    return decode_move(predicted_move_index, board, legal_moves)

def select_legal_move(model_output, legal_moves):
    """
    Filters the model's output to only consider legal moves.

    :param model_output: The softmax output of the chess model.
    :param legal_moves: A list of legal moves in the current game state.
    :return: The index of a legal move selected based on model output probabilities.
    """
    # Assume legal_moves are encoded in some format that matches model output indices
    # Filter model outputs to only include legal moves
    legal_probs = model_output[0, legal_moves]
    legal_move_index = legal_probs.argmax().item()  # Index of the highest probability legal move

    assert len(legal_probs) == len(legal_moves)
    # Map back to the original list of legal move
    # selected_move = legal_moves[legal_move_index]
    return legal_move_index
