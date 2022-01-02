# Forked by Alex Munoz "Python-Cisco-Backup" script https://github.com/AlexMunoz905/
# Mod & improvements by Ste Giraldo https://github.com/ste-giraldo
# Ver. 1.3.2 - 2022-01-02

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

sys.tracebacklimit = 0

print ("\nThis Python script sends 'show' or 'config' commands against devices listed in a CSV file. Use at your own risk.")

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('result-config'):
    os.makedirs('result-config')

# Current date and time
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H-%M")

# Gets the CSV file name for Cisco, and grabs the information from it.
#csv_name = input(bcolors.OKGREEN + "\nWhat is the name of your CSV file for Cisco devices?: " + bcolors.ENDC)

# Gives us the information we need to connect.
def get_saved_config_host(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
#        'device_type': 'cisco_ios_telnet',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Configuring from commands in variable config file.
    output = net_connect.send_config_from_file(conf_name)
    time.sleep(0.5)
    print()
    print(output)
    print()
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | i uptime")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name with hostname and date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the result-config folder with the special name and writes to it.
    backupFile = open("result-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

def get_saved_config_dns(host, username, password, enable_secret):
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
    # Configuring from commands in variable config file.
    output = net_connect.send_config_from_file(conf_name)
    time.sleep(0.5)
    print()
    print(output)
    print()
    # Creates the file name, which is the hostname, and the date and time.
    fileName = ip + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("result-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Open CSV file and ping test the hosts.
def csv_option_host():
    with open(csv_name, 'r') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "downDevices_" + dt_string + ".txt"
                downDeviceOutput = open("result-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                get_saved_config_host(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

def csv_option_dns():
    global ip # Exporting "ip" variable from csv_option_dns function to the global environment.
    with open(csv_name, 'r') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "downDevices_" + dt_string + ".txt"
                downDeviceOutput = open("result-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                get_saved_config_dns(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

# Asks the user what option they are going to use.
print("\n1. Filename output in hostname mode.")
print("2. Filename output in DNS mode.")
print("3. Exit.\n")
choice = input("Please pick an option. Check the README.md first: ")
if choice == "3":
 exit()

# Gets the Config file name for Cisco, and grabs the configs from it.
conf_name = input(bcolors.OKCYAN + "\nWhat is the name of your CONFIG file for Cisco devices?: " + bcolors.ENDC)
open(conf_name, 'r')

# Checks if the config file exists.
os.path.exists(os.path.join(conf_name))
print ("Ok, Config File exists")

# This basically runs the whole file.
# Run in hostname mode.
if choice == "1":
# Gets the CSV file name, and grabs the information from it.
 csv_name = input(bcolors.OKGREEN + "\nWhat is the name of your CSV file for Cisco devices?: " + bcolors.ENDC)
 os.path.exists(os.path.join(csv_name))
 print ("Ok, CSV File exists")
 while True:
   answer = input(bcolors.WARNING + "\nAre you shure to run this Script? y/n: " + bcolors.ENDC)
   if answer.lower().startswith("y"):
      print("\nSkynet is now operating on your Network. Please wait... ;)")
      csv_option_host()
      exit()
   elif answer.lower().startswith("n"):
      print("\nOk, Goodbye.")
      exit()

# Run in DNS mode.
elif choice == "2":
# Gets the CSV file name, and grabs the information from it.
 csv_name = input(bcolors.OKGREEN + "\nWhat is the name of your CSV file for Cisco devices?: " + bcolors.ENDC)
 os.path.exists(os.path.join(csv_name))
 print ("Ok, CSV File exists")
 while True:
   answer = input(bcolors.WARNING + "\nAre you shure to run this Script? y/n: " + bcolors.ENDC)
   if answer.lower().startswith("y"):
      print("\nSkynet is now operating on your Network. Please wait... ;)")
      csv_option_dns()
      exit()
   elif answer.lower().startswith("n"):
      print("\nOk, Goodbye.")
      exit()
