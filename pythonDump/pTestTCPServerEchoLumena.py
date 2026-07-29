import socket
import os
import sys
import time
import msvcrt
import binascii
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_address = ("0.0.0.0", 56789)
sock.bind(client_address)
sock.listen(1)
conn, addr = sock.accept()
try:
	conn.send(b'hello')
	print("connection up")
except Exception as e:
	print(e)
	print("couldn't connect")
while True:
	data = conn.recv(4096)
	if data:
		conn.send(b'\x06')
		print(data)
		print("replied")
#		if data == b'\x05':
#			conn.send(b'\x06')
#			print("sent")
