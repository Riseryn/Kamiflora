#!/usr/bin/env python3.
import sys
import os
FilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append (FilePath)
from datetime import datetime
from kamiconnect import Kamiconnect
from kamimessage import Kamimessage
from kamisun import Kamisun
from kalliope.core.NeuronModule import NeuronModule , MissingParameterException
from kalliope.core.Utils import Utils
from google_trans_new import google_translator 


class Kamiflora(NeuronModule):    
    def __init__(self, **kwargs):
        super(Kamiflora, self).__init__(**kwargs)        

        # Get parameters
        self.broker_url =   kwargs.get('broker_url',None)  
        self.broker_port =  int(kwargs.get('broker_port', None  ))
        self.secure =       kwargs.get('secure', None)
        self.user =         kwargs.get('user', None)    
        self.password =     kwargs.get('password', None)
        self.clt_certfile = kwargs.get('clt_certfile', None)
        self.serv_ca_cert = kwargs.get('serv_ca_cert', None)
        self.clt_ca_key =   kwargs.get('clt_ca_key', None)
        self.start_time =   kwargs.get('start_time', None)
        self.end_time =     kwargs.get('end_time', None)
        self.language =     kwargs.get('language', None)
        self.min_battery =  int( kwargs.get('min_battery', None))        
        self.latitude =     kwargs.get('latitude', None)
        self.longitude =    kwargs.get('longitude', None)
        self.altitude =     int(kwargs.get('altitude', None)) 
        self.time_now =     self.convert_str_to_time(datetime.strftime(datetime.now(),"%H:%M"))


        # print("self.clt_certfile = ",self.clt_certfile ) 
        # print("Kamiflora: self.serv_ca_cert = ",self.serv_ca_cert )  
        # print("self.clt_ca_key = ",self.clt_ca_key)   
        
        

        if self.start_time:
            self.start_time = self.convert_str_to_time(self.start_time)

        if self.end_time:
            self.end_time = self.convert_str_to_time(self.end_time)   

        # check if parameters have been provided
        if self.Is_parameters_ok(): 
            # self.say("lancement de kamiflora")
            
            if self.time_now > self.start_time and self.time_now < self.end_time:
                kc = Kamiconnect(self.broker_url, self.broker_port, self.user, self.password, self.secure, self.clt_certfile, self.serv_ca_cert, self.clt_ca_key)

                Kamiconnect.main(kc)
                dict_message = kc.dict_message

                for name in dict_message:
                    km = Kamimessage(dict_message,self.min_battery)
                    ref_parameters = Kamimessage.read_reference_file(km, name)

                    # checks if the sensor exists, in case of a bluetooth connection problem.
                    sensor_exists = self.sensor_exists(dict_message[name],"sensor")

                    if sensor_exists:
                        result_comparison = Kamimessage.compare_sensor_to_ref(km, name, ref_parameters, dict_message)                        

                        if self.language == "en":
                            self.say(result_comparison)
                        else:
                            try:
                                localized_message = self.translate_message(result_comparison, self.language)
                                self.say(localized_message)
                            except Exception as e :
                                print(str(e))
                
               
    
    
    def sensor_exists(self,element,*keys):
    # '''
    # Check if *keys (nested) exists in `element` (dict).
    # '''
 
        if not isinstance(element, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keys) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')        
        _element = element

        for key in keys:
            try:
                _element = _element[key]
                # print("_element ",_element)
            except KeyError:
                message = "unable to read sensor"
                localized_message = self.translate_message(message, self.language)
                self.say(localized_message)
                return False
        return True


    def translate_message(self, message, language):
        Translator = google_translator(url_suffix='"'+ language +'"',timeout=5)

        try:
            text = Translator.translate(message, lang_tgt=language, lang_src='en')
        except Exception as e :
            text="ERROR, no translation returned"
            print(str(e))
        
        return text

    def convert_str_to_time(self,time_str):
        date_time_obj = datetime.strptime(time_str, '%H:%M')
        return date_time_obj

    def Is_parameters_ok(self):
        
        if self.broker_url is None:
            raise MissingParameterException ("This neuron require a broker_url parameter")
        
        if self.broker_port is None:
            raise MissingParameterException ("This neuron require a broker_port parameter")
        
        if self.min_battery is None:
            raise MissingParameterException ("This neuron require a min_battery parameter")
        
        if self.language is None:
            raise MissingParameterException ("This neuron require a language parameter")

        if self.secure == "cert":
            if self.clt_certfile == None or self.serv_ca_cert == None or  self.clt_ca_key == None:
                raise MissingParameterException ("secure parameter is set to cert but there is missing parameters.\nCheck your parameters clt_certfile, serv_ca_cert, clt_ca_key.")
        
        if self.end_time is None or self.end_time == "" or self.start_time is None or self.start_time == "" :
            if self.latitude is None or self.latitude =="" or self.longitude is None or self.longitude == "" or self.altitude is None or self.altitude =="":
                raise MissingParameterException ("This neuron requires either to indicate start_time and end_time or latitude, longitude and altitude.")

            else:
                ks = Kamisun(self.latitude, self.longitude, self.altitude)
    
                if self.end_time is None or self.end_time =="":
                    self.end_time = self.convert_str_to_time(ks.time_set)
                if self.start_time is None or self.start_time =="":
                    self.start_time = self.convert_str_to_time(ks.time_rise)
 
            return True         
        return True    
 
