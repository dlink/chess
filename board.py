#!/usr/bin/python
# -*- coding: utf-8 -*-

from pieces import Pieces, Pawn, Rook, Knight

STANDARD = 'data/standard.board'

class Board(object):

    def __init__(self):
        '''Create the board matrix
           Create the pieces and add them to the board
        '''
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]
        self.pieces = []
        self.setup()

    def setup(self, setup_data=STANDARD):
        '''Set up the pieces on the board based in input file
        '''
        for row in open(setup_data).readlines():
            row = row.strip()

            # eq.: k-e1
            char, coord = row.split('-')
            piece = Pieces.getPiece(char)
            position = Position(coord)

            self.placePiece(piece, position)
            self.pieces.append(piece)

    def placePiece(self, piece, position):
        '''Place a piece at a position on the board
             piece is a Piece Object
             position is a Position Object
        '''

        self.matrix[position.y][position.x] = piece
        piece.position = position

    def display(self):
        '''Generate and return an ascii representation of the board
           in its current state, as a multiline string.
        '''
        o = ''
        o += '    a   b   c   d   e   f   g   h\n'
        o += '  ╔═══' + '╤═══' * 7 + '╗\n'
        for i, row in enumerate(reversed(self.matrix)):

            o += '%s ║' % (8-i)
            o += '│'.join(' %s ' % (p if p else ' ') for p in row)
            o += '║ %s\n' % (8-i)

            if i < 7:
                o += '  ╟───' + '┼───' * 7 + '╢\n'
            else:
                o += '  ╚═══' + '╧═══' * 7 + '╝\n'
                o += '    a   b   c   d   e   f   g   h\n'
        return o

class Position(object):
    '''Preside over squares on the board'''

    @staticmethod
    def xy2coord(x, y):
        file_ = y+1
        row = chr(x+97)
        return '%s%s' % (row, file_)

    def __init__(self, coord):
        self.coord = coord

    def __repr__(self):
        return self.coord

    @property
    def x(self):
        '''convert a,b,c, ... -> 0,1,2, ...'''
        return ord(self.coord[0])-97

    @property
    def y(self):
         '''convert 1,2,3, ... -> 0,1,2, ...'''
         return int(self.coord[1])-1

    def move(self, color, movement):
        # eq: f1
        direction, dist = movement
        dist = int(dist)
        vector = 1 if color == 'w' else -1
        if direction == 'f':
            y2 = self.y + (vector * dist)
        else:
            raise PositionError('unkonwn movment direction: %s' % direction)
        coord = Position.xy2coord(self.x, y2)
        return coord


if __name__ == '__main__':
    board = Board()
    print board.display()

    print 'piece, pos., move forward 1:'
    for i in range(0, 32):
        p = board.pieces[i]
        print p, p.position, p.possibleMoves()

