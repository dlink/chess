#!/usr/bin/python

'''Board Module

   Control the state of the games board, legal moves, captures, checks and check mates
   Uses Display module to display the board
   Uses Notation module to understand chess standard notation (SAN). eq.: e4, Nc3, etc.

   Example:

   Create a chess board with standard piece setup, using a 'standard' display
      board = Board()

   Create a chess board with a rooks and pieces setup, using a 'simple' display type
      board = Board('rooks_and_kings', 'standard')

'''
import re
from copy import deepcopy

from pieces import Pieces, Queen
from display import Display
from notation import Notation

SETUP_DATA = 'data/standard.board'
DISPLAY_TYPE = 'standard'

def xy2position(x, y):
    '''Given x and y as zero-indexed coordinates on the board
       Return position in standard notation

       eq.: 0, 0 --> a1
            0, 7 --> a8
            4, 3 --> e4
    '''
    file_ = y+1
    row = chr(x+97)
    return '%s%s' % (row, file_)

def position2xy(position):
    '''Given a postion on the board in standard notation
       Return x and y as zero-indexed coordinates on the board
       eq.:
         a1 --> 0, 0
         e4 --> 4, 3
    '''
    x = ord(position[0])-97 # convert a,b,c, ... -> 0,1,2, ...
    y = int(position[1])-1  # convert 1,2,3, ... -> 0,1,2, ...
    return x, y

class BoardError(Exception): pass

