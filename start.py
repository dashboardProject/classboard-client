#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, json
import random, string
import os
import subprocess
import time

default = {"end": "20:00", "dKey": None, "start": "08:00"}
def makeDeviceKey():
    pool = string.uppercase + string.digits
    return ''.join(random.choice(pool) for i in xrange(12))

if __name__ == "__main__":
    PATH = "/home/pi/classboard/config.txt"
    classBoardUrl = "http://www.classboard.co.kr/d/"
    networkErrUrl = "file:///home/pi/classboard/html/ClassBoard.html"

    #if os.path.isfile(PATH):
    try:
        config = open(PATH, "r")
        data = json.load(config)

        deviceKey = data["dKey"]
        
    #else:
    except:
        deviceKey = makeDeviceKey()

        default['dKey'] = deviceKey

        with open(PATH, 'w') as f:
            json.dump(default, f)


    clientUrl = classBoardUrl + deviceKey    

    errFlag=False
    while(True):
        try:
            data = urllib.urlopen(clientUrl + "/info").read()
            t = json.loads(data)
            if errFlag:
                os.system('killall chromium-browser')
            break
        except:
            if not errFlag:
                os.system('chromium-browser --noerrdialogs --disable-session-crashed-bubble --disable-infobars --kiosk '+networkErrUrl+' &')
                errFlag=True
            time.sleep(3)
            continue
        
    config = open(PATH, "w")
    config.write(data)
    config.close()
    os.system('chromium-browser --disable-session-crashed-bubble --disable-infobars --noerrdialogs --kiosk '+clientUrl+' &')

