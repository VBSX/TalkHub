var socket = io.connect('http://' + document.domain + ':' + location.port);
    
function sendMessage() {
    var recipient = document.getElementById('recipient').value;
    var message = document.getElementById('message').value;

    socket.emit('send_message', {
        recipient: recipient,
        message: message
    });

    // Limpe os campos de entrada após o envio da mensagem
    document.getElementById('recipient').value = '';
    document.getElementById('message').value = '';
}

socket.on('message_received', function(data) {
    var sender = data.sender;
    var message = data.message;
});