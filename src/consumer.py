#ogni volta che arriva un discord:Message, manda il messagio su Discord
import discord
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json
import os

first_results=1
print("#####################")
print("DISCORD CONSUMER v0.1")
print("#####################")

#-----MAIN---------------------------------------------------------------
mySAP = open("Resources/jsap_test.jsap", 'r')
_JSAP = json.load(mySAP)
print("####################################################################")
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


#CONFIGURAZIONE DISCORD
CHANNEL_ID = int(_JSAP['extended']['discordConfig']['CHANNEL_ID'])    
TOKEN = _JSAP['extended']['discordConfig']['TOKEN'] 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True
bot = discord.Client(intents=intents)

#-----------------------------------------------------------------------

def extract_query_bindings(query_results):  #estrae i bindings da una query
    return [query_results['results']['bindings']]

def take_last_info(res):    #mi mette la info pulita (taglia l'url delle onologie) (inutile se utilizzi blanc node)
    last = res.split('/')[-1]
    last = last.split('#')[-1]
    return last

def discord_message_data(a): #estrae i dati del messaggio discord ricevuto dalla sub. !!!restituisce una stringa
    if a == []:
        return []
    MESSAGE_VALUE = a[0]['message_value']['value']
    SOURCE = a[0]['source']['value']
    DATE = a[0]['timestamp']['value'].split('T')[0]
    TIME = a[0]['timestamp']['value'].split('T')[1].split('.')[0]
    return f"""
>>> ```
New message received from: {SOURCE}
{TIME}, {DATE}   
Content:                                
{MESSAGE_VALUE}
```
"""
#------------------------------------------------------------------------------------

#first_results=1
def on_notification(a,r):
    global first_results
    if first_results == 1:
        print("Ignored first results")
        first_results=0
        
        #print(first_results)
    else:
        print(discord_message_data(a))
        print(CHANNEL_ID)
        canale = bot.get_channel(CHANNEL_ID)
        bot.loop.create_task(canale.send(discord_message_data(a)))

@bot.event
async def on_ready():
    client = SEPA(sapObject=SAPObject(_JSAP))
    client.subscribe('ALL_DISCORD_MESSAGES', 'PROVA', {}, on_notification)

bot.run(TOKEN)
