import socket
import os
import sys
import time
import msvcrt
import binascii
#from pTestFileFormat import list_str_values
from LibTxt import f_get_order_from_hca,f_get_tubeid_from_hca,f_get_res_from_hca
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_address = ("127.0.0.2", 57000)
sock.bind(client_address)
sock.listen(1)
conn, addr = sock.accept()
str_continue = "y"
while str_continue != "n":
	dir = os.listdir()
#	print(dir)
	for file in dir:
#		print(file[-4:])
		if file[-13:] == "_hca_data.txt":
			print(file)
			str_order = f_get_order_from_hca(file)
			str_tubeid = f_get_tubeid_from_hca(file)
			str_res = f_get_res_from_hca(file)
			str_msg = "H|results\r\nP|lol\r\nO|"+str_order+"|O1\r\ntest|"+str_tubeid+"|A1a~A1b~HbF~LA1c~SA1c~A0~Variant1~Variant2|"+str_res+"|T3\r\n"
			print("order =", str_order)
			print("tubeid =", str_tubeid)
			print("results string =", str_res)
			print("raw message =",str_msg)
			bytes_msg = bytes(str_msg, 'ISO-8859-1')
			conn.send(b'\x04')
			conn.send(b'\x02')
#	conn.send(b'H|results\r\nP|lol\r\nO|2409150001|O1\r\ntest|2409150001|')
#	conn.send(b'A1a~A1b~HbF~LA1c~SA1c~A0~Variant1~Variant2|')
#	conn.send(b'0.43~0.98~0.43~2.13~6.48~91.31~0.00~0.00|T3\r\n')
			conn.send(bytes_msg)
			conn.send(b'\x03')
			conn.send(b'\x05')
			print("sent")
		print("continue ?")
		str_continue = input()
		if str_continue == "n":
			break
