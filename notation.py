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
        orig_an = an
        if an[-1] == '+':
            print 'check'
            an = an[0:-1]
        elif an[-1] == '#':
            print 'checkmate'
            an = an[0:-1]

        num_char = len(an)
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
            if not piece:
                raise NotationsError('Illegal move: %s' % an)
            
        elif num_char == 3:
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
                raise NotationsError('Illegal move: %s' % orig_an)
            elif len(pos_pieces) == 1:
                piece = pos_pieces[0]
            else:
                raise NotationsError('Ambiguous move: %s: (%s)' %
                                    (an, ', '.join(map(str, pos_pieces))))
        else:
            raise NotationsError('Unrecognzied notation: %s' % an)
        return piece, position
        
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

    board_ = Board(setup_data='data/2rooks_and_kings.board')
    
    n = Notations(board_)
    print n.getPieceAndDest(an, color)
    
