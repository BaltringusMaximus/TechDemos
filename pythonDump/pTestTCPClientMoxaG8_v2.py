import socket
import sys
import msvcrt
import binascii
import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1
#with open("test_tcp_g8_log.txt", "a") as log_file:
#	log_file.write("test")
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ("10.210.236.99", 4003)
#print >>sys.stderr, 'connecting to %s port %s' % server_address
#with open("test_tcp_g8_log.txt", "a") as log_file:
#	log_file.write("test 1")
sock.connect(server_address)
try:
	sock.send(b'test')
except:
	print("connection failed")
else:
	print("connection successful")
#with open("test_tcp_g8_log.txt", "a") as log_file:
#	log_file.write("test 2")
while True:
	data = sock.recv(4096)
#	print(data)
#	print(type(data))
#	print(data.hex())
	str_data = data.decode("ISO-8859-1")
#	print(str_data)
#	print(type(str_data))
	print("====================")
	with open("test_tcp_g8_log.txt", "a") as log_file:
		for i in str_data:
#			print(i)
#			print(type(i))
#			print("---")
			if i in ["0","1","2","3","4","5","6","7","8","9","."," "] or i.isalpha():
				log_file.write(i)
			else:
				sock.send(b'')
				log_file.write("\n")
				print(data)
				print(data.hex())
#				send(IP(dst="10.210.236.99")/TCP(sport=data.sport,dport=(4003),flags="A"))
#		try:
#			data.decode("utf-8")
#		except:
#			for i in data:
#				try:
#					i.decode("utf-8")
#				except:
#					log_file.write("\n")
#				else:
#					log_file.write(i)
#		else:
#			log_file.write(str_data)
#			log_file.write(" ")


