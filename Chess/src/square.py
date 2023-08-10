from piece import *

class Square:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)
    
    def isbishop(self, color):
        return True if isinstance(self.piece, Bishop) and self.piece.color == color else False
    
    def isrook(self, color):
        return True if isinstance(self.piece, Rook) and self.piece.color == color else False

    def isknight(self, color):
        return True if isinstance(self.piece, Knight) and self.piece.color == color else False

    def isqueen(self, color):
        return True if isinstance(self.piece, Queen) and self.piece.color == color else False

    def isbishoprook(self, color):
        return True if isinstance(self.piece, Bishop_Rook) and self.piece.color == color else False
    def isbishopknight(self, color):
        return True if isinstance(self.piece, Bishop_Knight) and self.piece.color == color else False
    def isqueenknight(self, color):
        return True if isinstance(self.piece, Queen_Knight) and self.piece.color == color else False
    def isrookknight(self, color):
        return True if isinstance(self.piece, Rook_Knight) and self.piece.color == color else False
    
    def fusionable(self):
        return True if self.isqueen or self.isbishop or self.isrook or self.isknight else False

    def fusionp(self):
        return True if self.isbishopknight or self.isbishoprook or self.isqueenknight or self.isrookknight else False

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True