#!/usr/bin/python3

import os



def start_backup_test():
	print("starting backup with command below")
	cmd = "sh {}/test_proc.sh".format(os.getcwd())
	os.system(cmd)


start_backup_test()