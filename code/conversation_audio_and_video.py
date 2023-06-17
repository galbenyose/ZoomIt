import cv2
import numpy as np
import socket
import threading
import pyaudio
from tkinter import *
from PIL import Image, ImageTk


# IP address and port for video streaming
HOST = '127.0.0.1' 
PORT = 12345

# Constants for audio streaming
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize video capture
cap = cv2.VideoCapture(0)  

# Initialize audio stream
audio_stream = pyaudio.PyAudio()
audio_stream_output = audio_stream.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    frames_per_buffer=CHUNK_SIZE,
    output=True
)
audio_stream_input = audio_stream.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    frames_per_buffer=CHUNK_SIZE,
    input=True
)

# Function to receive frames from the other participant
def receive_frames():
    global cap
    global video_frame
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, _ = sock.accept()
    while True:
        data = b''
        while len(data) < 921600:  # Adjust this value based on your frame size
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        video_frame = np.frombuffer(data[:921600], dtype=np.uint8).reshape((480, 640, 3))
        video_frame=cv2.flip(video_frame,1)
        return video_frame
        #cv2.imshow('Video Conference', video_frame)
        #label = Label(root, image=video_frame)
        #label.pack()
        
        if cv2.waitKey(1) == ord('q'):
            break
    conn.close()
    sock.close()
    
def converstion_page_design():
    root = Tk()
    root.title("ZOOM IT")
    root.configure(bg="black")
    # Create and start the threads
    receive_audio_thread = threading.Thread(target=receive_audio)
    receive_audio_thread.start()
    while True:
        img = Image.fromarray(receive_frames())
        imgtk= ImageTk.PhotoImage(image=img)
        lable=Label(root)
        lable.imgtk = imgtk
        lable.configure(image=imgtk)
        root.mainloop()
    # Wait for the threads to finish
    receive_video_thread.join()
    send_video_thread.join()
    receive_audio_thread.join()
    send_audio_thread.join()
    
def send_audio_and_frames_to_te_client():
    send_video_thread = threading.Thread(target=send_frames)
    send_audio_thread = threading.Thread(target=send_audio)
    send_video_thread.start()
    send_audio_thread.start()

        

# Function to send frames to the other participant
def send_frames():
    #global cap
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        ret, video_frame = cap.read()
        if not ret:
            break
        data = video_frame.tobytes()
        sock.sendto(data, (HOST, PORT))
    sock.close()

# Function to receive audio from the other participant
def receive_audio():
    global audio_stream_output
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT + 1))
    sock.listen(1)
    conn, _ = sock.accept()
    while True:
        data = conn.recv(CHUNK_SIZE)
        audio_stream_output.write(data)
    conn.close()
    sock.close()


# Function to send audio to the other participant
def send_audio():
    global audio_stream_input
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT + 1))
    while True:
        data = audio_stream_input.read(CHUNK_SIZE)
        sock.sendall(data)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

# Create and start the threads
receive_video_thread = threading.Thread(target=receive_frames)
send_video_thread = threading.Thread(target=send_frames)
receive_audio_thread = threading.Thread(target=receive_audio)
send_audio_thread = threading.Thread(target=send_audio)
receive_video_thread.start()
send_video_thread.start()
receive_audio_thread.start()
send_audio_thread.start()

# Wait for the threads to finish
receive_video_thread.join()
send_video_thread.join()
receive_audio_thread.join()
send_audio_thread.join()

def close_conversation():
# Release resources
   cap.release()
   cv2.destroyAllWindows()
   audio_stream.close()
#   stream.stop_stream()
#   stream.close()
#   audio.terminate()




# יצירת שיחה
#וידיאו ואודיו מחוברים