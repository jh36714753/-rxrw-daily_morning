from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

n_lines = 20

def get_weather():
  url = "https://api.seniverse.com/v3/weather/daily.json?key=ShIAlpiD-3tTqm7zD&location=beijing&language=zh-Hans&unit=c&start=0&days=5"
  r = requests.get(url, params=params)

  data = r.json()["results"]
  
  date = data[0]['daily'][0]['date']
  text_day = data[0]['daily'][0]['text_day']
  text_night = data[0]['daily'][0]['text_night']
  high = data[0]['daily'][0]['high']
  low = data[0]['daily'][0]['low']

  return date, text_day, text_night, high, low

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return (delta.days + 1)

def get_birthday():
  next = datetime.strptime(str(datetime.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return ((next - today).days - 1)

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def read_law_quotes(n_lines_):
    n = random.randint(0, n_lines_)
    
    file = open('law_quotes.txt', 'r')
    law_quotes = file.readlines()  # 读取所有行
    #print(law_quotes[n])
    file.close()
    
    file = open('law_quotes_authors.txt', 'r')
    law_quotes_authors = file.readlines() 
    #print(law_quotes_authors[n])
    file.close()
    
    return law_quotes[n], law_quotes_authors[n]

client = WeChatClient(app_id, app_secret)

params = {
    "key": "ShIAlpiD-3tTqm7zD",
}

wm = WeChatMessage(client)
date, text_day, text_night, high, low = get_weather()
law_quote, law_quote_author = read_law_quotes(n_lines)
data = {"date":{"value":date},
        "text_day":{"value":text_day},
        "text_night":{"value":text_night},
        "high":{"value":high},
        "low":{"value":low}, 
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday()}, 
        "words":{"value":get_words(), "color":get_random_color()},
        "law_quote":{"value":law_quote},
        "law_quote_author":{"value":law_quote_author}}

res = wm.send_template(user_id, template_id, data)

print(res)
