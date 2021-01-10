#!/usr/bin/env python3.
import json
import os
base_path = os.path.dirname(os.path.abspath(__file__))
from datetime import datetime

class Kamimessage :
    def __init__(self, dict_message, min_battery):
        self.message = dict_message
        self.min_battery = min_battery
        self.result = ""
        
        # print("entree dans kamimessage à : ",datetime.strftime(datetime.now(),"%H:%M:%S"))

#     extract data from sensors   
  
    def read_reference_file(self,filename):
        FilePath = base_path + "/plant-database-master/json/" + filename + ".json"
        try:
            with open(FilePath) as json_file:
                data = json.load(json_file)
                ref_parameters = data["parameter"]
                # print("ref_parameters ",ref_parameters)
                return ref_parameters               
        except Exception as e :
            print(str(e))

    def compare_sensor_to_ref(self, name, ref_parameters, dict_message):
        location = dict_message[name]["location"]
        self.result = ""

        if dict_message[name]['sensor']['light'] > ref_parameters["min_light_lux"] and dict_message[name]['sensor']['light'] < ref_parameters["max_light_lux"]:
            self.result += "" 

        if dict_message[name]['sensor']["light"] < ref_parameters["min_light_lux"]:
            self.result += "light " + str(dict_message[name]['sensor']["light"]) + " lumen is too low. Thank you to place it in a better lit place if possible."

        if dict_message[name]['sensor']["light"] > ref_parameters["max_light_lux"]:
            self.result += "light " + str(dict_message[name]['sensor']["light"]) + " is too high. Thank you to place it in a less lit place if possible."
    
        if dict_message[name]['sensor']["moisture"] > ref_parameters["min_soil_moist"] and dict_message[name]['sensor']["moisture"] < ref_parameters["max_soil_moist"]:
            self.result += "" 

        if dict_message[name]['sensor']["moisture"] < ref_parameters["min_soil_moist"]:
            self.result += "Quantity " + str(dict_message[name]['sensor']["moisture"]) + " of water is too low. Please add water."

        if dict_message[name]['sensor']["moisture"] > ref_parameters["max_soil_moist"]:
            self.result += " Be careful, " + str(dict_message[name]['sensor']["moisture"]) + " is too much water in your plant."
            
        if dict_message[name]['sensor']["conductivity"] > ref_parameters["min_soil_ec"] and dict_message[name]['sensor']["conductivity"] < ref_parameters["max_soil_ec"]:
            self.result += "" #" conductivity is ok."

        if dict_message[name]['sensor']["conductivity"] < ref_parameters["min_soil_ec"]:
            self.result += str(dict_message[name]['sensor']["conductivity"]) + " Fertilizer is too less, please add some."

        if dict_message[name]['sensor']["conductivity"] > ref_parameters["max_soil_ec"]:
            self.result += " Be careful, " + str(dict_message[name]['sensor']["conductivity"]) + " is too much fertilizer. Please add some water to dilute it."
        
        if dict_message[name]['sensor']["temperature"] > ref_parameters["min_temp"] and dict_message[name]['sensor']["temperature"] < ref_parameters["max_temp"]:
            self.result += "" #" temperature is ok."

        if dict_message[name]['sensor']["temperature"] < ref_parameters["min_temp"]:
            self.result += str(dict_message[name]['sensor']["temperature"]) + " degrees of temperature is too cold. Please put it in a warmer place if possible."

        if dict_message[name]['sensor']["temperature"] > ref_parameters["max_temp"]:    
            self.result += str(dict_message[name]['sensor']["temperature"]) +" degrees of temperature is too hot. Please put it in a cooler place if possible."
        
        if dict_message[name]['sensor']["battery"] > self.min_battery:
            self.result += ""
        else : 
            self.result += str(dict_message[name]['sensor']["battery"]) + " \% of battery level is too low. think about changing it."
        
        if self.result !="":
            self.result = "Your plant " + name + " located in " + location + ": " + self.result
        # else:
        #     self.result ="sensor "+ name + " is ok"
        return self.result
  

    