# -*- coding: utf-8 -*-

# TO DO: make Pieces an abstract class

# TO DO: use ascii chess chars, ie: ♖

class PiecesError(Exception): pass

class Pieces(object):

    @staticmethod
    def getPiece(p):
        orig_p = p
        p = p.lower()
        color = 'w' if p == orig_p else 'b'
        if p == 'p':
            return Pawn(color)
        elif p == 'n':
            return Knight(color)
        elif p == 'b':
            return Bishop(color)
        elif p == 'r':
            return Rook(color)
        elif p == 'q':
            return Queen(color)
        elif p == 'k':
            return King(color)
        else:
            raise PiecesError('Unrecognzied piece abbreviation: %s' % orig_p)

class PieceError(Exception): pass

class Piece(object):
    def __init__(self, color):
        if color not in ('w', 'b'):
            raise PiecesError('Unrecognized color: %s' % color)
        self.color = color

    def __repr__(self):
        return self.char if self.color == 'w' else self.char.upper()

class Pawn(Piece):
    char = 'p'
    value = 1

class Knight(Piece):
    char = 'n'
    value = 3

class Bishop(Piece):
    char = 'b'
    value = 3

class Rook(Piece):
    char = 'r'
    value = 5

class Queen(Piece):
    char = 'q'
    value = 9

class King(Piece):
    char = 'k'
    value = None

