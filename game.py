#!/usr/bin/python

import os
import sys
from copy import deepcopy

from random import randint, seed

from board import Board
from strategy import Strategy

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
            #self.whiteMove(self.randomMove('w'))
            self.whiteMove(self.computerMove('w'))
            self.blackMove(self.userMove('b'))

    def playBlack(self):
        os.system('clear')
        print self.board.display.display()
        print 'starting board'
        for i in range(0,100):
            self.whiteMove(self.userMove('w'))
            #self.blackMove(self.randomMove('b'))
            self.blackMove(self.computerMove('b'))

    def selfPlay(self):
        os.system('clear')
        print self.board.display.display()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            #self.whiteMove(self.randomMove('w'))
            self.whiteMove(self.computerMove('w'))
            self.user_pause()
            #self.blackMove(self.randomMove('b'))
            self.blackMove(self.computerMove('b'))
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

    def computerMove(self, color):
        best_piece = None
        best_piece_move = None
        best_piece_move_score = None
        
        for i, piece in enumerate(self.board.getActivePieces(color)):

            best_move = None
            best_move_score = None
            
            for j, new_position in enumerate(
                    self.board.possibleMoves(piece, check_check=0)):
                # build hypothetical board
                hypo_board = deepcopy(self.board)
                hypo_board.name = 'hypo_board2'
                hypo_piece = hypo_board.getPieceAt(piece.position)
                # make the move
                hypo_board.movePiece(hypo_piece, new_position, check_legal=0,
                                     check_check=0)
                ma, da, cca = Strategy(hypo_board).evaluation2()
                score = ma + da + cca

                if color == 'b':
                    score = -score
                if j == 0 or score > best_move_score:
                    best_move = new_position
                    best_move_score = score
                    #print '..best_move:', piece, new_position, best_move_score, ma, da, cca
                del hypo_board
            if not best_piece or best_move_score > best_piece_move_score:
                best_piece = piece
                best_piece_move = best_move
                best_piece_move_score = best_move_score
                #print 'best_piece_move:', best_piece, best_move, best_piece_move_score
        return self.board.movePiece(best_piece, best_piece_move, check_legal=0)
            
                
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
        print Strategy(self.board).evaluation
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
        print Strategy(self.board).evaluation
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
    game.selfPlay()
    #game.playWhite()
    #game.playBlack()
    
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
