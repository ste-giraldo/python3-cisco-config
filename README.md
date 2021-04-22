# python3-cisco-config

Script for configuring Cisco routers from a set of commands in an external file (prompt requested) against a list of devices in an external CSV file (prompt requested). 

## Installation

1. You must have Python3 and PIP installed on the device you are running the program on.

    1.1 To install 'pip3' on Debian GNU/Linux type: `apt-get install python3-pip`.
3. You need to run `pip3 install netmiko` or `pip install netmiko` in a command prompt / terminal on your computer.
4. You need to run `pip3 install ping3` or `pip install ping3` in a command prompt / terminal on your computer.

NB: Since netmiko provides only an extention for entering in "config mode" use this workaround: 
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
