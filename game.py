#!/usr/bin/python

import os
import sys
from copy import deepcopy
from random import randint, seed

from vlib.cli import CLI
from cli import CLI

from board import Board, BoardError
from notation import NotationError
from strategy import Strategy

class GameCLIError(Exception): pass

class GameCLI(object):
    '''Game Command Line Interface'''

    def run(self):
        '''Setup ommands and options. Launch CLI process'''

        commands = ['<white:h> <black:c> <board:standard>']
        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests'''

        white = 'h'
        black = 'c'
        board = 'standard'
        
        args = list(args)
        if len(args) == 1:
            white = args.pop(0)
        elif len(args) == 2:
            white = args.pop(0)
            black = args.pop(0)
        elif len(args) == 3:
            white = args.pop(0)
            black = args.pop(0)
            board = args.pop(0)
            
        game = Game(white, black, board)
        game.play()
        
class GameError(Exception): pass

class Game(object):
    
    def __init__(self, white, black, board):
        self.white = white
        self.black = black
        self.board = Board(display_type='standard',
                           setup_data='data/%s.board' % board)
        self.state = [self.board, '']
        self.history = []
        self.moves = []
        seed(1)

    def display_history(self):
        o = []
        for i, move in enumerate(self.history):
            o.append('%s. %s %s' % (i+1, move[0], move[1]))
        return ' '.join(o)

    def play(self):
        white = self.white
        black = self.black
        if white == 'h' and black == 'c':
            self.playBlack()
        elif white == 'c' and black == 'h':
            self.playWhite()
        elif white == 'c' and black == 'c':
            self.selfPlay()
        else:
            raise GameError('unrecognized white and black options: %s, %s. '
                            'Should be h c, c h, or c c' % white, black)
    
    def playWhite(self):
        os.system('clear')
        print 'You Play Black'
        print self.board.display.display()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            self.whiteMove(self.computerMove('w'))
            self.blackMove(self.userMove('b'))

    def playBlack(self):
        os.system('clear')
        print 'You Play White'
        print self.board.display.display()
        print 'starting board'
        for i in range(0,100):
            self.whiteMove(self.userMove('w'))
            self.blackMove(self.computerMove('b'))

    def selfPlay(self):
        os.system('clear')
        print 'Computer plays itself'
        print self.board.display.display()
        print 'starting board'
        self.user_pause()
        for i in range(0,100):
            self.whiteMove(self.computerMove('w'))
            self.user_pause()
            self.blackMove(self.computerMove('b'))
            self.user_pause()

    def userMove(self, color):
        input_okay = 0
        while not input_okay:
            an = raw_input('Enter move, x to exit: ')
            if not an:
                continue
            if an.lower() == 'x':
                self.endGame()
            try:
                an = self.board.move(an, color)
            except (NotationError, BoardError), e:
                print str(e)
                continue
            input_okay = 1
        return an
        
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
                # try looking one more turn
                '''
                for hype_piece2 = hypo_board.getActivePieces(piece.opposite_color):
                    black_best_move = None
                    black_best_move_score = None
                    for m, new_position2 in enumerate(
                            hypo_board.possibleMoves(hypo_piece2, check_check=0)):
                        ma, da, cca = Strategy(hypo_board).evaluation2()
                        sore = ma, da, cca
                        if piece.opposite_color == 'b':
                            score = -score
                        if m == 0 or score < black_best_move:
                            black_best_move = new_position2
                            black_best_move_score = score
                        black_best_move 
                '''
                if color == 'b':
                    score = -score
                if j == 0 or score > best_move_score:
                    best_move = new_position
                    best_move_score = score
                del hypo_board
            if not best_piece or best_move_score > best_piece_move_score:
                best_piece = piece
                best_piece_move = best_move
                best_piece_move_score = best_move_score
        #orig_position = best_piece.position
        an = self.board.movePiece(best_piece, best_piece_move, check_legal=0)
        return an
                
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
    GameCLI().run()
