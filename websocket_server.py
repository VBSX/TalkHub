from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu_secreto_aqui'
socketio = SocketIO(app)

class WebSocketServer:
    def __init__(self):
        self.clients = set()

    def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                socketio.emit('message', message, room=client)

    def start_server(self):
        @socketio.on('connect')
        def handle_connect():
            self.clients.add(request.sid)
            print(f"Cliente conectado: {request.sid}")

        @socketio.on('message')
        def handle_message(message):
            self.broadcast(message, request.sid)
            print(f"Mensagem recebida: {message}")

        @socketio.on('disconnect')
        def handle_disconnect():
            self.clients.remove(request.sid)
            print(f"Cliente desconectado: {request.sid}")
    @socketio.on('message')
    def handle_message(message):
        socketio.emit('message', message)

if __name__ == '__main__':
    server = WebSocketServer()
    server.start_server()
    socketio.run(app, port=5000, debug=True)