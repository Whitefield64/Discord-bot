import json
import openai
import discord

import core.JsapLoader as JsapLoader

print("#####################")
print("GPT PRODUCER v0.1")
print("#####################")

#-----OVERRIDE DEFAULT JSAP CONFIGURATION---------------------------------------------
_JSAP= JsapLoader.get_configured_jsap()
#------------------------------------------------------------------------------------- 


#DISCORD CONFIG-----------------------------------------------------------------------
CHANNEL_ID = int(_JSAP['extended']['discordConfig']['CHANNEL_ID'])    
TOKEN = _JSAP['extended']['discordConfig']['TOKEN'] 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True
bot = discord.Client(intents=intents)

#OPENAI CONFIG-------------------------------------------------------------------------------

openai.api_key = _JSAP['extended']['gpt_config']['API_key']

def get_response(messages:list):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = 1.0 
    )
    return response.choices[0].message

#------------------------------------------------------------------------------------

@bot.event
async def on_message(message):
    contenuto = message.content
    autore = message.author
    canale = message.channel
    if autore == bot.user:
        return
    if __name__ == "__main__":
        messages = [
            {"role": "system", "content": "You are a virtual assistant specialized in agricolture. You auto detect current language"}
        ]
        user_input = contenuto
        messages.append({"role": "user", "content": user_input})
        new_message = get_response(messages=messages)
        await canale.send(new_message['content'])
        messages.append(new_message)

bot.run(TOKEN)
