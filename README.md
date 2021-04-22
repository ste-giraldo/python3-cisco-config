# python3-cisco-config

Script for configuring Cisco routers from a set of commands in an external file (prompt requested) against a list of devices in an external CSV file (prompt requested). 

## Installation

1. You must have Python3 and PIP installed on the device you are running the program on;

    1.1 To install 'pip3' on Debian GNU/Linux or Ubuntu type: `apt-get install python3-pip`;
3. You need to run `pip3 install netmiko` or `pip install netmiko` in a command prompt / terminal on your computer;
4. You need to run `pip3 install ping3` or `pip install ping3` in a command prompt / terminal on your computer.

## Script usage

As reported by the author, [Ping3](https://github.com/kyan001/ping3) require root privilege, please run the script as 'sudo': 
  ```sh
$ sudo python3 conf_run3.py

This Python script sends 'show' or 'config' commands against devices listed in a CSV file. Use at your own risk.

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

Outputted to router1_04-22-2021_23-00.txt
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
