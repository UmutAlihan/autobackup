#!/usr/bin/python3

import configparser
import time
import sys
import subprocess
import inspect
import os

import pinger
import database
import process_checker



###TODO:
#database folder need to be in flash disk to avoid sdcard corruptions


###This script should run on home server
#rpi-r

## 1)shutdown without root pass -> sudo chmod u+s /sbin/shutdown


#some vars
######################################################
config = configparser.ConfigParser()
runtime_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
######################################################


#period related variables
######################################################
next_backup_period = "test"
if(next_backup_period == "test"): sleep_time = 1
else: sleep_time = 10
period = {
	"week": 604800,
	"day": 86400,
	"month": 2629743,
	"test":5
}
######################################################


#ip addresses to check whether machines are online/offline
######################################################
test_ip_state_on = "192.168.1.199"
ip_backup = "192.168.1.202"
ip_afsar = "192.168.1.200"
check_my_ip = "ifconfig"
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
cmd_run_backup = "ssh uad@{} 'sh /home/uad/backup/bp_all.sh'".format(ip_backup)
cmd_shutdown = "ssh uad@{} 'shutdown -h now'".format(ip_backup)
cmd_turn_on = "/usr/bin/python3 {}/servo_button.py".format(runtime_path)
run_test_proc = "test_proc.sh"
######################################################





#functions
######################################################
def turn_on():
	#Description: controls gpio-servo to physcially turn on backup machine
	#Input: -
	#Output: physical servo movement, turn on
	try:

		print("AUTOBACKUP: {}".format(cmd_turn_on))
		os.system(cmd_turn_on)
	except Exception as e:
		print("AUTOBACKUP: turn_on() failed! -> {}".format(e))



def turn_off():
	#Description: sends shutdown shell command to turn of backup machine
	#Input: -
	#Output: shell command, shutdown
	os.system(cmd_shutdown)
	#wait until shutdown complete
	while(pinger.is_online(ip_backup)):
		time.sleep(wait_betw_pingchecks)
		print("AUTOBACKUP: waiting for shutdown")
	time.sleep(wait_after_pingcheck_done)
	print("AUTOBACKUP: now offline")



def start_backup(n):
	time.sleep(0.1)
	#Description: sends backup shell command or runs test proccess
	#Input: retry count
	#Output: shel command, test_proc.sh or bp_all.sh
	try:
		#send backup command
		if(next_backup_period == "test"):
			print("AUTOBACKUP: running backup, test run (test_proc.sh)")
			os.system("sh {}/{}".format(runtime_path, run_test_proc))
		elif(bp_p == "production"):
			print("AUTOBACKUP: running bp_all.sh ")
			os.system(cmd_run_backup)
	except Exception as e:
		n -= 1
		if(n > 0):
			print("AUTOBACKUP: start_backup() failed, trying again")
			start_backup(n)
		print("AUTOBACKUP: startup_backup() failed! -> {}".format(e))



def send_cmd_parse_return(cmd):
	return subprocess.check_output(cmd, shell=True).decode("utf-8").strip("\n")



def process_check(proc_data):
	try:
		cmd = """ps auxw | grep {} | grep -v grep > /dev/null
		if [ $? = 0 ]
		then
		        echo "alive"
		else
	        echo "dead"
		fi""".format(proc_data)
		return send_cmd_parse_return(cmd)
	except Exception as e:
		print("AUTOBACKUP: process_check() failed! -> {}".format(e))
######################################################





####initiation of db for test purposes####
database.write("onoff", "0")
database.write("backingup", "0")
##################need to be erased for reallife execution



#
######################################################
for i in range(3): #-> dongu supervisorctl ile çalışacak
	#before backup process
	while(database.read("onoff") == 0):
		print("AUTOBACKUP: backup_machine turning on")
		turn_on()
		while(pinger.is_online(ip_backup) != True):
			print("AUTOBACKUP: backup machine still offline, waiting for boot")
		print("AUTOBACKUP: backup_machine online!")
		time.sleep(wait_after_pingcheck_done)
		print("AUTOBACKUP: backup started")
		start_backup(5)
		database.write("backingup", "1")
		database.write("onoff", "1")

	#after backup process
	while(database.read("onoff") == 1):
		while(database.read("backingup") == 1):
			while(process_check(run_test_proc) == "alive"):
				time.sleep(1)
			print("AUTOBACKUP: backup done")
			database.write("backingup", "0")
		print("AUTOBACKUP: shutting down")
		turn_off()
		database.write("onoff","0")
	print("AUTOBACKUP: entering wait_for_next_period")	
	database.write("runtime", time.time())
	while((time.time() - database.read("runtime")) < period[next_backup_period]):
			print("AUTOBACKUP: waiting for next backup period")
			time.sleep(sleep_time)
