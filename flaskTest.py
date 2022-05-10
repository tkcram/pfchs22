from src import create_maze, create_character
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/createMaze/<size>/<row>/<col>/<level>')
@cross_origin()
def test_function(size,row,col,level):
	maze = create_maze.createMaze(size,row,col,level)
	return maze

@app.route("/createCharacter/<level>")
@cross_origin()
def test_function_two(level):
	character = create_character.createCharacter(level)
	return character
