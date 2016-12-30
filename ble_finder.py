#!/usr/bin/env python

#----------------------------------------------
# ble_finder.py
#    Authors: Troy Brown (@waveguyd) and Garrett Gee (@ggee)
#    Developed for:
#      http://hackerwarehouse.com / @hackerwarehouse
#      http://hackerwarehouse.tv
#
# requirements:
#   run from blue_hydra directory and rssi file output option enabled
#   tailer module
#
# todo:
#   foxhunting
#   change last seen to dd:hh:mm:ss
#----------------------------------------------

import datetime, os
from time import sleep

import tailer
 
devices = [
['D5:3D:F4:CO:FF:EE', 'Ronalds tile tag', ''],
['CF:19:F8:0F:DE:AD', 'Gerrards tile tag', ''],
['FF:FF:C0:AF:BE:EF', 'Jasons iTAG', ''], 
]

# threshold for reporting in seconds
#seenthreshold = 10
seenthreshold = 45

for line in tailer.follow(open("blue_hydra_rssi.log")):
	for idx, (mac, name, lastseen) in enumerate(devices):
		if mac in line:
			currentseen = float(line.split()[0])
			if lastseen:
				lastseen = float(lastseen)			
				tdelta = datetime.datetime.fromtimestamp(currentseen) - datetime.datetime.fromtimestamp(lastseen)
				tsec = tdelta.total_seconds()
				if tsec >= seenthreshold:
					print name + ' (' + mac + ') is nearby - last seen ' + str(tsec) + ' seconds ago'
#					os.system('aplay ping.wav &')
			else:
				# first time seen
				print name + ' (' + mac + ') is nearby'
#				os.system('aplay ping.wav &')

			# update last seen field with current timestamp
			devices[idx][2] = currentseen
