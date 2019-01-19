#!/usr/bin/python

from board import Board

class Game(object):
    def __init__(self):
        self.board = Board()
        self.state = [self.board, '']
        self.history = []
        self.moves = []

if __name__ == '__main__':
    game = Game()
    print game.board.display.simple()
    #print 'state:'
    #print game.state
    
    #print ['%s%s' % (p.char, p.position) for p in game.board.pieces]
    #print 'possible moves:'
    #for i, p in enumerate(game.board.pieces):
    #    print '%s.' % (i+1), p, game.board.possibleMoves(p)
    
    white_move =  game.board.movePiece(game.board.pieces[0], 'e7')
    print game.board.display.simple()
    move = [white_move, None]
    game.history.append(move)
    print game.history
    
    black_move = game.board.movePiece(game.board.pieces[17], 'f1')
    print game.board.display.simple()
    game.history[-1][1] = black_move
    print game.history
    
