#!/usr/bin/python

import os
import sys

from random import randint, seed

from board import Board


class GameError(Exception): pass

class Game(object):
    def __init__(self):
        self.board = Board('data/3rooks_and_kings.board')
        self.state = [self.board, '']
        self.history = []
        self.moves = []
        seed(1)

    def display_history(self):
        o = []
        for i, move in enumerate(self.history):
            o.append('%s. %s %s' % (i+1, move[0], move[1]))
        return ', '.join(o)

    def playWhite(self):
        os.system('clear')
        print self.board.display.simple()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            white_move = self.randomMove('w')
            self.history.append([white_move,''])
            #os.system('clear')
            print self.board.display.simple()
            if self.board.in_check['b']:
                print 'CHECK ON BLACK'
            print self.display_history()

            black_move = self.userMove('b')
            self.history[-1][1] = black_move
            #os.system('clear')
            print self.board.display.simple()
            if self.board.in_check['w']:
                print 'CHECK ON WHITE'
            print self.display_history()
            self.user_pause()

    def selfPlay(self):
        os.system('clear')
        print self.board.display.simple()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            white_move = self.randomMove('w')
            self.history.append([white_move,''])
            #os.system('clear')
            print self.board.display.simple()
            if self.board.in_check['b']:
                print 'CHECK ON BLACK'
            print self.display_history()
            self.user_pause()

            black_move = self.randomMove('b')
            self.history[-1][1] = black_move
            #os.system('clear')
            print self.board.display.simple()
            if self.board.in_check['w']:
                print 'CHECK ON WHITE'
            print self.display_history()
            self.user_pause()

    def userMove(self, color):
        input = raw_input('Enter move, x to exit: ')
        input_okay = 0
        while not input_okay:
            if input.lower() == 'x':
                self.endGame()
            try:
                char, position = input.split('-')
            except Exception, e:
                print str(e)
            input_okay = 1
        piece = self.board.getPiece(char, color)
        self.board.movePiece(piece, position)
        return piece

    def randomMove(self, color):
        pieces = [p for p in self.board.pieces
                  if p.color == color and p.position != 'x']
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
        return self.board.movePiece(piece, position, check_legal=0)

    def user_pause(self):
        input = raw_input('Enter to continue, X to exit ')
        if input.lower() == 'x':
            self.endGame()

    def endGame(self):
        print 'Ending Game.'
        sys.exit(0)

if __name__ == '__main__':
    game = Game()
    game.selfPlay()
    #game.playWhite()

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
