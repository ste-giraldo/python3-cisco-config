# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping 
import getpass
import os
import sys
import time
import cmd

#sys.tracebacklimit = 0

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('result-config'):
    os.makedirs('result-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

#"""
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
    # Configuring from commands in variable filename.
    output = net_connect.send_config_from_file("cfg_file-29ef3eea-a099-11eb-bcbc-0242ac130002.temp")
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
#"""

# Gets the txt file name for Cisco, and grabs the configs from it.
conf_name = input("\nWhat is the name of your config file for Cisco devices?: ")
open(conf_name, 'r')

src = conf_name
dst = "cfg_file-29ef3eea-a099-11eb-bcbc-0242ac130002.temp"

# This creates a symbolic link on python
os.symlink(src, dst)

# Gets the CSV file name for Cisco, and grabs the information from it.
csv_name = input("\nWhat is the name of your CSV file for Cisco devices?: ")
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

# This removes a symbolic link on python
if os.path.exists("cfg_file-29ef3eea-a099-11eb-bcbc-0242ac130002.temp"):
 os.remove("cfg_file-29ef3eea-a099-11eb-bcbc-0242ac130002.temp")
