from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json
import time
import os
import sys

first_results=1
print("#####################")
print("DISCORD CONSUMER v0.1")
print("#####################")

#-----OVERRIDE DEFAULT JSAP CONFIGURATION---------------------------------------------------------------
def print_help():
    print("--<HELP WINDOW>--")
    print("Run with: python ./yourscript.py -jsap path.jsap")

if len(sys.argv) == 1 :
    #QUI SIAMO IN DOCKER
    print("####################################################################")
    mySAP = open("./Resources/default.jsap", 'r')
    _JSAP = json.load(mySAP)
    print("- Jsap loaded, overriding configuration")
    # OVERRIDE VARIABLES
    try:
        _JSAP["host"]=os.environ['HOST_NAME']
        print("- Env variable 'HOST_NAME' set with value: "+str(_JSAP["host"]))
    except:
        print("- Env variable 'HOST_NAME' not set, using default: "+str(_JSAP["host"]))
    finally:
        pass
    try:
        _JSAP["sparql11protocol"]["port"]=os.environ['HTTP_PORT']
        print("- Env variable 'HTTP_PORT' set with value: "+str(_JSAP["sparql11protocol"]["port"]))
    except:
        print("- Env variable 'HTTP_PORT' not set, using default: "+str(_JSAP["sparql11protocol"]["port"]))
    finally:
        pass
    try:
        _JSAP["sparql11seprotocol"]["availableProtocols"]["ws"]["port"]=os.environ['WS_PORT']
        print("- Env variable 'WS_PORT' set with value: "+str(_JSAP["sparql11seprotocol"]["availableProtocols"]["ws"]["port"]))
    except:
        print("- Env variable 'WS_PORT' not set, using default: "+str(_JSAP["sparql11seprotocol"]["availableProtocols"]["ws"]["port"]))
    finally:
        pass
    try:
        _JSAP['extended']['discordConfig']['CHANNEL_ID']=os.environ['CHANNEL_ID']
        print("- Env variable 'CHANNEL_ID' set with value: "+str(_JSAP['extended']['discordConfig']['CHANNEL_ID']))
    except:
        print("- Env variable 'CHANNEL_ID' not set, using default: "+str(_JSAP['extended']['discordConfig']['CHANNEL_ID']))
    finally:
        pass
    try:
        _JSAP['extended']['discordConfig']['TOKEN']=os.environ['TOKEN']
        print("- Env variable 'TOKEN' set with value: "+str(_JSAP['extended']['discordConfig']['TOKEN'] ))
    except:
        print("- Env variable 'TOKEN' not set, using default: "+str(_JSAP['extended']['discordConfig']['TOKEN'] ))
    finally:
        pass
    print("####################################################################")
else:
    if sys.argv[1] == "-jsap": # OVERRIDE WITH COMMAND LINE ARGUMENT
        #QUI SIAMO IN LOCALHOST
        print("####################################################################")
        print("Loading custom jsap from: "+sys.argv[2])
        mySAP = open(sys.argv[2], 'r')
        _JSAP = json.load(mySAP)
        print("- Custom Jsap loaded, skipping environment variables override")
        print("Host: "+str(_JSAP["host"]))
        print("####################################################################")
    elif sys.argv[1] == "-dev":
        print("Running in dev mode... (ovvero per ora niente)")
    elif sys.argv[1] == "-help":
        print_help()
    else:
        print("WARNING: unknown parameter: "+str(sys.argv[1]))
        print_help()
        
#------------------------------------------------------------------------------------
#Formats subscription data. Returns a fromatted string
def login_format(res): 
    if res == []:
        print('NON CI SONO USER') 
        return
    MAIL = res[0]['s']['value'].split('/')[-1]
    USERNAME = res[0]['o']['value']
    return f"A new user has registered\\nMail: {MAIL}\\nUsername: {USERNAME}"
#-------------------------------------------------------------------------------------   
#Called when a new login si received   
def on_notification(a,r):
    global first_results
    if first_results == 1:
        print('first results ignored')
        first_results = 0
    else:
        client.update('SEND_DISCORD_MESSAGE', forcedBindings={
        "message_value" : login_format(a),       
        "source" : "LOGIN_AGGREGATOR"
        })

client = SEPA(sapObject=SAPObject(_JSAP))
client.subscribe('ALL_USERNAMES', 'PROVA', {}, on_notification)

while(True):
    time.sleep(10)