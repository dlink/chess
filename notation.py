'''Chess Algebraic Notation Module'''

from pieces import Pieces

class NotationError(Exception): pass

class Notation(object):
    '''Preside over Chess Algebraic Notation

    Errors Raised
    
    N1: Invalid notation: %s
    N2: Invalid notation, too short: %s
    N2: Unrecognized file letter: %s
    N3: Invalid notation: Unrecognized 
    N4: Move not possible: %s
    N5: Ambiguous move: %s: (%s)
    N6: King can no longer castle
    N7: King can not in its starting square
    N8: Illegal move, promotion: %s
    '''

    def __init__(self, board):
        self.board = board

    def getNotation(self, orig_position, piece, disambiguous, capture,
                    castled, check, check_mate):
        '''Given a piece's original position, and piece already played
           Return an algebraic notation expression
        '''

        if castled:
            return castled
    
        if piece.char == 'P':
            an = disambiguous + piece.position
        else:
            an = piece.char + disambiguous + piece.position
            
        if capture:
            if len(an) == 2:
                an = orig_position[0] + 'x' + an
            else:
                an = an[0] + 'x' + an[1:]
        if check:
            an += '+'
        elif check_mate:
            an += '#'
            
        return an    

    def getPieceAndDest(self, an, color):
        '''Given an algebraic notation expression and color
           Return a piece, and destination
        '''

        orig_an = an
        check = 0
        checkmate = 0
        capture = 0

        # castle
        if an in ('0-0', '0-0-0'):
            # TO DO: move the validation into Board
            # TO DO: see if castle moves thru any checks
            if self.board.king_moved[color]:
                raise NotationError('N6: King can no longer castle')
            file_ = 1 if color == 'w' else 8
            rook_row = 'h' if an == '0-0' else 'a'
            piece = self.board.getPiece('K', color)
            rook = self.board.getPieceAt('%s%s' % (rook_row, file_))
            if not rook:
                raise NotationError('N7b: Can not castle: missing rook')
            print color, rook_row, self.board.rook_moved[color]
            if self.board.rook_moved[color][rook_row]:
                raise NotationError('N7c: Can not castle: rook has already '
                                    'moved')
                              
            if piece.position != 'e%s' % file_:
                raise NotationError('N7: King can not in its starting square')
            if an == '0-0':
                position = 'g%s' % file_
            else:
                position = 'b%s' % file_
            return piece, position

        # Preprocessing
        print 'an:', an
        if len(an) < 2:
            raise NotationError('N2: Invalid notation, too short: %s' % an)

        # check  checks: +
        if an[-1] == '+':
            check = 1
            an = an[0:-1]
            
        # check check make: #
        elif an[-1] == '#':
            checkmate = 1
            an = an[0:-1]

        # check captures
        if an[1] == 'x':
            capture = 1
            an = an[0] + an[2:]
            # pawns
            if an[0].upper() != an[0]:
                if an[0] not in 'abcdefgh':
                    raise NotationError('N2: Unrecognized file letter: %s' %
                                        an[0])
                an = an[1:]
        elif len(an) >= 3 and an[2] == 'x':
            capture = 1
            an = an[0:1] + an[3:]

        # processing
        
        num_char = len(an)

        # promption
        # TO DO: refactor to rely on board.possibleMoves()
        if num_char == 3 and \
           ((color == 'w' and an[1] == '8') or \
            (color == 'b' and an[1] == '1')):
            position = an[0:2]
            x, y = position2xy(position)
            piece_char = an[2]
            vector = -1 if color == 'w' else 1
            piece = self.board.matrix[y+vector][x]
            if not piece or piece.color != color:
                raise NotationError('N8: Illegal move, promotion: %s' %
                                    orig_an)
            print 'Promotion to: %s' % piece_char
            return piece, position

        # Two or three chars, eq. Nc3
        if num_char in (2, 3, 4, 5):
            file_ = None
            row = None
            if num_char == 2:
                # e4
                piece_char = 'P'
                position = an
            elif num_char == 3:
                # Nc3
                piece_char = an[0]
                position = an[1:]
            elif num_char == 4:
                # Rad1
                piece_char = an[0]
                file_ = an[1]
                if file_.isdigit():
                    # R1d1
                    row = file_
                    file_ = None
                position = an[2:]
            else:
                # Qc1c3
                piece_char = an[0]
                file_ = an[1]
                row = an[2]
                position = an[3:]
        
            if piece_char not in Pieces.piece_chars:
                raise NotationError('N3: Invalid notation: Unrecognized '
                                    'piece char: %s' % orig_an)
            pos_pieces = []
            for piece in self.board.getActivePieces(color):
                if piece.char == piece_char:
                    for pp in self.board.possibleMoves(piece, check_check=0):
                        if pp == position:
                            pos_pieces.append(piece)
                            break
            if not pos_pieces:
                raise NotationError('N4: Move not possible: %s' % orig_an)
            elif len(pos_pieces) == 1:
                piece = pos_pieces[0]
            else:
                # TO DO deal with file and row disambiguities
                # Eq.
                #    pieces: w:Qc1, w:Qc5, w:Qe5
                #    move Qc1c3
                
                # disambiguity
                if file_ and not row:
                    pos_file_pieces = [p for p in pos_pieces
                                       if p.position[0] == file_]
                    if len(pos_file_pieces) == 1:
                        piece = pos_file_pieces[0]
                    else:
                        raise NotationError(
                            'N5b: Ambiguous move: %s: (%s)' %
                            (an, ', '.join(map(str, pos_file_pieces))))
                    
                elif row and not file_:
                    pos_row_pieces = [p for p in pos_pieces
                                      if p.position[1] == row]
                    if len(pos_row_pieces) == 1:
                        piece = pos_row_pieces[0]
                    else:
                        raise NotationError(
                            'N5c: Ambiguous move: %s: (%s)' %
                            (an, ', '.join(map(str, pos_row_pieces))))
                elif file_ and row:
                    orig_position = an[1:3]
                    piece = self.board.getPieceAt(orig_position)
                else:
                    raise NotationError('N5: Ambiguous move: %s: (%s)' %
                                        (an, ', '.join(map(str, pos_pieces))))
            return piece, position
        
        raise NotationError('N1: Invalid notation: %s' % an)
        
def xy2position(x, y):
    file_ = y+1
    row = chr(x+97)
    return '%s%s' % (row, file_)

def position2xy(position):
    x = ord(position[0])-97 # convert a,b,c, ... -> 0,1,2, ...
    y = int(position[1])-1  # convert 1,2,3, ... -> 0,1,2, ...
    return x, y


if __name__ == '__main__':
    import sys
    from board import Board

    an = sys.argv[1]
    color = sys.argv[2]
    print "an:", an, "color:", color

    #board_ = Board(setup_data='data/2rooks_and_kings.board')
    #board_ = Board(setup_data='data/standard.board')
    #board_ = Board(setup_data='data/test.board')
    board_ = Board(setup_data='data/standard2.board')
    
    n = Notation(board_)
    print n.getPieceAndDest(an, color)
    
