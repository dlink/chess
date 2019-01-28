#!/usr/bin/python

'''Game Module

   Example:

   Play a game, human plays white against computer on a standard board
     game = Game('h', 'w', 'standard')
     game.play()
'''

import sys
from copy import deepcopy
from random import randint

from cli import CLI
from board import Board, BoardError
from notation import NotationError
from strategy import Strategy

class GameError(Exception): pass

class Game(object):
    '''Preside over a chess game
       A game has a white player and a black player,
         each can either be a human 'h' or the computer 'c'
       A user introduces moves into the game by using Standard
         Algebraic Notation (SAN)
    '''

    def __init__(self, white_player, black_player, board):
        '''Game constructor
            white player {'h'|'c'} (Human or Computer)
            black player {'h'|'c'} (Human or Computer)
            board - board set up data, eq.: 'standard'
        '''
        self.players = {'w': white_player,
                        'b': black_player}
        self.board = Board(display_type='standard',
                           setup_data='data/%s.board' % board)
        # TO DO: move history out of Game and into Board
        self.history = []

    def display_history(self):
        '''Return a string of all moves made so far in standard algebraic
           notation
        '''
        # TO DO: move this method into Board
        o = []
        for i, move in enumerate(self.history):
            o.append('%s. %s %s' % (i+1, move[0], move[1]))
        return ' '.join(o)

    def play(self):
        '''Start the game'''

        players_key = '%s%s' % (self.players['w'], self.players['b'])
        if   players_key == 'hc': start_message = 'You play white'
        elif players_key == 'ch': start_message = 'You play black'
        elif players_key == 'cc': start_message = 'Computer plays itself'
        else:                     start_message = 'You play black and white'

        print start_message
        print
        print self.board.display.display()
        for i in range(0, 200):
            if players_key == 'cc':
                self.pause()
            self.displayMove(self.getMove('w'))
            self.displayMove(self.getMove('b'))

    def displayMove(self, move_color):#move, color):
        move, color = move_color
        print
        print self.board.display.display()
        if self.board.check_mate[color]:
            print '  CHECK MATE'
            #move = str(move) + '#'
        elif self.board.in_check[color]:
            print '  Check'
            #move = str(move) + '+'

        # TO DO: move history maintanance into Board
        if color == 'w':
            self.history.append([move,''])
        else:
            self.history[-1][1] = move

        print self.display_history()
        print Strategy(self.board).evaluation
        print

        if self.board.check_mate[color]:
            self.endGame()

    def getMove(self, color):
        '''Given a color {'w'|'b'}
           Return the results of either a userMove() or a computerMove()
           depending on whose playing white and whose playing black
        '''
        if self.players[color] == 'h':
            return self.userMove(color)
        return self.computerMove(color)

    def userMove(self, color):
        '''Human user makes a move by typing it in in standard notation
           Moves entered does no have to include 'x' for capture or '+/#'
             for check
           Raises NotationError and BoardError
           Returns move as string in standard notation, and color
        '''
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
        return an, color

    def computerMove(self, color):
        '''Computer makes a move
           Uses Stragegy Module
           Returns move as string in standard notation and color
        '''
        best_piece = None
        best_piece_move = None
        best_piece_move_score = None

        for i, piece in enumerate(self.board.getActivePieces(color)):

            best_move = None
            best_move_score = None

            for j, new_position in enumerate(
                    self.board.possibleMoves(piece, check_check=0)):
                # build hypothetical board
                hboard = deepcopy(self.board)
                hboard.name = 'hboard2'
                hpiece = hboard.getPieceAt(piece.position)
                # make the move
                hboard.movePiece(hpiece, new_position, check_legal=0,
                                     check_check=0)
                ma, da, cca = Strategy(hboard).evaluation2()
                score = ma + da + cca
                # try looking one more turn
                '''
                for hype_piece2 = hboard.getActivePieces(piece.opposite_color):
                    black_best_move = None
                    black_best_move_score = None
                    for m, new_position2 in enumerate(
                            hboard.possibleMoves(hpiece2, check_check=0)):
                        ma, da, cca = Strategy(hboard).evaluation2()
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
                del hboard
            if not best_piece or best_move_score > best_piece_move_score:
                best_piece = piece
                best_piece_move = best_move
                best_piece_move_score = best_move_score
        #orig_position = best_piece.position
        an = self.board.movePiece(best_piece, best_piece_move, check_legal=0)
        return an, color

    def randomMove(self, color):
        '''Computer makes a random move
           Used for dbug
        '''
        # TO DO: fix this function to return string in standard notation
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

    def pause(self):
        '''Pause game
           Allow user to see the board before computer makes next move
        '''
        input = raw_input('Enter to continue, X to exit ')
        if input.lower() == 'x':
            self.endGame()

    def endGame(self):
        '''End the Game'''
        print 'Ending Game.'
        sys.exit(0)


# Command Line Interface

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

if __name__ == '__main__':
    GameCLI().run()
