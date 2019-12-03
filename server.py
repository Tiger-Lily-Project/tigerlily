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
from plant import Plant
from flask import json

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

# Renders the home page.
@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():

    species = request.form.getlist("species")
    if species is None:
        species = ''
    status = request.form.getlist("status")
    if status is None:
        status = ''
    dec_or_evg = request.form.getlist("dec_or_evg")
    if dec_or_evg is None:
        dec_or_evg = ''

    # Gets a list of all plants available in the database.
    try:
        database = Database()
        database.connect()
        plants = database.get_filtered_plants(200, species, status, dec_or_evg)

        all_species = database.get_all_species()

        status_vals = database.get_status_vals()
        
        dec_or_evg_vals = database.get_dec_or_evg_vals()

        # print("in try")
        # plants = []
        # plant1 = Plant("plant1", 40.3471, -74.6566, "rip")
        # print("made a plant")
        # plant1 = Plant.getDict(plant1)
        # print("got json")
        # plants.append(plant1)
        # print(plants)

        database.disconnect()
    except Exception as e:
        plants = []
    except Error as e:
        plants = []
    #     print(e)

    print("index in server.py: ")
    print(plants)

    plants = json.dumps(plants)

    # Render the home page, passing in the list of plants.
    html = render_template('index.html', 
    plants = plants,
    all_species = all_species,
    status_vals = status_vals,
    dec_or_evg_vals = dec_or_evg_vals)

    response = make_response(html)

    return response
#-----------------------------------------------------------------------

# Renders the details page.
@app.route('/')
@app.route('/plantdetails')
def plantdetails():

    common_name = request.args.get("common_name")
    # Gets a the information on the requested species.
    try:
        database = Database()
        database.connect()
        species_info = database.get_species_info(common_name)
        count = database.get_species_count(common_name)
        database.disconnect()
    except Exception as e:
        species_info = SpeciesInfo('','','','','')
        count = 0
    except Error as e:
        species_info = SpeciesInfo('','','','','')
        count = 0

    # Render the details page, passing in the plant.
    html = render_template('plantdetails.html', 
    common_name = common_name, 
    species_info = species_info,
    count = count)
    response = make_response(html)

    return response
#-----------------------------------------------------------------------

# Renders the catalog page.
@app.route('/')
@app.route('/catalog')
def catalog():

    search = request.args.get('search')
    if search is None:
        search = ''

    # Gets a list of all species available in the database.
    try:
        database = Database()
        database.connect()
        species = database.get_species_by_name(search)
        database.disconnect()
    except Exception as e:
        species = []
    except Error as e:
        species = []

    # Render the catalog page, passing in the list of species.
    html = render_template('catalog.html', 
    species = species)
    response = make_response(html)

    return response
#-----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10101, debug=True)
