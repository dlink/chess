#!/usr/bin/python
# -*- coding: utf-8 -*-

from pieces import Pieces, Pawn, Rook, Knight

STANDARD = 'data/standard.board'

class Board(object):

    def __init__(self):
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]

        self.setup()

    def setup(self, setup_data=STANDARD):
        '''Set up the pieces on the board'''
        for row in open(setup_data).readlines():
            row = row.strip()
            p, pos = row.split('-')
            piece = Pieces.getPiece(p)
            self.placePiece(piece, pos)

    def placePiece(self, piece, pos):
        '''Place a piece on the board
             piece is a Piece Object
             pos is in the form of a1, a2, etc
        '''
        file = ord(pos[0])-97  # convert a,b,c, ... -> 0,1,2, ...
        row  = int(pos[1])-1   # convert 1,2,3, ... -> 0,1,2, ...
        self.matrix[row][file] = piece

    def display(self):
        o = ''
        o += '╔═══' + '╤═══' * 7 + '╗\n'
        for i, row in enumerate(reversed(self.matrix)):

            o += '║'
            o += '│'.join(' %s ' % (p if p else ' ') for p in row)
            o += '║\n'
            
            if i < 7:
                o += '╟───' + '┼───' * 7 + '╢\n'
            else:
                o += '╚═══' + '╧═══' * 7 + '╝\n'
        return o

    
print Board().display()

                
