from flask import Flask, render_template, redirect, url_for, request, session, request 
from user_handle.modules.password_encrypt import PasswordCrypter
from user_handle.user_get import User
from flask_socketio import SocketIO, emit, join_room, leave_room


from db_handle.db_get import DatabaseGet
from chat_handle.chat import ChatUsers
from flask import jsonify

class ChatApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        # self.app = Flask(__name__)
        self.secret_key = 'My_Nice_secret_key'
        self.register_routes()
        self.crypter = PasswordCrypter()
        self.socketio = SocketIO(self)
        self.socketio.on_event('send_message', self.handle_message)
        self.socketio.on_event('connect', self.handle_connect)

        self.db_get = DatabaseGet()

    def register_routes(self):
        self.route('/')(self.index)
        self.route('/login', methods=['GET', 'POST'])(self.login)
        self.route('/logout')(self.logout)
        self.route('/start_chat', methods=['POST'])(self.start_chat)
        self.route('/display/<chat_name>/<user1>/<user2>', methods=['GET','POST'])(self.display)
        self.route('/send_message', methods=['POST'])(self.send_message)


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
                recipient_username = request.form['user_receptor']
                message = request.form['message']
                # Get the sender's user ID and client ID from the session
                sender_username = session['username']
                ChatUsers(sender_username, recipient_username).insert_new_message(message,  sender_username)
                return jsonify({'status': 200, 'message': 'Mensagem enviada com sucesso!'})
        else:
            return redirect(url_for('login'))   
         
 
    def handle_connect(self):
        room = request.args.get('room')
        sid = request.sid  # Get the session ID
        join_room(room)
        # Additional logic using the sid if needed
        
    def handle_message(self, data):
        if 'username' in session:
            sender_username = session['username']
            chat_name = data['chatName']
            message = data['message']
            user_sender = data['userSender']
            user_receptor = data['userReceptor']

            # Criação da slug para a sala
            slug = f'/display/{chat_name}/{user_sender}/{user_receptor}'

            # Envia a mensagem apenas para os clientes na sala correspondente
            emit('message_received', {'sender': sender_username, 'message': message}, room=slug)
    def start_chat(self):
        if request.method == 'POST':
            username_to_chat = request.form['username']
            username_of_starter_user = session['username']
            chat_name = f'chat{username_of_starter_user}{username_to_chat}'
            return redirect(url_for('display',chat_name=chat_name, user1=username_of_starter_user, user2=username_to_chat))

    def display(self,chat_name,user1, user2):
        if 'username' in session:
            if session['username'] == user1 or session['username'] == user2:
                chat_users = ChatUsers(user1, user2)
                messages = chat_users.get_all_messages()
                # Criação da slug para a sala
                slug = f'/display/{chat_name}/{user1}/{user2}'

                # Adiciona o cliente à sala correspondente
                join_room(slug)
                return render_template('chat.html',chat_name=chat_name, messages=messages, user1=user1, user2=user2)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))

if __name__ == '__main__':
    app = ChatApp()
    app.run(debug=True)
