import scapy.all as scapy
from scapy.all import raw,IP,TCP,sendp,sr1,Ether,Padding
import socket
import os
import sys
import time
import msvcrt
import binascii
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_address = ("127.0.0.3", 58000)
sock.bind(client_address)
sock.listen(1)
conn, addr = sock.accept()
while True:
	if input() == "0":
		conn.send(b'\x05')
		print("enq")
	try:
		data = conn.recv(4096)
		print(data)
		if data == b'\x05' :
			conn.send(b'\x06')
			print("ack")
	except Exception as e:
		print(e)

