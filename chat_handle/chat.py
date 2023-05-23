import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from user_handle.user_get import User
import datetime
from user_handle.modules.random_user_id import generate_random_chat_id

class ChatUsers():
    def __init__(self, name_user1, name_user2):
        self.user1 = User(name_user1)
        self.user2 = User(name_user2)
        engine = create_engine('sqlite:///db_handle/chat.db')
        Session = sessionmaker(bind=engine)
        self.session_db = Session()
        exist_table = self.check_if_table_exist()
        
        if not exist_table:
            self.creat_chat_db()
        
        self.chat_id = self.get_chat_id()

        
    
    def check_if_table_exist(self):
        query = text(f"""SELECT name FROM sqlite_master WHERE type='table'
            AND name='chat_{self.user1.user_id}_{self.user2.user_id}'; """)
        result = self.session_db.execute(query).fetchall()
        self.session_db.close()
        if result == []:
            return False
        else:
            return True
                
    def creat_chat_db(self):
        try:
            chat_id = generate_random_chat_id(self.user1.user_id+self.user2.user_id)
            query = text(f"""CREATE TABLE IF NOT EXISTS chat_{self.user1.user_id}_{self.user2.user_id}(
                'id' INTEGER UNIQUE,
                'message' TEXT,
                'client_id' TEXT,
                'name' TEXT,
                'date' TEXT,
                'hour' TEXT,
                'chat_id' TEXT DEFAULT '{chat_id}',
                PRIMARY KEY('id' AUTOINCREMENT)
                )
                """)
            self.session_db.execute(query)
            self.session_db.commit()
            self.session_db.close()
            
        except Exception as e:
            print(e)
  
    def get_all_messages(self):
        try:
            query = text(f"""SELECT * FROM chat_{self.user1.user_id}_{self.user2.user_id}""")
            result = self.session_db.execute(query).fetchall()
            self.session_db.close()
            return result
        except Exception as e:
            print(e)

    def insert_new_message(self, message, username):
        for user in [self.user1, self.user2]:
            if user.username == username:

                client_id = user.user_id
                break
            
        actual_date =  datetime.datetime.now()
        try:
            query = text(f"""INSERT INTO chat_{self.user1.user_id}_{self.user2.user_id}(message, client_id, name, date, hour)
                            VALUES(:message, :client_id, :name, :date, :hour)""")
            
            #client_id da pessoa que mandou a mensagem dentro do chat, assim como o "name"
            self.session_db.execute(query, {'message': f'{message}', 'client_id': f'{client_id}', 'name': f'{username}', 'date': f'{actual_date.date()}','hour': f'{actual_date.hour}:{actual_date.minute}:{actual_date.second}'})
            self.session_db.commit()
            self.session_db.close()
        except Exception as e:
            print(e)
            
    def get_chat_id(self):
        try:
            query = text(f"""SELECT chat_id FROM chat_{self.user1.user_id}_{self.user2.user_id}""")
            result = self.session_db.execute(query).fetchall()
            self.session_db.close()
            return result
        except Exception as e:
            print(e)
if __name__ == '__main__':
    chat1 = ChatUsers('user2', 'user1')
    chat1.insert_new_message('legal','user2')
    print(chat1.get_all_messages())
