#!usr/bin/env python

#----------------------------------------------------------------------
# database.py
# Performs database operations on the plants database
#----------------------------------------------------------------------

from psycopg2 import connect
from sys import stderr, exit
from os import path
from species_info import SpeciesInfo
from plant import Plant

#-----------------------------------------------------------------------------

class Database:

    # Creates a database.
    def __init__(self):
        self._connection = None

    # Connects to the registrar database
    def connect(self):
        self._connection = connect(database="plants", user="postgres", password="RahTiger867", host="127.0.0.1", port="5432")
    
    # Disconnects from the database.
    def disconnect(self):
        if self._connection is not None:
            self._connection.close()

    # Searches for plants within the range of the given latitude and longitude
    def search_in_range(self, lati, longi, radius):
        cursor = self._connection.cursor()
        stmt, values = self.create_range_stmt(lati, longi, radius)
        cursor.execute(stmt, values)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

    # Returns all species to create a catalog
    def get_all_species(self):
        cursor = self._connection.cursor()
        stmt = 'SELECT * FROM species_info;'
        cursor.execute(stmt)

        species = []
        row = cursor.fetchone()
        while row is not None:
            species_info = SpeciesInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            species.append(species_info)
            row = cursor.fetchone()
        cursor.close()
        return species

    # Returns all individual plants in the database
    def get_all_plants(self):
        cursor = self._connection.cursor()
        stmt = 'SELECT * FROM plant_indiv WHERE status != "Stump" AND status != "Removed";'
        cursor.execute(stmt)

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

    # Gets information on a plant species by its common name
    def get_species_info(self, common_name):
        cursor = self._connection.cursor()
        stmt = 'SELECT * FROM species_info WHERE common_name = %s;'
        cursor.execute(stmt, [common_name])

        row = cursor.fetchone()
        species_info = SpeciesInfo(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))

        return species_info
        
    # Creates a statement to search for pins based on range and given location
    def create_range_stmt(self, lati, longi, radius):

        # Will hold the search terms in the order they're used.
        search_values = []

        # Creates the baseline statement.
        stmtStr = 'SELECT * FROM plant_indiv WHERE lati >= %s AND lati <= %s AND longi >= %s AND longi <= %s'

        # Only selects those which are not removed or stumps.
        stmtStr += ' AND status != "Stump" AND status != "Removed";'

        # Append the boundaries for the latitude and longitude ranges.
        search_values.append(lati - radius)
        search_values.append(lati + radius)
        search_values.append(longi - radius)
        search_values.append(longi + radius)

        # Return the statement and the ordered list of values.
        return stmtStr, search_values

#---------------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    species_info = database.get_species_info("Japanese Black Pine")
    print(species_info)
    database.disconnect()
