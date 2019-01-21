# -*- coding: utf-8 -*-

# TO DO: make Pieces an abstract class

# TO DO: use ascii chess chars, ie: ♖

class PiecesError(Exception): pass

class Pieces(object):
    '''Preside of Pieces Objects'''

    @staticmethod
    def create(char):
        '''Given a char representation of a piece
           Return instantiated Piece object of that type
           Colors: chars lowercase = white
                   chars uppercase = black
        '''
        orig_char = char
        char = char.lower()
        color = 'w' if char == orig_char else 'b'
        if char == 'p':
            return Pawn(color)
        elif char == 'n':
            return Knight(color)
        elif char == 'b':
            return Bishop(color)
        elif char == 'r':
            return Rook(color)
        elif char == 'q':
            return Queen(color)
        elif char == 'k':
            return King(color)
        else:
            raise PiecesError('Unrecognzied piece abbreviation: %s' %orig_char)

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
    def opposite_color(self):
        return 'w' if self.color == 'b' else 'b'

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
    def move_ops(self):
        '''Can move one move or two depending starting pos.
           Can move diagnal forward to capture
        '''
        _move_ops = ['d1', 'e1', 'f1']
        if (self.color == 'w' and self.position[1] == '2') or \
           (self.color == 'b' and self.position[1] == '7'):
            _move_ops.append('f2')
        return _move_ops
        
class Knight(Piece):
    char = 'n'
    value = 3
    glyphs = ['♘', '♞']
    move_ops = ['i1','j1','k1','m1','n1','o1','p1','q1']

class Bishop(Piece):
    char = 'b'
    value = 3
    glyphs = ['♗', '♝']
    move_ops = ['d*', 'e*', 'g*', 'h*']

class Rook(Piece):
    char = 'r'
    value = 5
    glyphs = ['♖', '♜']
    move_ops =['f*', 'b*', 'l*', 'r*']

class Queen(Piece):
    char = 'q'
    value = 9
    glyphs = ['♕', '♛']
    move_ops = ['f*', 'b*', 'l*', 'r*',
                'd*', 'e*', 'g*', 'h*']

class King(Piece):
    char = 'k'
    value = 0
    glyphs = ['♔', '♚']
    move_ops = ['f1', 'b1', 'l1', 'r1',
                'd1', 'e1', 'g1', 'h1']
