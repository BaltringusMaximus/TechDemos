import socket
import os
import sys
import msvcrt
import binascii
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("10.210.225.96", 5000)
sock.connect(server_address)
print("connection")
try:
	sock.send(b'\x05')
except:
	print("connection failed")
else:
	print("connection alright")
counter = 0
while True:
	data = sock.recv(65536)
#	if counter < 10:
#		sock.send(b'\x05')
#		counter = counter + 1
#		print("sent")
	if input() == "0":
		sock.send(b'\x05')
		print("sent enq")
	print(data)
	print(data.hex()[0:2])
	print(type(data))
	print(data.hex())
	print(type(data.hex()))
#	if data.hex() == "05":
#		sock.send(b'\x06')
#	if data.hex()[0:2] == "02":
#		sock.send(b'\x06')
	print("===========")
	str_data = data.decode("ISO-8859-1")
#	time.sleep(1)

