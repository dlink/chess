#!/usr/bin/python

from flask import Flask, request
from flask_restful import Resource, Api

#from vlib.odict import odict

from board import Board

app = Flask(__name__)
api = Api(app)

class BoardR(Resource):
    def __init__(self):
        self.board = Board()
        
    def get(self):
        #return {'hi': 'there'}
        data = {'pieces': []}
        for piece in self.board.pieces:
            data['pieces'].append(piece.data)
        return data
    
api.add_resource(BoardR, '/board')

if __name__ == '__main__':
    app.run(debug=True)
