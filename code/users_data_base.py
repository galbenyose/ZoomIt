import mysql.connector
import hashlib
import random



class ZoomItDB:
    def __init__(self):
        return
    def _open(self):
        
        self._conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Galor2021',
            database='zoomit'
        )
        print('------------------------------')
        self._cur = self._conn.cursor(dictionary=True)
    
    def _close(self):
        self._cur.close()
        self._conn.close()
        
    @staticmethod
    def generate_salt():
        return str(random.randrange(1,1000))
        
    def salt_passw(self,passw, salt):
        return hashlib.sha256(str(passw+salt).encode()).hexdigest()
    
    def ip_Encryption(self,id):
        pass
    
    def insert(self, table_name, ip_user, **kwargs):
        print(kwargs)
        kwargs['client_ip']= ip_user
        kwargs['salt'] = self.generate_salt()
        kwargs['password_u'] = self.salt_passw(kwargs['password_u'], kwargs['salt'])
        query = f"INSERT INTO {table_name} ("
        for key in kwargs.keys():
            query += f"{key}," # (key1,key2
        query = query[:-1]
        query += ") VALUES ("
        for _ in kwargs.values():
            query += r"%s,"
        query = query[:-1]
        query += ");"
        self._open()
        inserted = False
        print(tuple(kwargs.values()))
        print(query, tuple(kwargs.values()))
        try:
            self._cur.execute(query, tuple(kwargs.values()))
            self._conn.commit()
        except Exception as err:
            print(str(err))
            raise
        else:
            inserted = True
        finally:
            self._close()
            return inserted
    
    def sign_in_check(self,password,username_u,table_name):
        #checking if the client in exist( if the username and the password are correct)
        print("SIGN IN START")
        check= True
        self._open()
        query_salt=f"SELECT salt FROM {table_name} Where username='{username_u}'"
        print(query_salt)
        self._cur.execute(query_salt)
        salt = self._cur.fetchone()
        if salt is None:
            return False
        salt_e=str(salt['salt'])
        passw_test=hashlib.sha256(str(password+salt_e).encode()).hexdigest()
        quert_passw=f" SELECT password_u FROM {table_name} Where username='{username_u}'"
        self._cur.execute(quert_passw)
        passw = self._cur.fetchone()
        passw_e=passw['password_u']
        print(passw_e, passw_test, sep='\n')
        if passw_test != passw_e:
            check= False
        
        return check
            

    def update_passw(self,table_name,passw,mail):
        # updating the password of the client 
        self._open()
        query_salt=f" SELECT salt FROM {table_name} Where mail=%s"
        self._cur.execute(query_salt,(mail,))
        salt = self._cur.fetchone()
        salt_for_new_pass=str(salt['salt'])
        new_passw=hashlib.sha256(str(passw+salt_for_new_pass).encode()).hexdigest()
        query_update=f" UPDATE {table_name} SET password_u={new_passw} Where mail=%s"
        self._cur.execute(query_update,(mail,))
        self._conn.commit()
    
    def update_state(self,userstate_new,table_name,mail):
        self._open()
        query_update =f"UPDATE {table_name} SET userstate= {userstate_new} Where mail=%s "
        self._cur.execute(query_update,(mail,))
        self._conn.commit()
        
    
    def update_conection_state(self,con_num,table_name,username):
        self._open()
        query_update =f"UPDATE {table_name} SET conectionstate={con_num} WHERE username=%s "
        self._cur.execute(query_update, (username,))
        self._conn.commit()
    
    
    def get_userstate(self,table_name,username_u):
        self._open()
        query_state=f"SELECT * FROM {table_name} WHERE username=%s"
        self._cur.execute(query_state,(username_u,))
        state=self._cur.fetchone()
        print(state)
        state_e=state['userstate']
        print(state_e)
        return state_e
    
    def get_user_name(self,table_name,username_u):
        self._open()
        query_state=f"SELECT name_u FROM {table_name} WHERE username=%s"
        self._cur.execute(query_state,(username_u,))
        name=self._cur.fetchone()
        user_n=name['name_u']
        print(user_n)
        return user_n
        
    def conected_people_username(self, table_name, conect=1):
        self._open()
        query_lst_connect_p=f" SELECT * FROM {table_name} WHERE conectionstate=%s"
        self._cur.execute(query_lst_connect_p,(conect,))
        lst_connect=self._cur.fetchall()
        lst_connect_u=list()
        i=1
        for ls in lst_connect:
            lst_connect_u.append(str(i)+" "+ls['username'])
            i+=1
        return lst_connect_u
    #פסיק על מנת שיהיה Tupel
    
    def conected_people_firstname(self, table_name, conect=1):
        self._open()
        query_lst_connect_p=f" SELECT * FROM {table_name} WHERE conectionstate=%s"
        self._cur.execute(query_lst_connect_p,(conect,))
        lst_connect=self._cur.fetchall()
        #מחזיר רשימה של מילונים
        lst_connect_n=list()
        i=1
        for ls in lst_connect:
            lst_connect_n.append(str(i)+" "+ls['name_u'])
            i+=1
        return lst_connect_n
    
    
    def get_user_ip(self, table_name,username):
        self._open()
        query_state=f"SELECT client_ip FROM {table_name} WHERE username=%s"
        self._cur.execute(query_state,(username,))
        client=self._cur.fetchone()
        client_ip=client['client_ip']
        print(client_ip)
        return client_ip
    
    def updat_client_id(self, table_name, username, id_user):
        self._open()
        id=self.id_Encryption(id_user)
        query_update =f"UPDATE {table_name} SET client_id= {id} WHERE username=%s "
        self._cur.execute(query_update, (username,))
        self._conn.commit()
        
    def checking_if_user_is_taken(self,username, table_name):
        self._open()
        query_lst_username=f"SELECT * FROM {table_name} WHERE username=%s"
        self._cur.execute(query_lst_username,(username,))
        lst_username_taken= self._cur.fetchone()
        if lst_username_taken is None:
            return False
        return True
    
    def cheking_if_email_is_taken(self,email,table_name):
        self._open()
        query_lst_email=f"SELECT * FROM {table_name} WHERE mail=%s"
        self._cur.execute(query_lst_email,(email,))
        lst_email_taken = self._cur.fetchone()
        if lst_email_taken is None:
            return False
        return True
    
    def get_user_by_email(self, email: str):
        self._open()
        self._cur.execute("SELECT * FROM users_u WHERE mail=%s", (email,))
        val = self._cur.fetchone()
        self._close()
        return val
    