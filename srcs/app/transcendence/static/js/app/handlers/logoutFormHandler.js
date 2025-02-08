import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class LogoutFormHandler extends AbstractHandler {
    constructor() {
        super();
        // disconnect the socket
        /* const chatManager = new ChatManager(); 
        chatManager.disconnectChatSocket();*/
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        view.bindUIEventHandlers();
        if (context.ok)
            navigateTo("/sign_in/");
    }

    getContext(_form, response) {
        return response;
    }
}