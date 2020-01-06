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
from flask_talisman import Talisman

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')
csp = {
 'default-src': '\'self\'',
 'script-src': [
     '\'self\'',
     'https://maps.googleapis.com'
     ],
 'style-src': 'unsafe-inline'
}
talisman = Talisman(app, content_security_policy=None)

#region Index

# Renders the home page.
@app.route('/')
@app.route('/index')
def index():

    # Gets a list of all plants available in the database.
    try:
        database = Database()
        database.connect()

        species = request.args.getlist("species")
        if species is None:
            species = []
        dec_or_evg = request.args.getlist("dec_or_evg")
        if dec_or_evg is None:
            dec_or_evg = []

        print("SPECIES")
        print(species)
        print("DEC OR EVG")
        print(dec_or_evg)

        all_species = database.get_all_species()
        
        dec_or_evg_vals = database.get_dec_or_evg_vals()

    except Exception as e:
        print("EXCEPTION")
        print(e)
        species = []
        dec_or_evg = []
        all_species = []
        dec_or_evg_vals = []
    except Error as e:
        print("ERROR")
        print(e)
        species = []
        dec_or_evg = []
        all_species = []
        dec_or_evg_vals = []

    database.disconnect()

    # Render the home page, passing in the list of plants.
    html = render_template('index.html',
    all_species = all_species,
    dec_or_evg_vals = dec_or_evg_vals)

    response = make_response(html)

    response.set_cookie("species", json.dumps(species))
    response.set_cookie("dec_or_evg", json.dumps(dec_or_evg))

    return response

#endregion

#region Details

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

# Renders the tour details page.
@app.route('/')
@app.route('/tourdetails')
def tourdetails():

    common_name = request.args.get("common_name")
    # Gets a the information on the requested species.
    try:
        database = Database()
        database.connect()
        species_info = database.get_species_info(common_name)
        blurb = database.get_tour_blurb(common_name)
    except Exception as e:
        print(e)
        species_info = SpeciesInfo('','','','','')
        blurb = ""
    except Error as e:
        print(e)
        species_info = SpeciesInfo('','','','','')
        blurb = ""

    database.disconnect()

    # Render the details page, passing in the plant.
    html = render_template('tourdetails.html', 
    common_name = common_name,
    species_info = species_info,
    blurb = blurb)
    response = make_response(html)

    return response

#endregion

#region Catalog

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

#endregion

#region About

# Renders the "about us" page.
@app.route('/')
@app.route('/about')
def about():

    # Render the catalog page, passing in the list of species.
    html = render_template('about.html')
    response = make_response(html)

    return response

#endregion

#region GetTourPlants

# Gets the tour plants
@app.route('/')
@app.route('/getTourPlants')
def getTourPlants():

    try:
        ids = request.args.get('ids')
        ids = json.loads(ids)
        print(ids)

        plants = []

        database = Database()
        database.connect()

        for id_num in ids:
            plant = database.get_plant_by_id(id_num)
            plants.append(plant)

        database.disconnect()
    
    except Exception as e:
        print(e)
        plants = []

    except Error as e:
        print(e)
        plants = []

    return json.jsonify(plants = plants)

#endregion
    
#region GetPins

@app.route('/getPins')
def getPins():
    print("in getPins")
    try:
        bounds = request.args.get('bounds')
        bounds = json.loads(bounds)

        south = bounds["south"]
        north = bounds["north"]
        east = bounds["east"]
        west = bounds["west"]

        
        species = request.args.get('species')
        dec_or_evg = request.args.get('dec_or_evg')

        print("SPECIES FROM REQUEST")
        print(species)
        print(len(species))
        print("DOE FROM REQUEST")
        print(dec_or_evg)
        print(len(dec_or_evg))

        print("south: ", south)
        print("north: ", north)
        print("east: ", east)
        print("west: ", west)

        database = Database()
        database.connect()

        plants = database.get_filtered_plants(species, dec_or_evg, south, north, east, west)

        database.disconnect()

    except Exception as e:
        plants = []
        print(e)
    
    return json.jsonify(plants = plants)

#endregion

#region Test
#-----------------------------------------------------------------------
# Renders the "about us" page.
@app.route('/')
@app.route('/tour')
def tour():

    # Render the catalog page, passing in the list of species.
    html = render_template('tour.html')
    response = make_response(html)

    return response
#-----------------------------------------------------------------------
#endregion

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10101, debug=True)
