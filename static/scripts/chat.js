var socket = io.connect('http://' + document.domain + ':' + location.port);
var metaElement = document.querySelector('meta[name="chat_name_js"]');
var chat_name = metaElement.getAttribute('content');
console.log(chat_name);
socket.on('connect', function() {
console.log('Connected to the server');
joinroom();
});

socket.on('message_received', function(data) {
    console.log('Mensagem recebida:', data);
    location.reload();
});

function joinroom() {
    socket.emit('join_room', { room: chat_name });
    console.log('entrando na sala')
}

function sendMessage(data) {
    // Enviar a mensagem para o servidor
    socket.emit('send_message', data);
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
