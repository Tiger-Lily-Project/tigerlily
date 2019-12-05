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

#region Connect/Disconnect

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

    # Searches for plants within the given coordinates
    def search_in_range(self, minLat, maxLat, minLong, maxLong):
        cursor = self._connection.cursor()
        stmt, values = self.create_range_stmt(minLat, maxLat, minLong, maxLong)
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

    # Returns plant json dict based on id number
    def get_plant_by_id(self, num):
        cursor = self._connection.cursor()
        stmt = "SELECT * FROM plant_indiv WHERE id = %s;"
        cursor.execute(stmt, [num])

        row = cursor.fetchone()

        # If search came back empty, throw exception
        if row is None:
            raise Exception("no plant exists with the id %d", num)
        else:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            plant = Plant.getDict(plant)

        return plant

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

    # Gets filtered plants
    def get_filtered_plants(self, n, species, status, dec_or_evg):

        if len(species) == 0 and len(status) == 0 and len(dec_or_evg) == 0:
            return self.get_n_plants(n)

        cursor = self._connection.cursor()

        stmtStr, vals = self.create_filter_stmt(n, species, status, dec_or_evg)
        print("made stmt")

        cursor.execute(stmtStr, vals)
        print("executed")

        plants = []
        row = cursor.fetchone()
        while row is not None:
            plant = Plant(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            print("made plant")
            plant = Plant.getDict(plant)
            print("made into dict")
           
            plants.append(plant)
            row = cursor.fetchone()
        cursor.close()
        return plants

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

#endregion

#region Search helpers

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

    # Create filtering SQL statement
    # Returns statement and ordered list of search values
    def create_filter_stmt(self, n, species, status, dec_or_evg):

        stmtStr = "SELECT common_name, lat, long, status FROM ( \
                SELECT plant_indiv.common_name, plant_indiv.lat, plant_indiv.long, plant_indiv.status, species_info.dec_or_evg \
                FROM plant_indiv JOIN species_info ON plant_indiv.common_name = species_info.common_name \
            ) tmp WHERE"

        # Append WHERE for names
        for i in range(0, len(species)):
            if i == 0:
                stmtStr += " common_name = %s"
            else:
                stmtStr += " OR common_name = %s"
            
        # Append AND if necessary
        if len(species) > 0 and len(status) > 0:
            stmtStr += " AND"
        elif len(species) > 0 and len(dec_or_evg) > 0:
            stmtStr += " AND"

        # Append WHERE for statuses
        for i in range(0, len(status)):
            if i == 0:
                stmtStr += " status = %s"
            else:
                stmtStr += " OR status = %s"
    
        # Append AND if necessary
        if len(status) > 0 and len(dec_or_evg) > 0:
            stmtStr += " AND"

        # Append WHERE for dec_or_evg
        for i in range(0, len(dec_or_evg)):
            if i == 0:
                stmtStr += " dec_or_evg = %s"
            else:
                stmtStr += " OR dec_or_evg = %s"

        # Limit by n
        stmtStr += " LIMIT %s"

        stmtStr += ";"

        # Create list of prepared values
        vals = []
        for spec in species:
            vals.append(spec)
        for stat in status:
            vals.append(stat)
        for d_o_e in dec_or_evg:
            vals.append(d_o_e)
        vals.append(n)

        # Return statment and list of search values
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
