# python3-cisco-config

Script for configuring Cisco routers from a set of commands in an external file (prompt requested) against a list of devices in an external CSV file (prompt requested). 

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
