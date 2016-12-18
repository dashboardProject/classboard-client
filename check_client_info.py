# -*- coding: utf-8 -*-
import json, urllib
import os, random, string

def makeDeviceKey():
	pool = string.uppercase + string.digits
	return ''.join(random.choice(pool) for i in xrange(12))

def isDiff(data1, data2):
	if (data1["status"] != data2["status"] or
		data1["end"] != data2["end"] or
		data1["dname"] != data2["dname"] or
		data1["dkey"] != data2["dkey"] or
		data1["gCalID"] != data2["gCalID"] or
		data1["start"] != data2["start"]):
		return 1
	else:
		return 0

if __name__ == "__main__":
	PATH = "/home/pi/classboard/config.txt"
	classBoardUrl = "http://www.classboard.co.kr/d/"
	
	if os.path.isfile(PATH):
		config = open(PATH)
		data = json.load(config)

		try:
			clientUrl = classBoardUrl + data["dkey"]
			urlData = urllib.urlopen(clientUrl + "/info").read()
			clientData = json.loads(urlData)

			if isDiff(data, clientData):
				config = open(PATH, "w")
				config.write(urlData)
		except:
			print "Network Error"


	else:
		dKey = makeDeviceKey()

		try:
			clientUrl = classBoardUrl + dKey
			urlData = urllib.urlopen(clientUrl + "/info").read()
			clientData = json.loads(urlData)

			config = open(PATH, "w")
			config.write(urlData)
		except:
			print "Network Error"
