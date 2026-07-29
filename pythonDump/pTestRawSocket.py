import socket
import struct
import time

# Create a raw socket
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

# Set the socket option to include the IP header
raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# Prepare the packet
#src_ip = '192.168.1.2'
#dst_ip = '192.168.1.1'
#packet = b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\xb1\xe6\xc0\xa8\x01\x02\xc0\xa8\x01\x01'
#packet += b'Hello from raw socket'

# Send the packet
#raw_socket.sendto(packet, (dst_ip, 0))
#print(f"Packet sent to {dst_ip}")
address = ("10.210.224.200",51564)
try:
	raw_socket.connect(address)
	print("bound")
	raw_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
except Exception as e:
	print(f"Unexpected error: {e}")
while True:
	print(socket.gethostbyname(socket.gethostname()))
	print("waiting")
	raw_socket.send(b'hello')
	time.sleep(1)
#	data = raw_socket.recv(4096)
#	print(data)
#	print(data.hex())
#	if "0ad2e0c8" in data.hex():
#		print("from said ip")
#	print(type(data.hex()))
#	str_data = data.decode("ISO-8859-1")
#	print(str_data)