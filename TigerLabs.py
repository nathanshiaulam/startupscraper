#!/usr/local/bin/python
import urllib
import json
import datetime
import ast
import time
import smtplib
from pymongo import MongoClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def get_pages(s):
    base_url = "http://api.crunchbase.com/v/1/search.js?query="
    api_key = "&api_key=brw59htzc8w4bgpxd9byc3qd"
    query_url = base_url + s + api_key
    tiggerCrunch = urllib.urlopen(query_url)
    htmlSourceCrunch = tiggerCrunch.read()
    htmlSourceDict = json.loads(htmlSourceCrunch)
    numPages = htmlSourceDict["total"]
    return int(numPages) / 10

def get_startups_on_page(s, i):
   base = "http://api.crunchbase.com/v/1/search.js?query="
   api = "&api_key=brw59htzc8w4bgpxd9byc3qd&page=" + str(i) == Integer.to
   query = base + s + api
   open_url = urllib.urlopen(query)
   startups_on_page = open_url.read()
   open_url.close
   return startups_on_page

def get_angelsid_on_page(s):
   query_id = "https://api.angel.co/1/search?query="+s+"&type=MarketTag"
   open_url = urllib.urlopen(query_id)
   market_query = open_url.read()
   market_dict = json.loads(market_query)
   market_list = market_dict[0]
   _id = market_list.get('id')e
   return _id

def get_startup_by_angelid(i):
   query_id = "https://api.angel.co/1/tags/"+i+"/startups"
   open_url = urllib.urlopen(query_id)
   startups_query = open_url.read()
   startups_dict = json.loads(startups_query)
   startups_list = startups_dict.get('startups')
   return startups_list
 
def find_data(): 
   client = MongoClient('localhost', 27017)
   db = client.tiger_labs
   collection = db.new_startups
   existing_names = []
   for startup in collection.find():
      existing_names.append(startup.get('name'))

   market_tags = ["mobile health", "health care", "health care information technology", "health and wellness", "personal health"]
   ids = []
   text = "<html>"
   for tag in market_tags:
       ids.append(get_angelsid_on_page(tag))
   for _id in ids:
       list_of_startups = get_startup_by_angelid(str(_id))
       for startup in list(list_of_startups):
          if startup.get('name') not in existing_names:
              select_information = {}
              text += "<b>" + "Name: " + "</b>" + startup.get('name').encode('utf-8') + "<br />" + "<br />"
              if startup.get('product_desc') is not None:
                  text += "<b>" + "Description: " + "</b>" + startup.get('product_desc').encode('utf-8') + "<br />" + "<br />"
              else:
                  text += "<b>" + "Description: " + "</b>" + "None." + "<br />" + "<br />"
              text += "<b>" + "Location: " + "</b>" + str(startup.get('locations')) + "<br />" + "<br />"
              text += "<b>" + "Creation Time: " + "</b>" + str(startup.get('created_at')) + "<br />" + "<br />"
              text += "<b>" + "Company URL: " + "</b>" + str(startup.get('company_url')) + "<br />" + "<br />"
              text += "<b>" + "Anglist URL: " + "</b>" + str(startup.get('angellist_url')) + "<br />" + "<br />"
              text += "<br />" + "<br />" + "<br />" + "<br />"

              collection.insert(startup)
              existing_names.append(startup.get('name'))
              print "THIS IS A NEW ANGELLIST STARTUP: " + startup.get('name').encode('utf-8')

   text += "</html>"
   if text != "<html></html>":
       nathan = "testerisgood@gmail.com"
       tigerlabs = "james@tigerlabs.co, bert@tigerlabs.co"
       msg = MIMEMultipart('alternative')
       msg['Subject'] = "New Startups"
       msg['From'] = nathan
       msg['To'] = tigerlabs
       part1 = MIMEText(text, 'html')
       msg.attach(part1)
       server = smtplib.SMTP('smtp.gmail.com:587')  
       server.starttls()  
       server.login("testerisgood@gmail.com", "testingisgood")
       server.sendmail(nathan, tigerlabs, msg.as_string())
       server.quit()
       print "sent"
   else:
       server = smtplib.SMTP('smtp.gmail.com:587')  
       server.starttls()  
       server.login("testerisgood@gmail.com", "testingisgood")
       server.sendmail("testerisgood@gmail.com", "nlam@princeton.edu", "Hi it worked.")
       server.quit()
       print "not_sent"

find_data()

