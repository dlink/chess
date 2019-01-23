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
        if len(an) == 2:
            x, y = position2xy(an)
            vector = -1 if color == 'w' else 1
            for j in range(y+vector, y+3*vector, vector):
                piece = self.board.matrix[j][x]
                if piece:
                    break
            if not piece:
                raise NotationsError('Illegal move: %s' % an)
            return piece, an
            
        else:
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
    
    n = Notations(Board())
    print n.getPieceAndDest(an, color)
    
