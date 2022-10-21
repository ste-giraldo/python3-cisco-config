# Forked by Alex Munoz "Python-Cisco-Backup" script https://github.com/AlexMunoz905/
# Mods & improvements by Ste Giraldo https://github.com/ste-giraldo and Mr.Wolf https://github.com/bbird81 
ver = "python3-cisco-config ver. 2.2.3 - 2022-05-24 | https://github.com/ste-giraldo"

# All pre-installed besides Netmiko.
import getpass, os, os.path, sys, getopt, time, cmd
import socket
import csv
import pathlib
from datetime import date, datetime
from netmiko import ConnectHandler
from netmiko import ssh_exception, Netmiko
from paramiko.ssh_exception import AuthenticationException, NoValidConnectionsError
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from ping3 import ping, verbose_ping 

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

# Current date and time in format: Year-Month-Day_Hours-Minutes.
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H-%M")

# Checking open ports between SSH and Telnet and tell to get_saved_config which protocol to use. It start checking using SSH.
'''
def check_port(ip):
    cp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_ssh = (ip, 22)
    ip_telnet = (ip, 23)
    try:
        check = cp.connect_ex(ip_ssh)
        if check == 0:
            return 'cisco_ios'
    except: #in case of closed ssh, telnet will be tested
        try:
            check = cp.connect_ex(ip_telnet)
            if check == 0:
                return 'cisco_ios_telnet'
        except:
            return '' #no port is open, implement raise exception and continue
'''

# Print the help message.
def help_page():
    print(ver)
    print('\nUsage: conf_run.py -c <config_filename> -s <host_list.csv> (Opt --verbose)')
    print('Note: Default output filename is DNS based (check README.md)')
    print()
    print('       -c, --conf <config_filename>')
    print('       -s, --csv <host_list.csv>')
    print('       Optional -v, --verbose')
    print('       Optional -n, --host    Output filename use hostname retrived from device')
    print('       Device connection method: --ssh (SSH: default), --tnet (telnet)')
    print('       -h, --help    Print this help and exit')
    print()
    print('       Please respect the proposed sequence in the options declaring.\n')

# Reads the CSV file, writes a file with non-pingable devices and returns a list of active_devices.
def test_devices():
    global downfileName
    print('\nChecking devices reachability: ')
    active_devices = []
    with open(csv_name, 'r') as csvfile:
        # Use CSV DictReader for file reading: it read the columns basing on column name and not on column position.
        csv_reader = csv.DictReader(csvfile, delimiter=',')
        for ip in csv_reader:
#            print(str(ip['IP'])) # Uncomment for debugging purpose.
            ip_ping = ping(str(ip['IP']))
            if ip_ping == None:
                downfileName = "downDevices_" + dt_string + ".txt"
                downDeviceOutput = open("result-config/" + downfileName, "a")
                downDeviceOutput.write(str(ip['IP']) + " Device_unreachable\n")
                print(str(ip['IP']) + " is down!")
            else: active_devices.append(str(ip['IP']))
    return active_devices

