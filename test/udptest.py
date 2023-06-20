import socket

#  udp server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 1337))

data, addr = sock.recvfrom(65535 * 8)

with open('recved.png', 'wb') as f:
    f.write(data)