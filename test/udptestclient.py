import socket
import cv2
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)


while True:
    ret, data = cap.read()
    data = cv2.resize(data, (320, 240))
    filename = 'temp.jpg'
    cv2.imwrite(filename, data)
    with open(filename, 'rb') as f:
        sock.sendto(f.read(), ('192.168.68.74', 1337))
    time.sleep(0.1)