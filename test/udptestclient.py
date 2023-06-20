import socket


#  ip - Internet Protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


with open('At_sign.svg.png', 'rb') as f:
    data = f.read()
sock.sendto(data, ('192.168.68.74', 1333))