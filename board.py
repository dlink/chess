#!/usr/bin/python

import re
from copy import deepcopy

from pieces import Pieces, Queen
from board_display import BoardDisplay

SETUP_DATA = 'data/standard.board'
DISPLAY_TYPE = 'standard'

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

    def __init__(self, setup_data=SETUP_DATA, display_type=DISPLAY_TYPE):
        '''Create the board matrix
           Create the pieces sand add them to the board
        '''
        self.name = 'board'
        self.setup_data = setup_data
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]
        self.pieces = []
        self.captured = []
        self.in_check = {'w': 0, 'b': 0}
        self.check_mate = {'w': 0, 'b': 0}
        self.setup()
        self.display = BoardDisplay(self)
        self.display.type = display_type

    def __repr__(self):
        return self.display.one_line()

    def setup(self):
        '''Set up the pieces on the board based in input file
        '''
        for row in open(self.setup_data).readlines():

            # ignore comments, skip blank lines
            row = re.sub('#.*', '', row).strip()
            if not row:
                continue
            
            # eq.: w:Ke1
            color, piece_position = row.split(':')
            char = piece_position[0]
            position = piece_position[1:]
            piece = Pieces.create(char, color)

            self.placePiece(piece, position)
            self.pieces.append(piece)

    def getPieceAt(self, position):
        x, y = position2xy(position)
        return self.matrix[y][x]

    def getPiece(self, char, color):
        '''Given a character representation of a piece and color
           Return first occurance of it on the board
        '''
        orig_char = char
        file_ = None
        if len(char) > 1:
            char, file_ = char

        for piece in self.pieces:
            if piece.char == char and piece.color == color:
                if not file_:
                    return piece
                if piece.position[0] == file_:
                    return piece
        raise BoardError('Could not find piece: %s, %s' % (orig_char, color))

    def getActivePieces(self, color):
        return [p for p in self.pieces
                if p.color == color and p.position != 'x']

    def placePiece(self, piece, position):
        '''Place a piece on the board at a given position
             piece is a Piece Object
             position is a str coordinate, eq.: a1
        '''
        x,y = position2xy(position)
        self.matrix[y][x] = piece
        piece.position = position
        return piece

    def move00(self, color, an, check_legal=1, check_check=1):
        '''Move a piece on the board to a given position
           confirm move is valid
           perform captures if applicable
           promote pawns
        '''
        piece, position = self.notation.getPieceAndDest(an, color)

        # init in_check
        self.in_check[piece.opposite_color] = 0

        if check_legal:
            if position not in self.possibleMoves(piece):
                raise BoardError('Invalid Move: %s can not move to %s' %
                                 (piece, position))
        # remove piece from the board
        x,y = position2xy(piece.position)
        self.matrix[y][x] = None

        # check capture
        x,y = position2xy(position)
        opponent_piece = self.matrix[y][x]
        if opponent_piece:
            opponent_piece.position = 'x'
            self.captured.append(opponent_piece)

        # promote pawns
        if piece.char == 'P':
            if (piece.color == 'w' and position[1] == '8') or \
               (piece.color == 'b' and position[1] == '1'):
                ind = self.pieces.index(piece)
                piece = Queen(piece.color)
                self.pieces[ind] = piece

        # place piece
        piece.position = position
        self.matrix[y][x] = piece

        # is this check?
        if check_check:
            opponent_king = self.getPiece('K', piece.opposite_color)
            if opponent_king.position in self.possibleMoves(piece):
                self.in_check[opponent_king.color] = 1

                # is this check mate?
                has_escape = 0
                for op_piece in self.getActivePieces(piece.opposite_color):
                    op_possibilities = self.possibleMoves(op_piece)
                    if op_possibilities:
                        has_escape = 1
                        break
                if not has_escape:
                    self.check_mate[piece.opposite_color] = 1
        return piece
    
    def movePiece(self, piece, position, check_legal=1, check_check=1):
        '''Move a piece on the board to a given position
           confirm move is valid
           perform captures if applicable
           promote pawns
        '''
        capture = 0
        check = 0
        check_mate =0
        
        # init in_check
        self.in_check[piece.opposite_color] = 0

        if check_legal:
            if position not in self.possibleMoves(piece):
                raise BoardError('Invalid Move: %s can not move to %s' %
                                 (piece, position))
        # remove piece from the board
        x,y = position2xy(piece.position)
        self.matrix[y][x] = None

        # check capture
        x,y = position2xy(position)
        opponent_piece = self.matrix[y][x]
        if opponent_piece:
            opponent_piece.position = 'x'
            self.captured.append(opponent_piece)
            capture = 1
        
        # promote pawns
        if piece.char == 'p':
            if (piece.color == 'w' and position[1] == '8') or \
               (piece.color == 'b' and position[1] == '1'):
                ind = self.pieces.index(piece)
                piece = Queen(piece.color)
                self.pieces[ind] = piece

        # place piece
        piece.position = position
        self.matrix[y][x] = piece

        # is this check?
        if check_check:
            opponent_king = self.getPiece('K', piece.opposite_color)
            if opponent_king.position in self.possibleMoves(piece):
                
                # is this check mate?
                has_escape = 0
                for op_piece in self.getActivePieces(piece.opposite_color):
                    op_possibilities = self.possibleMoves(op_piece)
                    if op_possibilities:
                        has_escape = 1
                        break
                if has_escape:
                    self.in_check[opponent_king.color] = 1
                    check = 1
                else:
                    self.check_mate[piece.opposite_color] = 1
                    check_mate = 1

        return piece, capture, check, check_mate

    def possibleMoves(self, piece, check_check=1, captureable_only=0):
        '''Given a piece on the board
           Return a list of possible positions it can move to
        '''
        
        # TO DO: handle castling
        
        if not piece:
            return []

        possibilities = []
        for move_op in piece.move_ops:
            new_positions = self.getMoveDestination(piece, move_op)
            if not check_check:
                possibilities.extend(new_positions)
                continue

            # Will you be in check?
            for new_position in new_positions:
                if piece.color == 'b' and piece.char == 'P':
                    print 'new_position:', piece, new_position

                # build hypothetical board
                hypo_board = deepcopy(self)
                hypo_board.name = 'hypo_board'
                hypo_piece = hypo_board.getPieceAt(piece.position)
                # make the move
                hypo_board.movePiece(hypo_piece, new_position, check_legal=0,
                                     check_check=0)
                # Can they capture your king?
                king = hypo_board.getPiece('K', hypo_piece.color)
                puts_you_in_check = 0
                for p in hypo_board.getActivePieces(hypo_piece.opposite_color):
                    hypo_possibilities = hypo_board.possibleMoves(
                        p, check_check=0)
                    if king.position in hypo_possibilities:
                        puts_you_in_check = 1
                        break

                del hypo_board
                if not puts_you_in_check:
                    possibilities.append(new_position)

        #print '%s possibilities: %s: %s' % (self.name, piece, possibilities)
        return possibilities

    def getMoveDestination(self, piece, move, captureable_only=0):
        '''Given a piece on the board, and a move instruction
           Return the destination postion after the move
             or None if the move is not possible.
        '''
        x,y = position2xy(piece.position)
        direction, dist = move

        x2 = x
        y2 = y

        new_positions = []
        vector = 1 if piece.color == 'w' else -1
        dists = range(1,8) if dist == '*' else [int(dist)]
        for d in dists:
            
            if captureable_only:
                if piece.char == 'p' and direction == 'f':
                    continue
                                                     
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

            new_position = xy2position(x2, y2)

            # occupied squre?
            piece2 = self.getPieceAt(new_position)

            # handle pawn capture
            if piece.char == 'P':
                if direction == 'f':
                    if piece2:
                        break
                else:
                    # diagonal move
                    if not piece2 or piece2.color == piece.color:
                        break

            # pieces other than pawns
            else:
                if piece2:
                    if piece2.color != piece.color:
                        # can capture opponents piece
                        new_positions.append(new_position)
                    break

            new_positions.append(new_position)

        return new_positions

if __name__ == '__main__':
    board = Board()
    print board.display.one_line()
    print board.display.simple()
    print board.display.standard()
