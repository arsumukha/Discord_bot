import discord
import os
import requests, json 
from keep_alive import keep_alive

from datetime import datetime
import pytz

api_key = os.getenv('TOKENS')
base_url = "http://api.openweathermap.org/data/2.5/weather?"

tz_NY = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz_NY)

times = now.strftime("%m/%d/%Y, %H:%M:%S")
client = discord.Client()
@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  if message.content.startswith("$time"):
    await message.channel.send(times+"  IST")
  if message.content.startswith("$help"):
    await message.channel.send("Welcome to my app use $weather city_name to get the weather updates.Thank you")
  if message.content.startswith('$weather'):
    city=message.content.split(" ")
    city_name = city[1]
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json() 
    if x["cod"] != "404":
      y = x["main"]
      current_temperature = y["temp"]
      current_pressure = y["pressure"]
      current_humidiy = y["humidity"]
      z = x["weather"]
      weather_description = z[0]["description"]
      await message.channel.send("Place="+city_name+" \nTemperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description)+
                    "\n Temperature in celsius =" +str(round(int(current_temperature)-273.15,2))) 
    else:
      await message.channel.send("format for weather code is '$weather city'")
keep_alive()
client.run(os.getenv('TOKEN'))
