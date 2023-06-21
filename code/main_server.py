import socket
import pprint
from users_data_base import *
import base64
import threading
from class_Face import *
from Face_data_base import *
import rsa

#מבנה של הודעה 
#את כל ערך הנשלח לשרת מקיפות |
#1-בקשת יצירת שיחה
#1.2-אישור כניסה לשיחה
#1.3-סירוב כניסה לשיחה
#2-שינוי סיסמא
#3-הוספת משתמש
#4-כניסת משתמש קיים לתוכנה
# דוגמה למבנה הודעה
#|1|email|username|ip of the client who sent the request|
#הודעת פיענוח פנים תהיה שונה מהבקשות
#5 הכנסת המידע למסד פיענוח הפנים
#5.1-נגיעה באף
#5.2- נגיעה בפה
#5.3-נגיעה באוזן
#5.4-הנחת יד על המצח
#5.5-קיווץ הפה
#מבנה ההודעה
#מספר המוקף בקו |
#|1|

# def send_face_actions_to_the_interwered(image,ip_interviewd):
#     db=Face(image)
#     if db.Thouching_the_nose==True:
#         server_socket.sendto("|4|",ip_interviewd)
#     elif db.Thouching_the_mouth==True:
#         server_socket.sendto("|5|"+ip_interviewd)
#     elif db.Thouching_the_ear==True:
#         server_socket.sendto("|6|"+ip_interviewd)
#     elif db.Thouching_the_forehead==True:
#         server_socket.sendto("|7|"+ip_interviewd)
#     elif db.mouth_clenched==True:
#         server_socket.sendto("|8|"+ip_interviewd)

pp = pprint.PrettyPrinter(indent=4)

SEPARATOR = b'!!!'
MESSAGE_END = b'###'
FALSE = 'false'
TRUE = 'true'
RSA_PUBLIC_KEY = 'RSA_PUBLIC_KEY'
RSA_PRIVATE_KEY = 'RSA_PRIVATE_KEY'

