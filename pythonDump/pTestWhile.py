import socket
import sys
import protocols
from protocols.ipv4 import IPv4

PACKET_SIZE = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

sock.bind(("0.0.0.0", 0))

try:
    while True:
        # read in a packet
        raw_buffer = sock.recvfrom(PACKET_SIZE)[0]
        # create an IP packet object
        ip_header = IPv4(raw_buffer)
        # print the packet
        print(ip_header)
except KeyboardInterrupt:
    print("\nExiting...")
    sock.close()
    sys.exit(0)