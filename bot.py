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

@client.command()
async def sean():
    await client.say("Seansux")

@client.command()
async def weather(zip : str):
    print (zip)
    apiKey = '13c40a7680f1a39e960be305fa7e46f2'
    metric = "&units=metric"
    url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip + "&APPID=" + apiKey + metric
    try:
        response = requests.get(url)
        value = response.json()

        temp = (float(value['main']['temp']) * 1.8) + 32
        intTemp = int(temp)

        print (intTemp)
        await client.say("The temperature at zip code " + zip + " is " + str(intTemp))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        await client.say("Uh, we failed cap'n")
    except KeyError:
        await client.say("Nope, didn't find that zip")
client.run(TOKEN)
