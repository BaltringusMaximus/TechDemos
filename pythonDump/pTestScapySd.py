import socket
import os
import sys
import binascii
import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1
s = scapy.conf.L3socket(filter="tcp and ip host 10.210.236.99")
send(IP(dst='10.210.236.99')/TCP(dport=4003, flags='S')/"06")