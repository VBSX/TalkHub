from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import sys
path = os.path.abspath('./')
sys.path.append(path)


class User():
    def __init__(self, name):
        self.username = name
        engine = create_engine('sqlite:///db_handle/chat.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.password = self.get_password()
        self.name = self.get_name()
        self.last_name = self.get_last_name()
        self.user_id = self.get_user_id()
        self.id = self.get_identify() 

    
    def get_password(self):
        query = text(f'SELECT password FROM users WHERE username = :name')
        result = self.session.execute(query, {'name': self.username}).fetchall()
        self.session.close()
        return result[0][0]
    
    def get_name(self):
        query = text('SELECT name FROM users WHERE username = :name')
        result = self.session.execute(query, {'name': self.username}).fetchall()
        self.session.close()
        return result[0][0]
    
    def get_last_name(self):
        query = text('SELECT last_name FROM users WHERE username = :name')
        result = self.session.execute(query, {'name': self.username}).fetchall()
        self.session.close()
        return result[0][0]
    
    def get_user_id(self):
        query = text('SELECT user_id FROM users WHERE username = :name')
        result = self.session.execute(query, {'name': self.username}).fetchall()
        self.session.close()
        return result[0][0]
    
    def get_identify(self):
        query = text('SELECT id FROM users WHERE username = :name')
        result = self.session.execute(query, {'name': self.username}).fetchall()
        self.session.close()
        return result[0][0]
    
if __name__ == '__main__':
    User('user1')