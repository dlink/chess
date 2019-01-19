#!/usr/bin/python

from pieces import Pieces
from board_display import BoardDisplay

STANDARD = 'data/standard.board'

def xy2coord(x, y):
    file_ = y+1
    row = chr(x+97)
    return '%s%s' % (row, file_)

def position2xy(position):
    x = ord(position[0])-97 # convert a,b,c, ... -> 0,1,2, ...
    y = int(position[1])-1  # convert 1,2,3, ... -> 0,1,2, ...
    return x, y

class BoardError(Exception): pass

class Board(object):

    def __init__(self):
        '''Create the board matrix
           Create the pieces sand add them to the board
        '''
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]
        self.pieces = []
        self.setup()
        self.display = BoardDisplay(self)

    def __repr__(self):
        return self.display.one_line()

    def setup(self, setup_data=STANDARD):
        '''Set up the pieces on the board based in input file
        '''
        for row in open(setup_data).readlines():
            row = row.strip()

            # eq.: k-e1
            char, position = row.split('-')
            piece = Pieces.getPiece(char)

            self.placePiece(piece, position)
            self.pieces.append(piece)

    def getPiece(self, coord):
        x, y = position2xy(coord)
        return self.matrix[y][x]

    def placePiece(self, piece, position):
        '''Place a piece at a position on the board
             piece is a Piece Object
             position is a str coordinate, eq.: a1
        '''
        x,y = position2xy(position)
        self.matrix[y][x] = piece
        piece.position = position

    def possibleMoves(self, piece):
        '''Given a piece on the board
           Return a list of possible positions it can move to
        '''
        if not piece:
            return []

        possibilities = []
        for move in piece.moves:
            coord2 = self.getMoveDestination(piece, move)
            if not coord2:
                continue
            piece2 = self.getPiece(coord2)
            if piece2 and piece2.color == piece.color:
                continue
            possibilities.append(coord2)
        return possibilities

    def getMoveDestination(self, piece, move):
        '''Given a piece on the board, and a move instruction
           Return the destination postion after the move
             or None if the move is not possible.
        '''
        x,y = position2xy(piece.position)
        direction, dist = move

        # hack
        if dist == '*':
            dist = '1'

        dist = int(dist)
        vector = 1 if piece.color == 'w' else -1
        if direction == 'f':
            y2 = y + (vector * dist)
        else:
            return None
            #raise BoardError('unkonwn movment direction: %s' % direction)
        coord2 = xy2coord(x, y2)
        return coord2

if __name__ == '__main__':
    board = Board()
    print board.display.one_line()
    print board.display.simple()
    print board.display.standard()
