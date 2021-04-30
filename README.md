# Kamiflora
A neuron for [Kalliope](https://kalliope-project.github.io/)

This Neuron allows Kalliope to control the Xiaomi Mi Plant (new name of Xiaomi Mi Flora) which is a bluetooth-connected sensor that monitors watering (humidity), soil fertility (electrical conductivity of the soil) , temperature and sunshine.

Kalliope can thus warn you if one of your plants requires your care.

## Third parties script
This neuron use the following scripts :
- [google_trans_new](https://github.com/lushan88a/google_trans_new) by lushan88a<br>
- [miflora-mqtt-daemon](https://github.com/ThomDietrich/miflora-mqtt-daemon) by Thomas Dietrich<br>
- [Plant-database](https://github.com/vrachieru/plant-database) by Victor Rachieru<br>
- [ephem](https://pypi.org/project/ephem/) by  Brandon Rhodes

## Prerequisites
This neuron require python 3.

You must have an MQTT broker like Mosquitto installed. You can learn more about Mosquitto  on the project's [Github page](https://github.com/eclipse/mosquitto) or on the [Mosquitto website](https://mosquitto.org/).
You also, obviously, need to have bluetooth enabled on your system.



## Installation

``cd your/kalliope_starter_kit``<br>
``kalliope install --git-url https://github.com/Riseryn/Kamiflora.git``<br>

The installation can take quite a long time...Be patient...

The [miflora-mqtt-daemon](https://github.com/ThomDietrich/miflora-mqtt-daemon) module by Thomas Dietrich will be installed. This module will read the data from your Mi Plant sensors and send them to your broker so that Kalliope can access them.

If the installation is stuck at this step:
<br>
``
PLAY [kamiflora] ***************************************************************

TASK [Install python lib with pip] *********************************************
``<br>

interrupt it with ctrl + c
then <br>
``
cd resources/neurons/kamiflora
ansible-playbook install.yml -K
``
<br>
After this command is succesful, installation is complete.
Now configure miflora-mqtt-daemon.
To configure miflora-mqtt-daemon follow the instructions on the [miflora-mqtt-daemon](https://github.com/ThomDietrich/miflora-mqtt-daemon) page.

## Options
<table>
    <tr>
        <td>Parameters</td>
        <td>Default</td>
         <td>Value</td>
         <td>Comments</td>
    </tr>
        <td>broker_url</td>
        <td>127.0.0.1</td>
        <td>string</td>
        <td>The broker's address can be internal (broker_url="192.168.1.184") or external (broker_url="iot.eclipse.org"</td>
   </tr>
   <tr> 
        <td>broker_port</td>
        <td>1883</td>
        <td>string</td>
        <td>Indicate the port used by your broker. Usually port 1883</td>
   </tr>
   <tr> 
        <td>secure</td>
        <td>none</td>
        <td>string</td>
        <td>set Secure to passwd if you are using user/password protection for your broker. You must set user and password parameters.
            Don't forget to configure the miflora-mqtt-daemon config.ini with this value.
    </td>
   </tr>
    <tr> 
        <td>user</td>
        <td>none</td>
        <td>string</td>
        <td>The user name for the broker.</td>
   </tr>
   <tr> 
        <td>password</td>
        <td>none</td>
        <td>string</td>
        <td>Password for the broker.</td>
   </tr>
    <tr> 
        <td>start_time</td>
        <td>none</td>
        <td>string</td>
        <td>The time at which Kalliope begins to report the data from the sensors. If this parameter is not provided, the location parameters (latitude, longitude and altitude) must be entered for a sunrise time calculation. The sunrise time at your location will then become the start_time.</td>
   </tr>
   <tr> 
        <td>end_time</td>
        <td>none</td>
        <td>string</td>
        <td>The time at which Kalliope stop to report the data from the sensors. If this parameter is not provided, the location parameters (latitude, longitude and altitude) must be entered for a sunset time calculation. The sunset time at your locationwill then become the end_time.</td>
   </tr>
   <tr> 
        <td>latitude</td>
        <td>none</td>
        <td>string</td>
        <td>your latitude, longitude and altitude can be obtained by this [site](https://www.mapsdirections.info/fr/coordonnees-sur-google-map.html). </td>
   </tr> 
   <tr> 
        <td>longitude</td>
        <td>none</td>
        <td>string</td>
        <td>your latitude, longitude and altitude can be obtained by this [site](https://www.mapsdirections.info/fr/coordonnees-sur-google-map.html). </td>
   </tr>   
   <tr> 
        <td>altitude</td>
        <td>none</td>
        <td>string</td>
        <td>your latitude, longitude and altitude can be obtained by this [site](https://www.mapsdirections.info/fr/coordonnees-sur-google-map.html). </td>
   </tr>  
   <tr> 
        <td>min_battery</td>
        <td>none</td>
        <td>string</td>
        <td>Level from which you wish to be warned that the battery of your MiPlant must be changed</td>
   </tr>  
   <tr> 
        <td>language</td>
        <td>none</td>
        <td>string</td>
        <td>Language in which you would like Kalliope to report to you.
CAUTION sensitive to case.
Accepts fr, de, en, etc but not Fr or FR</td>
   </tr>  
</table>

## Return values
<table>
    <tr>
        <td>Name</td>
        <td>Type</td>
        <td>Description</td>
         <td>Comments</td>
    </tr>
    <tr>
        <td>result_comparison</td>
        <td>string</td>
        <td>raw answer in english</td>
   </tr>
   <tr>
        <td>localized_message</td>
        <td>string</td>
        <td>Message translated into the language specified by the language parameter</td>
   </tr>
 </table>
 
## Synapses example 

In this example Kalliope will check your sensors every two hours.
The broker does not require a password.
Reports will start at 8:35 am and end at sunset.
You will be notified when the battery is at 5%.
The language of the response is French ("fr").


    - name: "kamiflora"
      signals:  
      - event:  
          hour:  "*/2"
      neurons:  
          - kamiflora:      
              broker_url: "192.168.10.150"          
              broker_port: "1883"                    
              start_time: "08:35:00"                   
              latitude: "48.07807894349862"          
              longitude: "-1.6699218750000002"          
              altitude: "30"          
              min_battery: "5"          
              language: "fr"          
          

