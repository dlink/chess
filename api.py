#!/usr/bin/python

from flask import Flask, request
from flask_restful import abort, Api, Resource

#from vlib.odict import odict

from board import Board, BoardError

app = Flask(__name__)
api = Api(app)

class BoardR(Resource):
    def __init__(self):
        self.board = getBoard()
        
    def get(self):
        data = {'pieces': []}
        for piece in self.board.pieces:
            data['pieces'].append(piece.data)
        return data

class MoveR(Resource):

    def __init__(self):
        self.board = getBoard()

    def get(self, move_str):
        '''Make a move on the board
           move_str in the form of "x1,y1,x2,y2"
        '''
        try:
            x1, y1, x2, y2 = map(int, move_str.split(','))
        except ValueError:
            abort(404, message = "move most be numbers in the form of " \
                  "'x1,y1,x2,y2'")
        try:
            p, s, e, m = self.board.move2(x1, y1, x2, y2)
        except BoardError, e:
            abort(404, message = str(e))

        # testing data only
        data = {
            'move_str': move_str,
            'piece_name': p,
            'start_position': s,
            'end_destination': e,
            'move': m,
        }
        return data
    
api.add_resource(BoardR, '/board')
api.add_resource(MoveR, '/move/<move_str>')

class BoardFactory():
    '''Singleton factory class for Board class'''

    def __init__(self):
        self._board = None

    def getInstance(self):
        if not self._board:
            self._board = Board()
        return self._board

boardFactory = BoardFactory()
def getBoard():
    return boardFactory.getInstance()

if __name__ == '__main__':
    app.run(debug=True)
