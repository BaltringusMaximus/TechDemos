import scapy.all as scapy
from scapy.all import raw,IP,TCP,sendp,sr1,Ether,Padding
import socket
import os
import binascii
import msvcrt
import time

s = scapy.conf.L2socket(filter="tcp and ip host 127.0.0.3", iface="\\Device\\NPF_Loopback")
print(scapy.get_if_list())
#sendp(b'\x02\x00\x00\x00\x45\x02\x00\x29\x51\x35\x40\x00\x80\x06\x00\x00\x7f\x00\x00\x03\x7f\x00\x00\x01\xe2\x90\xec\x49\x30\x5c\xa0\x8a\x4f\x78\xd6\x04\x50\x18\x27\xf9\xbf\x8f\x00\x00\x05',iface="\\Device\\NPF_Loopback")
sendp(b'\x02\x00\x00\x00\x45\x02\x00\x29\x51\x4f\x40\x00\x80\x06\x00\x00\x7f\x00\x00\x03\x7f\x00\x00\x01\xe2\x90\xff\x2b\x26\x02\x77\x7b\x1d\xe5\xda\x6b\x50\x18\x27\xf9\x0d\x43\x00\x00\x05',iface="\\Device\\NPF_Loopback")
while True: 
	try:
		data = s.recv()
		packet = scapy.raw(data)
		str_packet = str(binascii.hexlify(packet))
		print(str_packet)
#		sendp(Ether()/IP(src = "127.0.0.3",dst = "127.0.0.1")/TCP()/"test",iface="\\Device\\NPF_Loopback")
#		time.sleep(1)
	except Exception as e:
#		print(e)
		a = 0
#		time.sleep(1)