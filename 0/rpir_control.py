#!/usr/bin/python3

import configparser
import time
import sys
import os


import pinger
import database



ip_bp = "192.168.1.202"
ip_afsar = "192.168.1.200"


wait_betw_pingchecks = 0.1
wait_after_pingcheck_closed = 5

##pasword soruyor hala .200 ve .199 da!!!
cmd_start_backup = "sudo sh /home/uad/backup/bp_all.sh"
cmd_shutdown = "sudo shutdown -Pf now"



def temp_machine(cmd):
	os.system("ssh -p37214 -t uad@192.168.1.200 {}".format(cmd))


def servo_off():
	servo_off = "python3 servo.py 40"
	#os.system(servo_off)
	temp_machine(servo_off)  ###ana makineye geçince kalkmali

	


def turn_on():
	#send servo command
	servo_on = "python3 servo.py 10"
	return temp_machine(servo_on)  ###ana makineye geçince kalkmali


def turn_off():
	#send shutdown command
	os.system("ssh -t uad@192.168.1.202 {}".format(cmd_shutdown))
	#wait until shutdown complete
	while(pinger.is_online(ip_bp)):
		time.sleep(wait_betw_pingchecks)
		print("turning off, still online")
	time.sleep(wait_after_pingcheck_closed)
	print("now offline")
	#send servo command
	servo_off()



def start_backup():
	#run remote bp-all.sh
	try:
		os.system("ssh -t uad@192.168.1.202 {}".format(cmd_start_backup))
	except:
		start_backup()

config = configparser.ConfigParser()

period = {
	"week": 604800,
	"day": 86400,
	"month": 2629743,
	"test":15
}

p = "test"

for i in range(100):  #cron ise dongu gereksiz
	time.sleep(1)
	if(database.read("opened") == 1):
		print("It is already turned on w/servo")
		if(database.read("backingup") == 1):
			print("It is backing up")
		else:
			print("It is not backing up")
			if(database.read("firstquery") == 1):
				print("it is intial query")
				print("running start-bp.sh")
				##interactions
				#command
				start_backup()
				#database
				database.write("backingup", 1)
				database.write("firstquery", 0)
				database.write("canclose", 0)
				time.sleep(1)
			else:
				if(database.read("canclose") == 1):
					print("sendin turn off command") ####send shutdown w/ssh
					###interactions
					#command
					turn_off()
					#database
					database.write("opened", 0)
					database.write("firstquery", 1)
					database.write("ip", 0)
					#waits for next backup period
					while((time.time() - float(database.read("runtime"))) < period[p]):
						time.sleep(1)
						print("waiting")

	else:
		print("turning on w/servo")
		#database
		database.write("opened", 1)
		if(pinger.is_online(ip_bp) != 1):
			#command
			turn_on()
			print("sent servo command")
			while(pinger.is_online(ip_bp) != 1): 
				time.sleep(wait_betw_pingchecks)



####bu script rpi-r tarafından supervisorctl/cron ile çalıştırılacak