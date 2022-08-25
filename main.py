#!/usr/bin/python
# -*- coding:utf8 -*-
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

#today = datetime.now ()
today = datetime.now ().strftime ( '%Y-%m-%d-%H:%M' )
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday_gril = os.environ['BIRTHDAY_GRIL']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get ( url ).json ()
    weather = res[ 'data' ][ 'list' ][ 0 ]
    return weather[ 'city' ], weather[ 'weather' ], math.floor ( weather[ 'low' ] ), math.floor ( weather[ 'high' ] ), \
           weather[
               'airQuality' ], math.floor (
        weather[ 'temp' ] )


def get_count():
    delta = today - datetime.strptime ( start_date, "%Y-%m-%d" )
    return delta.days


def get_birthday(birthday):
    next = datetime.strptime ( str ( date.today ().year ) + "-" + birthday, "%Y-%m-%d" )
    if next < datetime.now ():
        next = next.replace ( year=next.year + 1 )
    return (next - today).days


def get_words():
    words = requests.get ( "https://api.shadiao.pro/chp" )
    if words.status_code != 200:
        return get_words ()
    return words.json ()[ 'data' ][ 'text' ]


def get_random_color():
    return "#%06x"%random.randint ( 0, 0xFFFFFF )


client = WeChatClient ( app_id, app_secret )

wm = WeChatMessage ( client )
city, wea, low, high, airQuality, temperature = get_weather ()
data = {"data": {"value": today.strftime ( '%Y-%m-%d' ), "color": get_random_color ()},
        "city": {"value": city, "color": get_random_color ()},
        "weather": {"value": wea, "color": get_random_color ()},
        "low": {"value": low, "color": get_random_color ()},
        "high": {"value": high, "color": get_random_color ()},
        "air": {"value": airQuality, "color": get_random_color ()},
        "temperature": {"value": temperature, "color": get_random_color ()},
        "love_days": {"value": get_count (), "color": get_random_color ()},
        "birthday_gril": {"value": get_birthday ( birthday_gril ), "color": get_random_color ()},
        "words": {"value": get_words (), "color": get_random_color ()}}
res = wm.send_template ( user_id, template_id, data )
print ( res )

'''
{{data.DATA}}
城市：{{city.DATA}}
今日天气：{{weather.DATA}}
当前温度：{{temperature.DATA}}
最高气温：{{high.DATA}}
最低气温：{{low.DATA}}
空气质量：{{air.DATA}}
距离生日还有{{birthday_gril.DATA}}天
{{words.DATA}}
为你推送了{{love_days.DATA}}天
'''
