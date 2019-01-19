# -*- coding: utf-8 -*-

class BoardDisplay(object):
    
    def __init__(self, board):
        self.board = board
        
    def one_line(self):
        '''Return a representation of the board in one line
           RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr
        '''
        o = ''
        for i, row in enumerate(reversed(self.board.matrix)):
            o += ''.join('%s' % (p.char_glyph if p else '.') for p in row)
        return o

    def simple(self):
        '''Return a simple representation of the board as text

           R N B Q K B N R
           P P P P P P P P
           . . . . . . . .
           . . . . . . . .
           . . . . . . . .
           . . . . . . . .
           p p p p p p p p
           r n b q k b n r
        '''
        o = ''
        for i, row in enumerate(reversed(self.board.matrix)):
            o += ' '.join('%s' % (p.glyph if p else '.') for p in row) + '\n'
        return o

    def standard(self):
        '''Return an ASCII representation of the board with boarders
           and row and file labels as text

               a   b   c   d   e   f   g   h
             ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗
           8 ║ R │ N │ B │ Q │ K │ B │ N │ R ║ 8
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           7 ║ P │ P │ P │ P │ P │ P │ P │ P ║ 7
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           6 ║   │   │   │   │   │   │   │   ║ 6
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           5 ║   │   │   │   │   │   │   │   ║ 5
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           4 ║   │   │   │   │   │   │   │   ║ 4
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           3 ║   │   │   │   │   │   │   │   ║ 3
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           2 ║ p │ p │ p │ p │ p │ p │ p │ p ║ 2
             ╟───┼───┼───┼───┼───┼───┼───┼───╢
           1 ║ r │ n │ b │ q │ k │ b │ n │ r ║ 1
             ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝
               a   b   c   d   e   f   g   h
        '''
        o = ''
        o += '    a   b   c   d   e   f   g   h\n'
        o += '  ╔═══' + '╤═══' * 7 + '╗\n'
        for i, row in enumerate(reversed(self.board.matrix)):

            o += '%s ║' % (8-i)
            o += '│'.join(' %s ' % (p.char_glyph if p else ' ') for p in row)
            o += '║ %s\n' % (8-i)

            if i < 7:
                o += '  ╟───' + '┼───' * 7 + '╢\n'
            else:
                o += '  ╚═══' + '╧═══' * 7 + '╝\n'
                o += '    a   b   c   d   e   f   g   h\n'
        return o


