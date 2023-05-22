document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('menu-button');
    var closeButton = document.getElementById('close-button'); // Seleciona o botão de fechamento
    var sidebar = document.querySelector('.sidebar');

    menuButton.addEventListener('click', function() {
        sidebar.classList.add('open');
    });

    closeButton.addEventListener('click', function() { // Adiciona o evento de clique no botão de fechamento
        sidebar.classList.remove('open');
    });
});