# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-


import requests
import urllib2
import json
import base64
import time
import subprocess
import tempfile
from datetime import datetime


u_a = {'User-Agent':'Mozilla/5.0'}


def speech_synthesis(out_f="hoge.wav", s="ゆっくりしていってね"):
    json_data = { "method":"speak", "params":["1.1", {"language":"ja","text":s, "voiceType":"*","audioType":"audio/x-wav"}]}
    
    url = 'http://rospeex.ucri.jgn-x.jp/nauth_json/jsServices/VoiceTraSS'
    res = requests.post(url, data=json.dumps(json_data))
    response = json.loads(res.text)
    tmp = response['result']['audio']
    speech = base64.decodestring(tmp.encode('utf-8'))

    with open(out_f, 'wb') as wav: wav.write(speech)
    args = ['aplay']
    args.append(out_f)
    p = subprocess.call(args)
    print "Success!!" if p==0 else "Fail..."


if __name__ == "__main__":
    URL = 'http://api.openweathermap.org/data/2.5/weather?q=Kyoto,jp'
    weather_data = requests.post(URL, headers=u_a).json()

    weather = weather_data['weather'][0]['main']
    clouds = weather_data['clouds']['all']

    temp = weather_data['main']['temp'] - 273.15
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']

    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset'])

    contents = "只今の気温は{0}です. 湿度は{1}%,気圧は{2}で,雲の量は{3}%です.".format(temp, humidity, pressure, clouds)
    sunrise = "{0}年{1}月{2}日の 日の出は{3}時{4}分です.".format(sunrise.year, sunrise.month, sunrise.day, sunrise.hour, sunrise.minute)
    sunset = "日没は{0}時{1}分です.".format(sunset.hour, sunset.minute)
    contents += sunrise+sunset

    speech_synthesis(s=contents)


def speech_recognition(in_f="hoge.wav"):
    URL ='http://rospeex.ucri.jgn-x.jp/nauth_json/jsServices/VoiceTraSR' 
    with open(in_f, 'rb') as rf: wav = rf.read()
    buf = base64.b64encode(wav)
    json_data = { "method":"recognize",
                  "params":( "ja",
                             {"audio":buf, "audioType":"audio/x-wav", "voiceType":"*" } ) }
    response = requests.post(URL, data=json.dumps(json_data))
    json_data = json.loads(response.text)
    return json_data['result'].encode('utf-8')


