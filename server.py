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
    try:
        database = Database()
        database.connect()
        plants = database.get_n_plants(30)
        database.disconnect()
    except Exception as e:
        plants = []
    except Error as e:
        plants = []

    # Render the home page, passing in the list of plants.
    html = render_template('index.html', plants = plants)
    response = make_response(html)

    return response
#-----------------------------------------------------------------------

# Renders the home page.
@app.route('/')
@app.route('/plantdetails')
def plantdetails():

    common_name = request.args.get("common_name")
    # Gets a list of all plants available in the database.
    try:
        database = Database()
        database.connect()
        species_info = database.get_species_info(common_name)
        database.disconnect()
    except Exception as e:
        species_info = SpeciesInfo('','','','','')
    except Error as e:
        species_info = SpeciesInfo('','','','','')

    # Render the home page, passing in the list of plants.
    html = render_template('plantdetails.html', 
    common_name = common_name, 
    species_info = species_info)
    response = make_response(html)

    return response
#-----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10101, debug=True)
