import pyaudio
import base64
from PIL import Image, ImageTk
import socket
import cv2
import numpy as np
import rsa
from class_Face import *

SEPARATOR = b'!!!'
MESSAGE_END = b'###'
FALSE = 'false'
TRUE = 'true'


class Client:
    #מחלקת לקוח כללית כוללת בתוכה פעולות כלליות 
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
    
    @staticmethod
    def create_message(request_number: int, parameters: dict[str, str]) -> bytes:
        parameters['REQUEST'] = str(request_number) # 
        message = b'|' 
        for key, value in parameters.items():
            b64_key = base64.b64encode(key.encode())
            b64_value = base64.b64encode(str(value).encode())
            message += b64_key + SEPARATOR + b64_value + b'|'
        return message + MESSAGE_END

    @staticmethod    
    def extract_parameters(message: bytes) -> dict[str, str]:
        message = message.strip(b'#')
        message = message.strip(b'|')
        splitted = message.split(b'|')
        parameters = dict() # REQUEST!!!1, RESULT!!!true
        values = [item.split(SEPARATOR) for item in splitted]
        for b64_key, b64_value in values:
            key = base64.b64decode(b64_key).decode()
            value = base64.b64decode(b64_value).decode()
            parameters[key] = value
        return parameters

        
    def send_and_recv(self, message: str) -> dict[str, str]:
        # encryted = encrypt(message)
        with socket.create_connection((self.ip, self.port)) as sock:
            sock.send(message)
            data = sock.recv(1024)
            while not data.endswith(b'###'):
                data += sock.recv(1024)
        return data
    

class CallClient(Client):
    # Constants for audio streaming
    global CHUNK_SIZE 
    CHUNK_SIZE = 2048
    global FORMAT
    FORMAT = pyaudio.paInt16
    global CHANNELS 
    CHANNELS = 1
    global RATE
    RATE = 44100
    PORT = 12345
    
    
    THOUCHINGTHENOSE="5.1"
    THOUCHINGTHEMOUTH="5.2"
    THOUCHINGTHEEAR="5.3"
    THOUCHINGTHEFOREHEAD="5.4"
    MOUTHCLENCHED="5.5"
    
    
    def __init__(self, ip: str) -> None:
        super().__init__(ip, self.PORT)
        # Initialize video capture
        self.CAP= cv2.VideoCapture(0)
        # Initialize audio stream
        audio_stream = pyaudio.PyAudio()
        self.audio_stream_output = audio_stream.open(
            
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK_SIZE,
            output=True
        )
        self.audio_stream_input = audio_stream.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        frames_per_buffer=CHUNK_SIZE,
        input=True
        )
    
    # Function to receive frames from the other participant
    
    def receive_frames(self):
        global video_frame
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))
        while True:
           data = b''
           while len(data) < 921600:  # Adjust this value based on your frame size
               packet, _ = sock.recvfrom(4096)
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
        
    def send_frames(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            ret, video_frame = self.CAP.read()
            if not ret:
               break
            data = video_frame.tobytes()
            data_length = len(data)
            chunks = data_length // CHUNK_SIZE
            for i in range(chunks):
                sock.sendto(data[i*CHUNK_SIZE: (i+1) * CHUNK_SIZE], (self.ip, self.port))
        sock.close()
    
    # Function to receive audio from the other participant
    def receive_audio(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port+1))
        while True:
           data, _ = sock.recvfrom(CHUNK_SIZE)
           self.audio_stream_output.write(data)
        conn.close()
        sock.close()
        
    # Function to send audio to the other participant
    def send_audio(self):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = (self.ip, self.port + 1)
        while True:
           data = self.audio_stream_input.read(CHUNK_SIZE)
           sock.sendto(data, addr)
        sock.close()
    
    def Face_decoding(self,image):
        face=Face(image)
        if face.Thouching_the_ear()==True:
            message=self.create_message(self.THOUCHINGTHEEAR)
            response_from_the_server = self.send_and_recv(message)
            return self.THOUCHINGTHEEAR
        
        elif face.mouth_clenched()==True:
            message = self.create_message(self.MOUTHCLENCHED)
            response_from_the_server=self.send_and_recv(message)
            return self.MOUTHCLENCHED
        
        elif face.Thouching_the_forehead()==True:
            message = self.create_message(self.THOUCHINGTHEFOREHEAD)
            response_from_the_server=self.send_and_recv(message)
            return self.THOUCHINGTHEFOREHEAD
        
        elif face.Thouching_the_mouth()==True:
            message = self.create_message(self.THOUCHINGTHEMOUTH)
            response_from_the_server=self.send_and_recv(message)
            return self.THOUCHINGTHEMOUTH
        
        elif face.Thouching_the_nose()== True:
            message = self.create_message(self.THOUCHINGTHENOSE)
            response_from_the_server=self.send_and_recv(message)
            return self.THOUCHINGTHENOSE
        
        
    

