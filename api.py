import flask
from flask import request, jsonify, redirect, url_for
from model.simple_model import parse_model
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/process-model', methods=['GET'])
def home():
    print(request.is_json)
    dt = request.get_json()
    print(json.dumps(dt, indent=4))
    return parse_model(dt['parameters'],
                       dt['variables'],
                       dt['restrictions'],
                       dt['objective_functions'])


if __name__ == '__main__':
    app.run()
