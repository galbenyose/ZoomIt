import mysql.connector
import time

class Facedatabase:
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
    
    def insert(self, table_name, **kwargs):
        time_call= time.time()
        kwargs["calltime"]=time_call
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
        print(query % tuple(kwargs.values()))
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
    
    def print_lst_of_converstion(self,table_name,interwere_name,email):
        self._open()
        query_lst_converstion=f"SELECT * FROM {table_name} WHERE interwere_name=%s AND mail=%s"
        self._cur.execute(query_lst_converstion,(interwere_name,email,))
        lst_converstion=self._cur.fetchone()
        #לחזור לבדוק
        #להרכיב לולאה שמדפיסה הכל כל תא במילון שווה לשם במסד של הערך
        # מחזיר את המילון לטפל בפעולת הצגת שיחה
        return lst_converstion
    
    def lst_conversition_of_specific_interwerer(self,table_name,interwed_name,interwere_name):
        self._open()
        query_lst_converstion=f"SELECT * FROM {table_name} WHERE interwere_name=%s AND interwed_name=%s"
        self._cur.execute(query_lst_converstion,(interwere_name,interwed_name,))
        lst_converstion=self._cur.fetchone()
        return lst_converstion