# Executes commands and saves config file.
def get_saved_config(host, username, password, enable_secret, flag_host, dport):
    global downfileName
    if dport == 22:
        driver = 'cisco_ios'
    elif dport == 23:
        driver ='cisco_ios_telnet'
    else: 
        driver = 'cisco_ios'

    cisco_ios = {
#            'device_type': check_port(host), #checks whichever port 22-23 is open and returns name of corresponding netmiko driver.
            'device_type': driver, # Use related protocol basing on selected option from CLI.
            'host': host,
            'username': username,
            'password': password,
            'secret': enable_secret
    }
    # Initialize downfileName variable for all tests
    downfileName = ("downDevices_" + dt_string + ".txt")
    # Creates connection to the device.
    try:
        net_connect = ConnectHandler(**cisco_ios)
        net_connect.enable()
        # Configuring from commands in variable config file.
        output = net_connect.send_config_from_file(conf_name)
        time.sleep(0.3)
        print()
        print(output)
        # Creates the file name with either hostname/ip and date and time.
        if flag_host:
            # Gets and splits the hostname for the output file name.
            hostname = net_connect.send_command("show ver | i uptime")
            hostname = hostname.split()
            hostname = hostname[0]
            fileName = hostname + "_" + dt_string
        else:
            fileName = host + "_" + dt_string
        # Creates the text file in the result-config folder with the special name and writes to it.
        backupFile = open("result-config/" + fileName + ".txt", "w+")
        backupFile.write(output)
        print("Outputted to " + fileName + ".txt")

    # Handle an authentication error.
    except (AuthenticationException, NetMikoAuthenticationException):
        print(bcolors.WARNING + "Login failed on " + bcolors.ENDC + host)
        downDeviceOutput = open("result-config/" + downfileName, "a")
        downDeviceOutput.write(host + " Login_failed\n")
        downDeviceOutput.close()
    # Handle a NoValidConnectionsError.
    except (NoValidConnectionsError):
        print(bcolors.WARNING + "No valid connection to: " + bcolors.ENDC + host)
        downDeviceOutput = open("result-config/" + downfileName, "a")
        downDeviceOutput.write(host + " No_valid_connection\n")
        downDeviceOutput.close()
    # Handle a NetMikoTimeoutException.
    except (NetMikoTimeoutException):
        print(bcolors.WARNING + "Timeout opening connection to: " + bcolors.ENDC + host)
        downDeviceOutput = open("result-config/" + downfileName, "a")
        downDeviceOutput.write(host + " Timeout_opening_connection\n")
        downDeviceOutput.close()
    # Handle the connection refused condition by adding the host line in the downDevices file.
    except (ConnectionRefusedError):
        print(bcolors.WARNING + "Connection refused from: " + bcolors.ENDC + host)
        downDeviceOutput = open("result-config/" + downfileName, "a")
        downDeviceOutput.write(host + " Device_refused_connection\n")
        downDeviceOutput.close()

# Define command arguments for inline options.
def main(argv):
    global conf_name
    global csv_name
    try:
        # Set host or DNS mode flag to False.
        flag_host = False
        opts, args = getopt.getopt(argv,"hnc:vs:",["conf=","csv=","help","host","verbose","ssh","tnet"])
    except getopt.GetoptError:
        help_page()
        sys.exit(2)
    for opt, arg in opts:
#        if opt == ("-h"):
        if opt in ("-h", "--help"):
            help_page()
            sys.exit()
        elif opt in ("-c", "--conf"):
            conf_name = arg
        elif opt in ("-s", "--csv"):
            csv_name = arg
        elif opt in ("-v", "--verbose"):
            print("Config filename is: " + bcolors.OKCYAN + conf_name + bcolors.ENDC)
            print("CSV filename is: " + bcolors.OKGREEN + csv_name + bcolors.ENDC)
        elif opt in ("--ssh"):
            print("Running in SSH mode")
            dport = 22
        elif opt in ("--tnet"):
            print("Running in telnet mode")
            dport = 23
        # Choose if run in IP address or DNS mode. If no flag is set, default option is DNS mode.
        elif opt in ("-n", "--host"):
            flag_host = True

    # Handle the default connection method in SSH.
    try:
        dport
    except:
        dport=22
        print("Running in SSH mode")
 
    # Function to testing working IPs, it creates a file with down devices and provide a list with the up devices.
    active_devices = test_devices()

    # Cycle on reachable devices: credentials retrieve, commands run and output saving.
    for ip in active_devices:
        print(bcolors.OKGREEN + '\nRunning on: ' + bcolors.ENDC + ip)
        with open(csv_name, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            # Retrieve username and password
            '''
            Every row of csv file will look like this dictionary:

                {
                "IP": "10.0.0.1",
                "Username": "admin",
                "Password": "password",
                "Enable Secret": "enable_secret_password"
                }
            '''
            for row in csv_reader: # Finding device related row
                if row['IP'] == ip: # Row found, getting info
                    username = row['Username']
                    password = row['Password']
                    enable_secret =row['Enable Secret']
                    get_saved_config(ip, username, password, enable_secret, flag_host, dport)
                    continue # Exiting from cycle and trying on the next device.

if __name__ == "__main__": # Runs only from the command line.
   main(sys.argv[1:])
   conf_name=''
   csv_name=''

# If we have devices unreachable or with connetion refused, print the file name and path with the list.
downfile = pathlib.Path("result-config/" + downfileName)
if downfile.exists ():
    print(bcolors.WARNING + "\nThe list of devices down or that refused the connection is in: " + bcolors.ENDC + "result-config/" + downfileName + "\n")
else:
    pass
