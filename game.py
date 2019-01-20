#!/usr/bin/python

import os
import sys

from random import randint, seed

from board import Board


class GameError(Exception): pass

class Game(object):
    def __init__(self):
        self.board = Board(display_type='standard',
                           setup_data='data/standard.board') 
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
        print self.board.display.display()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            self.whiteMove(self.randomMove('w'))
            self.blackMove(self.userMove('b'))

    def playBlack(self):
        os.system('clear')
        print self.board.display.display()
        print 'starting board'
        for i in range(0,100):
            self.whiteMove(self.userMove('w'))
            self.blackMove(self.randomMove('b'))

    def selfPlay(self):
        os.system('clear')
        print self.board.display.display()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            self.whiteMove(self.randomMove('w'))
            self.user_pause()
            self.blackMove(self.randomMove('b'))
            self.user_pause()

    def userMove(self, color):
        input_okay = 0
        while not input_okay:
            input = raw_input('Enter move, x to exit: ')
            if input.lower() == 'x':
                self.endGame()
            try:
                char, position = input.split('-')
                piece = self.board.getPiece(char, color)
                self.board.movePiece(piece, position)
            except Exception, e:
                print str(e)
                continue
            input_okay = 1
        return piece

    def randomMove(self, color):
        pieces = self.board.getActivePieces(color)
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

    def whiteMove(self, move):
        print 
        print self.board.display.display()
        if self.board.check_mate['b']:
            print '  CHECK MATE'
            move = str(move) + '#'
        elif self.board.in_check['b']:
            print '  Check'
            move = str(move) + '+'
            
        self.history.append([move,''])
        print self.display_history()
        print
        
        if self.board.check_mate['b']:
            self.endGame()

    def blackMove(self, move):
        print
        print self.board.display.display()
        if self.board.check_mate['w']:
            print 'CHECK MATE ON WHITE'
            move = str(move) + '#'
        elif self.board.in_check['w']:
            print 'CHECK ON WHITE'
            move = str(move) + '+'

        self.history[-1][1] = move
        print self.display_history()
        print
        
        if self.board.check_mate['w']:
            self.endGame()

    def user_pause(self):
        input = raw_input('Enter to continue, X to exit ')
        if input.lower() == 'x':
            self.endGame()

    def endGame(self):
        print 'Ending Game.'
        sys.exit(0)

if __name__ == '__main__':
    game = Game()
    #game.selfPlay()
    #game.playWhite()
    game.playBlack()
    
    #print game.board.display.display()
    #print 'state:'
    #print game.state

    #print 'possible moves:'
    #for i, p in enumerate(game.board.pieces):
    #    print '%s.' % (i+1), p, game.board.possibleMoves(p)

    '''
    white_move =  game.board.movePiece(game.board.pieces[0], 'e7')
    print game.board.display.display()
    move = [white_move, None]
    game.history.append(move)
    print game.history

    black_move = game.board.movePiece(game.board.pieces[17], 'f1')
    print game.board.display.display()
    game.history[-1][1] = black_move
    print game.history
    '''
g
