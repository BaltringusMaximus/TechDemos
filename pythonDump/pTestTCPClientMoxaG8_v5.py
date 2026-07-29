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
int_line_count = 0
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
			print(int_line_count)
			str_barcode = str_line[3:15]
			int_line_count = 0
#		print("barcode =",str_barcode)
#		print("line =",str_line)
		if i.isdigit() == False and i.isalpha() == False and i not in ["."," "] and bytes(i,"ISO-8859-1") == b'\x02':
			int_line_count = int_line_count+1
			print("number of line since message start =",int_line_count)
			print("barcode =",str_barcode)
			print("line =",str_line)
			print(bytes(i,"ISO-8859-1"))
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
	if data == b'\x04':
		print("================end message================")
		print("total number of line =", int_line_count)
		with open(str_barcode+".txt", "a") as tube_file:
			tube_file.write("\n================end message================")
#		if j == "04":
#			print("================end message================")
#	print(str_line)
