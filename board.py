#!/usr/bin/python

from pieces import Pieces, Queen
from board_display import BoardDisplay

STANDARD = 'data/standard.board'

def xy2position(x, y):
    file_ = y+1
    row = chr(x+97)
    return '%s%s' % (row, file_)

def position2xy(position):
    x = ord(position[0])-97 # convert a,b,c, ... -> 0,1,2, ...
    y = int(position[1])-1  # convert 1,2,3, ... -> 0,1,2, ...
    return x, y

class BoardError(Exception): pass

class Board(object):

    def __init__(self, setup_data=STANDARD):
        '''Create the board matrix
           Create the pieces sand add them to the board
        '''
        self.setup_data = setup_data
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]
        self.pieces = []
        self.captured = []
        self.setup()
        self.display = BoardDisplay(self)

    def __repr__(self):
        return self.display.one_line()

    def setup(self):
        '''Set up the pieces on the board based in input file
        '''
        for row in open(self.setup_data).readlines():
            row = row.strip()

            # eq.: k-e1
            char, position = row.split('-')
            piece = Pieces.getPiece(char)

            self.placePiece(piece, position)
            self.pieces.append(piece)

    def getPiece(self, position):
        x, y = position2xy(position)
        return self.matrix[y][x]

    def placePiece(self, piece, position):
        '''Place a piece on the board at a given position
             piece is a Piece Object
             position is a str coordinate, eq.: a1
        '''
        x,y = position2xy(position)
        self.matrix[y][x] = piece
        piece.position = position
        return piece

    def movePiece(self, piece, position):
        '''Move a piece on the board to a given position
           confirm move is valid
           perform captures if applicable
           promote pawns
        '''
        if position not in self.possibleMoves(piece):
            raise BoardError('Invalid Move: %s can not move to %s' %
                             (piece, position))
        # remove piece from the board
        x,y = position2xy(piece.position)
        self.matrix[y][x] = None

        # check capture
        x,y = position2xy(position)
        if self.matrix[y][x]:
            self.captured.append(self.matrix[y][x])

        # promote pawns
        if piece.char == 'p':
            if (piece.color == 'w' and position[1] == '8') or \
               (piece.color == 'b' and position[1] == '1'):
                ind = self.pieces.index(piece)
                piece = Queen(piece.color)
                self.pieces[ind] = piece

        # place piece
        self.matrix[y][x] = piece
        piece.position = position
        return piece

    def possibleMoves(self, piece):
        '''Given a piece on the board
           Return a list of possible positions it can move to
        '''
        #print 'possibleMoves(%s)' % piece
        if not piece:
            return []

        possibilities = []
        for move in piece.moves:
            new_positions = self.getMoveDestination(piece, move)
            if not new_positions:
                continue
            for new_position in new_positions:
                piece2 = self.getPiece(new_position)
                if piece2 and piece2.color == piece.color:
                    continue
                possibilities.append(new_position)
        return possibilities

    def getMoveDestination(self, piece, move):
        '''Given a piece on the board, and a move instruction
           Return the destination postion after the move
             or None if the move is not possible.
        '''
        #print 'getMoveDestination(%s, %s)' % (piece, move)

        x,y = position2xy(piece.position)
        direction, dist = move

        x2 = x
        y2 = y

        new_positions = []
        vector = 1 if piece.color == 'w' else -1
        dists = range(1,8) if dist == '*' else [int(dist)]
        for d in dists:
            vdist = vector * d
            # orthonal movements
            if direction == 'f':
                y2 = y + vdist
            elif direction == 'b':
                y2 = y - vdist
            elif direction == 'l':
                x2 = x - vdist
            elif direction == 'l':
                x2 = x - vdist
            elif direction == 'r':
                x2 = x + vdist

            # diagonal movements
            elif direction == 'd':
                x2 = x - vdist; y2 = y + vdist
            elif direction == 'e':
                x2 = x + vdist; y2 = y + vdist
            elif direction == 'g':
                x2 = x - vdist; y2 = y - vdist
            elif direction == 'h':
                x2 = x + vdist; y2 = y - vdist

            # knight L-move
            elif direction == 'i':
                x2 = x - vdist*2; y2 = y + vdist
            elif direction == 'j':
                x2 = x - vdist; y2 = y + vdist*2
            elif direction == 'k':
                x2 = x + vdist; y2 = y + vdist*2
            elif direction == 'm':
                x2 = x + vdist*2; y2 = y + vdist
            elif direction == 'n':
                x2 = x + vdist*2; y2 = y - vdist
            elif direction == 'o':
                x2 = x + vdist; y2 = y - vdist*2
            elif direction == 'p':
                x2 = x - vdist; y2 = y - vdist*2
            elif direction == 'q':
                x2 = x - vdist*2; y2 = y - vdist

            else:
                raise BoardError('unknown movment direction: %s' % direction)

            # off the board:
            if y2 not in range(0, 8) or x2 not in range(0, 8):
                break

            # piece there?
            new_position = xy2position(x2, y2)
            piece2 = self.getPiece(new_position)
            if piece2:
                # opponents piece?
                if piece2.color != piece.color:
                    new_positions.append(new_position)
                # your piece?
                break

            new_positions.append(new_position)

        return new_positions

if __name__ == '__main__':
    board = Board()
    print board.display.one_line()
    print board.display.simple()
    print board.display.standard()
