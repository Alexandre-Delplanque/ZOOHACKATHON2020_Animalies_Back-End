from flask import Flask
from flask import jsonify
from flask_cors import CORS

from .datamodel import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
dataset = DataSetFromShapeFile("./shpfiles/etosha_15_elephant_3857/etosha_15_elephants_EPSG3857", [])

@app.route('/elephants/<id>')
def elephant_with_id(id):
    return jsonify([ a.to_dict() for a in dataset.filter(IdDataFilter(id)) ])

@app.route('/elephants/<id>/timespan/<start>/<stop>')
def elephant_time_filter(start, stop):
    return "TODO"

@app.route('/areas')
def areas():
    return "TODO"


