import AbstractView from "./abstractView.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class Chat extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        /* this.chatManager = new ChatManager();
        this.chatManager.tryConnectToChatSocket(); */

        this.setTitle("Chat");
        this.currentChatId = null;
        this.handleMessageUI = this.handleMessageUI.bind(this);
        this.atualizaChat = this.atualizaChat.bind(this);
        this.handleChatChange = this.handleChatChange.bind(this);
        this.sendMessage = this.sendMessage.bind(this);
        this.sendMessageEnterKey = this.sendMessageEnterKey.bind(this);
    }

    async getHtml() {
        try {
            const response = await fetch('/chat/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch (error) {
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {

        const chatList = document.querySelectorAll('[chat_id]');
        if (chatList.length > 0) {
            this.selectFirstChat(chatList[0]);
        }
        for (var i = 0; i < chatList.length; i++) {
            chatList[i].addEventListener('click', this.handleChatChange);
        }

        var sendButton = document.getElementById('send-msg-button');
        sendButton.addEventListener('click', this.sendMessage);

        var input = document.getElementById('chat-message-input');
        input.addEventListener('keydown', this.sendMessageEnterKey);

        document.addEventListener('chatMessageReceived', this.handleMessageUI);
    }

    selectFirstChat(chatDiv) {
        this.currentChatId = chatDiv.getAttribute('chat_id');
        this.highlightSlectedChat(chatDiv);
    }

    removeUIEventHandlers() {

        var chatList = document.querySelectorAll('[chat_id]');
        for (var i = 0; i < chatList.length; i++) {
            chatList[i].removeEventListener('click', this.handleChatChange);
        }

        var sendButton = document.getElementById('send-msg-button');
        sendButton.removeEventListener('click', this.sendMessage);

        document.removeEventListener('chatMessageReceived', this.handleMessageUI);
    }

    chatWindowIsOpen() {
        return document.getElementById('chat-messages') !== null;
    }

    handleMessageUI(event) {
        if (this.chatWindowIsOpen() && event.detail == this.currentChatId)
            this.displayMessage(this.chatManager.chatHistory.get(event.detail).at(-1));
    }

    handleChatChange(event) {
        this.unhighlightPreviousChat();
        this.currentChatId = event.currentTarget.getAttribute('chat_id');
        this.highlightSlectedChat(event.currentTarget);
        this.atualizaChat();
    }

    highlightSlectedChat(eventTarget) {
        const outerDiv = eventTarget.closest('.friend');
        if (outerDiv)
            outerDiv.classList.add('selected');
    }

    unhighlightPreviousChat() {
        const selectedChat = document.querySelector('.selected');
        if (selectedChat)
            selectedChat.classList.remove('selected');
    }

    sendMessageEnterKey(event) {
        if (event.key === "Enter")
            this.sendMessage();
    }

    sendMessage() {

        const messageInputDom = document.getElementById('chat-message-input');
        if (!messageInputDom) {
            return;
        }

        const message = messageInputDom.value;

        if (!message || !this.currentChatId) {
            return;
        }

        if (this.chatManager.chatSocket.readyState === WebSocket.OPEN) {
            this.chatManager.chatSocket.send(JSON.stringify({
                'message': message,
                'chat_id': this.currentChatId
            }));
            messageInputDom.value = '';
        } else {
        }
    }

    displayMessage(messageInfo) {
        const messagesContainer = document.getElementById('chat-messages');
        const sender = document.createElement('p');
        const newMessage = document.createElement('p');
        const msgTime = new Date(messageInfo.time);
        sender.textContent = messageInfo.sender + ', ' + String(msgTime.getHours()).padStart(2, '0') + ':' + String(msgTime.getMinutes()).padStart(2, '0');
        newMessage.textContent = messageInfo.message;
        sender.classList.add('chat-msg-user-time');
        newMessage.classList.add('chat-msg-content');
        messagesContainer.appendChild(sender);
        messagesContainer.appendChild(newMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    atualizaChat() {
        this.limpaChat();
        if (this.chatManager.chatHistory.has(this.currentChatId)) {
            this.loadChatHistory(this.chatManager.chatHistory.get(this.currentChatId));
        }
        else {
            this.chatManager.chatHistory.set(this.currentChatId, new Array());
        }
    }

    loadChatHistory() {
        this.chatManager.chatHistory.get(this.currentChatId).forEach(message => {
            this.displayMessage(message);
        });
    }

    limpaChat() {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
    }
}
