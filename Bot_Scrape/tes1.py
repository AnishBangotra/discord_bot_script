from bs4 import BeautifulSoup
import requests, discord, time, tracemalloc
from discord import Embed
from datetime import datetime

#from urllib.request import Request, urlopen
#from urllib import parse
#from urllib import request

footwearURL = "https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000"
tracemalloc.start()
#newurl = "https://www.innvictus.com/jordan/c/jordan"+"?"+para
#strt = request.Request(newurl, data)

def fetchData(url):
    main = 'https://www.innvictus.com'
    sizes=["Low", "High", "Mid"]
    size=''
    try:
        link=url
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'lxml')
        title = soup.find('h1')
        product = title.text
        for i in sizes:
            if i in product:
                size=i
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
        #print(product, price, model, status, quantity, size, img_url)
        return(product, price, model, status, quantity, size, img_url, link)
    except:pass


def scrape(url):
        main = 'https://www.innvictus.com'
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml')
        #div = soup.find_all('span', class_="is-gridwallCard__item__name")
        div1 = soup.find_all('a', class_="js-gtm-product-click")
        links=list()
        data=list()
        for i in div1:
                if 'Jordan' and 'Low' in i.get('data-productname'):links.append(i.get('href'))
                elif 'Jordan' and 'Mid' in i.get('data-productname'):links.append(i.get('href'))
                elif 'Jordan' and 'High' in i.get('data-productname'):links.append(i.get('href'))

        for i in links:
            final_url = main+i
            product, price, model, status, quantity, size, img_url, link = fetchData(final_url)
            data.append([product, price, model, status, quantity, size, img_url, link])
        #print(data)
        return data

def fetchPages(url):
    page = 0
    result = list()
    while page <=2:
        data = scrape(url)
        result+=data
        print('nextPage')
        url = "https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000"
        page+=1
        url = url+'&page='+str(page)
        #result += data
        #print(result)
    return result
#print(fetchPages("https://www.innvictus.com/jordan/c/jordan?q=%3Arelevance%3Atype%3A100010000000000000"))
