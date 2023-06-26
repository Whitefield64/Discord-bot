import discord
from discord.ext import commands
from discord import app_commands
from sepy.SAPObject import *
from sepy.SEPA import SEPA
import time

import core.JsapLoader as JsapLoader

_JSAP= JsapLoader.get_configured_jsap()

#NUOVA CONFIGURAZIONE-------------------------------------------
CHANNEL_ID = int(_JSAP['extended']['discordConfig']['CHANNEL_ID'])    
TOKEN = _JSAP['extended']['discordConfig']['TOKEN'] 
bot = commands.Bot(command_prefix='/', description='', intents=discord.Intents.all())
#---------------------------------------------------------------


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

@bot.tree.command(name='availablewater', description='Send AvailableWater parameter')
@app_commands.describe(feature='insert the interested feature')
async def availablewater(interaction:discord.Interaction, feature:str):
    client = SEPA(sapObject=SAPObject(_JSAP))
    client.query('Unit_irrigation_needs')
    #scompongo la query pr ottenere l'available water della determinata feature
    res = 0 
    emb = discord.Embed(title=f'{feature} available water:', description=f'{res}', color=discord.Color.from_rgb(0,0,255))  
    await interaction.response.send_message(embed=emb)


bot.run(TOKEN)