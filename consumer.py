#ogni volta che arriva un discord:Message, manda il messagio su Discord
import discord
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import json

mySAP = open("jsap_test.jsap.txt", 'r')
_JSAP = json.load(mySAP)

#CONFIGURAZIONE DISCORD
CHANNEL_ID = _JSAP['extended']['discordConfig']['CHANNEL_ID']    
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

def on_notification(a,r):
    print(discord_message_data(a))
    canale = bot.get_channel(CHANNEL_ID)
    bot.loop.create_task(canale.send(discord_message_data(a)))

@bot.event
async def on_ready():
    client = SEPA(sapObject=SAPObject(_JSAP))
    client.subscribe('ALL_DISCORD_MESSAGES', 'PROVA', {}, on_notification)

bot.run(TOKEN)
