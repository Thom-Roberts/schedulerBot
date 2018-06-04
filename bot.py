# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
#import discord
import requests #allows for the api calls

from discord.ext.commands import Bot
from TOKEN import TOKEN #gets the token from token.py
from TOKEN import BUNGIEAPIKEY

client = Bot(command_prefix="?")
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

@client.command()
async def sean():
    userName = "sr_jeebs/"
    getUserUrl = "https://www.bungie.net/Platform//Destiny2/SearchDestinyPlayer/2/" + userName
    response = requests.get(getUserUrl, headers={"X-API-Key": BUNGIEAPIKEY})
    value = response.json()

    membershipId = value["Response"][0]["membershipId"] #gets a bungie user membershipId

    getStatsUrl = "https://www.bungie.net/Platform/Destiny2/2/Account/" + membershipId + "/Stats/"
    response5 = requests.get(getStatsUrl, headers={"X-API-Key": BUNGIEAPIKEY})
    value5 = response5.json()
    deathsPvp = value5["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["deaths"]["basic"]["value"]
    deathsPve = value5["Response"]["mergedAllCharacters"]["results"]["allPvE"]["allTime"]["deaths"]["basic"]["value"]

    await client.say("Sean has died a total of " + str(int(deathsPve + deathsPvp)) + " times")

@client.command()
async def sports():
    await client.say("Never play MLB The Show, not even once")

@client.command()
async def scoops():
    await client.say("#chrispaulsux")

#NOTE: figure out a way to get this activating daily?
#see discord python tutorial part 2
@client.command()
async def motivate():
    url = "http://quotes.rest/qod.json"
    response = requests.get(url)
    value = response.json()
    qod = value['contents']['quotes'][0]['quote']
    await client.say(qod)

@client.command()
async def weather(zip : str):
    apiKey = '13c40a7680f1a39e960be305fa7e46f2'
    metric = "&units=metric"
    url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip + "&APPID=" + apiKey + metric
    try:
        response = requests.get(url)
        value = response.json()

        temp = (float(value['main']['temp']) * 1.8) + 32
        intTemp = int(temp)

        await client.say("The temperature at zip code " + zip + " is " + str(intTemp))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        await client.say("Uh, we failed cap'n")
    except KeyError:
        await client.say("Nope, didn't find that zip")

#gets a bunch of arguments, instead of just one at a time
@client.command()
async def test(*args):
    await client.say('{} arguments: {}'.format(len(args), ', '.join(args)))

@client.command()
async def image():
    await client.say('https://ichef.bbci.co.uk/news/660/cpsprodpb/71E1/production/_99735192_gettyimages-459467912.jpg')

@client.command()
async def getKd(userName : str):
    getUserUrl = "https://www.bungie.net/Platform//Destiny2/SearchDestinyPlayer/2/" + userName
    response = requests.get(getUserUrl, headers={"X-API-Key": BUNGIEAPIKEY})
    value = response.json()
    membershipId = value["Response"][0]["membershipId"] #gets a bungie user membershipId

    getStatsUrl = "https://www.bungie.net/Platform/Destiny2/2/Account/" + membershipId + "/Stats/"
    response2 = requests.get(getStatsUrl, headers={"X-API-Key": BUNGIEAPIKEY})
    value2 = response2.json()

    kills = value2["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["kills"]["basic"]["value"]
    deaths = value2["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["deaths"]["basic"]["value"]
    killDeath = round((kills/deaths), 2)

    await client.say("PVP kill/death: " + str(killDeath))

@client.command()
async def helloWorld():
    await client.say("!play Never gonna give you up")

client.run(TOKEN)
