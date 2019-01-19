#!/usr/bin/python
import os

from random import randint

from board import Board

class GameError(Exception): pass

class Game(object):
    def __init__(self):
        self.board = Board('data/pawns_only.board')
        self.state = [self.board, '']
        self.history = []
        self.moves = []

    def display_history(self):
        o = []
        for i, move in enumerate(self.history):
            o.append('%s. %s %s' % (i+1, move[0], move[1]))
        return ', '.join(o)

    def selfPlay(self):
        os.system('clear')
        print self.board.display.simple()
        click = raw_input('click any key to continue')
        for i in range(0,100):
            white_move = self.randomMove('w')
            os.system('clear')
            print self.board.display.simple()
            print self.display_history()
            print
            click = raw_input('Hit entier to continue')


            black_move = self.randomMove('b')
            self.history.append((white_move, black_move))
            os.system('clear')
            print self.board.display.simple()
            print self.display_history()
            print
            click = raw_input('Hit entier to continue')

    def randomMove(self, color):
        pieces = [p for p in self.board.pieces if p.color == color]
        possible_moves = None
        moveable_piece_found = 0
        while not moveable_piece_found:
            dice = randint(0, len(pieces)-1)
            piece = pieces[dice]
            possible_moves = self.board.possibleMoves(piece)
            if not possible_moves:
                del pieces[dice]
                if not pieces:
                    raise GameError('White can not move')
                continue
            moveable_piece_found = 1

        dice = randint(0, len(possible_moves)-1)
        position = possible_moves[dice]
        return self.board.movePiece(piece, position)



if __name__ == '__main__':
    game = Game()
    game.selfPlay()

    #print game.board.display.simple()
    #print 'state:'
    #print game.state

    #print 'possible moves:'
    #for i, p in enumerate(game.board.pieces):
    #    print '%s.' % (i+1), p, game.board.possibleMoves(p)

    '''
    white_move =  game.board.movePiece(game.board.pieces[0], 'e7')
    print game.board.display.simple()
    move = [white_move, None]
    game.history.append(move)
    print game.history

    black_move = game.board.movePiece(game.board.pieces[17], 'f1')
    print game.board.display.simple()
    game.history[-1][1] = black_move
    print game.history
    '''
