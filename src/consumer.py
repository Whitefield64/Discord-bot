import discord
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json
import os
import sys

# Di default usiamo questo
_message_graph= "http://www.vaimee.it/my2sec/messages/discord"

first_results=1
print("#####################")
print("DISCORD CONSUMER v0.1")
print("#####################")

#-----OVERRIDE DEFAULT JSAP CONFIGURATION---------------------------------------------------------------
def print_help():
    print("--<HELP WINDOW>--")
    print("Run with: python ./yourscript.py -jsap path.jsap")
    print("For a complete description of how to run the Bot see the 'configuration' chapter in the readme file on GitHub: https://github.com/Whitefield64/Discord-bot/blob/master/README.md")
    print('-------------------------------------------------------------------------------')
if len(sys.argv) == 1 :
    print("####################################################################")
    mySAP = open("./Resources/default.jsap", 'r')
    _JSAP = json.load(mySAP)
    print("- Jsap loaded, overriding configuration")
    # OVERRIDE VARIABLES
    try:
        _message_graph=os.environ['MESSAGE_GRAPH']
        print("- Env variable 'MESSAGE_GRAPH' set with value: "+str(_message_graph))
    except:
        print("- Env variable 'MESSAGE_GRAPH' not set, using default: "+str(_message_graph))
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
        
#------------------------------------------------------------------------
#DISCORD CONFIGURATION
CHANNEL_ID = int(_JSAP['extended']['discordConfig']['CHANNEL_ID'])    
TOKEN = _JSAP['extended']['discordConfig']['TOKEN'] 
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
#!cambia ID canale
#-----------------------------------------------------------------------
def discord_message_data(a):
    if a == []:
        return []
    MESSAGE_VALUE = a[0]['message_value']['value']
    SOURCE = a[0]['source']['value']
    DATE = a[0]['timestamp']['value'].split('T')[0]
    TIME = a[0]['timestamp']['value'].split('T')[1].split('.')[0]
    return f"""
>>> {TIME}, {DATE}: New message received from: **{SOURCE.split('/')[-1]}**
```{MESSAGE_VALUE}
```
"""
#------------------------------------------------------------------------------------

def on_notification(a,r):
    global first_results
    if first_results == 1:
        print("Ignored first results")
        first_results=0
    else:
        if discord_message_data(a) == []:
            return
        else:
            canale = bot.get_channel(CHANNEL_ID)
            bot.loop.create_task(canale.send(discord_message_data(a)))
            print('message sent successfully')

@bot.event
async def on_ready():
    client = SEPA(sapObject=SAPObject(_JSAP))
    client.subscribe('ALL_DISCORD_MESSAGES', 'PROVA', {
        "message_graph":_message_graph
    }, on_notification)

bot.run(TOKEN)
