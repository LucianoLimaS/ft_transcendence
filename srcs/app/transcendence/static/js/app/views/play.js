import AbstractView from "./abstractView.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class Play extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        /* const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket(); */
        this.setTitle("Play");
    }

    async getHtml() {
        try {
            const response = await fetch('/play/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
    }

    removeUIEventHandlers() {
    }
}
