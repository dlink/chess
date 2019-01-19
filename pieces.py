# -*- coding: utf-8 -*-

# TO DO: make Pieces an abstract class

# TO DO: use ascii chess chars, ie: ♖

class PiecesError(Exception): pass

class Pieces(object):
    '''Preside of Pieces Objects
    '''

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
    '''Super class for all pieces
    '''
    def __init__(self, color):
        if color not in ('w', 'b'):
            raise PiecesError('Unrecognized color: %s' % color)
        self.color = color
        self.postion = None

    def __repr__(self):
        return self.char if self.color == 'w' else self.char.upper()

    def possibleMoves(self):
        'test case: move forward one'
        c = self.position.move(self.color, 'f1')
        return c

class Pawn(Piece):
    char = 'p'
    value = 1
    moves = ['f1', 'f2']
    # to do: restrict f2 movements to rows 2 and 7
    # to do: build custom capture logic

class Knight(Piece):
    char = 'n'
    value = 3
    moves = ['f2,l1', 'f2,r1',
             'l2,f1', 'l2,b1',
             'b2,l1', 'b2,r1',
             'r2,f1', 'r2,b1']

class Bishop(Piece):
    char = 'b'
    value = 3
    moves = ['d*', 'e*', 'g*', 'h*']

class Rook(Piece):
    char = 'r'
    value = 5
    moves =['f*', 'b*', 'l*', 'r*']

class Queen(Piece):
    char = 'q'
    value = 9
    moves = ['f*', 'b*', 'l*', 'r*',
             'd*', 'e*', 'g*', 'h*']

class King(Piece):
    char = 'k'
    value = None
    moves = ['f1', 'b1', 'l1', 'r1',
             'd1', 'e1', 'g1', 'h1']

