# player.py
from piece import Pawn, Rook, Knight, Bishop, Queen, King

class Player:
    def __init__(self, side) -> None: # side can be either black or white
        self.point = 0

        self.pieces = [Rook(side), Knight(side), Bishop(side), Queen(side),
                        King(side), Bishop(side), Knight(side), Rook(side)]
        for i in range(8):
            self.pieces.append(Pawn(side))
