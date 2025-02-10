import AbstractView from "./abstractView.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class Update_info extends AbstractView {
    constructor() {
        super();
        /* const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket(); */
        this.setTitle("Update_info");
    }

    async getHtml() {
        try {
            const response = await fetch('/update_info/', {
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
