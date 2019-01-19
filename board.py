#!/usr/bin/python
# -*- coding: utf-8 -*-

from pieces import Pawn, Rook, Knight

class Board(object):

    def __init__(self):
        self.matrix= [[None for j in range(0, 8)] for i in range(0, 8)]

        # test
        self.matrix[0][0] = Rook()
        self.matrix[0][1] = Knight()
        self.matrix[1][0] = Pawn()

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

                
