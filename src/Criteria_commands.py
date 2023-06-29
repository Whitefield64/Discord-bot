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
    return 
#----------------------------------------------------------------
#PER RENDERLO SCALABILE
'''client = SEPA(sapObject=SAPObject(_JSAP))
res = client.query('getAllProperties')
properties = ['Drainage', 'AvailableWater']

#----------------------------------------------------------------
for property in properties:
    @bot.tree.command(name=property.lower(), description=f'Send {property} parameter')
    @app_commands.describe(feature='insert the interested feature')
    async def propertycommand(interaction:discord.Interaction, feature:str):
        conc_feature = 'https://vaimee.com/meter#'+feature+'_table'
        conc_porperty = 'https://vaimee.com/meter/criteria/property#'+property
        print(conc_feature)
        print(conc_porperty)
        client = SEPA(sapObject=SAPObject(_JSAP))
        a = client.query('getUnitProperty',{
            "feature": conc_feature,
            "property": conc_porperty
        })['results']['bindings']
        if a == []:
            canale = bot.get_channel(CHANNEL_ID)
            await canale.send(f'This feature has no {property} parametres or it does not exist')
            print(f'This feature has no {property} parametres or it does not exist')
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
            emb = discord.Embed(title=f'{feature} {property}:', description=f"{PTIME[0]}: {VALUE[0]} {UNIT[0].split('/')[-1]}\n{PTIME[1]}: {VALUE[1]} {UNIT[1].split('/')[-1]}\n{PTIME[2]}: {VALUE[2]} {UNIT[2].split('/')[-1]}", color=discord.Color.from_rgb(0,0,255))  
            await interaction.response.send_message(embed=emb)
'''

@bot.tree.command(name='availablewater', description=f'Send availablewater parameter')
@app_commands.describe(feature='insert the interested feature')
async def availablewater(interaction:discord.Interaction, feature:str):
    conc_feature = 'https://vaimee.com/meter#'+feature+'_table'
    conc_porperty = 'https://vaimee.com/meter/criteria/property#AvailableWater'
    print(conc_feature)
    print(conc_porperty)
    client = SEPA(sapObject=SAPObject(_JSAP))
    a = client.query('getUnitProperty',{
        "feature": conc_feature,
        "property": conc_porperty
    })['results']['bindings']
    if a == []:
        canale = bot.get_channel(CHANNEL_ID)
        await canale.send(f'This feature has no AvailableWater parametres or it does not exist')
        print(f'This feature has no AvailableWater parametres or it does not exist')
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
        emb = discord.Embed(title=f'{feature} AvailableWater:', description=f"{PTIME[0]}: {VALUE[0]} {UNIT[0].split('/')[-1]}\n{PTIME[1]}: {VALUE[1]} {UNIT[1].split('/')[-1]}\n{PTIME[2]}: {VALUE[2]} {UNIT[2].split('/')[-1]}", color=discord.Color.from_rgb(0,0,255))  
        await interaction.response.send_message(embed=emb)
        #!scvuota chacheeeee

@bot.tree.command(name='drainage', description=f'Send drainage parameter')
@app_commands.describe(feature='insert the interested feature')
async def drainage(interaction:discord.Interaction, feature:str):
    conc_feature = 'https://vaimee.com/meter#'+feature+'_table'
    conc_property = 'https://vaimee.com/meter/criteria/property#Drainage'
    print(conc_feature)
    print(conc_property)
    client = SEPA(sapObject=SAPObject(_JSAP))
    a = client.query('getUnitProperty',{
        "feature": conc_feature,
        "property": conc_property
    })['results']['bindings']
    if a == []:
        canale = bot.get_channel(CHANNEL_ID)
        await canale.send(f'This feature has no Drainage parametres or it does not exist')
        print(f'This feature has no Drainage parametres or it does not exist')
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
        emb = discord.Embed(title=f'{feature} Drainage:', description=f"{PTIME[0]}: {VALUE[0]} {UNIT[0].split('/')[-1]}\n{PTIME[1]}: {VALUE[1]} {UNIT[1].split('/')[-1]}\n{PTIME[2]}: {VALUE[2]} {UNIT[2].split('/')[-1]}", color=discord.Color.from_rgb(0,0,255))  
        await interaction.response.send_message(embed=emb)
        #!scvuota chacheeeee

bot.run(TOKEN)