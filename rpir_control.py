#!/usr/bin/python3

import configparser
import time
import sys
import os


import pinger
import database


ip_test_on = "127.0.0.1"
ip_bp = "192.168.1.202"
ip_afsar = "192.168.1.200"

wait_betw_pingchecks = 0.1
wait_after_pingcheck_done = 3

servo_on_angle = 10
servo_off_angle = 40

##pasword soruyor hala .200 ve .199 da!!! ssh read permissonlar! 
cmd_start_backup = "sudo sh /home/uad/backup/bp_all.sh"
cmd_shutdown = "sudo shutdown -Pf now"



def temp_machine(cmd):
	os.system("ssh -p37214 -t uad@192.168.1.200 {}".format(cmd))


def turn_on():
	#send servo command
	
	return temp_machine(servo_on)  ###ana makineye geçince kalkmali

def turn_on_test():
	try:
		print("Şu komutu göndererek servo ile rpi açıyorum:")
		database.write("servoangle", servo_on_angle)
		servo_on = "python3 servo.py 10"
		print("ssh -p37214 -t uad@192.168.1.200 {}".format(servo_on))
	except:
		print("turn_on_test() failed!")

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


def start_backup_test():
	print("starting backup with command below")
	print("ssh -t uad@192.168.1.202 {}".format(cmd_start_backup))

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

#for i in range(100):  #cron ise dongu gereksiz
while(database.read("onoff") == 0):
	turn_on_test()
	while(pinger.is_online(ip_test_on) != True):
		time.sleep(wait_betw_pingchecks)
		print("henüz offline")
	print("online oldu!")
	time.sleep(wait_after_pingcheck_done)
	start_backup_test()




while(database.read("onoff") == 0):
	print("ok 0")


####bu script rpi-r tarafından supervisorctl/cron ile çalıştırılacak