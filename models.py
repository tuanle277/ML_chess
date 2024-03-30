# piece.py
class Piece:
    def __init__(self, color):
        self.color = color

    def move(self, board, start_pos, end_pos):
        raise NotImplementedError("This method should be implemented by subclasses.")

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def move(self, board, start_pos, end_pos):
        # Implement pawn-specific move logic here
        pass
