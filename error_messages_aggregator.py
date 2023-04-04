from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json
import time

first_results = 1
#-------------------------------------------------------------------------------------
def extract_query_bindings(query_results):  #estrae i bindings da una query
    return [query_results['results']['bindings']]

def extract_subscription_bindings(subscription_results):  #estrae i bindings da una subscription
    return [subscription_results['results']['addedResults']['bindings']]

def error_format(res): 
    if res == []:
        print('NON CI SONO ERRORI') 
        return
    SOURCE = res[0]['Source']['value']
    TIME = res[0]['Time']['value'].split('T')[1].split('.')[0]
    ERRORTYPE = res[0]['ErrorType']['value']
    DESCRIPTION = res[0]['Value']['value']
    COMMENT = res[0]['Comment']['value']
    return f"Error generated from {SOURCE} AT {TIME}\\nErrorType: {ERRORTYPE}\\nComment:\\n{COMMENT}\\n----------------------------------------\\nDescription:\\n{DESCRIPTION}"
#-------------------------------------------------------------------------------------   
    
def on_notification(a,r):
    global first_results
    if first_results == 1:
        print('first results ignored')
        first_results = 0
    else:
        errori = error_format(a)
        print(errori)
        client.update('SEND_DISCORD_MESSAGE', forcedBindings={
        "message_value" : error_format(a),       
        "source" : "ERROR_MESSAGES_AGGREGATOR"
        })
#-------------------------------------------------------------------------------------
#SETUP
mySAP = open("jsap_test.jsap.txt", 'r')
_JSAP = json.load(mySAP)
client = SEPA(sapObject=SAPObject(_JSAP))
#--------------------------------------------------

client.subscribe('ALL_ERROR', 'PROVA', {}, on_notification)

while(True):
    time.sleep(10)
