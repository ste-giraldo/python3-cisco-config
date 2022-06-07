[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/ste-giraldo/python3-cisco-config)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# python3-cisco-config

This project propose two scripts: 

`conf_run.py` is a script for configuring Cisco routers from a set of commands in an external file (prompt requested) against a list of devices in an external CSV file (prompt requested). Have a look at the CSV file in order to understand how to write it. 

`inline_conf_run.py` works as conf_run.py but the options are inline and not prompt requested. **This version can run as oneshot or in a crontab for automation. Also, since it contains a lot of improvements than conf_run.py, I highly suggest to use this one.**

## Installation

1. You must have Python3 and PIP installed;

    1.1 To install 'pip3' on Debian GNU/Linux or Ubuntu type: `apt-get install python3-pip`;
2. Then install Netmiko: `pip3 install netmiko` or `pip install netmiko`;
3. And Ping3: `pip3 install ping3` or `pip install ping3`.

## Hostname or DNS mode for output filename for conf_run.py

As first thing, you will be prompted to choose "hostname mode" or "DNS mode" for filename output. This script, place a text file in the result-config folder with the output of the configs done during the execution, it's useful for debugging or for further executions.

***Hostname mode***: by selecting this option, the script will retrieve the hostname from the device, this can be useful if your CSV file contains only IP address and you want to output files starting with the hostname configured on the device; 

***DNS mode***: by selecting this option, the script will retrieve the hostname from the first column of your CSV file, so if you type "router1" as device name, the output file will be router1_DATE.txt. The script will use your DNS servers in order to resolv router1, hence it's useful for those who have device names rightly mapped in their DNS servers. If you type an IP address instead of a name, the IP will be used as hostname, in this way: IP_DATE.txt.

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

## CSV file syntax

Please have a look a the files cisco_hosts.csv and cisco_hosts2.csv. In the column `IP` you can type IP addresses or DNS resolvable hostnames. The column `Enable Secret` can be populated or not depending on your device authentication mode. If you don't need to enter an enable password, leave the column blank, but don't forget the `comma` after the first password.

## Ping test and downDevices file

Before try to deploy any config, these scripts perform a ping test to check wheter a device is reachable or not and skip those unreachables. In case of unreachables, you will find in the result-config folder a file named downDevices_DATE.txt with the list of those devices that doesn't replied to the ping. 

Please note: if you filter ICMP echo request (ping) on your devices, remember to allow it from the host you use to run this script.

## conf_run.py Script usage

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

## conf_run.py Screenshot of a run
![Screenshot of a run](https://i.imgur.com/dEO40P7.jpg)

## inline_conf_run.py Script usage

As reported by the author, [Ping3](https://github.com/kyan001/ping3) require root privilege, please run the script as 'sudo': 
  ```sh
$ sudo python3 inline_conf_run.py --help
[sudo] password for operatore: 
python3-cisco-config ver. 2.2.3 - 2022-05-24 | https://github.com/ste-giraldo

Usage: conf_run.py -c <config_filename> -s <host_list.csv> (Opt --verbose)
Note: Default output filename is DNS based (check README.md)

       -c, --conf <config_filename>
       -s, --csv <host_list.csv>
       Optional -v, --verbose
       Optional -n, --host    Output filename use hostname retrived from device
       Device connection method: --ssh (SSH: default), --tnet (telnet)
       -h, --help    Print this help and exit

  ```
  Please respect the optional variables positioning, always use -c and -s (or long options) before any other options
  
  ```sh
$ sudo python3 inline_conf_run.py -c config_file -s cisco_hosts.csv --verbose --ssh
Config filename is: config_file
CSV filename is: cisco_hosts.csv
Running in SSH mode

Checking devices reachability: 
10.100.100.1 is down!
10.100.100.2 is down!

Running on: router1

config term
Enter configuration commands, one per line.  End with CNTL/Z.
router1(config)#end
router1#sh clock
12:09:37.992 CEST Tue Jun 7 2022
router1#sh ntp a

  address         ref clock       st   when   poll reach  delay  offset   disp
*~10.25.0.9       127.127.1.1      2    775   1024   377  0.000  -4.000  1.978
x~10.25.0.10      127.127.1.1      2    989   1024   377  1.000  16.500  1.977
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
router1#
Outputted to router1_2022-06-07_12-09.txt

The list of devices down or that refused the connection is in: result-config/downDevices_2022-06-07_12-09.txt
  ```

## inline_conf_run.py Screenshot of a run
![Screenshot of a run](https://i.imgur.com/13P117S.jpg)

## Credits 
Thanks to Alex Munoz https://github.com/AlexMunoz905/ for the original script and ping check improvement.

Thanks to Mr. Wolf https://github.com/bbird81 for the precious improvements with getopt for inline version, try, except and "all the fish".
