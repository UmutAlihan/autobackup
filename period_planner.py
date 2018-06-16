#!/usr/bin/python3

import configparser
import time
import sys
#import database


def read(data):
	config.read("./config.ini")
	state_data = config.get("database",data)
	return float(state_data)

def write(data, new_state):
	config.read("./config.ini")
	config["database"][data] = str(new_state)
	print(data,new_state)
	with open("./config.ini", "w+") as conf_file:
		config.write(conf_file)

config = configparser.ConfigParser()

week = 604800
day = 86400
month = 2629743
test = 10

period = test

if((time.time() - read("runtime")) > test):
	print("time to turn on")
else:
	print("time to wait")

	#wrte("runbool", 0)
#else 
	#pass