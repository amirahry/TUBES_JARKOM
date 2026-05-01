import socket

MCAST_GRP = '224.1.1.1'
PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "Hello Multicast"
sock.sendto(msg.encode(), (MCAST_GRP, PORT))