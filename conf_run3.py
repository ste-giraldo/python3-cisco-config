# Forked by Alex Munoz "Python-Cisco-Backup" script https://github.com/AlexMunoz905/
# Mod & improvement by Ste Giraldo https://github.com/ste-giraldo

# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping 
import getpass, os, os.path, sys, time, cmd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#sys.tracebacklimit = 0

print ()
print ("This Python script sends 'show' or 'config' commands against devices listed in a CSV file. Use at your own risk.")

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('result-config'):
    os.makedirs('result-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gives us the information we need to connect.
def get_saved_config(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
#        'device_type': 'cisco_ios_telnet',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Configuring from commands in temp file.
    output = net_connect.send_config_from_file(conf_name)
    time.sleep(0.5)
    print()
    print(output)
    print()
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | i uptime")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the result-config folder with the special name, and writes to it.
    backupFile = open("result-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gets the Config file name for Cisco, and grabs the configs from it.
conf_name = input(bcolors.OKCYAN + "\nWhat is the name of your CONFIG file for Cisco devices?: " + bcolors.ENDC)
open(conf_name, 'r')

# Checks if the config file exists.
os.path.exists(os.path.join(conf_name))
print ("Ok, Config File exists")

# Gets the CSV file name for Cisco, and grabs the information from it.
csv_name = input(bcolors.OKGREEN + "\nWhat is the name of your CSV file for Cisco devices?: " + bcolors.ENDC)

# Checks if the config file exists.
os.path.exists(os.path.join(csv_name))
print ("Ok, CSV File exists")

# Open CSV file and ping test the hosts.
with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_Cisco_Devices_" + dt_string + ".txt"
                downDeviceOutput = open("result-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                get_saved_config(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
