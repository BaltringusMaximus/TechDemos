import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1,Ether,sendp,Padding
import socket
import os
import binascii
import msvcrt

s = scapy.conf.L2socket(filter="tcp and ip host 10.210.225.96")
#for i in range(15):
#	send(IP(src="10.210.225.96",dst="10.14.1.40")/TCP(sport = 5000, dport = 52578)/"\x06")
while True: 
	packet = s.recv()
#	print(packet)
	try:
		data = scapy.raw(packet)
		str_hex_code = str(binascii.hexlify(data))
#		print(str_hex_code)
#		print(str_hex_code[-3:-1])
		if str_hex_code[2:14] == "94bf947ab781":
			print("outgoing")
			if str_hex_code[-3:-1] == "05":
				print("enq")
#				print(str_hex_code)
				str_bytes = ""
				counter = 0
				for i in str_hex_code:
					str_bytes = str_bytes + i
					counter = counter + 1
					if counter % 2 == 0:
						str_bytes = str_bytes + "\\x"
				str_bytes = str_bytes[2:-3]
				bytes = bytes.fromhex(str_hex_code[2:-1])
				print(bytes)
				print(str_bytes)
#				data_to_send = data
#				if data_to_send	!= 0:
#					sendp(data_to_send)
#					data_to_send = 0
				
#				print(str_bytes)
#				print(binascii.hexlify(data))
#				sendp(binascii.hexlify(data))
		if str_hex_code[2:14] == "005056a2c2c0":
			print("incoming")
			if str_hex_code[-13:-11] == "06":
				print("ack")
#				print(str_hex_code)
#				print(data)
#		if str_hex_code[-3:-1] == "05":
#			try:
#				pad = Padding()
#				pad.load = '\x00'*5
#				ack = Ether(src="94:bf:94:7a:b7:81",dst="00:50:56:a2:c2:c0")/IP(src="10.210.225.96",dst="10.14.1.40")/TCP(sport = 5000, dport = 62232)/"\x06"/pad
#				sendp(b'\x00\x50\x56\xa2\xc2\xc0\x94\xbf\x94\x7a\xb7\x81\x08\x00\x45\x02\x00\x29\x80\xf6\x40\x00\x3e\x06\xc4\x6e\x0a\xd2\xe1\x60\x0a\x0e\x01\x28\x13\x88\xf3\x18\x82\xcc\xa9\xfe\xae\x68\x4e\x65\x50\x18\x01\xf5\x80\x34\x00\x00\x06'/pad)
#				sendp(b'\x00\x50\x56\xa2\xc2\xc0\x94\xbf\x94\x7a\xb7\x81\x08\x00\x45\x02\x00\x29\x82\x3d\x40\x00\x3e\x06\xc4\x6e\x0a\xd2\xe1\x60\x0a\x0e\x01\x28\x13\x88\xc4\x56\x82\xcc\xbf\xc0\xae\x68\x4e\x65\x50\x18\x01\xf5\x80\x34\x00\x00\x06\x00\x00\x00\x00\x00')
#				sendp(ack)
#				print("ack sent")
#			except Exception as e:
#				print(e)
#		print(packet.src)
#		print(type(packet.src))
#		if packet.src == "94:bf:94:7a:b7:81":
#			print(str_hex_code)
#			print(packet.payload)
#		print(data)
#		print(packet)
	except Exception as e:
		print(e)
		a = 0