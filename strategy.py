

class Strategy(object):

    def __init__(self, board):
        self.board = board

    @property
    def evaluation(self):
        o = ''
        o += 'Material Advantage: %s:%s\n' % self.materialAdvantage()
        wd, bd, wc, bc = self.developmentAndCenterAdvantage()
        o += 'Development Advantage: %s:%s\n' %  (wd, bd)
        o += 'Center Control Advantage: %s:%s' %  (wc, bc)
        return o
    
    def evaluation2(self):
        wma, bma = self.materialAdvantage()
        wda, bda, wcca, bcca = self.developmentAndCenterAdvantage()
        return wma-bma, wda-bda, wcca-bcca
        return o

    def materialAdvantage(self):
        '''Return material advantage scores as a tuple for White and for Black
        '''
        white = sum([p.value for p in self.board.getActivePieces('w')])
        black = sum([p.value for p in self.board.getActivePieces('b')])
        diff =  white - black
        if diff > 0:
            return diff, 0
        return 0, -diff

    def developmentAndCenterAdvantage(self):
        '''Return development advantage and center control advantage'''
        
        center = ['d4', 'e4', 'd5', 'e5']

        white_development = 0
        white_center = 0
        for piece in self.board.getActivePieces('w'):
            possibilities = self.board.possibleMoves(
                piece, check_check=0, captureable_only=1)
            
            # development
            if piece.char in ('r', 'n', 'b', 'q'):
                white_development += len(possibilities)
                
            # center control
            for c in center:
                if c in possibilities:
                    white_center += 1
                    
        black_development = 0
        black_center = 0
        for piece in self.board.getActivePieces('b'):
            possibilities = self.board.possibleMoves(
                piece, check_check=0, captureable_only=1)
            # development
            if piece.char in ('r', 'n', 'b', 'q'):
                black_development  += len(possibilities)

            # center_control
            for c in center:
                if c in possibilities:
                    black_center += 1
                
        dev_diff = white_development - black_development
        if dev_diff > 0:
            wd, bd =  dev_diff, 0
        else:
            wd, bd =  0, -dev_diff

        center_diff = white_center - black_center
        if center_diff > 0:
            wc, bc = center_diff, 0
        else:
            wc, bc = 0, -center_diff

        return wd, bd, wc, bc
            
    def centerControl(self):
        
        white = 0
        for piece in self.board.getActivePieces('w'):
            white += len(self.board.possibleMoves(piece, check_check=0))
        black = 0
        for piece in self.board.getActivePieces('b'):
            if piece.char in ('r', 'n', 'b', 'q'):
                black += len(self.board.possibleMoves(piece, check_check=0))
        print 'white-black:', white, black
        diff = white - black
        if diff > 0:
            return diff, 0
        return 0, -diff
    
            
            
if __name__ == '__main__':
    from board import Board
    s = Strategy(Board())
    s.materialadvantage()
    
        
