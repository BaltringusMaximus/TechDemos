import socket
import sys
import msvcrt
import binascii
def is_barcode(str):
	if str[0:3] in ["112","122"] and len(str) >= 15: 
		if str[0:14].isdigit():
			return True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("10.210.236.99", 4003)
sock.connect(server_address)
try:
	sock.send(b'test')
except:
	print("connection failed")
else:
	print("connection successful")
#str_barcode = str()
str_barcode = "init"
str_line = str()
while True:
	data = sock.recv(4096)
#	print(data)
#	print(type(data))
#	print(data.hex())
	str_data = data.decode("ISO-8859-1")
#	print(str_data)
#	print(type(str_data))
#	print("====================")
	for i in str_data:
#		print(i)
#		print(type(i))
#		print("---")
		if i.isdigit() or i.isalpha() or i in ["."," "]:
#			print("i is digit")
			str_line = str_line+i
#			print(str_line)
		if is_barcode(str_line):
			str_barcode = str_line[3:15]
#		print("barcode =",str_barcode)
#		print("line =",str_line)
		if i.isdigit() == False and i.isalpha() == False and i not in ["."," "]:
			print("barcode =",str_barcode)
			print("line =",str_line)
			if str_barcode != "init":
				try:
					with open(str_barcode+".txt", "a") as tube_file:
						tube_file.write("\n")
						tube_file.write(str_line)
#						print("barcode =",str_barcode)
#						print("line =",str_line)
				except IOError:
					with open(str_barcode+".txt", "w") as tube_file:
						tube_file.write("\n")
						tube_file.write(str_line)
#						print("barcode =",str_barcode)
#						print("line =",str_line)
			str_line = str()
#	print(str_line)
