from scapy.all import *

#sport = random.randint(1024, 65535)
sport = 55000

# SYN
ip = IP(src='10.14.1.40', dst='10.210.236.99')
SYN = TCP(sport=sport, dport=80, flags='S', seq=1000)
SYNACK = sr1(ip/SYN)

# SYN-ACK
ACK = TCP(sport=sport, dport=80, flags='A', seq=SYNACK.ack + 1, ack=SYNACK.seq + 1)
send(ip/ACK)