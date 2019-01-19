#!/usr/bin/python

from board import Board

class Game(object):
    def __init__(self):
        self.board = Board()
        self.state = [self.board, '']
        self.moves = []

if __name__ == '__main__':
    game = Game()
    print game.board.display()
    print game.state
    print ['%s%s' % (p.char, p.position) for p in game.board.pieces]
    p1 = game.board.pieces[10]
    print 'p1:', p1, p1.position, game.board.possibleMoves(p1)
