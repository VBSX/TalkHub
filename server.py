from flask import Flask, render_template, redirect, url_for, request, session   
from user_handle.password_encrypt import PasswordCrypter
from user_handle.user_get import User
from flask_socketio import SocketIO, emit

class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'My_Nice_secret_key'
        self.register_routes()
        self.crypter = PasswordCrypter()
        self.socketio = SocketIO(self.app)
        self.socketio.on_event('send_message', self.handle_message)



    def register_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout)

    def index(self):
        if 'username' in session:
            return render_template('index.html', username=session['username'])
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

            # Implemente a lógica para enviar a mensagem para o destinatário
            # usando a biblioteca SocketIO e os IDs de cliente dos usuários

            emit('message_received', {'sender': sender_username, 'message': message}, room=recipient_client_id)

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    auth_app = ChatApp()
    auth_app.run()
