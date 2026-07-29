import socket
import os
import sys
import time
from datetime import datetime
import msvcrt
import binascii
import shutil
from LibTxt import f_get_order_from_hca,f_get_tubeid_from_hca,f_get_res_from_hca,f_get_alarm_from_hca,f_get_qc_id
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_address = ("127.0.0.2", 57000)
sock.bind(client_address)
sock.listen(1)
conn, addr = sock.accept()
str_continue = "y"
str_msg = ""
while str_continue != "n":
	str_date_today = datetime.today().strftime("%d%m%Y")
	fol_hca_archive_today = 'C:\\pierre\\apps\\python apps\\server\\hca_archive\\'+str_date_today+'\\'
	print("date =",str_date_today)
	os.makedirs(fol_hca_archive_today, exist_ok = True)
	dir = os.listdir()
	for file in dir:
		if file[-12:] == "_hca_msg.txt":
			print(file)
			str_order = f_get_order_from_hca(file)
			str_tubeid = f_get_tubeid_from_hca(file)
			if file[0:2] == "AB":
				str_qc_id = f_get_qc_id(file)
				print("QC result")
				print(str_qc_id)
			if file[0:2] != "AB":
				str_qc_id = ""
			try:
				str_res = f_get_res_from_hca(file)
			except Exception as e:
				print(e)
				print("no results found, returned 0")
				if str_qc_id[0:2] == "AB":
					str_res = "0~0~0~0~0~0~0~0"
				if str_tubeid[0:2] in ["01","09"]:
					str_res = "0~0~0~0~0~0~0~0"
				if str_tubeid[0:2] == "47":
					str_res = "0~0~0~0~0~0"
			try:
				str_alarm = f_get_alarm_from_hca(file)
			except Exception as e:
				print(e)
				print("no alarm found, returned nan")
				str_alarm = "nan"
			if str_qc_id[0:2] == "AB":
				str_msg = "H|qcresults\r\nqc|"+str_qc_id+"\r\ntest|"+str_qc_id+"|A1a~A1b~HbF~LA1c~SA1c~A0~Variant1~Variant2|"+str_res+"|Q3|00\r\n"
			if str_tubeid[0:2] in ["01","09"]:
				str_msg = "H|results\r\nP|lol\r\nO|"+str_order+"|O1\r\ntest|"+str_tubeid+"|A1a~A1b~HbF~LA1c~SA1c~A0~Variant1~Variant2|"+str_res+"|T3|"+str_alarm+"\r\n"
			if str_tubeid[0:2] == "47":
				str_msg = "H|results\r\nP|lol\r\nO|"+str_order+"|O1\r\ntest|"+str_tubeid+"|Hb F~Hb A0~Hb A2~Hb D+~Hb S+~Hb C+|"+str_res+"|T3|"+str_alarm+"\r\n"
			print("order =", str_order)
			print("tubeid =", str_tubeid)
			print("results string =",str_res)
			print("raw message =\n",str_msg)
			bytes_msg = bytes(str_msg, 'ISO-8859-1')
			conn.send(b'\x04')
			conn.send(b'\x02')
			conn.send(bytes_msg)
			conn.send(b'\x03')
			conn.send(b'\x05')
			print("message sent")
			shutil.copy2(file,fol_hca_archive_today)
			os.remove(file)
			str_msg = ""
			str_qc_id = ""
		if msvcrt.kbhit():
			str_continue = "n"
			break
		time.sleep(1)
