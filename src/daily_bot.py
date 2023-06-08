import discord
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
from sepy.SAPObject import *
from sepy.SEPA import SEPA

mySAP = open("default.jsap", 'r')
_JSAP = json.load(mySAP)

scheduler = AsyncIOScheduler()

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

def data_formatter(res):
    if res == []:
        return []
    #inserire la formattazione dei dati
    return f"""
>>> Eccoti il tuo recap giornaliero:
dati formattati
"""
#------------------------------------------------------------------------------------
#DAILY TASKS
async def send_remember():
    channel = bot.get_channel(CHANNEL_ID)  
    await channel.send("Buongiorno. Ti sei ricordato di avviare My2sec?")

async def send_recap():
    client = SEPA(sapObject=SAPObject(_JSAP))
    res = client.query('ALL_USERNAMES')  
    channel = bot.get_channel(CHANNEL_ID) 
    await channel.send(data_formatter(res))

@bot.event
async def on_ready():
    scheduler.add_job(send_remember, 'cron', hour=10, minute=24) #alle 8 avvia la task send_remember
    scheduler.add_job(send_recap, 'cron', hour=10, minute=25) #alle 20 avvia la task send_recap
    scheduler.start()

@bot.event
async def on_message(message):
    content = message.content
    author = message.author
    canale = message.channel
    if author == bot.user:
        return
    if content.startswith('!recap'):
        scheduler.add_job(send_recap)
        scheduler.start()
        
bot.run(TOKEN)