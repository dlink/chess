'''Chess Algebraic Notation Module'''

class NotationsError(Exception): pass

class Notations(object):

    def __init__(self, board):
        self.board = board

    def getNotation(self, piece, destination, color):
        '''Given a piece and a destination and color
           Return an algebraic notation expression
        '''
        pass

    def getPieceAndDest(self, an, color):
        '''Given an algebraic notation expression and color
           Return a piece, and destination
        '''
        # TO DO: handle pawn capture

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
        
        # check  checks: +
        if an[-1] == '+':
            print 'check'
            check = 1
            an = an[0:-1]
            
        # check check make: #
        elif an[-1] == '#':
            print 'checkmate'
            checkmate = 1
            an = an[0:-1]

        # check captures
        if an[1] == 'x':
            print 'capture'
            capture = 1
            an = an[0] + an[2:]
        elif an[2] == 'x':
            print 'capture'
            capture = 1
            an = an[0:1] + an[3:]

        # processing
        
        num_char = len(an)
        # chars, eq.: e4
        if num_char == 2:
            position = an
            x, y = position2xy(an)
            if x > 7 or y > 7:
                raise NotationsError('Illegal move: %s' % an)
            
            vector = -1 if color == 'w' else 1
            for j in range(y+vector, y+3*vector, vector):
                piece = self.board.matrix[j][x]
                if piece:
                    break
            if not piece or piece.color != color:
                raise NotationsError('Illegal move: %s' % orig_an)
            return piece, position
        
        # promption
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

        # Three chars, eq. Nc3
        if num_char == 3:
            piece_char = an[0]
            position = an[1:]
            pos_pieces = []
            for piece in self.board.getActivePieces(color):
                if piece.char == piece_char.lower():
                    for pp in self.board.possibleMoves(piece, check_check=0):
                        if pp == position:
                            pos_pieces.append(piece)
                            break
            if not pos_pieces:
                raise NotationsError('Move not possible: %s' % orig_an)
            elif len(pos_pieces) == 1:
                piece = pos_pieces[0]
            else:
                raise NotationsError('Ambiguous move: %s: (%s)' %
                                    (an, ', '.join(map(str, pos_pieces))))
            return piece, position
        
        raise NotationsError('Unrecognzied notation: %s' % an)
        
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
    board_ = Board(setup_data='data/test.board')
    
    n = Notations(board_)
    print n.getPieceAndDest(an, color)
    
