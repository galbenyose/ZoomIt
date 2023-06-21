import socket
import tkinter
import threading
from PIL import Image, ImageTk

#  udp server


def recv_frames_and_update_tkinter():
    global imagetk, button, window, sock
    while True:
        data, addr = sock.recvfrom(65535 * 8)
        filename = 'temp.jpg'
        with open(filename, 'wb') as f:
            f.write(data)
        image = Image.open(filename)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        imagetk = ImageTk.PhotoImage(image)
        button.config(image=imagetk)
        window.update()


def window_mainloop():
    global window, button, imagetk
    window = tkinter.Tk()
    button = tkinter.Button(window)
    imagetk = None
    button.pack()
    window.mainloop()
    
    
window = None
button = None
imagetk = None
        
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 1337))



mainloop_thread = threading.Thread(target=window_mainloop)
mainloop_thread.start()
thread = threading.Thread(target=recv_frames_and_update_tkinter)
thread.start()