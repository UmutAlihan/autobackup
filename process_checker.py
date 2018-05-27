import os
import sys
import database
import subprocess




def check(proc_data):
	#process = database.read(proc_data)
	cmd = """ps auxw | grep {} | grep -v grep > /dev/null
	if [ $? = 0 ]
	then
	        echo "alive"
	else
	        echo "dead"
	fi""".format(proc_data)
	status = subprocess.check_output(cmd, shell=True)
	return status.decode("utf-8").strip("\n")



if __name__=="__main__":
	status = check("test_proc")
	print(status)
