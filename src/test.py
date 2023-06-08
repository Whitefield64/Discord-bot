import discord
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
from sepy.SAPObject import *
from sepy.SEPA import SEPA

mySAP = open("default.jsap", 'r')
_JSAP = json.load(mySAP)

client = SEPA(sapObject=SAPObject(_JSAP))
res = client.query('ALL_USERNAMES')  
print(res)