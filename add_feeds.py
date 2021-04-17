#! /usr/bin/python3
import feedparser
import pymongo
import time
import os
import smtplib
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGO_DB_CONN_STRING'))
db = client.Rss

feeds = [{"link": "https://taz.de/!p4615;rss/", "name": "TAZ | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.faz.net/rss/aktuell/politik/", "name": "FAZ | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.bild.de/rss-feeds/rss-16725492,feed=politik.bild.html", "name": "Bild | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.waz.de/politik/rss", "name": "WAZ | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.welt.de/feeds/section/politik.rss", "name": "Die Welt | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.handelsblatt.com/contentexport/feed/politik", "name": "Handelsblatt | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.nzz.ch/startseite.rss", "name": "NZZ | Startseite", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.derstandard.at/rss", "name": "Der Standard | Startseite", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.tagesschau.de/xml/rss2/", "name": "ARD | Tagesschau", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://rss.dw.com/xml/rss_de_politik", "name": "DW | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://rss.orf.at/news.xml", "name": "ORF", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://www.srf.ch/news/bnf/rss/1922", "name": "SRF | International", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "http://newsfeed.zeit.de/politik/index", "name": "Zeit | Politik", "modified": time.localtime(time.time()), "etag": "" },
  {"link": "https://rss.sueddeutsche.de/rss/Politik", "name": "SZ | Politik", "modified": time.localtime(time.time()), "etag": "" }]

for feed in feeds:
  if db.feeds.find_one({"name": feed["name"]}):
    continue
  else:
    db.feeds.insert_one(feed)
 
