import socket
import cv2
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

print('asdasd' + str(cap))

while True:
    ret, data = cap.read()
    data = cv2.resize(data, (320, 240))
    filename = 'temp.jpg'
    cv2.imwrite(filename, data)
    with open(filename, 'rb') as f:
        sock.sendto(f.read(), ('10.92.13.182', 1337))
    time.sleep(0.1)