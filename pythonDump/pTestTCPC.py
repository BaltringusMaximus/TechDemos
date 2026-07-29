import socket
import sys
import msvcrt
import binascii
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.3", 58000)
sock.connect(server_address)
try:
	sock.send(b'test')
	print("connected")
except:
	print("connection failed")
while True:
	data = sock.recv(4096)
	print(data)
	if data == b'\x05':
		sock.send(b'\x06')
		print("ack")