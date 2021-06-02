#!/usr/bin/python

from flask import Flask, request
from flask_restful import abort, Api, Resource

from game import Game

app = Flask(__name__)
api = Api(app)

class BoardR(Resource):
    def __init__(self):
        self.game = getGame()
        
    def get(self):
        data = {'pieces': []}
        for piece in self.game.board.pieces:
            data['pieces'].append(piece.data)
        return data

class MoveR(Resource):

    def __init__(self):
        self.game = getGame()

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
            p, s, e, m = self.game.board.move2(x1, y1, x2, y2)
            x = self.game.computerMove('b')
        except Exception, e: #BoardError, e:
            abort(404, message = str(e))

        data = {'pieces': []}
        for piece in self.game.board.pieces:
            data['pieces'].append(piece.data)
        return data

        # testing data only
        data = {
            'move_str': move_str,
            'piece_name': p,
            'start_position': s,
            'end_destination': e,
            'move': m,
        }
        # board pieces
        data['pieces'] = []
        for piece in self.game.board.pieces:
            data['pieces'].append(piece.data)
        return data
    
api.add_resource(BoardR, '/board')
api.add_resource(MoveR, '/move/<move_str>')

class GameFactory():
    '''Singleton factory class for Game class'''

    def __init__(self):
        self._game = None

    def getInstance(self):
        if not self._game:
            self._game = Game('h', 'c', 'standard', None)
        return self._game

gameFactory = GameFactory()
def getGame():
    return gameFactory.getInstance()

if __name__ == '__main__':
    app.run(debug=True)
