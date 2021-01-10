#!/usr/bin/env python3.
import sys
import os
FilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append (FilePath)
import paho.mqtt.client as mqtt
import json
import time
import random
#import ssl
from datetime import datetime
from kalliope.core.NeuronModule import NeuronModule , MissingParameterException

class Kamiconnect :
    def __init__(self, broker_url, broker_port, user, password,  secure, clt_certfile, serv_ca_cert, clt_ca_key):
        
        self.broker_url =   broker_url                           
        self.broker_port =  int(broker_port)
        self.user =         user                
        self.password =     password
        self.secure =       secure
        self.clt_certfile = clt_certfile
        self.serv_ca_cert = serv_ca_cert
        self.clt_ca_key =   clt_ca_key
        self.dict_message = {}
        self.list_topic  =  []

    def on_connect(self,client, userdata, flags, rc, ):
             
        # if rc == 0:
        #     print("Broker connection OK")
        if rc == 1:
            print("Broker connection refused – incorrect protocol version")
        elif rc == 2:
            print("Broker connection refused – invalid client identifier")
        elif rc == 3:
            print("Broker connection refused – server unavailable")
        elif rc == 4:
            print("Broker connection refused – bad username or password")
        elif rc == 5:
            print("Broker connection refused – not authorised")
        else:
            pass

    def on_disconnect(client, userdata, rc):
        print("Client Got Disconnected, rc= ", rc)

    def on_message(self,client, userdata, message):
        sensors = json.loads(message.payload.decode("utf-8"))

        if message.topic == "miflora/$announce":            
            for sub_sensor in sensors:
                inner = sensors[sub_sensor]
                self.dict_message[inner['name_pretty']] = {}
                self.dict_message[inner['name_pretty']]["location"] =str(inner['location_pretty'])                
                self.list_topic.append(inner['topic']) 

        else:            
            plant_name = message.topic[8:].replace("-"," ")
            self.dict_message[plant_name]["sensor"] = sensors

    def subscribe_topic(self,sub_topic):
        cname = self.client_name()
        client = mqtt.Client(cname, clean_session = False)

        # testing secure connection     
        if self.secure == "pswd":
            if self.user and self.password:
                client.username_pw_set(username= self.user, password= self.password)
            else:
                print(" no user defined, does your broker need user/password connection?\nVerify your secure parameter\nMaybe it must be set to False or cert.")
        else:              
            client.on_connect = self.on_connect
            # To Process Every Other Message 
            client.on_disconnect = self.on_disconnect 
            client.on_message = self.on_message
            client.connect(self.broker_url, self.broker_port)
            client.subscribe(sub_topic)
            client.loop_start()
            time.sleep(1)
            client.loop_stop()

    def client_name(self):
        rand = random.randint(1,10000)
        cname = "kamiflora-" + str(rand)
        return cname

    def main(self):

        while not self.list_topic:
            topic = "miflora/$announce"
            self.topic = topic
            self.subscribe_topic(topic) 
        else:
            for topic in self.list_topic:
                self.topic = topic
                self.subscribe_topic(topic)
