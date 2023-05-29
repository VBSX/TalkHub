from modules.password_encrypt import PasswordCrypter
from modules.random_user_id import generate_random_user_id
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class NewUser():
    def __init__(self,name, last_name, username, password):
        self.name = name
        self.last_name = last_name
        crypter = PasswordCrypter()
        self.username = username
        self.password = password
        self.user_id = generate_random_user_id(self.username)
        self.password_hash = crypter.encrypt(self.password)
        engine = create_engine('sqlite:///components/db_handle/chat.db')
        Session = sessionmaker(bind=engine)
        self.session_new_user = Session()
        exist_user = self.verify_if_user_exists()
        if not exist_user:
            self.create_user()
            print('User created')
        else:
            return False, 'usuário ja criado'
        
    def create_user(self):
        self.session_new_user.execute(text(
            """INSERT INTO users 
            (name, last_name, username, password, user_id) 
            VALUES (:name, :last_name, :username, :password, :user_id)"""),
            {'name':self.name,'last_name':self.last_name,
            'user_id': self.user_id, 'username': self.username, 'password': self.password_hash})
        
        self.session_new_user.commit()
        return self.user_id
    
    def verify_if_user_exists(self):
        user = self.session_new_user.execute(text("select * from users where username = :username")
        , {'username':self.username}).fetchone()
        if user:
            return True
        else:
            return False
        
if __name__ == '__main__':
    user = NewUser('drougas','','drougas','123456')

