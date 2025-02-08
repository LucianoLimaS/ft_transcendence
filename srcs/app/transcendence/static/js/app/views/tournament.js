import AbstractView from "./abstractView.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class Tournament extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        /* const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket(); */
        this.setTitle("Tournament");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            return "<p>Error loading Tournament page</p>";
        }
    }

    async loadComponents() {
        // Carregando o script handle-tournament.js dinamicamente
        await import('../pong/handle-tournament.js').then((module) => {
        }).catch((error) => {
        });
    }

    bindUIEventHandlers() {
    }

    removeUIEventHandlers() {
    }
}