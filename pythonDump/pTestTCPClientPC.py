import socket
import sys
import msvcrt
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("10.210.236.20", 80)
sock.connect(server_address)
while True:
	data = sock.recv(4096)
	print(data)
	print("====================")
	if msvcrt.kbhit():
		break