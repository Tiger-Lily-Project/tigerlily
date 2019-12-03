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

    # Creates a database.
    def __init__(self):
        self._connection = None

    # Connects to the registrar database
    def connect(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self._connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Disconnects from the database.
    def disconnect(self):
        if self._connection is not None:
            self._connection.close()

    # Searches for plants within the given coordinates
    def search_in_range(self, minLat, maxLat, minLong, maxLong):
        cursor = self._connection.cursor()
        stmt, values = self.create_range_stmt(minLat, maxLat, minLong, maxLong)
        cursor.execute(stmt, values)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
            plant = Plant.getDict(plant)
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

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

    # Returns all individual plants in the database
    def get_all_plants(self):
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM plant_indiv;"
        cursor.execute(stmt)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
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
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
            plant = Plant.getDict(plant)
           
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

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
        
    # Creates a statement to search for pins based on range and given location
    def create_range_stmt(self, minLat, maxLat, minLong, maxLong):

        # Will hold the search terms in the order they're used.
        search_values = []

        # Creates the baseline statement.
        stmtStr = "SELECT * FROM plant_indiv WHERE lat >= %s AND lat <= %s AND long >= %s AND long <= %s"

        # Append the boundaries for the latitude and longitude ranges.
        search_values.append(minLat)
        search_values.append(maxLat)
        search_values.append(minLong)
        search_values.append(maxLong)

        # Return the statement and the ordered list of values.
        return stmtStr, search_values

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

    # Gets possible values of status
    def get_status_vals(self):

        cursor = self._connection.cursor()
        stmtStr = "SELECT DISTINCT status FROM plant_indiv;"
        cursor.execute(stmtStr)

        status_vals = []
        
        row = cursor.fetchone()
        while row is not None:
            status_vals.append(str(row[0]))
            row = cursor.fetchone()

        cursor.close()

        status_vals.sort()

        return status_vals

    # Gets filtered plants
    def get_filtered_plants(self, n, species, status, dec_or_evg):

        return self.get_n_plants(n)

    

#---------------------------------------------------------------------------

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
