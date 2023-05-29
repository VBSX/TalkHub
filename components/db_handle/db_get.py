import sys
import os
path = os.path.abspath('./')
sys.path.append(path)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

class DatabaseGet():
    def __init__(self):
        engine = create_engine('sqlite:///components/db_handle/chat.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def get_all_users(self):
        query = text(f'SELECT name, last_name, username, user_id FROM users')
        result = self.session.execute(query).fetchall()
        self.session.close()
        return result
if __name__ == '__main__':
    db = DatabaseGet()
    print(db.get_all_users())