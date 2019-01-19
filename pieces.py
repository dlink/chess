class Pieces(object):
    
    @staticmethod
    def getPiece(p):
        if p == 'p':
            return Pawn()
        elif p == 'r':
            return Rook()
        elif p == 'n':
            return Knight()
        else:
            raise PiecesError('Unrecognzied piece abbreviation: %s' % p)

class Piece(object):
    def __init__(self):
        pass
    
    def __repr__(self):
        return 'r'

class Pawn(Piece):
    def __repr__(self):
        return 'p'
    
class Rook(Piece):
    def __repr__(self):
        return 'r'
    
class Knight(Piece):
    def __repr__(self):
        return 'n'
    
