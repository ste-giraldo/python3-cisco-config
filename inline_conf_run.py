# Forked by Alex Munoz "Python-Cisco-Backup" script https://github.com/AlexMunoz905/
# Mods & improvements by Ste Giraldo https://github.com/ste-giraldo
ver = "python3-cisco-config ver. 1.5.0i - 2022-03-06 | https://github.com/ste-giraldo"

# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from netmiko import ssh_exception, Netmiko
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException
from ping3 import ping, verbose_ping 
import getpass, os, os.path, sys, getopt, time, cmd

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

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('result-config'):
    os.makedirs('result-config')

# Current date and time in format: Year-Month-Day_Hours-Minutes
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H-%M")

# Gives us the information we need to connect.
def get_saved_config_host(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates connection to the device.
    try:
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
    # Handle an authentication error.
    except (AuthenticationException, NetMikoAuthenticationException):
        print("Login failed " + host)

def get_saved_config_dns(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    try:
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
    # Handle an authentication error.
    except (AuthenticationException, NetMikoAuthenticationException):
        print("Login failed " + host)

def get_saved_config_host_tnet(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios_telnet',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates connection to the device.
    try:
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
    # Handle an authentication error.
    except (AuthenticationException, NetMikoAuthenticationException):
        print("Login failed " + host)

def get_saved_config_dns_tnet(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios_telnet',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    try:
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
    # Handle an authentication error.
    except (AuthenticationException, NetMikoAuthenticationException):
        print("Login failed " + host)

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

def csv_option_host_tnet():
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
                get_saved_config_host_tnet(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

def csv_option_dns_tnet():
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
                get_saved_config_dns_tnet(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

# Define command arguments for inline options

def main(argv):
    global conf_name
    global csv_name
    try:
        # Set host or DNS mode flag to Flase
        flag_host = False
        opts, args = getopt.getopt(argv,"hnc:vs:",["conf=","csv=","help","host","verbose","ssh","tnet"])
    except getopt.GetoptError:
        print(ver)
        print()
        print('Usage: conf_run.py -c <config_filename> -s <host_list.csv> (Opt --verbose)')
        print('Note: Default output filename is DNS based (check README.md)')
        print()
        print('       -c, --conf <config_filename>')
        print('       -s, --csv <host_list.csv>')
        print('       Optional -v, --verbose')
        print('       Optional -n, --host    Output filename use hostname retrived from device')
        print('       Device connection method: --ssh (SSH: default), --tnet (telnet)')
        print('       -h, --help    Print this help and exit')
        sys.exit(2)
    for opt, arg in opts:
#        if opt == ("-h"):
        if opt in ("-h", "--help"):
            print(ver)
            print()
            print('Usage: conf_run.py -c <config_filename> -s <host_list.csv> (Opt --verbose)')
            print('Note: Default output filename is DNS based (check README.md)')
            print()
            print('       -c, --conf <config_filename>')
            print('       -s, --csv <host_list.csv>')
            print('       Optional -v, --verbose')
            print('       Optional -n, --host    Output filename use hostname retrived from device')
            print('       Device connection method: --ssh (SSH: default), --tnet (telnet)')
            print('       -h, --help    Print this help and exit')
            sys.exit()
        elif opt in ("-c", "--conf"):
            conf_name = arg
        elif opt in ("-s", "--csv"):
            csv_name = arg
        elif opt in ("-v", "--verbose"):
            print("Config filename is: " + bcolors.OKGREEN + conf_name + bcolors.ENDC)
            print("CSV filename is: " + bcolors.WARNING + csv_name + bcolors.ENDC)
        # Choose if run in IP address or DNS mode. If no flag is set, default option is DNS mode.
        elif opt in ("-n", "--host"):
            flag_host = True
    if flag_host == True:
        print()
        print("Output filename will use device hostname")
        if opt in ("--ssh"):
            print()
            print("Running in SSH mode")
            csv_option_host()
        elif opt in ("--tnet"):
            print()
            print("Running in telnet mode")
            csv_option_host_tnet()     
    else:
        print()
        print("Output filename will be DNS based")
        if opt in ("--ssh"):
            print()
            print("Running in SSH mode")
            csv_option_dns()
        elif opt in ("--tnet"):
            print()
            print("Running in telnet mode")
            csv_option_dns_tnet()     

if __name__ == "__main__":
   main(sys.argv[1:])
   conf_name=''
   csv_name=''
