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

feeds = db.feeds.find()
count = 0

for feed in feeds:
  response = feedparser.parse(feed["link"], etag=feed["etag"], modified=feed["modified"])
  etag = response.get('etag', '')
  modified = response.get('modified_parsed', '')
  db.feeds.update_one({"name": feed["name"]}, {"$set": {"etag": etag, "modified": modified}})
  for entry in response.entries:
    mydict = {}
    try:
      mydict["title"] = entry.title
    except:
      continue
    mydict["summary"] = BeautifulSoup(entry.get("summary", ''), "html.parser").get_text()
    mydict["date"] = entry.get("published", time.localtime(time.time()))
    mydict["link"] = entry.get("link", '')
    mydict["source"] = feed["name"]
    if db.entries.find_one({"title": mydict["title"]}):
      continue
    else:
      db.entries.insert_one(mydict)
      count += 1

server = smtplib.SMTP_SSL("mail.cdtm.de", 465)
server.login(os.getenv('CDTM_E_MAIL'), os.getenv('CDTM_PW'))
ms = f"""From: {os.getenv('CDTM_E_MAIL')}
To: felderer.and@gmail.com
Subject: RSS

Added {count} Feed entries to DB
Feed entry's size is {round(db.command("collstats", "entries")["size"]/1000000, 3)} MB"""

server.sendmail(os.getenv('CDTM_E_MAIL'), "felderer.and@gmail.com", ms)
