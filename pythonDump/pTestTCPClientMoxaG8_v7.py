import socket
import sys
import msvcrt
import binascii
import shutil
import os
fol_graphgen = 'C:\\pierre\\apps\\python apps\\graphgen\\'
sys.path.append(fol_graphgen)
def is_barcode(str):
	if str[0:3] in ["112","122"] and len(str) >= 15: 
		if str[0:14].isdigit():
			return True
def is_qc(str):
	if str[0:3] in ["112","122"] and "AB8050L" in str:
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
str_barcode = "init"
str_line = str()
int_line_count = 0
while True:
	data = sock.recv(4096)
	str_data = data.decode("ISO-8859-1")
	for i in str_data:
		if i.isdigit() or i.isalpha() or i in ["."," "]:
			str_line = str_line+i
		if is_barcode(str_line):
			print(int_line_count)
			str_barcode = str_line[3:15]
			int_line_count = 0
		if is_qc(str_line):
			str_barcode = str_line[3:11]
			int_line_count = 0
		if i.isdigit() == False and i.isalpha() == False and i not in ["."," "] and bytes(i,"ISO-8859-1") in [b'\x02',b'\x04']:
			int_line_count = int_line_count+1
			print("number of line since message start =",int_line_count)
			print("barcode =",str_barcode)
			print("tube type =",str_barcode[0:2])
			print("line =",str_line)
			print(bytes(i,"ISO-8859-1"))
			if str_barcode != "init":
				try:
					with open(str_barcode+".txt", "a") as tube_file:
						tube_file.write("\n")
						tube_file.write(str_line)
				except IOError:
					with open(str_barcode+".txt", "w") as tube_file:
						tube_file.write("\n")
						tube_file.write(str_line)
			str_line = str()
	if data == b'\x04' and "AB8050L" in str_barcode and int_line_count > 57:
		print("================end message================")
		print("total number of line =", int_line_count)
		with open(str_barcode+".txt", "a") as tube_file:
			tube_file.write("\nnumber of lines =")
			tube_file.write(str(int_line_count))
			tube_file.write("\n================end message================")
		shutil.copy2(str_barcode+'.txt',fol_graphgen)
		os.remove(str_barcode+'.txt')
		str_barcode = "init"
	if data == b'\x04' and str_barcode[0:2] in ["01","09"] and int_line_count > 57:
		print("================end message================")
		print("total number of line =", int_line_count)
		with open(str_barcode+".txt", "a") as tube_file:
			tube_file.write("\nnumber of lines =")
			tube_file.write(str(int_line_count))
			tube_file.write("\n================end message================")
		shutil.copy2(str_barcode+'.txt',fol_graphgen)
		os.remove(str_barcode+'.txt')
		str_barcode = "init"
	if data == b'\x04' and str_barcode[0:2] in ["47"] and int_line_count > 93:
		print("================end message================")
		print("total number of line =", int_line_count)
		with open(str_barcode+".txt", "a") as tube_file:
			tube_file.write("\nnumber of lines =")
			tube_file.write(str(int_line_count))
			tube_file.write("\n================end message================")
		shutil.copy2(str_barcode+'.txt',fol_graphgen)
		os.remove(str_barcode+'.txt')
		str_barcode = "init"