class Board(object):
    '''Preside over the Chess Board'''

    def __init__(self, setup_data=SETUP_DATA, display_type=DISPLAY_TYPE):
        '''Create the board matrix
           Initializes board attributes
           Calls setup() which, create the pieces and add them to the board

           setup_data:  a filename which maps to data/<filename>.board 
                        which uses color and standard notation to denote
                        which pieces go where.
                        eq.: w:a2 places a white Pawn on a2

                        default is 'standard' which is a normal start
                        game position.  you can create other types
                        of setups.
           display_type: Sets default display type supported by the Display
                         module valid options at time of writing are:
                         'standard', 'simple', and 'one_line'
        '''
        self.name = 'board'
        self.setup_data = setup_data
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]
        self.pieces = []
        self.captured = []
        self.in_check = {'w': 0, 'b': 0}
        self.check_mate = {'w': 0, 'b': 0}
        self.king_moved = {'w': 0, 'b': 0}
        self.rook_moved = {'w': {'a': 0, 'h': 0},
                           'b': {'a': 0, 'h': 0}}
        self.setup()
        self.display = Display(self)
        self.display.type = display_type
        self.notation = Notation(self)
        self.history = []
        self.last_move_position = None

    def __repr__(self):
        return self.display.one_line()

    def setup(self):
        '''Set up the pieces on the board based self.setup_data'''
        
        # read setup data
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

    def display_history(self):
        '''Return a string of all moves made so far in standard notation'''

        o = []
        for i, move in enumerate(self.history):
            o.append('%s. %s %s' % (i+1, move[0], move[1]))
        return ' '.join(o)

    def getPieceAt(self, position):
        '''Given a postion in standard notation
           Return Piece object on the board at that location or None
        '''
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
        raise BoardError('B3: Could not find piece: %s, %s' %
                         (orig_char, color))

    def getActivePieces(self, color):
        '''Given a color char {'w', 'b'}
           Return a list of all active pieces on the board of that color
        '''
        return [p for p in self.pieces
                if p.color == color and p.position != 'x']

    def placePiece(self, piece, position):
        '''Place a piece on the board at a given position
             piece: a Piece Object
             position:  string in standard notation, eq.: a1
           Behavior: Also changes piece's position to the new position
           Returns the Piece object
        '''
        x,y = position2xy(position)
        self.matrix[y][x] = piece
        piece.position = position
        return piece

    def move(self, an, color):
        '''Given a chess move as a string in standard notation, and its color
           Perform the move
           Returns the move as a string in standard notation, which may
              be different than the input. May add 'x', '+', or '#' to the move
        '''
        piece, position = self.notation.getPieceAndDest(an, color)
        return self.movePiece(piece, position)
        
    def movePiece(self, piece, position, check_legal=1, check_check=1):
        '''Given a piece object, and a position in standard notation
           Perform the move.

           Confirm move is valid - if check_legal=1
           Perform captures if applicable
           Promote pawns
           checks for checks and check mates -- if check_chec
           Sets pieces position attr to the new position

           Returns move as a string in standard notation
        '''
        orig_position = piece.position

        capture = 0
        check = 0
        check_mate = 0
        castled = 0

        # init in_check
        self.in_check[piece.opposite_color] = 0

        if check_legal:
            if position not in self.possibleMoves(piece):
                raise BoardError('B2: Invalid Move: %s can not move to %s' %
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
        
        # promote pawns: d8Q, e8xQ
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

        # king move?
        if piece.char == 'K':
            # mark king moved
            self.king_moved[piece.color] = 1
            
            # castling? move rook, too
            f = 1 if piece.color == 'w' else 8
            if orig_position == 'e%s' % f:
                rpos1, rpos2 = None, None
                if position == 'b%s' % f:
                    rpos1, rpos2 = 'a%s' % f, 'c%s' % f
                    self.rook_moved[piece.color]['a'] = 1
                    castled = '0-0-0'
                elif position == 'g%s' % f:
                    rpos1, rpos2 = 'h%s' % f, 'f%s' % f
                    self.rook_moved[piece.color]['h'] = 1
                    castled = '0-0'
                # perform castle
                if rpos1:
                    x1,y1 = position2xy(rpos1)
                    x2,y2 = position2xy(rpos2)
                    rook = self.getPieceAt(rpos1)
                    self.matrix[y1][x1] = None
                    self.matrix[y2][x2] = rook
                    rook.position = rpos2

        # did rooks move?
        if piece.char == 'R':
            orig_file = orig_position[0]
            if orig_file in ('a', 'h'):
                self.rook_moved[piece.color][orig_file] = 1

        move = self.notation.getNotation(orig_position, piece, capture,
                                         castled, check, check_mate)
        
        # record history
        if piece.color == 'w':
            self.history.append([move,''])
        else:
            self.history[-1][1] = move
        self.last_move_position = piece.position
        
        return move

    def possibleMoves(self, piece, check_check=1, captureable_only=0):
        '''Given a piece on the board
           Return a list of possible positions it can move to in 
                  standard notation
           Set check_check=0 when nec. to avoid infinate recursion
        '''
        # TO DO: Why do we need captureable_only flag?
        
        if not piece:
            return []

        possibilities = []
        for move_op in piece.move_ops:
            new_positions = self.getMoveDestination(piece, move_op)

            # skip check check
            if not check_check:
                possibilities.extend(new_positions)
                continue

            # check check - Invalid move, due to a check? (Uses recursion)
            for new_position in new_positions:

                # build hypothetical board and make move on it.
                hboard = deepcopy(self)
                hboard.name = 'hboard'
                hpiece = hboard.getPieceAt(piece.position)
                hboard.movePiece(hpiece, new_position, check_legal=0,
                                     check_check=0)
                # check opponent's possible moves 
                in_check = 0
                king = hboard.getPiece('K', hpiece.color)
                for p in hboard.getActivePieces(hpiece.opposite_color):
                    hpossibilities = hboard.possibleMoves(
                        p, check_check=0)
                    if king.position in hpossibilities:
                        in_check = 1
                        break
                del hboard
                
                # in check?
                if not in_check:
                    possibilities.append(new_position)
        
        return possibilities

    def getMoveDestination(self, piece, move_op, captureable_only=0):
        '''Given a piece on the board, and a move_op instruction
           Return  a list of destinatins it can move to based on
             how the piece moves - regardless of what's legal on 
             the current board.
           See Piece Objects for how move_ops are defined.
        '''
        x,y = position2xy(piece.position)
        direction, dist = move_op

        x2 = x
        y2 = y

        new_positions = []
        vector = 1 if piece.color == 'w' else -1
        dists = range(1, 8) if dist == '*' else range(1, int(dist)+1)
        for d in dists:

            if captureable_only:
                if piece.char == 'P' and direction == 'f':
                    continue
   
            vdist = vector * d
            # orthonal move_op
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

            # diagonal move_op
            elif direction == 'd':
                x2 = x - vdist; y2 = y + vdist
            elif direction == 'e':
                x2 = x + vdist; y2 = y + vdist
            elif direction == 'g':
                x2 = x - vdist; y2 = y - vdist
            elif direction == 'h':
                x2 = x + vdist; y2 = y - vdist

            # knight L-move_op
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

            # king castle
            elif direction == 'y':
                x2 = x - 3; y2 = y
            elif direction == 'z':
                x2 = x + 2; y2 = y
            else:
                raise BoardError('B1: Unknown movment direction: %s' %
                                 direction)

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
                    # diagonal move_op
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
