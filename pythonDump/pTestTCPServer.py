import socket
import os
import sys
import time
import msvcrt
import binascii
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_address = ("127.0.0.2", 57000)
sock.bind(client_address)
sock.listen(1)
conn, addr = sock.accept()
while True:
	conn.send(b'\x04')
	conn.send(b'\x02')
#	conn.send(b'\x03')
#	conn.send(b'H\x7cORM\r\n')
#	conn.send(b'H|^~&|||G8||ORM||||||A2.2|20240831133130\r\ntest|\r\n')
	conn.send(b'H|results\r\nP|lol\r\nO|987654321|O1\r\ntest|987654321|testg8~testg8a~testg8b|mdr~lmao~rofl|T3\r\n')
#	conn.send(b'H\x02result\r\n')
#	conn.send(b'\x02')
	conn.send(b'\x03')
#	conn.send(b'\x04')
	conn.send(b'\x05')
	print("test")
	time.sleep(1)