class Server:
    CREAT_CONVERSATION='1'
    CALL_ENTRY_CONFIRMATION="1.2"
    DENYING_ENTRY_TO_CALL="1.3"
    CHANGE_PASSWORD='2'
    SIGNUP_REQUEST = '3'
    LOGIN_REQUEST = '4'
    THOUCHINGTHENOSE="5.1"
    THOUCHINGTHEMOUTH="5.2"
    THOUCHINGTHEEAR="5.3"
    THOUCHINGTHEFOREHEAD="5.4"
    MOUTHCLENCHED="5.5"
    
    CONVERSATION_PORT = 1357
    def __init__(self, port) -> None:
        self.port = port
        self.clients = dict()
        self.dict_face={"nose":0,"mouth_t":0,"clenched":0,"ear":0,"forehead":0}
        # clients[IP] => socket
        
    @staticmethod
    def get_all_data(sock: socket.socket):
        data = sock.recv(1024)
        while not data.endswith(b"###"):
            data += sock.recv(1024)
        return data
        
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

    def creatconversation(self,client: socket.socket, data ,addr):
        username_interviewee = data["USERNAME"]
        email = data['EMAIL']
        db=ZoomItDB()
        ip_interviewee=db.get_user_ip("users_u",username_interviewee)
        user = db.get_user_by_email(email)
        interviewer_ip=db.get_user_ip("users_s","siv")
        #בקשה ליצירת שיחה
        with socket.create_connection((ip_interviewee, self.CONVERSATION_PORT)) as sock:
            call_request = self.create_message(self.CALL_ENTRY_CONFIRMATION, {
                'FIRST_NAME': user['name_u'],
                'IP': addr,
                "IP_INTERVIEWER": interviewer_ip
            })
            sock.send(call_request)
            data = self.get_all_data(sock)
        parameters = self.extract_parameters(data)
        # מחזיר true
        if parameters['RESULT'] == TRUE:
            message = self.create_message(self.CALL_ENTRY_CONFIRMATION, {
                'RESULT': TRUE,
                'IP': ip_interviewee,
                'PORT': str(self.CONVERSATION_PORT)
            })
        else:
            message = self.create_message(self.DENYING_ENTRY_TO_CALL, {
                'RESULT': FALSE,
            })
        encrypted_message=self._prepare_message(message,addr)
        client.send(encrypted_message)

    def change_password(self,client: socket.socket,data, addr):
        db=ZoomItDB()
        passw=data["PASSWORD"]
        table_name="users_u"
        email=data["EMAIL"]
        db.update_passw(table_name,passw,email)
        message= self.create_message(self.CHANGE_PASSWORD,{
            "RESULT":TRUE
        })
        encrypted_message = self._prepare_message(message, addr)
        client.send(encrypted_message)

    
    def dict_face_adding(self,data):
        if data=="5.1":
            self.dict_face["nose"]+=1
        elif data=="5.2":
            self.dict_face["mouth_t"]+=1
        elif data=="5.3":
            self.dict_face["ear"]+=1
        elif data=="5.4":
            self.dict_face["forehead"]+=1
        elif data=="5.5":
            self.dict_face["clenched"]+=1
    
    def Adding_to_face_data(self):
        face=Facedatabase()
        face.insert("face",T_mouth=self.dict_face["mouth_t"],T_nose=self.dict_face["nose"],
                    T_ear=self.dict_face["ear"],T_forehead=self.dict_face["forehead"],
                    C_mouth=self.dict_face["clenched"],interviewer_name="",interviewee_name="",mail_interviewer="")
    
    def signup(self,client: socket.socket,data,addr):
        db=ZoomItDB()
        fname=data["FIRST_NAME"]
        lname=data["LAST_NAME"]
        email=data["EMAIL"]
        passw=data["PASSWORD"]
        username=data["USERNAME"]
        type_user=data["TYPE"]
        print(type_user)
        ip=data["IP"]
        if db.checking_if_user_is_taken(username,"users_u")!=True:
            if db.cheking_if_email_is_taken(email,"users_u")!=True:
                db.insert('users_u',ip,name_u=fname,lastname=lname, mail=email,username=username,password_u=passw,userstate=type_user,conectionstate=0)
                server_response = self.create_message(
                    self.SIGNUP_REQUEST,{
                        "RESULT":TRUE
                    }
                )
            else:
              server_response = self.create_message(
                  self.SIGNUP_REQUEST,{
                      "RESULT":FALSE,
                      "REASON": 'email'
                  }

              )
        else:
            server_response = self.create_message(
                self.SIGNUP_REQUEST,{
                    "RESULT":FALSE,
                    "REASON": 'username'
                }
            )
        encrypted_message = self._prepare_message(server_response, addr)
        client.send(encrypted_message)
            
    
    def login(self, client: socket.socket, data,addr):
        db=ZoomItDB()
        password_u=data["PASSWORD"] 
        username_u=data["USERNAME"]
        print(password_u, username_u)
        if db.sign_in_check(password_u,username_u,"users_u")==True:
            db.update_conection_state(1,'users_u',username_u)
            user_first_name=db.get_user_name('users_u',username_u)
            type_of_client= db.get_userstate('users_u',username_u)
            server_response=self.create_message(self.LOGIN_REQUEST,{
                "RESULT":TRUE,
                "TYPE":str(type_of_client),
                "FIRST_NAME":user_first_name
            }
            )
            encrypted_message = self._prepare_message(server_response, addr)
            client.send(encrypted_message)
        else:
            server_response=self.create_message(
                self.LOGIN_REQUEST, {
                    "RESULT": FALSE
                }
            )
            encrypted_message = self._prepare_message(server_response, addr)            
            client.send(encrypted_message) 
            
    def do_handshake(self, client: socket.socket, data, addr: str):
        client_public_key = rsa.PublicKey(int(data['n']), int(data['e']))
        self.clients[addr][RSA_PUBLIC_KEY] = client_public_key
        server_public_key, private_key = rsa.newkeys(1024)
        self.clients[addr][RSA_PRIVATE_KEY] = private_key
        message = self.create_message(0, {
            "n": str(server_public_key.n),
            "e": str(server_public_key.e)
        })
        client.send(message)
    
    def _prepare_message(self, message, addr):
        return rsa.encrypt(message, self.clients[addr][RSA_PUBLIC_KEY]) + b"###"

    def _decrypt_message(self, encrypted, addr):
        encrypted = encrypted[:-len(MESSAGE_END)]
        return rsa.decrypt(encrypted, self.clients[addr][RSA_PRIVATE_KEY])
        
    def handle_client(self, client, addr):
        """
        Takes a client and sends him to his request
        """
        print("--------------------------------------")
        data = self.get_all_data(client)
        functions = {
            self.CREAT_CONVERSATION: self.creatconversation,
            self.CHANGE_PASSWORD: self.change_password,
            self.SIGNUP_REQUEST: self.signup,
            self.LOGIN_REQUEST: self.login,
            self.THOUCHINGTHENOSE: self.dict_face_adding,
            self.THOUCHINGTHEMOUTH: self.dict_face_adding,
            self.THOUCHINGTHEEAR: self.dict_face_adding,
            self.THOUCHINGTHEFOREHEAD: self.dict_face_adding,
            self.MOUTHCLENCHED: self.dict_face_adding
        }
        addr = addr[0]
        pp.pprint(self.clients)
        if not (addr in self.clients):
            self.clients[addr] = dict()
        if not self.clients[addr].get(RSA_PUBLIC_KEY):
            parameters = self.extract_parameters(data)
            self.do_handshake(client, parameters, addr)
            return
        print(addr)
        print("THE SERVER REACEHD THE DECRYPTION")
        decrypted = self._decrypt_message(data, addr)
        print(decrypted)
        parameters = self.extract_parameters(decrypted)
        num_of_request=parameters['REQUEST']
        functions[num_of_request](client, parameters, addr)
        client.close()
    
        
    
    def mainloop(self):
        """
        Start server. start threads to the handle_client method
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.port))
        server.listen()
        print("server is up")
        threads = []
        while True:
            client, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
        server.close()
        
if __name__ == '__main__':
    Server(1337).mainloop()