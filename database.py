import time
import configparser


def read(data):
	config.read("./config.ini")
	state_data = config.get("database",data)
	if (data == "proc_backup"):
		return str(state_data)
	return float(state_data)

def write(data, new_state):
	config.read("./config.ini")
	config["database"][data] = str(new_state)
	#print(data,new_state)
	with open("./config.ini", "w+") as conf_file:
		config.write(conf_file)

config = configparser.ConfigParser()


#read(
