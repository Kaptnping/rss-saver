#! /usr/bin/python3
import feedparser
import pymongo
import time
import os
import json
import smtplib
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGO_DB_CONN_STRING'))
db = client.Rss

feeds = json.loads("feeds.json")
for feed in feeds["feeds"]:
  if db.feeds.find_one({"name": feed["name"]}):
      continue
    else:
      db.feeds.insert_one(feed)
 
