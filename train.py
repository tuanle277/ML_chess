import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import numpy as np
from chess_env import *  # This is a placeholder; you need an actual environment
from model import ChessModel  # Ensure this matches your actual model definition
from encoder import encode_board_state, decode_move, select_legal_move
from board import Board
import os
import pygame
import constants

class ChessDataset(Dataset):
    """Chess dataset for loading self-play data."""
    def __init__(self, states, moves):
        self.states = states
        self.moves = moves

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return self.states[idx], self.moves[idx]

def train_model(model, epochs, learning_rate, self_play_data):
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        dataset = ChessDataset(self_play_data['states'], self_play_data['moves'])
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

        model.train()
        total_loss = 0

        for states, moves in dataloader:
            states = torch.tensor(states, dtype=torch.float)
            moves = torch.tensor(moves, dtype=torch.long)

            optimizer.zero_grad()
            outputs = model(states)
            loss = F.cross_entropy(outputs, moves)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f'Epoch {epoch+1}, Loss: {total_loss/len(dataloader)}')

def generate_self_play_data(model, games):
    data = {'states': [], 'moves': []}
    # print("Chess environment creating...")
    env = ChessEnv()  # Ensure ChessEnv is properly defined and integrated with your model
    # print("Chess environment created!")
    clock = pygame.time.Clock()

    total_moves = 0  # Track the total number of moves for all games

    for game_index in range(1, games + 1):
      print("___________")
      env.reset()
      game_moves = 0  # Track the number of moves for the current game
      turn = "white"
      recent_moves = []

      while not env.is_game_over():
        turn = "white" if turn == "black" else "black"

        # print("Getting board state...")
        state_tensor = env.get_board_state()  # Assuming this returns a PyTorch tensor directly
        state_tensor = torch.from_numpy(state_tensor).float()  # Convert NumPy array to PyTorch tensor and ensure float type
        # print("Getting board state completed!")

        with torch.no_grad():
            # print("Getting move...")
            model.eval()
            output = model(state_tensor.unsqueeze(0))
            # Filter out moves that lead to repetitive states
            legal_moves = env.get_legal_moves(turn)
            non_repetitive_moves = [move for move in legal_moves if move not in recent_moves]
            if non_repetitive_moves:
                # Select the best move from non-repetitive legal moves
                predicted_move_index = select_legal_move(output, non_repetitive_moves)
                move = decode_move(predicted_move_index, env.board, non_repetitive_moves)
                success, _ = env.make_move(move, turn)
                if success:
                  recent_moves.append(move)  # Update game history with the successful move
                  data['states'].append(state_tensor.numpy())
                  data['moves'].append(predicted_move_index)
                  total_moves += 1
                  game_moves += 1

                  env.board.print_board()
            else:
                print("Potential repetitive move detected.")
                # Attempt to select a different move, or implement a strategy to break the cycle
                # This part is conceptual; actual implementation will depend on your logic for selecting moves
                env.board.undo_move()
                break

        pygame.time.wait(constants.VISUAL_TIME)  # Slow down the visualization (milliseconds)

      print(f"Game {game_index}/{games} completed with {game_moves} moves.")

    avg_moves = total_moves // games if games > 0 else 0
    print(f"Generated {total_moves} total moves over {games} games (avg {avg_moves:.2f} moves/game).")

    return data

model = ChessModel()

print("Self playing instantiating...")
# Initial self-play data generation
self_play_data = generate_self_play_data(model, constants.TRAIN_GAMES)
pygame.quit()

print("Model training...")
# Train the model
train_model(model, epochs=constants.EPOCH, learning_rate=0.001, self_play_data=self_play_data)

# Save the trained model
torch.save(model.state_dict(), 'trained_chess_model.pth')
