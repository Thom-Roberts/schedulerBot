import requests
import json

bungieRoot = "https://www.bungie.net/Platform"
getBungieAccount = "https://www.bungie.net/platform/User/GetBungieAccount/13323790/254/"
getProfile = "/Destiny.HistoricalStats.Definitions.DestinyStatsCategoryType"
apiKey = '7684297ff9e64e08901eff25e6ff376a'
#url = bungieRoot + "?X-API-Key=" + apiKey
url = getBungieAccount;
membershipType = 2 #psn

"""response = requests.get(url, headers={"X-API-Key": apiKey})
value = response.json()

response2 = requests.get(bungieRoot + getProfile + "/4611686018467821536/", headers={"X-API-Key": apiKey})
value2 = response2.json()
"""
#response3 = requests.get(bungieRoot + getProfile, headers={"X-API-Key": apiKey})
#value3 = response3.json()

"""
response4 = requests.get("https://www.bungie.net/Platform/Destiny2/2/Account/4611686018449352128/Stats/", headers={"X-API-Key": apiKey})
value4 = response4.json()
kills = value4["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["kills"]["basic"]["value"]
deaths = value4["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["deaths"]["basic"]["value"]
killDeath = round((kills/deaths), 2)
#print (value)
#print (value2)
#print (value3)
print (kills)
print (deaths)
print ("Kill death ratio = " + str(killDeath))
"""


userName = "sr_jeebs/"
getUserUrl = "https://www.bungie.net/Platform//Destiny2/SearchDestinyPlayer/2/" + userName
response = requests.get(getUserUrl, headers={"X-API-Key": apiKey})
value = response.json()

membershipId = value["Response"][0]["membershipId"] #gets a bungie user membershipId

getStatsUrl = "https://www.bungie.net/Platform/Destiny2/2/Account/" + membershipId + "/Stats/"
response5 = requests.get(getStatsUrl, headers={"X-API-Key": apiKey})
value5 = response5.json()
deathsPvp = value5["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["deaths"]["basic"]["value"]
deathsPve = value5["Response"]["mergedAllCharacters"]["results"]["allPvE"]["allTime"]["deaths"]["basic"]["value"]

print(deathsPve)
print(deathsPvp)
