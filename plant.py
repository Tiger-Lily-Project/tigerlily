#!/usr/bin/env python

#----------------------------------------------------------------------
# plant.py
# Stores information about a specific plant on campus
#----------------------------------------------------------------------

# Defines a plant
class Plant:
    def __init__(self, name, lati, longi, status, id_num):
        self._name = name
        self._lat = lati
        self._long = longi
        self._status = status
        self._id_num = id_num

    # toString()
    def __str__(self):
        return "%s %s %s %s %s" % (self._name, self._lat, self._long, self._status, self._id_num)

    # getters
    def getName(self):
        return self._name
    
    def getLat(self):
        return self._lat

    def getLong(self):
        return self._long
    
    def getStatus(self):
        return self._status

    def getIdNum(self):
        return self._id

    def getDict(self):
        json = {}
        json["title"] = self._name
        json["lat"] = self._lat
        json["lng"] = self._long
        json["status"] = self._status
        json["id_num"] = self._id_num
        return json