export default class ChatManager {
    constructor() {
        if (ChatManager.instance) {
            return ChatManager.instance;
        }

        this.chatHistory = new Map();
        this.chatSocket = this.tryConnectToChatSocket();

        ChatManager.instance = this; // Enforce singleton pattern
    }

    tryConnectToChatSocket() {
        if (!this.chatSocket) {
            try {
                const protocol = window.location.protocol === "https:" ? "wss" : "ws";
                this.chatSocket = new WebSocket(
                    `${protocol}://`
                    + window.location.host
                    + '/ws/chat/'
                );
                this.loadEventHandlers()
                this.handleMessage = this.handleMessage.bind(this);
            } catch (err) {
                this.chatSocket = null;
            }
        }
        return;
    }

    disconnectChatSocket() {
        if (this.chatSocket) {
            this.chatSocket.close();
            this.chatSocket = undefined;
        }
        return;
    }

    loadEventHandlers() {
        this.chatSocket.addEventListener("message", this.handleMessage);
    }

    handleMessage(event) {
        try {
            var data = JSON.parse(event.data);
            let messageInfo = {
                ...data,
                'time': Date.now()
            }
            this.atualizaHistorico(messageInfo);
            document.dispatchEvent(new CustomEvent('chatMessageReceived', { detail: messageInfo.chat_id }));
        } catch (err) {
        }
    };

    atualizaHistorico(messageInfo) {
        let chatMessages = this.chatHistory.get(messageInfo.chat_id);
        if (!chatMessages) {
            chatMessages = [];
            this.chatHistory.set(messageInfo.chat_id, chatMessages);
        }
        chatMessages.push(messageInfo);
    }

}
