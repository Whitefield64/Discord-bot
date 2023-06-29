import discord
from discord.ext import commands
from discord import app_commands
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import time
import core.JsapLoader as JsapLoader

_JSAP= JsapLoader.get_configured_jsap()

#DISCROD CONFIGURATION-------------------------------------------
CHANNEL_ID = int(_JSAP['extended']['discordConfig']['CHANNEL_ID'])    
TOKEN = _JSAP['extended']['discordConfig']['TOKEN'] 
bot = commands.Bot(command_prefix='/', description='', intents=discord.Intents.all())

#COMMAND SYNCHRONIZATION-----------------------------------------
@bot.event
async def on_ready():
    print('---------BOT ONLINE---------')
    try:
        synced = await bot.tree.sync()  #sincronizza i comandi
        print(f'---------SYNCHRONIZED COMMANDS: {len(synced)}---------')
        for i in range(len(synced)):
            print(synced[i])   #contiene i nomi di tutti i comandi nel tree, che inserisco sotto
        print("------------------------------------------")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = ''))
    except Exception:
        print('!!!SOMETHING WENT WRONG WITH COMMANDS SYNCHRONIZATION!!!')
#----------------------------------------------------------------
_CACHE={}  
def add_to_cache(observation):
    ptime= observation["ptime"]["value"] 
    value= observation["value"]["value"] 
    unit= observation["unit"]["value"] 

    if ptime not in _CACHE:
        print(f"Adding new ptime: {ptime}")
        _CACHE[ptime]={}
        _CACHE[ptime]["value"]=value
        _CACHE[ptime]["unit"]=unit
#----------------------------------------------------------------

'''client = SEPA(sapObject=SAPObject(_JSAP))
res = client.query('getAllProperties')
properties = ['AvailableWater', 'Drainage']'''

#----------------------------------------------------------------

@bot.tree.command(name='availablewater', description='Send AvailableWater parameter')
@app_commands.describe(feature='insert the interested feature')
async def availablewater(interaction:discord.Interaction, feature:str):
    conc_feature = 'https://vaimee.com/meter#'+feature+'_table'
    conc_porperty = 'https://vaimee.com/meter/criteria/property#AvailableWater'
    client = SEPA(sapObject=SAPObject(_JSAP))
    a = client.query('getUnitProperty',{
        "feature": conc_feature,
        "property": conc_porperty
    })['results']['bindings']
    if a == []:
        canale = bot.get_channel(CHANNEL_ID)
        await canale.send('This feature has no availablewater parametres or it does not exist')
        print('This feature has no availablewater parametres or it does not exist')
    else:
        for observation in a:
            add_to_cache(observation)    
        PTIME = []
        VALUE = []
        UNIT = []
        for ptime in _CACHE:
                PTIME.append(ptime)
                VALUE.append(_CACHE[ptime]['value']) 
                UNIT.append(_CACHE[ptime]['unit'])
        emb = discord.Embed(title=f'{feature} available water:', description=f"{PTIME[0]}: {VALUE[0]} {UNIT[0].split('/')[-1]}\n{PTIME[1]}: {VALUE[1]} {UNIT[1].split('/')[-1]}\n{PTIME[2]}: {VALUE[2]} {UNIT[2].split('/')[-1]}", color=discord.Color.from_rgb(0,0,255))  
        await interaction.response.send_message(embed=emb)

bot.run(TOKEN)