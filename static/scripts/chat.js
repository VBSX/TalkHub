var socket = io.connect('http://' + document.domain + ':' + location.port);
var metaElement = document.querySelector('meta[name="chat_name_js"]');
var metaElement_user_sender = document.querySelector('meta[name="user1"]');
var chat_name = metaElement.getAttribute('content');
var user1 = metaElement_user_sender.getAttribute('content');

console.log(chat_name);
access_to_notification_push();
socket.on('connect', function() {
    console.log('Connected to the server');
    joinroom();
    scrollToBottom()
});
socket.on('message_received', function(data) {
    location.reload();
    scrollToBottom();
    if (verify_if_user1_is_the_mensage_sender(data)==false) {
        console.log('Mensagem recebida:', data);
        send_notification('Mensagem recebida: '+ data.message+ ' \nde ' + data.sender);
    }
});
function verify_if_user1_is_the_mensage_sender(data) {
    if (data.sender == user1) {
        return true;
    } else {
        return false;
    }
}
function joinroom() {
    socket.emit('join_room', { room: chat_name });
    console.log('entrando na sala')
}
function sendMessage(data) {
    socket.emit('send_message', data);
}

function scrollToBottom() {
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: 'smooth' // animação suave
    });
}
function submitForm() {
    var form = document.getElementById('message-form');
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send_message');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
            var chat_name = document.getElementById('chat_name').value;
            var message = document.getElementById('message_send').value;
            var userSender = document.getElementById('user_sender').value;
            var userReceptor = document.getElementById('user_receptor').value;
            var data = {
                chat_name: chat_name,
                message: message,
                userSender: userSender,
                userReceptor: userReceptor
            };
                // Enviar a mensagem para o servidor
                sendMessage(data);       
        } else {
            console.error('Error:', xhr.status);
        }
    };
    xhr.send(formData);
}

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('message-form');
    var inputField = document.getElementById('message_send');
    inputField.focus();
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar o comportamento padrão de envio do formulário
        submitForm();
    });
    inputField.addEventListener('keydown', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault(); // Evitar o comportamento padrão de envio do formulário
            submitForm();
        }
    });
});
function access_to_notification_push(){

    var notification_permission = Notification.permission;
    if (notification_permission === 'granted') {
        console.log('Notificação já ativada');
    } else if (notification_permission === 'denied') {
        console.log('Notificação não ativada');
    } else {
        Notification.requestPermission(function(permission) {
            if (permission === 'granted') {
                console.log('Notificação ativada');
            } else {
                console.log('Notificação não ativada');
            }
        });
    }
}
function send_notification(message){
    new Notification(message);
}