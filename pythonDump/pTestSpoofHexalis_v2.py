import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1,Ether,sendp,Padding
import socket
import os
import binascii
import msvcrt

s = scapy.conf.L2socket(filter="tcp and ip host 10.210.225.96")
sendp(b'\x94\xbf\x94\x7a\xb7\x81\x00\x50\x56\xa2\xc2\xc0\x08\x00\x45\x02\x00\x29\x45\xe2\x40\x00\x80\x06\x00\x00\x0a\x0e\x01\x28\x0a\xd2\xe1\x60\xe1\x1a\x13\x88\xe2\x8d\xbb\x84\x8d\x7f\xa5\x3c\x50\x18\x20\x14\xf7\x83\x00\x00\x05')
while True: 
	packet = s.recv()
	try:
		data = scapy.raw(packet)
		str_hex_code = str(binascii.hexlify(data))
		if str_hex_code[2:14] == "94bf947ab781":
			print("outgoing")
			if str_hex_code[-3:-1] == "05":
				print("enq")
				print(str_hex_code)
				hex_string = str_hex_code[2:-1]
				print(hex_string)
				src_ip = hex_string[0:12]
				print("src =",src_ip)
				dst_ip = hex_string[12:24]
				print("dst =",dst_ip)
				type_ipv4 = hex_string[24:28]
				print("ip version =",type_ipv4)
				hex_string_ip = hex_string[28:68]
				print("hex_string_ip =",hex_string_ip)
				seq = hex_string[76:84]
				ack = hex_string[84:92]
				print("seq =",seq,"ack =",ack)
		if str_hex_code[2:14] == "005056a2c2c0":
			print("incoming")
			if str_hex_code[-13:-11] == "06":
				print("ack")

	except Exception as e:
#		print(e)
		a = 0