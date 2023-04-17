#ogni volta che arriva un update su serra:temperature, aggrega i dati e li carica nel message_value di un discord:Message
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json
import time

#-------------------------------------------------------------------------------------
def extract_query_bindings(query_results):  #estrae i bindings da una query
    return [query_results['results']['bindings']]

def mean_temp(res):   #fa la media di tutte le temperature. se non ho temperature printa che non ce ne sono e ne aspetta
    if res == []:
        print('NON CI SONO TEMPERATURE') 
        return
    sum = 0
    for i in range(len(res)):
        sum += float(res[i]['Temperature']['value'])
    return sum/(i+1)
      
    
def on_notification(a,r):
    res = extract_query_bindings(client.query('ALL_TEMPERATURE'))[0]
    print(mean_temp(res))
    client.update('SEND_DISCORD_MESSAGE', forcedBindings={
    "message_value" : str(f'Medium temperature: {mean_temp(res)}'),       
    "source" : "serra"
    })  
#-------------------------------------------------------------------------------------
#SETUP
mySAP = open("jsap_test.jsap.txt", 'r')
_JSAP = json.load(mySAP)
client = SEPA(sapObject=SAPObject(_JSAP))
#--------------------------------------------------

client.subscribe('ALL_TEMPERATURE', 'PROVA', {}, on_notification)

while(True):
    time.sleep(10)
