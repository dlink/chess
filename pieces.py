# -*- coding: utf-8 -*-

# TO DO: make Pieces an abstract class

class PiecesError(Exception): pass

class Pieces(object):
    '''Preside of Pieces Objects'''

    piece_chars = ['P', 'N', 'B', 'R', 'Q', 'K']
    
    @staticmethod
    def create(char, color):
        '''Given a char representation of a piece, and a color (w,b)
           Return instantiated Piece object of that type
           It will not yet have a postion
        '''
        char = char
        if char == 'P':
            return Pawn(color)
        elif char == 'N':
            return Knight(color)
        elif char == 'B':
            return Bishop(color)
        elif char == 'R':
            return Rook(color)
        elif char == 'Q':
            return Queen(color)
        elif char == 'K':
            return King(color)
        else:
            raise PiecesError('Unrecognzied piece abbreviation: %s' % char)

class PieceError(Exception): pass

class Piece(object):
    '''Super class for all pieces
    '''
    def __init__(self, color):
        if color not in ('w', 'b'):
            raise PiecesError('Unrecognized color: %s' % color)
        self.color = color
        self.postion = None
        self.moved = False
        self.possibleMoves = None

    def __repr__(self):
        return '%s:%s%s' %(self.color, self.char, self.position)

    @property
    def opposite_color(self):
        return 'w' if self.color == 'b' else 'b'

    @property
    def char_glyph(self):
        return self.char.lower() if self.color == 'w' else self.char

    @property
    def glyph(self):
        if self.color == 'w':
            return self.glyphs[0]
        else:
            return self.glyphs[1]

class Pawn(Piece):
    #  d f e
    #    .

    char = 'P'
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
            _move_ops[-1] = 'f2'
        return _move_ops
        
    def __repr__(self):
        return '%s:%s' %(self.color, self.position)

class Knight(Piece):
    #    j   k
    #  i       m
    #      .
    #  q       n
    #    p   o
    
    char = 'N'
    value = 3
    glyphs = ['♘', '♞']
    move_ops = ['i1','j1','k1','m1','n1','o1','p1','q1']

class Bishop(Piece):
    #  d   e
    #    .
    #  g   h
    
    char = 'B'
    value = 3
    glyphs = ['♗', '♝']
    move_ops = ['d*', 'e*', 'g*', 'h*'] 

class Rook(Piece):
    #    f 
    #  r . l
    #    b

    char = 'R'
    value = 5
    glyphs = ['♖', '♜']
    move_ops =['f*', 'b*', 'l*', 'r*']

class Queen(Piece):
    #  d f e
    #  r . l
    #  g b h
    
    char = 'Q'
    value = 9
    glyphs = ['♕', '♛']
    move_ops = ['f*', 'b*', 'l*', 'r*',
                'd*', 'e*', 'g*', 'h*']

class King(Piece):
    #  d f e
    #  r . l
    #  g b h    and y, z -> castle queen side, king side
    
    char = 'K'
    value = 0
    glyphs = ['♔', '♚']
    move_ops = ['f1', 'b1', 'l1', 'r1', # orthogonal
                'd1', 'e1', 'g1', 'h1', # diaganal
                'y1', 'z1']               # castle
