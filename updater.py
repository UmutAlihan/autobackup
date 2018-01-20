#!/usr/bin/python3


import configparser
import time



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


### ssh ile ulaşıp öyle bu komutları çalıştırmalı! rpir'de buna özel script olsn
write("backingup", 0)
write("canclose", 1)
write("runtime", time.time())


#####Bu script rpi-backup bash tarafından, backuplar tamamlanınca çalıştırılacak

####root user ssh keys!
###start bp_all.sh
### if psaux backup script bitti -> canclose!
