# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import requests #allows for the api
import xml.etree.cElementTree as ET

from discord.ext.commands import Bot
from discord.ext.commands import MemberConverter
from TOKEN import TOKEN #gets the token from token.py
from TOKEN import BUNGIEAPIKEY

bot = Bot(command_prefix="?")

@bot.command(pass_context = True)
async def createTeam(ctx, teamName: str):
    #teamName should be in the tag
    #the author should be inserted as a member of that team
    userName = ctx.message.author
    tree = ET.parse('bot.xml')
    root = tree.getroot()
    team = ET.SubElement(root, 'team')
    team.set('teamName', teamName)
    team.set('leader', str(userName))

    for x in range(6):
        member = ET.Element("member")
        team.append(member)
    
    # Add leader as the first member
    team[0].text = str(userName)

    tree.write('bot.xml')

    await bot.say("Created team with name: " + teamName)

@bot.command(pass_context = True)
async def addTo(ctx, teamName: str, member1: discord.Member):
    userName = ctx.message.author
    tree = ET.parse('bot.xml')
    root = tree.getroot()
    memberAdded = False
    duplicateMember = False
    FailMessage = (str(member1) + ' was not added to the team')
    SuccessMessage = (str(member1) + ' was added successfully')

    for team in root.iter('team'):
        if teamName == team.attrib['teamName']:
            for member in team.iter('member'):
                """
                    Stop on each member
                    Check if the name equals the input member
                    if it does match, then we can set a local bool
                    Our if statement can include that local bool and make sure it equal false
                """
                if member.text == str(member1):
                    duplicateMember = True
                    memberAdded = False

                if member.text == None and duplicateMember == False:
                    member.text = str(member1)
                    print(member.text)
                    memberAdded = True
                    duplicateMember = True
    
    message = ''
    if memberAdded == False:
        message = FailMessage
    else:
        message = SuccessMessage
        tree.write('bot.xml')
  
    await bot.say(message)


@bot.command(pass_context = True)
async def removeFrom(ctx, teamName: str, member1: discord.Member):

    tree = ET.parse('bot.xml')
    root = tree.getroot()
    memberRemoved = False
    FailMessage = (str(member1) + ' was not removed to the team')
    SuccessMessage = (str(member1) + ' was removed successfully')

    for team in root.iter('team'):
        if teamName == team.attrib['teamName']:
            for member in team.iter('member'):
                if member.text == str(member1):
                    member.text = None
                    memberRemoved = True
                    break
    
    message = ''
    if memberRemoved == False:
        message = FailMessage
    else:
        message = SuccessMessage
        tree.write('bot.xml')

    await bot.say(message)

@bot.command(pass_context = True)
async def showTeam(ctx, teamName: str):
    tree = ET.parse('bot.xml')
    root = tree.getroot()
    default_message = 'Team currently constists of: '
    member_list = ''
    for team in root.iter('team'):
        if teamName == team.attrib['teamName']:
            for member in team.iter('member'):
                member_list += member.text
    
    await bot.say(default_message + member_list)


@bot.command()
async def xml(type: str, category: str, message: str):
    if type == "write":
        root = ET.Element('root')
        ET.SubElement(root, category).text = message
        tree = ET.ElementTree(root)
        tree.write('bot.xml')
    elif type == "get":
        root = tree.getroot()
        output = ''
        for child in root:
            if child.text == message:
                output = child.text
        if output == '':
            await bot.say('Message not found')
        else:
            await bot.say('Message: ' + output)
    else:
        await bot.say('Command not recognized')

#does the whole bitcoin thing
@bot.command()
async def invest():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    value = value.replace(",", "") #doesn't work if there are commas
    if float(value) > 8000:
        await bot.say("INVEST! Bitcoin is amazing.")
    else:
        await bot.say("Are you seriously asking me about bitcoin? Stop it already")
    await bot.say("Bitcoin price is: " + value)

@bot.command()
async def jeebs():
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

    await bot.say("Sean has died a total of " + str(int(deathsPve + deathsPvp)) + " times")

#NOTE: figure out a way to get this activating daily?
#see discord python tutorial part 2
@bot.command()
async def motivate():
    url = "http://quotes.rest/qod.json"
    response = requests.get(url)
    value = response.json()
    qod = value['contents']['quotes'][0]['quote']
    await bot.say(qod)

@bot.command()
async def weather(zip : str):
    apiKey = '13c40a7680f1a39e960be305fa7e46f2'
    metric = "&units=metric"
    url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip + "&APPID=" + apiKey + metric
    try:
        response = requests.get(url)
        value = response.json()

        temp = (float(value['main']['temp']) * 1.8) + 32
        intTemp = int(temp)

        await bot.say("The temperature at zip code " + zip + " is " + str(intTemp))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        await bot.say("Uh, we failed cap'n")
    except KeyError:
        await bot.say("Nope, didn't find that zip")

#gets a bunch of arguments, instead of just one at a time
@bot.command()
async def test(*args):
    await bot.say('{} arguments: {}'.format(len(args), ', '.join(args)))




@bot.command()
async def image():
    await bot.say('https://ichef.bbci.co.uk/news/660/cpsprodpb/71E1/production/_99735192_gettyimages-459467912.jpg')

@bot.command()
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

    await bot.say("PVP kill/death: " + str(killDeath))

@bot.command()
async def efficiency(userName : str):
    getUserUrl = "https://www.bungie.net/Platform//Destiny2/SearchDestinyPlayer/2/" + userName
    response = requests.get(getUserUrl, headers={"X-API-Key": BUNGIEAPIKEY})
    value = response.json()
    membershipId = value["Response"][0]["membershipId"] #gets a bungie user membershipId

    getStatsUrl = "https://www.bungie.net/Platform/Destiny2/2/Account/" + membershipId + "/Stats/"
    response2 = requests.get(getStatsUrl, headers={"X-API-Key": BUNGIEAPIKEY})
    value2 = response2.json()

    kills = value2["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["kills"]["basic"]["value"]
    deaths = value2["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["deaths"]["basic"]["value"]
    assists = value2["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["assists"]["basic"]["value"]
    efficiency = round(((kills + assists)/deaths), 2)

    await bot.say("PVP efficiency: " + str(efficiency))

#this is how you get the context, which is from the first parameter
@bot.command(pass_context = True)
async def test2(ctx):
    #gets the author's tag
    member = ctx.message.author
    #member.mention will tag the author in with it
    #Documentation for the member object:
    #https://discordpy.readthedocs.io/en/rewrite/api.html#discord.Member
    await bot.say("Greetings " + str(member.mention))

@bot.command()
async def helloWorld():
    await bot.say("!play Never gonna give you up")

bot.run(TOKEN)
