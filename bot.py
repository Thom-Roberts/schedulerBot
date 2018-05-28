# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
#import discord
import requests

from discord.ext.commands import Bot
from TOKEN import TOKEN #gets the token from token.py

client = Bot(command_prefix="!")

#does the whole bitcoin thing
@client.command()
async def invest():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    value = value.replace(",", "") #doesn't work if there are commas
    if float(value) > 8000:
        await client.say("INVEST! Bitcoin is amazing.")
    else:
        await client.say("Are you seriously asking me about bitcoin? Stop it already")
    await client.say("Bitcoin price is: " + value)

#Links a youtube video
@client.command()
async def play():
    await client.say("This should be a good song for ya")
    await client.say("https://www.youtube.com/watch?v=HZ5m_nlfZe4&list=RDHZ5m_nlfZe4&start_radio=1")

client.run(TOKEN)
