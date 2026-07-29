import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1,hexdump
import socket
import os
import binascii
import msvcrt
import codecs
from LibPCap import f_tcp_ipv4_data
s = scapy.conf.L3socket(filter="tcp and ip host 10.210.224.200")
list_msg_data = []
while True:
	packet = s.recv()
	str_msg = str()
	if type(packet) != type(None):
		load = scapy.raw(packet)
		hex_list = []
		hex_bytes = binascii.hexlify(load)
		if packet.src == "10.210.224.200":
			str_hex_code = str(binascii.hexlify(load,'-'))[2:-1]
			str_hex_element = str()
			list_hex_data = []
			int_is_msg = 0
			for i in str_hex_code:
				if i.isalpha() or i.isdigit():
					str_hex_element = str_hex_element + i
				if i == "-":
					list_hex_data.append(str_hex_element)
					str_hex_element = str()
			try:
				list_hex_tcp_data = f_tcp_ipv4_data(list_hex_data)[7]
#				list_msg_data = []
				if list_hex_tcp_data[0:2] == ["0b","4d"]:
					int_is_msg = 1
#					print(list_hex_tcp_data)
					list_msg_data = []
					for i in list_hex_tcp_data:
						list_msg_data.append(i)
				if list_hex_tcp_data[-2:] == ["0d","1c"]:
#					print(list_hex_tcp_data)
					for i in list_hex_tcp_data:
						list_msg_data.append(i)
					str_row=str()
					for i in list_msg_data:
						if i not in ["0b","0d"]:
							str_row = str_row + i
#							print(bytearray.fromhex(str_row).decode())
						if i in ["0b","0d"]:
							try:
								str_row_ascii = bytearray.fromhex(str_row).decode("ISO-8859-1")
							except Exception as e:
								print(e)
								print("can't decode str_row")
								str_row_ascii = str_row
							print(str_row_ascii)
							str_msg = str_msg + str_row_ascii + "\n"
							try:
								with open("cob_msg_log.txt","a",encoding="utf-8") as log_file:
									log_file.write(str_row_ascii)
									log_file.write("\n")
							except Exception as e:
								print("can't log the line")
								print(e)
								with open("cob_msg_log.txt","w",encoding="utf-8") as log_file:
									log_file.write(str_row_ascii)
									log_file.write("\n")
							except Exception as e:
								print(e)
								print("move on to next line")
							str_row = str()
						int_is_msg = 0
				if list_hex_tcp_data[0:2] != ["0b","4d"] and list_hex_tcp_data[-2:] != ["0d","1c"]:
					for i in list_hex_tcp_data:
						list_msg_data.append(i)
#					print(list_msg_data)
			except Exception as e:
				print(e)
				print("nothing to see here")