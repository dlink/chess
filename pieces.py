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
        return '%s-%s' %(self.char if self.color == 'w' else self.char.upper(),
                         self.position)
    @property
    def char_glyph(self):
        return self.char if self.color == 'w' else self.char.upper()

    @property
    def glyph(self):
        if self.color == 'w':
            return self.glyphs[0]
        else:
            return self.glyphs[1]

    def possibleMoves(self):
        'test case: move forward one'
        c = self.position.move(self.color, 'f1')

        return c

class Pawn(Piece):
    char = 'p'
    value = 1
    glyphs = ['♙', '♟']

    @property
    def moves(self):
        _moves = ['f1']
        if (self.color == 'w' and self.position[1] == '2') or \
           (self.color == 'b' and self.position[1] == '7'):
            _moves.append('f2')
        return _moves

    # to do: build custom capture logic

class Knight(Piece):
    char = 'n'
    value = 3
    glyphs = ['♘', '♞']
    moves = ['i1','j1','k1','m1','n1','o1','p1','q1']

class Bishop(Piece):
    char = 'b'
    value = 3
    glyphs = ['♗', '♝']
    moves = ['d*', 'e*', 'g*', 'h*']

class Rook(Piece):
    char = 'r'
    value = 5
    glyphs = ['♖', '♜']
    moves =['f*', 'b*', 'l*', 'r*']

class Queen(Piece):
    char = 'q'
    value = 9
    glyphs = ['♕', '♛']
    moves = ['f*', 'b*', 'l*', 'r*',
             'd*', 'e*', 'g*', 'h*']

class King(Piece):
    char = 'k'
    value = None
    glyphs = ['♔', '♚']
    moves = ['f1', 'b1', 'l1', 'r1',
             'd1', 'e1', 'g1', 'h1']
