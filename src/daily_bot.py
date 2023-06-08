import discord
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import sys
import os
#prova
mySAP = open("default.jsap", 'r')
_JSAP = json.load(mySAP)

scheduler = AsyncIOScheduler()

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
        first_results=os.environ['FIRST_RESULTS']
        print("- Env variable 'FIRST_RESULTS' set with value: "+str(first_results))
    except:
        first_results=1
        print("- Env variable 'FIRST_RESULTS' not set, using default: "+str(first_results))
    finally:
        pass
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
#-------------------------------------------------------------------------
#DISCORD CONFIGURATION
CHANNEL_ID = _JSAP['extended']['discordConfig']['CHANNEL_ID']    
TOKEN = _JSAP['extended']['discordConfig']['TOKEN'] 

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True
bot = discord.Client(intents=intents)

#--------------------------------------------------------------------------

def recap_formatter(res):
    if res == []:
        return []
    #inserire la formattazione dei dati
    return f""">>> Here is your daily recap:\\ndati formattati"""
#------------------------------------------------------------------------------------
#DAILY TASKS
async def send_remember():
    client = SEPA(sapObject=SAPObject(_JSAP))
    client.update('SEND_DISCORD_MESSAGE', forcedBindings={
    "message_value" : 'Good morning, did you remember to turn on My2sec?',       
    "source" : "Daily Bot"
    })

async def send_recap():
    client = SEPA(sapObject=SAPObject(_JSAP))
    res = client.query('ALL_USERNAMES') 
    print('query done') 
    client.update('SEND_DISCORD_MESSAGE', forcedBindings={
    "message_value" : recap_formatter(res),       
    "source" : "Daily Bot"
    })

@bot.event
async def on_ready():
    scheduler.add_job(send_remember, 'cron', hour=12, minute=43)
    scheduler.add_job(send_recap, 'cron', hour=12, minute=44) 
    scheduler.start()
        
bot.run(TOKEN)
