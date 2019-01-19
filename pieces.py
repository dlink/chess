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
    
