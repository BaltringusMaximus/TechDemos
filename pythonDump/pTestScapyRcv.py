import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1
import socket
import os
import binascii
import msvcrt
s = scapy.conf.L3socket(filter="tcp and ip host 10.210.236.99")
print(s)
while True:
	packet = s.recv()
	if type(packet) != type(None):
		print("=======================")
		load = scapy.raw(packet)
		if packet.dst == "10.210.236.99":
			print(load)
			str_code=load.decode("ISO-8859-1")
			print(str_code)
			str_hex_code = str(binascii.hexlify(load))
			print(str_hex_code)
			str_hex_data = str_hex_code[82:86]
			print(str_hex_data)
		if msvcrt.kbhit():
			break