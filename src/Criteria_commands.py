import discord
from discord.ext import commands
from discord import app_commands
from sepy.SAPObject import *
from sepy.SEPA import SEPA
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
 
def format(res):
    PTIME = []
    VALUE = []
    UNIT = []
    for observation in res:
        PTIME.append(observation['ptime']['value'])
        VALUE.append(observation['value']['value']) 
        UNIT.append(observation['unit']['value'])
    text = ''
    for i in range(len(PTIME)):
        text = text+f"* {PTIME[i].split('T')[0]}: {VALUE[i]} {UNIT[i].split('#')[-1]}\n"
    return text
'''
#----------------------------------------------------------------
#PER RENDERLO SCALABILE
#client = SEPA(sapObject=SAPObject(_JSAP))
#res = client.query('getAllProperties')
properties = ['Drainage', 'AvailableWater']

#----------------------------------------------------------------
for property in properties:
    @bot.tree.command(name=property.lower(), description=f'Send {property} parameter')
    @app_commands.describe(feature='insert the interested feature')
    async def command(interaction:discord.Interaction, feature:str):
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
            descr = format(a)    
            emb = discord.Embed(title=f'{feature} {property}:', description=descr, color=discord.Color.from_rgb(0,0,255))  
            #emb.set_author(name='Agrifirm Bot', icon_url='https://grafana.criteria.vaimee.com/public/img/grafana_icon.svg') #!immagine non discponibile
            await interaction.response.send_message(embed=emb)

'''

@bot.tree.command(name='availablewater', description=f'Send availablewater parameter')
@app_commands.describe(feature='insert the interested feature')
async def availablewater(interaction:discord.Interaction, feature:str):
    conc_feature = 'https://vaimee.com/meter#'+feature
    conc_porperty = 'https://vaimee.com/meter/criteria/property#AvailableWater'
    #print(conc_feature)
    #print(conc_porperty)
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
        descr = format(a)    
        emb = discord.Embed(title=f'AvailableWater:', description=descr, color=discord.Color.from_rgb(35,139,232))  
        emb.set_author(name=feature, icon_url='https://raw.githubusercontent.com/Whitefield64/Discord-bot/master/img/farmplot.jpg')
        emb.set_thumbnail(url='https://raw.githubusercontent.com/Whitefield64/Discord-bot/master/img/water-drop-icon.png')
        await interaction.response.send_message(embed=emb)

@bot.tree.command(name='drainage', description=f'Send drainage parameter')
@app_commands.describe(feature='insert the interested feature')
async def drainage(interaction:discord.Interaction, feature:str):
    conc_feature = 'https://vaimee.com/meter#'+feature
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
        descr = format(a)
        emb = discord.Embed(title=f'Drainage:', description=descr, color=discord.Color.from_rgb(35,139,232))
        emb.set_author(name=feature, icon_url='https://raw.githubusercontent.com/Whitefield64/Discord-bot/master/img/farmplot.jpg')
        emb.set_thumbnail(url='https://raw.githubusercontent.com/Whitefield64/Discord-bot/master/img/water-drop-icon.png') 
        await interaction.response.send_message(embed=emb)

bot.run(TOKEN)