[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/ste-giraldo/python3-cisco-config)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# python3-cisco-config

Script for configuring Cisco routers from a set of commands in an external file (prompt requested) against a list of devices in an external CSV file (prompt requested). Have a look at the CSV file in order to understand how to write it.

## Installation

1. You must have Python3 and PIP installed;

    1.1 To install 'pip3' on Debian GNU/Linux or Ubuntu type: `apt-get install python3-pip`;
2. Then install Netmiko: `pip3 install netmiko` or `pip install netmiko`;
3. And Ping3: `pip3 install ping3` or `pip install ping3`.

## Hostname or DNS mode for output filename

As first thing, you will be prompted to choose "hostname mode" or "DNS mode" for filename output. This script, place a text file in the result-config folder with the output of the configs done during the execution, it's useful for debugging or for further executions.

***Hostname mode***: by selecting this option, the script will retrieve the hostname from the device, this can be useful if your CSV file contains only IP address and you want to output files starting with the hostname configured on the device; 

***DNS mode***: by selecting this option, the script will retrieve the hostname from the first column of your CSV file, so if you type "router1" as device name, the output file will be router1_DATE.txt. The script will use your DNS servers in order to resolv router1, hence it's useful for those who have device names rightly mapped in their DNS servers. If you type an IP address instead of a name, the IP will be used as hostname, in this way: IP_DATE.txt.

## CSV file syntax

Please have a look a the files cisco_hosts.csv and cisco_hosts2.csv. In the column `IP` you can type IP addresses or DNS resolvable hostnames. The column `Enable Secret` can be populated or not depending on your device authentication mode. If you don't need to enter an enable password, leave the column blank, but don't forget the `comma` after the first password.

## Script usage

As reported by the author, [Ping3](https://github.com/kyan001/ping3) require root privilege, please run the script as 'sudo': 
  ```sh
$ sudo python3 conf_run.py

This Python script sends 'show' or 'config' commands against devices listed in a CSV file. Use at your own risk.

1. Filename output in hostname mode.
2. Filename output in DNS mode.
3. Exit. 

Please pick an option. Check the README.md first: 2

What is the name of your CONFIG file for Cisco devices?: config_file
Ok, Config File exists

What is the name of your CSV file for Cisco devices?: cisco_hosts.csv
Ok, CSV File exists

config term
Enter configuration commands, one per line.  End with CNTL/Z.
router1(config)#end
router1#sh clock
23:00:25.218 CET-DST Thu Apr 22 2021
router1#sh ntp a
  address         ref clock       st   when   poll reach  delay  offset   disp
+~193.204.114.232 .CTD.            1    776   1024   377  2.955  -0.530  1.131
*~193.204.114.233 .CTD.            1    299   1024   377  2.977  -0.375  1.087
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
router1#

Outputted to router1_2021-04-22_23-00.txt
10.0.0.1 is down!
  ```
## SSH or Telnet mode 

By changing the `device_type:` into `conf_run3.py` script, you can select the connection mode. Comment and decomment the line basing on your needs: 

  ```sh
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
  ```
## Commands file usage

Since netmiko provides only an extention for entering in "config mode" use this workaround: 
1) When you have to use "show commands" add an "end" in your file at the begin and then all the commands, like this: 
  ```sh
end
sh clock
sh ntp a
  ```
2) When you have to go in config mode, just enter commands for config, like this:
  ```sh
ip host test3 3.3.3.3
no ip host test3 3.3.3.3
do write
  ```
## Ping test and downDevices file

Before try to deploy any config, this script perform a ping test to check wheter a device is reachable or not and skip those unreachables. In case of unreachables, you will find in the result-config folder a file named downDevices_DATE.txt with the list of those devices that doesn't replied to the ping. 

Please note: if you filter ICMP echo request (ping) on your devices, remember to allow it from the host you use to run this script.

## Screenshot of a run:
![Screenshot of a run](https://i.imgur.com/jA7oB0j.jpeg)
