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

# Renders the home page.
@app.route('/')
@app.route('/index')
def index():

    # Gets a list of all plants available in the database.
    database = Database()
    database.connect()
    plants = database.get_all_plants()
    database.disconnect()

    # Render the home page, passing in the list of plants.
    html = render_template('index.html', plants = plants)
    response = make_response(html)

    return response
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10101, debug=True)
