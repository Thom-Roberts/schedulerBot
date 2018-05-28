import requests

apiKey = '13c40a7680f1a39e960be305fa7e46f2'
zip = "84037"
metric = "&units=metric"
url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip + "&APPID=" + apiKey + metric
response = requests.get(url)
value = response.json()

temp = (float(value['main']['temp']) * 1.8) + 32
intTemp = int(temp)

print (intTemp)
