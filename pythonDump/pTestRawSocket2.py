import socket
import os

# Check for administrative privileges
#if os.getpid() != 0:
#    print("You need to run this script as administrator.")
#    exit(1)

try:
    # Create a raw socket for capturing all IP packets
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    
    # Set socket option to include IP headers
    raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Bind to all interfaces
    raw_socket.bind(('10.14.1.40', 56000))

    print("Listening for packets...")

    while True:
        packet = raw_socket.recvfrom(65565)
        data = raw_socket.recv(4096)
        data.hex()
#        print(f"Packet received: {packet[0]}")
        print(data)

except OSError as e:
    print(f"OSError: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    raw_socket.close()