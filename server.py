#!/usr/bin/env python

#-----------------------------------------------------------------------
# server.py
# Server to host our web app.
#-----------------------------------------------------------------------

from sys import argv, stderr
from database import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from sqlite3 import Error

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():

    html = render_template('index.html')
    response = make_response(html)

    return response
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10101, debug=True)
