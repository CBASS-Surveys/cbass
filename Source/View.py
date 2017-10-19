#!/bin/python
# coding: utf-8

import flask

import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
app = flask.Flask(__name__, static_url_path='/static')


def __init__(self):
    print("not much")


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/get")
def get():
    return flask.jsonify(flask.request.args)


@app.route("/post", methods=['POST'])
def post():
    return flask.jsonify(flask.request.get_json())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
