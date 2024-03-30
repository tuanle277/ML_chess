# game.py
from board import Board

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.player_turn = "White"

    def switch_turns(self):
        self.player_turn = "Black" if self.player_turn == "White" else "White"

    def play(self):
        while True:
            self.board.print_board()
            print(f"{self.player_turn}'s turn")
            start_pos = input("Enter start position (e.g., 'e2'): ")
            end_pos = input("Enter end position (e.g., 'e4'): ")
            if self.board.move_piece(start_pos, end_pos):
                self.switch_turns()

if __name__ == "__main__":
    game = ChessGame()
    game.play()
