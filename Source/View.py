#!/bin/python
# coding: utf-8

import time
from flask import Flask, jsonify
from flask import render_template
from werkzeug.contrib.cache import SimpleCache
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
app = application = Flask("VueFlask")
cache = SimpleCache()


def __init__(self):
    print("not much")


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
