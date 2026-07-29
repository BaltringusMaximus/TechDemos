import socket
import os
import sys
import binascii
import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1
#print("test")
#log_file = open("test_tcp_g8_log.txt", "a")
#log_file.write("test")
#sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
server_address = ("10.210.224.200",60430)
sock.bind(server_address)
print("connection")
try:
	sock.send(b'')
except:
	print("connection failed")
else:
	print("connection alright")
#sock.send(b'\x06')
while True:
	data = sock.recv(1)
	print(data)
	print(type(data))
	print(data.hex())
	print(type(data.hex()))
	if data.hex() == "03":
		sock.send(b'\x06')
	print("===========")
	str_data = data.decode("ISO-8859-1")
