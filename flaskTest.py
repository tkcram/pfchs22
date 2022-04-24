from src import test_maze, api_test
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/createMaze/<size>/<row>/<col>/<level>')
@cross_origin()
def test_function(size,row,col,level):
	maze = test_maze.createMaze(size,row,col,level)
	return maze

@app.route("/createCharacter/<level>")
@cross_origin()
def test_function_two(level):
	character = api_test.createCharacter(level)
	return character
