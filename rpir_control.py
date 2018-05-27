#!/usr/bin/python3

import configparser
import time
import sys
import os

import pinger
import database
import process_checker

###database folder need to be in flash disk to avoid sdcard corruptions


###This script should run on home server
#rpi-r

## 1)shutdown without root pass -> sudo chmod u+s /sbin/shutdown



####initiation of db for test purposes####
database.write("onoff", "0")
database.write("backingup", "0")
##################need to be erased for reallife execution


#period between two backup sessions
######################################################
bp_p = "test"
######################################################


#ip addresses to check whether machines are online/offline
######################################################
ip_test_on = "192.168.1.199"
ip_bp = "192.168.1.202"
ip_afsar = "192.168.1.200"
######################################################


#wait periods for ping controls
######################################################
wait_betw_pingchecks = 1
wait_after_pingcheck_done = 5
######################################################


#obvious as in var name
######################################################
servo_on_angle = 10
servo_off_angle = 60
######################################################

 
#obvious as in var name
######################################################
cmd_run_backup = "ssh uad@192.168.1.202 'sh /home/uad/backup/bp_all.sh'"
cmd_shutdown = "ssh uad@192.168.1.202 'shutdown -h now'"
cmd_turn_on = "/usr/bin/python3 /home/uad/autobackup/servo_button.py"
test_run = "test_proc.sh"
######################################################





def turn_on():
	try:
		print("AUTOBACKUP: {}".format(cmd_turn_on))
		os.system(cmd_turn_on)
	except:
		print("turn_on() failed!")

def turn_off():
	#send shutdown command
	print("AUTOBACKUP: shutting rpiw down")
	os.system("ssh uad@192.168.1.202 {}".format(cmd_shutdown))
	#wait until shutdown complete
	while(pinger.is_online(ip_bp)):
		time.sleep(wait_betw_pingchecks)
		print("AUTOBACKUP: waiting for shutdown")
	time.sleep(wait_after_pingcheck_done)
	print("AUTOBACKUP: now offline")


n = 1
def start_backup():
	try:
		#sending backup command
		print("AUTOBACKUP: running backup")
		if(bp_p == "test"):
			print("AUTOBACKUP: (test run)")
			os.system("sh {}/{}".format(os.getcwd(),test_run))
		elif(bp_p == "production"):
			os.system(cmd_run_backup)
	except:
		if(n < 5):
			print("AUTOBACKUP: failed trying again")
			start_backup()
			n = n+1
		else:
			print("AUTOBACKUP: start_backup() failed exiting")
			sys.exit()



def process_check(proc_data):
	try:
		cmd = """ps auxw | grep {} | grep -v grep > /dev/null
		if [ $? = 0 ]
		then
		        echo "alive"
		else
	        echo "dead"
		fi""".format(proc_data)
		status = subprocess.check_output(cmd, shell=True)
		return status.decode("utf-8").strip("\n")
	except:
		print("process_status_test() failed")





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
		turn_on()
		print("2")
		#checking whether remote machine is turned on
		while(pinger.is_online(ip_bp) != True):
			time.sleep(wait_betw_pingchecks)
			print("still offline")
		print("online!")
		print("3")
		time.sleep(wait_after_pingcheck_done)
		print("4")
		print("5")
		start_backup()
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
			while(process_check() == "alive"):
				time.sleep(1)
			print("11")
			database.write("backingup", "0")
		print("12")
		turn_off()	
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


