#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, urllib
import os, random, string
from datetime import datetime

def makeDeviceKey():
    pool = string.uppercase + string.digits
    return ''.join(random.choice(pool) for i in xrange(12))

def isDiff(data1, data2):
    try:
        if (data1["status"] != data2["status"] or
            data1["end"] != data2["end"] or
            data1["dName"] != data2["dName"] or
            data1["dKey"] != data2["dKey"] or
            data1["gCalID"] != data2["gCalID"] or
            data1["start"] != data2["start"]):
            return 1
        else:
            return 0
    except:
        return 0

if __name__ == "__main__":
    PATH = "/home/pi/classboard/config.txt"
    classBoardUrl = "http://www.classboard.co.kr/d/"
    confData = None
    
    if os.path.isfile(PATH):
        config = open(PATH, "r")
        confData = json.load(config)
        dKey = confData["dKey"]
    else:
        dKey = makeDeviceKey()

    clientUrl = classBoardUrl + dKey

    print clientUrl
    try:
        urlData = urllib.urlopen(clientUrl + "/info").read()

        clientData = json.loads(urlData)

        
        if isDiff(confData, clientData):
            config = open(PATH, "w")
            config.write(urlData)
            confData = clientData

        os.system('xdotool key F5')
    except:
        print "Error"


    
    now = datetime.now().strftime('%H:%M')
    
    try:
        if confData['status']:
            start = confData['start']
            end = confData['end']
            if start!=None and end!=None:
                if now < end:
                    if start < now and now < end:
                        os.system('vcgencmd display_power 1')
                    else:
                        os.system('vcgencmd display_power 0')
                else:
                    if now < end and start < now:
                        os.system('vcgencmd display_power 1')
                    else:
                        os.system('vcgencmd display_power 0')
    except:
        os.system('vcgencmd display_power 1')
        
