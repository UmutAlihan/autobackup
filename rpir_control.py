#!/usr/bin/python3

import configparser
import time
import sys
import os

import pinger
import database
import process_checker

###database folder need to be in flash disk to avoid sdcard corruptions


####initiation of db for test purposes####
database.write("onoff", "0")
database.write("backingup", "0")
##################need to be erased for reallife execution


#period between two backup sessions
nextbp_p = "test"



#ip addresses to check whether machines are online/offline
#wait periods for ping controls
ip_test_on = "192.168.1.207"
ip_bp = "192.168.1.202"
ip_afsar = "192.168.1.200"
wait_betw_pingchecks = 0.1
wait_after_pingcheck_done = 5




#obvious as in var name
####need constantly sending signal by another script for failed voltages disruptions
servo_on_angle = 10
servo_off_angle = 60


##pasword soruyor hala .200 ve .199 da!!! ssh read permissonlar! 
#obvious as in var name
cmd_start_backup = "ssh uad@192.168.1.202 'sh /home/uad/backup/bp_all.sh'"
cmd_shutdown = "ssh uad@192.168.1.202 'shutdown -Pf now'"






def turn_on_test():
	try:
		print("Şu komutu göndererek servo ile rpi açıyorum:")
		database.write("servoangle", servo_on_angle)
		servo_on = "python3 servo.py 10"
		print(servo_on)
	except:
		print("turn_on_test() failed!")

def turn_off_test():
	print("sending shut down command:")
	print("ssh uad@192.168.1.202 {}".format(cmd_shutdown))
	while(pinger.is_online(ip_test_on) == True):
		time.sleep(wait_betw_pingchecks)
		print("turning off, still online")
	print("now offline")
	time.sleep(wait_after_pingcheck_done)
	print("sending command:")
	print("python3 servo.py 40")

def start_backup_test():
	try:
		print("starting backup with command below")
		print("ssh uad@192.168.1.202 {}".format(cmd_start_backup))
		cmd = "sh {}/test_proc.sh".format(os.getcwd()) ###buraya backup commandi gelmeli
		os.system(cmd)
	except:
		print("start_backup_test() failed")

def process_status_test():
	try:
		return process_checker.check("proc_backup")  ###process ismini güncelle!
	except:
		print("process_status_test() failed")





def turn_off():
	#send shutdown command
	#os.system("ssh -t uad@192.168.1.202 {}".format(cmd_shutdown))
	#temp_machine(cmd_shutdown)
	#wait until shutdown complete
	while(pinger.is_online(ip_bp)):
		time.sleep(wait_betw_pingchecks)
		print("turning off, still online")
	time.sleep(wait_after_pingcheck_done)
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
	"test":5
}



for i in range(100):  #cron ise dongu gereksiz #supervisorctl ile kontrol edilecek!
	while(database.read("onoff") == 0):
		print("1")
		turn_on_test()
		print("2")
		#checking whether remote machine is turned on
		while(pinger.is_online(ip_test_on) != True):
			time.sleep(wait_betw_pingchecks)
			print("still offline")
		print("online!")
		print("3")
		time.sleep(wait_after_pingcheck_done)
		print("4")
		print("5")
		start_backup_test()
		print("6")
		database.write("backingup", "1")
		database.write("onoff", "1")
		print("7")
	#
	while(database.read("onoff") == 1):
		print("8")
		while(database.read("backingup") == 1):
			print("9")
			#checking whether the backup process is still alive
			# proc_status = process_status_test()
			print("10")
			while(process_status_test() == "alive"):
				time.sleep(1)
			print("11")
			database.write("backingup", "0")
		print("12")
		turn_off_test()	
		print("13")
		database.write("onoff","0")
		print("14")
	#entering the unixtime of current backup period
	database.write("runtime", time.time())
	while((time.time() - database.read("runtime")) < period[nextbp_p]):
		print("waiting for next backup period")
		time.sleep(1)
	print("final 15 congrats")

####bu script rpi-r tarafından supervisorctl/cron ile çalıştırılacak


