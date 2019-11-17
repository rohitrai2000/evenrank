import csv
import requests
import json
from bs4 import BeautifulSoup as soup

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

def removeBackslashn(s):
    s = removeNonAscii(s) 
    return s.replace('\n','')

def getData(link):
    newLink = BASEURL + link
    sp = soup(requests.get(newLink).text, "lxml")
    title = sp.find("h1")
    rating = sp.find("span", itemprop="ratingValue")
    releaseDate = sp.find("a", title="See more release dates")
    summaryText = sp.findAll("div", class_="credit_summary_item")
    poster = sp.find("div", class_="poster")
    directors = []
    stars = []
    writers = []

    for item in summaryText:
        if(item.h4.text == "Director:" or item.h4.text == "Directors:"):
            alla = item.findAll("a")
            for i,a in enumerate(alla):
                directors.append(removeBackslashn(a.text))
        
        if(item.h4.text=="Writers:" or item.h4.text=="Writer:"):
            alla = item.findAll("a")
            for i,a in enumerate(alla):
                if(not ("more credit" in a.text or "more credits" in a.text)):
                    writers.append(removeBackslashn(a.text))

        if(item.h4.text=="Stars:" or item.h4.text=="Star:"):
            alla = item.findAll("a")
            for i,a in enumerate(alla):
                if(a.text != "See full cast & crew"):
                    stars.append(removeBackslashn(a.text))

    listItem = {
        "name" : removeBackslashn((title.text)),
        "directors" : (directors),
        "stars" : (stars),
        "writers" : (writers),
        "rating" : removeBackslashn(rating.text),
        "relase_date": removeBackslashn(releaseDate.text),
        "imageLink": poster.a.img['src']
    }

    print(listItem)
    lista.append(listItem)
    #print(director.text)

def scrape(link):
    processes = []
    sp = soup(requests.get(link).text, "lxml")
    allTds = sp.findAll("td",class_="titleColumn")
    for td in allTds:
        getData(td.a['href'])
    print(lista)
    json.dump(lista, open("out.json", "w"))


BASEURL = "https://www.imdb.com"
lista = []
scrape("https://www.imdb.com/chart/top?ref_=nv_mv_250")

