#!/usr/bin/python3
import ephem

"""
return sunset and sunrise in local time
"""

class Kamisun:
    def __init__(self, latitude,  longitude, altitude):

         # Get parameters
        self.latitude    =  latitude 
        self.longitude = longitude
        self.altitude    =  altitude
        
        # utc = pytz.utc
        
        city = ephem.Observer()
        city.lat    = self.latitude
        city.lon =  self.longitude
        city.elevation    =  self.altitude
        

        sun = ephem.Sun()
        sunrise = ephem.localtime(city.next_rising(sun))
        sunset  = ephem.localtime(city.next_setting(sun))
         
        heurec = str(sunset)
        long = len(heurec)
        fin = long - 15
        self.time_set = heurec[fin:long-10]

        heurel = str(sunrise)
        long = len(heurel)
        fin = long - 14
        self.time_rise = heurel[fin:long-10]

         
