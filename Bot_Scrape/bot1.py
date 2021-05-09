from bs4 import BeautifulSoup
import requests, discord, time, sys, tracemalloc
from discord import Embed
from discord.ext import commands
from datetime import datetime
from sys import exit
from tes1 import fetchPages as fp

#value=[['Tenis Air Jordan 1 Low Triple White','$2,399', '553558-130', 'Available', '1', 'Low', 'https://www.innvictus.com/medias/tenis-air-jordan-1-low-triple-white-in-553558-130-1.png?context=bWFzdGVyfGltYWdlc3w3MDI2N3xpbWFnZS9wbmd8aW1hZ2VzL2hkYS9oNjgvOTY2Mzk0NjkxNTg3MC5wbmd8NzFmMTEzMjI5MDdlYTEyZmM4NTAxYjIxY2YzODIwMmY5MjVkZTQxZTA1YjE4MjNlY2FmZWY1N2EyMDExNDExMw'],['Tenis Air Jordan 1 Mid ALT TD Black Gym Red', '$999.', 'AR6352-122', 'Available', '1', 'Low', 'https://www.innvictus.com/medias/tenis-air-jordan-1-mid-alt-td-black-gym-red-in-AR6352-122-1.png?context=bWFzdGVyfGltYWdlc3w2Nzc3M3xpbWFnZS9wbmd8aW1hZ2VzL2g0My9oMGYvMTAxMjAyNTI2MjA4MzAucG5nfGViZGJjZjIyYWVkNDlhM2IwY2Q4MTM5OTQ3OWJkNjI1NjZlYWNmMjYxZjJiODU2ZmU1NjRjOTMyNGJjNDI4YmY']]
footwearURL = "https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000"
tracemalloc.start()
#newurl = "https://www.innvictus.com/jordan/c/jordan"+"?"+para
#strt = request.Request(newurl, data)
global dataCheck
main = 'https://www.innvictus.com/'
client = discord.Client()
bot = commands.Bot(command_prefix='!')
        #my_secret = os.environ['Token']
        #@client.event
async def on_command_error(ctx, exc):
        if isinstance(exc, CommandNotFound):pass
        else:raise exc.original


@client.event
async def on_ready():
          print('We are activated as {0.user}'.format(client))
          channel = client.get_channel(838131329597177932)
          data = fp("https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000")
          for i in data:
              product,price,model,stat,quant,size,img,link =i[0], i[1], i[2], i[3], i[4], i[5],i[6],i[7]
              embed = Embed(title = product, url=link, colour=0x3b35c0, timestamp = datetime.utcnow())
              fields = [("Status",stat+' 🟢',True),
                        ("Price",price, True),
                        ("Cart Limit",quant, True),
                        ("Style Code",model, True),
                        ("Sizes", '['+size+']', False)]
              dataCheck=stat
              for name, value, inline in fields:
                  embed.add_field(name=name, value=value, inline=inline)
              embed.set_author(name=main)
              embed.set_thumbnail(url=img)
              embed.set_footer(text="Notifier-Bot By @AnishBangotra")
              await channel.send(embed = embed)
        
          #await client.close()
#print(dataCheck)
@client.event
async def on_message(message):
          if message.author ==  client.user:return
          if message.content == 'Reminder':
             if dataCheck != "Availble":
                 embed = Embed(title="Last Product Status", description = "Out Of Stock(Updated!)")
             else:
                 embed = Embed(title="Last Product Status", description = "Availble(Updated!)")
             await message.channel.send(embed = embed)
             return

client.run('ODM4MTMxODY3MDA1ODc4MzIy.YI2pIA.YBpIHYxfvPBUTFAtalTTiHBWAIw')
