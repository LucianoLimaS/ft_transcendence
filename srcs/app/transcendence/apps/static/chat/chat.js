let chatSocket = null;

function initializeChat(username) {
    if (!chatSocket || chatSocket.readyState === WebSocket.CLOSED) {
        chatSocket = new WebSocket('ws://localhost:8001/ws/chat/');

        chatSocket.onopen = function (e) {
            console.log('Conexão estabelecida com sucesso!');
        };

        chatSocket.onclose = function (e) {
            console.error('Chat socket fechado inesperadamente');
        };
    }

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('Mensagem recebida:', data.message); // Log de depuração
        const chatMessages = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username}: ${data.message}`; // Exibe o nome do usuário
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Rolagem automática
    };

    document.getElementById('chat-form').onsubmit = function (e) {
        e.preventDefault();
        const messageInput = document.getElementById('message');
        const message = messageInput.value;

        if (chatSocket.readyState === WebSocket.OPEN) {
            console.log('Enviando mensagem:', message); // Log de depuração
            chatSocket.send(JSON.stringify({
                'message': message,
                'username': username // Incluindo o nome do usuário na mensagem
            }));
            messageInput.value = '';
        } else {
            console.error('WebSocket não está aberto. Estado atual:', chatSocket.readyState);
        }
    };
}

// Inicialize o chat quando a página for carregada
document.addEventListener('DOMContentLoaded', function () {
    const username = document.getElementById('username').textContent;
    initializeChat(username);
});

// Reexecutar a função após o conteúdo ser carregado com HTMX
document.body.addEventListener('htmx:afterSwap', function (event) {
    if (event.detail.target.id === 'chat-container') {
        const username = document.getElementById('username').textContent;
        initializeChat(username);
    }
});