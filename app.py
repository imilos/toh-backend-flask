from flask import Flask, send_from_directory, request
from flask import jsonify
import os
from in_memory_db import IMDB

app = Flask(__name__)
imdb = IMDB()
BASE_URL = os.path.abspath(os.path.dirname(__file__))
CLIENT_APP_FOLDER='./tour/'

def route_error(code, message):
	print('Error!:', code, message)
	response = jsonify({'message':message})
	response.status_code = code
	return response

#-----File server

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./tour', path)


@app.route('/')
def root():
  return send_from_directory('./tour', 'index.html')


# API rute
@app.route('/api/heroes', methods=['GET'])
def getAllHeroes():
    return jsonify(imdb.getAllHeroes())

@app.route('/api/heroes/<int:heroId>', methods=['GET'])
def getHero(heroId):
	return jsonify(imdb.getHero(heroId))

#@app.route('/api/heroes/<int:heroId>', methods=['PUT'])
@app.route('/api/heroes', methods=['PUT'])
#def updateHero(heroId):
def updateHero():
	podaci = request.json
	return jsonify(imdb.updateHero(podaci['id'], podaci))

@app.route('/api/heroes', methods=['POST'])
def createHero():
	return jsonify(imdb.createHero(request.json))

@app.route('/api/heroes/<int:id>', methods=['DELETE'])
def deleteHero(id):
	imdb.deleteHero(id)
	return jsonify('success')

@app.route('/api/heroes/', methods=['GET'])
def searchHero():
	return jsonify(imdb.searchHero(request.args))

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

