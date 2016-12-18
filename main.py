# -*- coding: utf-8 -*-
import urllib, json
import random, string
import os, commands

def makeDeviceKey():
	pool = string.uppercase + string.digits
	return ''.join(random.choice(pool) for i in xrange(12))

if __name__ == "__main__":
	PATH = "/home/pi/classboard/config.txt"
	classBoardUrl = "http://www.classboard.co.kr/d/"
	
	if os.path.isfile(PATH):
		config = open(PATH, "r")
		data = json.load(config)
		clientUrl = classBoardUrl + data["dkey"]

	else:
		deviceKey = makeDeviceKey()
		
		clientUrl = classBoardUrl + deviceKey
		data = urllib.urlopen(clientUrl + "/info").read()

		config = open(PATH, "w");
		config.write(data)

