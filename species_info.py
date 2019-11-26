#!/usr/bin/env python

#----------------------------------------------------------------------
# species_info.py
# Stores information about a species of plant
#----------------------------------------------------------------------

# Defines a plant
class SpeciesInfo:
    def __init__(self, common_name, latin_name, img, dec_or_evg, blurb):
        self._common_name = common_name
        self._latin_name = latin_name
        self._img = img
        self._dec_or_evg = dec_or_evg
        self._blurb = blurb


    # toString()
    def __str__(self):
        return "%s %s %s %s %s" % (self._common_name, self._latin_name, self._img, self._dec_or_evg, self._blurb)

    # getters
    def getCommonName(self):
        return self._common_name

    def getEncodedCommonName(self):
        trimmed_name = self._common_name.strip()
        return trimmed_name.replace(" ", "%20")

    def getLatinName(self):
        return self._latin_name
    
    def getImg(self):
        return self._img

    def getDecOrEvg(self):
        return self._dec_or_evg
    
    def getBlurb(self):
        return self._blurb