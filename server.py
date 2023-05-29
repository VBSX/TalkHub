from flask import Flask, render_template, redirect, url_for, request, session
from components.user_handle.modules.password_encrypt import PasswordCrypter
from components.user_handle.user_get import User
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from components.db_handle.db_get import DatabaseGet
from components.chat_handle.chat import ChatUsers
from flask import jsonify
import eventlet

class ChatApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config['SECRET_KEY'] = 'My_Nice_secret_key'
        self.register_routes()
        eventlet.monkey_patch()
        CORS(self)
        self.crypter = PasswordCrypter()
        self.socketio = SocketIO(self, async_mode='eventlet')
        self.socketio.on_event('send_message', self.handle_message)
        self.socketio.on_event('join_room', self.handle_join_room)
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
                sender_username = session['username']
                if recipient_username == sender_username:
                    return jsonify({'status': 400, 'message': 'Não é possível enviar mensagem para vocé mesmo.'})
                elif message == '':
                    return jsonify({'status': 400, 'message': 'Não é possível enviar mensagem vazia.'})
                else:
                    ChatUsers(sender_username, recipient_username).insert_new_message(message,  sender_username)
                    return jsonify({'status': 200, 'message': 'Mensagem enviada com sucesso!'})
        else:
            return redirect(url_for('login'))   
         
    def handle_join_room(self, data):
        # TODO: Implementar a lógica para verificar se o usuário já está na sala
        # TODO: Implementar a lógica para verificar se o usuário está na lista de usuários da sala

        room = data['room']
        print(room)
        sid = request.sid  # Get the session ID of the client that sent the message
        join_room(room, sid=sid)
         
    def handle_message(self, data):
        chat_name = data['chat_name']
        message = data['message']
        user_sender = data['userSender']
        # Envia a mensagem apenas para os clientes na sala correspondente
        emit('message_received', {'sender': user_sender, 'message': message}, room=chat_name)

    def start_chat(self):
        if request.method == 'POST':
            username_to_chat = request.form['username']
            username_of_starter_user = session['username']
            chat = ChatUsers(username_of_starter_user, username_to_chat)
            chat_name = chat.chat_name
            return redirect(url_for('display',chat_name=chat_name, user1=username_of_starter_user, user2=username_to_chat))

    def display(self,chat_name,user1, user2):
        if 'username' in session:
            if session['username'] == user1 or session['username'] == user2:
                chat_users = ChatUsers(user1, user2)
                messages = chat_users.get_all_messages()
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
    debug = False
    if debug == True:
        app.socketio.run(app, host='127.0.0.1',debug=True)
    else:
        app.socketio.run(app, host='0.0.0.0',debug=False)

    

