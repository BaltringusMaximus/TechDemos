import scapy.all as scapy
from scapy.all import raw,IP,TCP,send,sr1
import socket
import os
import binascii
import msvcrt

s = scapy.conf.L2socket(filter="tcp")

while True:
	packet = s.recv()
	if type(packet) != type(None):
		load = scapy.raw(packet)
		str_code=load.decode("ISO-8859-1")
		str_hex_code = str(binascii.hexlify(load))
		str_hex_data = str_hex_code[82:86]
		print(str_code)
		print(str_hex_code)
		if packet.src == "10.210.236.99":
			print("full data =", str_code)
			print("data =", str_hex_data)
			print(packet.seq)
			print(packet.ack)
#			ACK = TCP(sport=sport, dport=4003, flags='A', seq=packet.seq+1, ack=packet.ack+1)
#			send(ip/ACK)
#			print(packet.getlayer(raw))
#			tcp_seg_len = len(packet.getlayer(raw).load)
#			ans_ack,unans_ack = sr(IP(dst=ip)/TCP(sport=packet[1].dport, dport=packet[1].sport, seq=packet[1].ack, ack=packet[1].seq + tcp_seg_len,flags="A"),verbose=0, timeout=1)
			file_log.write("====")
			file_log.write("\n")
			file_log.write(str_hex_data)
			file_log.write("\n")
			file_log.write(str_hex_code)
			file_log.write("\n")
		if msvcrt.kbhit():
			break