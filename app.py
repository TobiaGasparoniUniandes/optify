import flask
from flask import request
from models.simple_model import parse_model
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/process-models', methods=['GET'])
def home():
    # print(request.is_json)
    dt = request.get_json()
    # print(json.dumps(dt, indent=4))
    return parse_model(dt['sets'],
                       dt['indexes'],
                       dt['parameters'],
                       dt['variables'],
                       dt['constraints'],
                       dt['objective_functions'])


if __name__ == '__main__':
    app.run()

"""
set FLASK_ENV=development
set FLASK_APP=app.py
flask run

"""
