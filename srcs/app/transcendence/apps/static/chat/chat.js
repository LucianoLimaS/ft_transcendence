let chatSocket = null;

function initializeChat(username) {
    if (!window.location.pathname.includes('chat')) {
        return; // Sai se não estiver na página do chat
    }

    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        return; // Sai se o socket já estiver aberto
    }

    chatSocket = new WebSocket('ws://localhost:8001/ws/chat/');

    chatSocket.onopen = (e) => {
        console.log('Conexão WebSocket estabelecida.');
    };

    chatSocket.onclose = (e) => {
        console.error('Conexão WebSocket fechada.', e);
        chatSocket = null;
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('Mensagem recebida:', data.message);
        const chatMessages = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username}: ${data.message}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    document.getElementById('chat-form').onsubmit = function (e) {
        e.preventDefault();
        const messageInput = document.getElementById('message');
        const message = messageInput.value;

        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) { // Verifica se o socket existe e está aberto
            console.log('Enviando mensagem:', message);
            chatSocket.send(JSON.stringify({
                'message': message,
                'username': username
            }));
            messageInput.value = '';
        } else {
            console.error('WebSocket não está aberto ou não existe. Estado atual:', chatSocket ? chatSocket.readyState : 'null');
        }
    };
}