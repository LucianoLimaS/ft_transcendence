import AbstractView from "./abstractView.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class Profile extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        /* const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket(); */
        this.setTitle("Profile");
    }

    async getHtml() {
        try {
            const response = await fetch('/profile/', {
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