class User(Client):
    #מחלקת משתמש יורשת ממחלקת לקוח וכוללת בתוכה פעולות של העברת מידע בין השרת ללקוח 
    CREATCONVERSATION ='1'
    CHANGE_PASSW ='2'
    SIGN_UP_REQUEST = '3'
    LOGIN_REQUEST = '4'
    
    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port)
            
    def do_handshake(self):
        public_key, private_key = rsa.newkeys(1024)
        self.private_key = private_key
        message = self.create_message(0, {
            'N': str(public_key.n),
            'E': str(public_key.e)
        })
        data = self.send_and_recv(message)
        server_public_key = rsa.PublicKey(int(data['N']), int(data['E']))
        self.public_key = server_public_key
    
    def adding_data_to_face_database(self):
        pass
        
    def login(self, username: str, password: str):
        # create a message
        # JSON / create one
        message = self.create_message(self.LOGIN_REQUEST, {
            'USERNAME': username,
            'PASSWORD': password
        })
        encrypted = self._prepare_message(message)
        encrypted_data = self.send_and_recv(encrypted)
        server_response = self._decrypt_message(encrypted_data)
        # do what you want with response    
        # |4|True|
        if server_response['RESULT'] == TRUE:
            return server_response
        return False
    
    def sign_up(self, 
                email: str, 
                password: str, 
                username: str, 
                lname: str,
                type: str,
                fname: str):
        
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        message = self.create_message(
            self.SIGN_UP_REQUEST, {
                "EMAIL":email,
                "PASSWORD":password,
                "USERNAME":username,
                "LAST_NAME":lname,
                "TYPE":type,
                "FIRST_NAME":fname,
                "IP":ip
            }
        )
        encrypted = self._prepare_message(message)
        encrypted_data = self.send_and_recv(encrypted)
        server_response = self._decrypt_message(encrypted_data)
        #|3|True|-return true
        #|3|False|-return false to say that the email or the username are exist
        return server_response
    
    def change_password(self,password: str,table_name: str,email:str):
        message= self.create_message(self.CHANGE_PASSW,{
            "PASSWORD":password,
            "table_name":table_name,
            "EMAIL":email
            })    
        encrypted = self._prepare_message(message)
        encrypted_data = self.send_and_recv(encrypted)
        server_response = self._decrypt_message(encrypted_data)
        #|2|True|-to say that the password update
        if server_response["RESULT"]=='True':
            return True
        return False
    
    def _prepare_message(self, message):
        return rsa.encrypt(message, self.public_key)
    
    def _decrypt_message(self, encrypted):
        return self.extract_parameters(rsa.decrypt(encrypted, self.private_key))
        
    def creatconvesation(self,email: str,username: str):
        message=self.create_message(self.CREATCONVERSATION, {
            'EMAIL': email,
            'USERNAME': username
        })
        encrypted = self._prepare_message(message)
        encrypted_data = self.send_and_recv(encrypted)
        server_response = self._decrypt_message(encrypted_data)
        if server_response["RESULT"]==TRUE: # RESULT = 1, IP = 3  username = 2
            return server_response
        else:
            return False
    
    
