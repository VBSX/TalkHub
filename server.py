from flask import Flask, render_template, redirect, url_for, request, session   
from user_handle.modules.password_encrypt import PasswordCrypter
from user_handle.user_get import User
from flask_socketio import SocketIO, emit
from db_handle.db_get import DatabaseGet
from chat_handle.chat import ChatUsers

class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'My_Nice_secret_key'
        self.register_routes()
        self.crypter = PasswordCrypter()
        self.socketio = SocketIO(self.app)
        self.socketio.on_event('send_message', self.handle_message)
        self.db_get = DatabaseGet()

    def register_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout)
        self.app.add_url_rule('/start_chat', 'start_chat', self.start_chat, methods=['POST'])
        self.app.add_url_rule('/display/<slug>', 'display', self.display, methods=['GET'])


    def index(self):
        if 'username' in session:
            user_list = self.db_get.get_all_users()
            for user in user_list:
                if session['username'] == user[2]:
                    user_list.pop(user_list.index(user))
                    break
            return render_template('index.html', username=session['username'], all_users=user_list)
        else:
            return redirect(url_for('login'))
        
    def login(self):
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']

                try:
                    user = User(username)
                    if self.crypter.decrypt(password, user.password):
                        session['username'] = username
                        session['user_id'] = user.user_id
                        session['user_name'] = user.name
                        session['last_name'] = user.last_name
                        print(session)
                        return redirect(url_for('index'))
                    else:
                        return render_template('login.html', error='Usuário ou senha inválidos.')
                except:
                    return render_template('login.html', error='Usuário ou senha inválidos.')

            return render_template('login.html')
        
    def send_message(self):
        if 'username' in session:
            if request.method == 'POST':
                recipient_username = request.form['recipient']
                message = request.form['message']
                # Get the sender's user ID and client ID from the session
                sender_id = session['user_id']
                sender_client_id = session['client_id']
                # Get the recipient's user ID and client ID
                recipient = User(recipient_username)
                recipient_id = recipient.user_id
                recipient_client_id = recipient.client_id
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))    
        
    def handle_message(self, data):
        if 'username' in session:
            sender_username = session['username']
            recipient_username = data['recipient']    
            message = data['message']
            emit('message_received', {'sender': sender_username, 'message': message}, room=recipient_username)

    def start_chat(self):
        if request.method == 'POST':
            username_to_chat = request.form['username']
            username_of_starter_user = session['username']
            
            chat_users = ChatUsers(username_of_starter_user, username_to_chat)
            messages = chat_users.get_all_messages()
            chat_id = chat_users.chat_id
            
            slug = f'chat {username_of_starter_user}-{username_to_chat}'
            return render_template('chat.html',slug=slug, messages=messages, user1=username_of_starter_user, user2=username_to_chat)

    
    def display(slug):
        messages = request.args.get('messages')
        user1 = request.args.get('user1')
        user2 = request.args.get('user2')
        return render_template('display.html', messages=messages, user1=user1, user2=user2)

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    auth_app = ChatApp()
    auth_app.run()
