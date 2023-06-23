from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json
import time
import os
import sys

import core.JsapLoader as JsapLoader

first_results=1
print("#####################")
print("CRITERIA AGGREGATOR v0.1")
print("#####################")

#-----OVERRIDE DEFAULT JSAP CONFIGURATION---------------------------------------------------------------
_JSAP= JsapLoader.get_configured_jsap()
#------------------------------------------------------------------------------------
#Formats subscription data. Returns a formatted string
def irrigation_format(res): 

    return
#------------------------------------------------------------------------------------- 
_CACHE={}  
def add_to_cache(binding):
    #print(binding)
    farm_name= binding["feature"]["value"] #Nome del campo
    ptime= binding["ptime"]["value"] #phenomenon time (oggi, domani e dopodomani)
    value= binding["value"]["value"] #il valore misurato
    unit= binding["unit"]["value"] #unità di misura

    #If cache does not exist, create new one
    if farm_name not in _CACHE:
        print(f"Adding new farm: {farm_name}")
        _CACHE[farm_name]={}

    if ptime not in _CACHE[farm_name]:
        print(f"Adding new ptime: {ptime}")
        _CACHE[farm_name][ptime]={}
        _CACHE[farm_name][ptime]["value"]=value
        _CACHE[farm_name][ptime]["unit"]=unit
    

def irrigation_format(feature_obs,feature_name):
    print("DEVO UPLOADARE!!!")
    print(feature_obs)
    #da non inviare se il il value di tutti i ptime (tutti  e 3) è uguale a 0

def check_cache():
    for feature in _CACHE:
        print(f"** {feature} cache length: {len(_CACHE[feature])}")
        if len(_CACHE[feature])==3:
            feature_obs=_CACHE[feature]
            irrigation_format(feature_obs,feature)
            _CACHE[feature]={} #!CLEAN CACHE
    return

def on_notification(a,r):
    global first_results
    if first_results == 1:
        print('first results ignored')
        first_results = 0
    else:
        #print(a)
        for binding in a:
            add_to_cache(binding)   
            print(_CACHE)    

        '''client.update('SEND_DISCORD_MESSAGE', forcedBindings={
        "message_value" : irrigation_format(a),       
        "source" : "CRITERIA_AGGREGATOR"
        })'''
        check_cache()


client = SEPA(sapObject=SAPObject(_JSAP))
client.subscribe('Unit_irrigation_needs', 'PROVA', {}, on_notification)

while(True):
    time.sleep(10)