from sepy.SAPObject import *
from sepy.SEPA import SEPA
import time

import core.JsapLoader as JsapLoader

first_results=1
print("#####################")
print("CRITERIA AGGREGATOR v0.1")
print("#####################")

#-----OVERRIDE DEFAULT JSAP CONFIGURATION---------------------------------------------------------------
_JSAP= JsapLoader.get_configured_jsap()
#------------------------------------------------------------------------------------- 
_CACHE={}  
def add_to_cache(binding):
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
    
def check_cache():
    for feature in _CACHE:
        print(f"** {feature} cache length: {len(_CACHE[feature])}")
        if len(_CACHE[feature])==3:
            feature_obs=_CACHE[feature]
            irrigation_format(feature_obs, feature)
            _CACHE[feature]={} #!CLEAN CACHE
    return

def irrigation_format(feature_obs,feature_name):
    comp = []
    for ptime in feature_obs:
        comp.append(float(feature_obs[ptime]['value']))
    if sum(comp) != 0:
        #print("value's sum is higher than 0 so we have to send data")
        PTIME = []
        VALUE = []
        UNIT = []
        for ptime in feature_obs:
            PTIME.append(ptime)
            VALUE.append(feature_obs[ptime]['value']) 
            UNIT.append(feature_obs[ptime]['unit'])
          
        client.update('SEND_DISCORD_MESSAGE', forcedBindings={
            "message_value" : f"Feature **{feature_name.split('/')[-1]}** irrigation needs:\\n{PTIME[0]}: {VALUE[0]} {UNIT[0].split('/')[-1]}\\n{PTIME[1]}: {VALUE[1]} {UNIT[1].split('/')[-1]}\\n{PTIME[2]}: {VALUE[2]} {UNIT[2].split('/')[-1]}" ,       
            "source" : "http://www.vaimee.it/sources/criteria_aggregator"
            })
        print(f"discord message sent")
    else:
        print(f"discord message not sent because all feature's irrigation value was 0")

def on_notification(a,r):
    global first_results
    if first_results == 1:
        print('first results ignored')
        first_results = 0
    else:
        for binding in a:
            add_to_cache(binding)   
            print(_CACHE)  

        check_cache()

client = SEPA(sapObject=SAPObject(_JSAP))
client.subscribe('Unit_irrigation_needs', 'PROVA', {}, on_notification)

while(True):
    time.sleep(10)