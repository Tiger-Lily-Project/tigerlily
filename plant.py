#!/usr/bin/env python

#----------------------------------------------------------------------
# plant.py
# Stores information about a specific plant on campus
#----------------------------------------------------------------------

# Defines a plant
class Plant:
    def __init__(self, name, lati, longi, status):
        self._name = name
        self._lat = lati
        self._long = longi
        self._status = status

    # toString()
    def __str__(self):
        return "%s %s %s %s" % (self._name, self._lat, self._long, self._status)

    # getters
    def getName(self):
        return self._name
    
    def getLat(self):
        return self._lat

    def getLong(self):
        return self._long
    
    def getStatus(self):
        return self._status

    def getJson(self):
        print("getting json")
        json = {}
        # json["name"] = self._name
        json["name"] = '\'' + self._name + '\''
        json["lat"] = self._lat
        json["lng"] = self._long
        json["status"] = self._status
        print(json)
        return json