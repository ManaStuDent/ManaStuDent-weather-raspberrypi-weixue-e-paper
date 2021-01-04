#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import requests
import json
import time

logging.basicConfig(level=logging.DEBUG)

try:
    
    
    logging.info("start flush weather %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))) 

    request = requests.get(
            "https://devapi.qweather.com/v7/weather/3d?location=101190201&key=00090117a3a34c2c9b1f63539cd05176")
    dataJson = json.loads(request.text)

    today = dataJson.get('daily')[0]
    tomorrow = dataJson.get('daily')[1]
    dayOfTomorrow = dataJson.get('daily')[2]

    textDay = today.get('textDay')
    fxDate = today.get('fxDate')
    moonPhase = today.get('moonPhase')
    iconDay = today.get('iconDay')
    tempMin = today.get('tempMin')
    tempMax = today.get('tempMax')

    tIconDay = tomorrow.get('iconDay')
    tTempMin = tomorrow.get('tempMin')
    tTempMax = tomorrow.get('tempMax')

    dIconDay = dayOfTomorrow.get('iconDay')
    dTempMin = dayOfTomorrow.get('tempMin')
    dTempMax = dayOfTomorrow.get('tempMax')

    logging.info("today weather is %s %s - %s" % (textDay, tempMin, tempMax))
    

    # Drawing on the image
    font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font29 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 29)
    
    logging.info("epd2in13_V2 Demo")
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
   
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    # 边框
    draw.line([(0,0),(250,0)], fill = 0,width = 2)
    draw.line([(0,120),(250,120)], fill = 0,width = 2)

    draw.line([(0,0),(0,120)], fill = 0,width = 2)
    draw.line([(248,0),(248,120)], fill = 0,width = 2)

    # 左下角刷新时间
    draw.text((2, 110), time.strftime("%H", time.localtime()) , font=font10, fill=0)

    draw.text((5, 5), '%s  %s' % (fxDate, moonPhase), font=font15, fill=0)
    bmp = Image.open('weather_icon/%s.jpg' % iconDay)
    image.paste(bmp, (2, 32))
    if len(textDay) == 1:
        draw.text((74, 45), textDay, font=font29, fill=0)
    elif len(textDay) < 3:
        draw.text((64, 45), textDay, font=font29, fill=0)
    elif len(textDay) < 5:
        draw.text((67, 40), '%s\n%s' % (textDay[:2], textDay[2:]), font=font20, fill=0)
    elif len(textDay) < 9:
        draw.text((64, 45), '%s\n%s' % (textDay[:4], textDay[4:]), font=font15, fill=0)
    draw.text((10, 90), '%3s - %2s°C' % (tempMin, tempMax), font=font24, fill=0)
    # 右上方 天气图标
    bmp2 = Image.open('weather_icon/%s.jpg' % tIconDay)
    image.paste(bmp2, (132, 2))
    # 右上方 最低温度 最高温度
    draw.text((191, 0), '%3s°C' % tTempMin, font=font24, fill=0)
    draw.text((191, 30), '%3s°C' % tTempMax, font=font24, fill=0)
    # 右下方 天气图标
    bmp3 = Image.open('weather_icon/%s.jpg' % dIconDay)
    image.paste(bmp3, (132, 56))
    # 右下方 最低温度 最高温度
    draw.text((191, 62), '%3s°C' % dTempMin, font=font24, fill=0)
    draw.text((191, 91), '%3s°C' % dTempMax, font=font24, fill=0)
    
    
    epd.display(epd.getbuffer(image))
    
    time.sleep(3)
    epd.Dev_exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()

