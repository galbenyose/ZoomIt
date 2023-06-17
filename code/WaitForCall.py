import socket
import base64

SEPARATOR = b'!!!'
MESSAGE_END = b'###'
FALSE = 'false'
TRUE = 'true'

class WaitForCall:
    CREAT_CONVERSATION = '1'
    ACCEPT_CONVERSATION = '1.2'
    REJECT_CONVERSATION = '1.3'
    PORT = 1357
    IP = '0.0.0.0'
    
    
    def __init__(self, main_server_adrss):
        # IPv4 => 12.127.32.52
        self.main_server_address = main_server_adrss
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = server_socket
        

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

    @staticmethod
    def get_all_data(sock: socket.socket):
        data = sock.recv(1024)
        while not data.endswith(b"###"):
            data += sock.recv(1024)
        return data
    
    def wait_for_connection(self) -> dict[str, str]:
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen(1)
        main_server_socket, addr = self.socket.accept()
        print(addr, self.main_server_address)
        while not addr[0] == self.main_server_address:
            main_server_socket.close()
            main_server_socket, addr = self.socket.accept()
        self.main_server_socket = main_server_socket
        return self.extract_parameters(self.get_all_data(main_server_socket))
    
    def accept_conversation(self):        
        message = self.create_message(self.ACCEPT_CONVERSATION, {
            'RESULT': TRUE    
        }) #TODO create message
        self.main_server_socket.send(message)
        
    def reject_conversation(self):        
        message = self.create_message(self.REJECT_CONVERSATION, {
            'RESULT': FALSE    
        }) #TODO create message
        self.main_server_socket.send(message)
        
