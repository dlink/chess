'''Chess Algebraic Notation Module'''

class NotationError(Exception): pass

class Notation(object):

    def __init__(self, board):
        self.board = board

    def getNotation(self, orig_position, piece, capture, check, check_mate):
        '''Given a piece's original position, and piece already played
           Return an algebraic notation expression
        '''

        # TO DO: check if another piece of this type could also have moved
        #        to the same postion

        if piece.char == 'P':
            an = piece.position
        else:
            an = piece.char + piece.position
        #else:
        #    an = '%s^%s' % (orig_position, piece)
        
        if capture:
            if len(an) == 2:
                an = orig_position[0] + 'x' + an
            else:
                an = an[0] + 'x' + an[1:]
        elif check:
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
        if an == '0-0':
            print 'King side castle'
            return 'pending'
        if an == '0-0-0':
            print 'Queen side castle'
            return 'pending'

        # Preprocessing
        print 'an:', an
        if len(an) < 2:
            raise NotationError('Invalid notation: %s' % an)

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
                    raise NotationError('Unrecognized first leter: %s' % an[0])
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
                raise NotationError('Illegal move: %s' % orig_an)
            print 'Promotion to: %s' % piece_char
            return piece, position

        # Two or three chars, eq. Nc3
        if num_char in (2, 3):
            if num_char == 2:
                piece_char = 'P'
                position = an
            else:
                piece_char = an[0]
                position = an[1:]
            pos_pieces = []
            for piece in self.board.getActivePieces(color):
                if piece.char == piece_char:
                    for pp in self.board.possibleMoves(piece, check_check=0):
                        if pp == position:
                            pos_pieces.append(piece)
                            break
            if not pos_pieces:
                raise NotationError('Move not possible: %s' % orig_an)
            elif len(pos_pieces) == 1:
                piece = pos_pieces[0]
            else:
                raise NotationError('Ambiguous move: %s: (%s)' %
                                    (an, ', '.join(map(str, pos_pieces))))
            return piece, position
        
        raise NotationError('Unrecognzied notation: %s' % an)
        
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
    
