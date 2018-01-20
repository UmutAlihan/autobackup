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


def turn_on():
	#send servo command
	servo_on = "python3 servo.py 10"
	return temp_machine(servo_on)  ###ana makineye geçince kalkmali


def turn_off():
	#send shutdown command
	#os.system("ssh -t uad@192.168.1.202 {}".format(cmd_shutdown))
	temp_machine(cmd_shutdown)
	#wait until shutdown complete
	while(pinger.is_online(ip_bp)):
		time.sleep(wait_betw_pingchecks)
		print("turning off, still online")
	time.sleep(wait_after_pingcheck_closed)
	print("now offline")
	#send servo command
	servo_off = "python3 servo.py 40"
	temp_machine(servo_off)  ###ana makineye geçince kalkmali



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



####bu script rpi-r tarafından supervisorctl/cron ile çalıştırılacak