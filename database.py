#!usr/bin/env python

#----------------------------------------------------------------------
# database.py
# Performs database operations on the plants database
#----------------------------------------------------------------------

import psycopg2
from sys import stderr, exit
import os
from species_info import SpeciesInfo
from plant import Plant

#-----------------------------------------------------------------------------

class Database:

#region Constructors

    # Creates a database.
    def __init__(self):
        self._connection = None

#endregion

#region Connections

    # Connects to the registrar database
    def connect(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self._connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Disconnects from the database.
    def disconnect(self):
        if self._connection is not None:
            self._connection.close()

#endregion

#region Plant searches

    # Searches for plants within the given coordinates
    def search_in_range(self, south, north, east, west):
        cursor = self._connection.cursor()
        stmt, values = self.create_range_stmt(south, north, east, west)
        cursor.execute(stmt, values)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            plant = Plant.getDict(plant)
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

    # Returns all individual plants in the database
    def get_all_plants(self):
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM plant_indiv;"
        cursor.execute(stmt)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            plant = Plant.getDict(plant)
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

    # Returns n plants from the database
    def get_n_plants(self, n):
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM plant_indiv LIMIT %s;"
        cursor.execute(stmt, [n])

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            plant = Plant.getDict(plant)
           
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

    # Gets plant informtion by primary id
    def get_plant_by_id(self, id_num):
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM plant_indiv WHERE primary_id = %s;"
        cursor.execute(stmt, [id_num])

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            plant = Plant.getDict(plant)
           
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

#endregion

#region Species searches

    # Returns all species to create a catalog
    # Returns dictionary, key = first letter, value = list of species starting with key
    def get_all_species(self):
        cursor = self._connection.cursor()
        stmt = 'SELECT * FROM species_info ORDER BY common_name ASC;'
        cursor.execute(stmt)

        species = {}
        row = cursor.fetchone()
        while row is not None:

            species_info = SpeciesInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            # Get first character of common name
            first_char = species_info.getCommonName()[0]
            # Create list if it doesn't exist
            if first_char not in species.keys():
                species[first_char] = []
            # Append species to list
            species[first_char].append(species_info)

            row = cursor.fetchone()

        cursor.close()

        return species

    # Returns species containing
    # Returns dictionary, key = first letter, value = list of species starting with key
    def get_species_by_name(self, search):

        if search == '':
            return self.get_all_species()
        
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM species_info WHERE LOWER(common_name) LIKE LOWER(%s) ORDER BY common_name ASC;"
        cursor.execute(stmt, ['%' + search + '%'])

        species = {}
        row = cursor.fetchone()
        while row is not None:

            species_info = SpeciesInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            # Get first character of common name
            first_char = species_info.getCommonName()[0]
            # Create list if it doesn't exist
            if first_char not in species.keys():
                species[first_char] = []
            # Append species to list
            species[first_char].append(species_info)

            row = cursor.fetchone()

        cursor.close()

        return species

    # Gets information on a plant species by its common name
    def get_species_info(self, common_name):
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM species_info WHERE species_info.common_name = %s;"
        cursor.execute(stmt, [common_name])

        row = cursor.fetchone()
        species_info = SpeciesInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))

        return species_info

    # Get number of plants of a certain species by common name
    def get_species_count(self, common_name):
        cursor = self._connection.cursor()
        stmt = "SELECT COUNT(common_name) FROM plant_indiv WHERE common_name = %s;"
        cursor.execute(stmt, [common_name])

        row = cursor.fetchone()
        count = int(row[0])

        return count

#endregion

#region Filter searches

    # Gets possible values of dec_or_evg
    def get_dec_or_evg_vals(self):

        cursor = self._connection.cursor()
        stmtStr = "SELECT DISTINCT dec_or_evg FROM species_info;"
        cursor.execute(stmtStr)

        dec_or_evg_vals = []
        
        row = cursor.fetchone()
        while row is not None:
            dec_or_evg_vals.append(str(row[0]))
            row = cursor.fetchone()

        cursor.close()

        dec_or_evg_vals.sort()

        return dec_or_evg_vals

    # Gets filtered plants
    def get_filtered_plants(self, species, dec_or_evg, south, north, east, west):

        print("species is", len(species))
        print("doe is", len(dec_or_evg))

        if len(species) == 0 and len(dec_or_evg) == 0:
            print("not filtering")
            return self.search_in_range(south, north, east, west)

        cursor = self._connection.cursor()

        print("filtering")

        stmtStr, vals = self.create_filter_stmt(species, dec_or_evg, south, north, east, west)

        cursor.execute(stmtStr, vals)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            plant = Plant.getDict(plant)
           
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

#endregion

#region Search helpers

    # Creates a statement to search for pins based on range and given location
    def create_range_stmt(self, south, north, east, west):

        # Will hold the search terms in the order they're used.
        search_values = []

        # Creates the baseline statement.
        stmtStr = "SELECT * FROM plant_indiv WHERE lat >= %s AND lat <= %s AND long <= %s AND long >= %s"

        # Append the boundaries for the latitude and longitude ranges.
        search_values.append(south)
        search_values.append(north)
        search_values.append(east)
        search_values.append(west)

        # Return the statement and the ordered list of values.
        return stmtStr, search_values

    # Create filtering SQL statement
    def create_filter_stmt(self, species, dec_or_evg, south, north, east, west):

        stmtStr = "SELECT common_name, lat, long, status, primary_id FROM ( \
                SELECT plant_indiv.common_name, plant_indiv.lat, plant_indiv.long, \
                    plant_indiv.status, plant_indiv.primary_id, species_info.dec_or_evg \
                FROM plant_indiv JOIN species_info ON plant_indiv.common_name = species_info.common_name \
            ) tmp WHERE lat >= %s AND lat <= %s AND long <= %s AND long >= %s AND"

        # Append WHERE for names
        for i in range(0, len(species)):
            if i == 0:
                stmtStr += " common_name = %s"
            else:
                stmtStr += " OR common_name = %s"
            
        # Append AND if necessary
        if len(species) > 0 and len(dec_or_evg) > 0:
            stmtStr += " AND"

        # Append WHERE for dec_or_evg
        for i in range(0, len(dec_or_evg)):
            if i == 0:
                stmtStr += " dec_or_evg = %s"
            else:
                stmtStr += " OR dec_or_evg = %s"

        stmtStr += ";"

        # Create list of prepared values
        vals = []
        vals.append(south)
        vals.append(north)
        vals.append(east)
        vals.append(west)
        for spec in species:
            vals.append(spec)
        for d_o_e in dec_or_evg:
            vals.append(d_o_e)

        print("stmtStr = ", stmtStr)

        return stmtStr, vals

#endregion

#---------------------------------------------------------------------------

#region Testing

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    species = database.get_all_species()
    for first_char in species:
        print(first_char)
        for info in species[first_char]:
            print(info.getCommonName())
    database.disconnect()

#endregion