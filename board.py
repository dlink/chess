#!/usr/bin/python
# -*- coding: utf-8 -*-

class Board(object):

    def __init__(self):
        self.matrix= [[[] for j in range(0, 8)] for i in range(0, 8)]

    def display(self):
        o = ''
        o += '╔═══' + '╤═══' * 7 + '╗\n'
        for i, row in enumerate(self.matrix):
            
            o += '║'
            o += '│'.join(' p ' for r in row)
            o += '║\n'
            
            if i < 7:
                o += '╟───' + '┼───' * 7 + '╢\n'
            else:
                o += '╚═══' + '╧═══' * 7 + '╝\n'
        return o

    
print Board().display()

                
