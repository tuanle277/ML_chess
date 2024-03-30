# piece.py
class Piece:
    def __init__(self, color):
        self.color = color
        self.symbol = " "  # Placeholder, will be set by subclasses
        self.point = 0

    def move(self, board, start, end):
        # Basic move validation to be overridden by specific piece classes
        raise NotImplementedError("This method must be overridden in the subclass.")

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P' if color == "white" else 'p'
        self.point = 1

    def __str__(self) -> str:
        return super().__str__()

    def move(self, board, start, end):
          start_row, start_col = start
          end_row, end_col = end
          direction = 1 if self.color == "white" else -1

          # Check for moving forward one square
          if start_col == end_col and board.get_piece(end_row, end_col) is None:
              if (direction > 0 and start_row - end_row == 1) or (direction < 0 and end_row - start_row == 1):
                  return True  # Single square move
              # Check for moving forward two squares from the starting position
              if ((direction > 0 and start_row == 6) or (direction < 0 and start_row == 1)) and board.get_piece(start_row - direction, start_col) is None and board.get_piece(end_row, end_col) is None:
                  if (direction > 0 and start_row - end_row == 2) or (direction < 0 and end_row - start_row == 2):
                      return True  # Double square move

          # Check for capturing diagonally
          if abs(start_col - end_col) == 1:
              if (direction > 0 and start_row - end_row == 1) or (direction < 0 and end_row - start_row == 1):
                  if board.get_piece(end_row, end_col) is not None and board.get_piece(end_row, end_col).color != self.color:
                      return True  # Diagonal capture

          return False  # If none of the above conditions are met, the move is invalid

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R' if color == "white" else 'r'
        self.point = 5

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if start_row == end_row: # meaning it moves horizontally
            i = start_col
            while end_col != i:
                i = i - 1 if end_col < start_col else i + 1
                if board.get_piece(start_row, i):
                    return False

        elif start_col == end_col: # meaning it moves vertical
            i = start_row
            while end_row != i:
                i = i - 1 if end_row < start_row else i + 1
                if board.get_piece(i, start_col):
                    return False

        if (start_row == end_row or start_col == end_col):
            # if board.get_piece(end_row, end_col) == None:
            #     return True

            # elif board.get_piece(start_row, start_col).color != board.get_piece(end_row, end_col).color:  # Rook captures straight
            #     return True
            return True

        return False

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'N' if color == "white" else 'n'
        self.point = 3

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
           (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):  # L shape
            return True
        return False

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B' if color == "white" else 'b'
        self.point = 3

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if abs(start[0] - end[0]) == abs(start[1] - end[1]):  # Bishop moves diagonally
            i, j = start_row, start_col
            if start_row > end_row + 1 and start_col > end_col + 1: # if it goes from bottom right to top left
                while i > end_row + 1 and j > end_col + 1:
                    i -= 1
                    j -= 1
                    if board.get_piece(i, j):
                        return False

            elif start_row < end_row - 1 and start_col < end_col - 1: # if it goes from top left to bottom right
                while i < end_row - 1 and j < end_col - 1:
                    i += 1
                    j += 1
                    if board.get_piece(i, j):
                        return False

            elif start_row > end_row + 1 and start_col < end_col - 1: # if it goes from bottom left to top right
                while i > end_row + 1 and j < end_col - 1:
                    i -= 1
                    j += 1
                    if board.get_piece(i, j):
                        return False

            elif start_row < end_row - 1 and start_col > end_col + 1: # if it goes from top right to bottom left
                while i < end_row - 1 and j > end_col + 1:
                    i += 1
                    j -= 1
                    if board.get_piece(i, j):
                        return False

            if board.get_piece(end_row, end_col) == None or board.get_piece(start_row, start_col).color != board.get_piece(end_row, end_col).color:
                return True

        return False

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'Q' if color == "white" else 'q'
        self.point = 10

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        # Combines the power of Rook and Bishop
        if Rook(self.color).move(board, start, end) or Bishop(self.color).move(board, start, end) and board.get_piece(end_row, end_col) is not None and board.get_piece(end_row, end_col).color != self.color:
            return True
        return False

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'K' if color == "white" else 'k'
        self.point = 0

    def move(self, board, start, end):
      start_row, start_col = start
      end_row, end_col = end
      if max(abs(start[0] - end[0]), abs(start[1] - end[1])) == 1 and board.get_piece(end_row, end_col) is not None and board.get_piece(end_row, end_col).color != self.color:  # King moves one square any direction
        return True
      return False
