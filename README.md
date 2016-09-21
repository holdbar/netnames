
This script may be useful if you have DHCP-server running on Linux system, and there is no complete network with domain and stuff, so you don't see names of the devices.
Netnames.py analyzes DHCP-log, ARP-tables and then brings you output - list of current users of your DHCP server with IP, Device-name (if it's possible) and MAC.
You can run netnames.py directly in the shell as root or using 'sudo' (it's necessary to recieve info from ARP-tables). Also it can be attached to the webserver (even python-cgi-server).