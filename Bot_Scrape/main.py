from bs4 import BeautifulSoup
import requests, discord, time, sys, tracemalloc
from discord import Embed
from discord.ext import commands
from datetime import datetime
from sys import exit

#from urllib.request import Request, urlopen
#from urllib import parse
#from urllib import request

footwearURL = "https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000"
tracemalloc.start()
#newurl = "https://www.innvictus.com/jordan/c/jordan"+"?"+para
#strt = request.Request(newurl, data)
def botWorking(product, price, model, stat, quant, size, img):
        main = 'https://www.innvictus.com/'
        client = discord.Client()
        bot = commands.Bot(command_prefix='!')
        #my_secret = os.environ['Token']
        #@client.event
        #async def on_command_error(ctx, exc):
        #    if isinstance(exc, CommandNotFound):pass
        #    else:raise exc.original

        #@bot.command(name="shutdown")
        #async def shutdown(Ctx):
        #    if Ctx.author.guild_permissions.administrator:
        #        await Ctx.send('Shutting_down!')
        #        await close()
        #        return

        @client.event
        async def on_ready():
          print('We are activated as {0.user}'.format(client))
          channel = client.get_channel(838131329597177932)

          embed = Embed(title = product, colour=0x3b35c0, timestamp = datetime.utcnow())
          fields = [("Status",stat,True),
                    ("Price",price, True),
                    ("Cart Limit",quant, True),
                    ("Style Code",model, True),
                    ("Sizes & Levels", '['+size+']', False)]
          for name, value, inline in fields:
              embed.add_field(name=name, value=value, inline=inline)
          embed.set_author(name=main)
          embed.set_thumbnail(url=img)
          embed.set_footer(text="By @AnishBangotra")
          await channel.send(embed = embed)
          #await client.close()

        @client.event
        async def on_message(message):
          if message.author ==  client.user:return
          if message.content.startswith('next'):
             await client.logout()

        client.start('ODM4MTMxODY3MDA1ODc4MzIy.YI2pIA.YBpIHYxfvPBUTFAtalTTiHBWAIw')

def fetchData(url, size):
    main = 'https://www.innvictus.com'
    try:
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'lxml')
        title = soup.find('h1')
        product = title.text
        value = soup.find('span', class_="price-int", id="pdpCurrent_wholePart")
        price='$'+str(value.text)
        number = soup.find('p', {'class' : "product-titles__model"})
        model = number.text
        model = model[7:]
        #size_stock = soup.find('a', {'class':'product-size__option'}, onclick="ACC.productDetail.getNewProductSize(this)")
        img = soup.find('img', alt=product)
        img_url = main+str(img.get('src'))
        avail = soup.find_all('a', {'class': "buy-button buy-button--buy-now"})
        quantity=0
        status=''
        if avail:
            status = 'Available'
            quantity = 1
        else:
            status = 'Out of Stock'
            quantity = 0
        return(product, price, model, status, quantity, size, img_url)
    except:pass


def scrape(url):
    main = 'https://www.innvictus.com'
    try:
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml')
        #div = soup.find_all('span', class_="is-gridwallCard__item__name")
        div1 = soup.find_all('a', class_="js-gtm-product-click")
        links=list()
        size=list()
        data=list()
        for i in div1:
                if 'Jordan' and 'Low' in i.get('data-productname'):
                    links.append(i.get('href'))
                    size.append('Low')
                elif 'Jordan' and 'Mid' in i.get('data-productname'):
                    links.append(i.get('href'))
                    size.append('Mid')
                elif 'Jordan' and 'High' in i.get('data-productname'):
                    links.append(i.get('href'))
                    size.append('High')
        q=0
        for i in links:
            final_url = main+i
            product, price, model, status, quantity, size, img_url = fetchData(final_url, size[q])
            data.append([product, price, model, status, quantity, size, img_url])
            print(data)
            q+=1
        return data
    except:return('done')

def fetchPages(url):
    page = 0
    while page <=2:
        scrape(url)
        break
        url = "https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000"
        page+=1
        url = url+'&page='+str(page)
        print('done1')
